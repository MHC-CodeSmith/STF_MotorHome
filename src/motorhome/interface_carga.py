"""Despacho condicionado de EVSE discreto, inversor compartilhado e PV48V.

Não altera o modelo anterior nem seus arquivos de proveniência. Reutiliza sua
máquina de estados e verificação elétrica, acrescentando limites AC/DC e EVSE.
"""

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix

from motorhome.agenda_portatil import _states, _validate_inputs, verificar_agenda


def potencias_interface(spec):
    """Pac=V*I*PF; Pdc=Pac/eta_inv; pack recebe eta_obc*Pac."""
    currents = np.asarray(spec['charge']['current_modes_a_assumed'], dtype=float)
    inv, charge = spec['inverter'], spec['charge']
    positive = [inv['continuous_power_kw_at40c'], inv['apparent_power_kva_at25c'],
                charge['voltage_v_assumed']]
    fractions = [inv['efficiency_assumed'], inv['household_power_factor_assumed'],
                 charge['onboard_efficiency_assumed'], charge['power_factor_assumed']]
    if (any(not np.isfinite(x) or x <= 0 for x in positive)
            or any(not np.isfinite(x) or not 0 < x <= 1 for x in fractions)
            or currents.ndim != 1 or len(currents) < 1 or currents[0] != 0
            or not np.isfinite(currents).all() or (currents < 0).any()
            or len(set(currents)) != len(currents)):
        raise ValueError('Modos/eficiências/limites da interface inválidos')
    ac = currents*charge['voltage_v_assumed']*charge['power_factor_assumed']/1000
    return ac, ac/inv['efficiency_assumed']


def verificar_interface(rows, data, c, powers, spec, initial, final, driving_cap_h):
    ac, dc = potencias_interface(spec)
    verification = verificar_agenda(rows, data, c, powers, initial, final, driving_cap_h, float(dc.max()))
    max_active, max_apparent, starts = 0., 0., 0
    previous = False
    for r, (_, inputs) in zip(rows, data.iterrows()):
        q = r['transfer_kw']
        j = int(np.argmin(abs(dc-q)))
        if abs(q-dc[j]) > 1e-6:
            raise ValueError('Corrente de carga fora dos modos discretos')
        if abs(r['charge_current_a']-spec['charge']['current_modes_a_assumed'][j]) > 1e-6:
            raise ValueError('Corrente exportada divergente')
        total_ac = ac[j]+inputs['house_ac_kw']
        apparent = ac[j]/spec['charge']['power_factor_assumed']+inputs['house_ac_kw']/spec['inverter']['household_power_factor_assumed']
        if (total_ac > spec['inverter']['continuous_power_kw_at40c']+1e-7
                or apparent > spec['inverter']['apparent_power_kva_at25c']+1e-7):
            raise ValueError('Limite AC compartilhado excedido')
        if inputs['dc12_kw'] > spec['household']['dc12_power_limit_kw']+1e-7:
            raise ValueError('ConversorDC excedido')
        starts += int(j > 0 and not previous)
        previous = j > 0
        max_active, max_apparent = max(max_active, total_ac), max(max_apparent, apparent)
    return dict(verification, max_shared_active_kw=max_active, max_shared_apparent_kva=max_apparent,
                charging_starts=starts, interface_oem_verified=False)


def otimizar_interface(data, c, powers, spec, initial, final, driving_cap_h, target_km=None):
    """Máximo diário condicionado, um modo EVSE constante por intervalo.

    Serviços48V recebem somente solar dessa tensão. `house_kw` contém perdas
    residenciais e standby; transferênciaDC recebe perda inv, depois perdaOBC.
    Os limites de saída são compartilhados pela casa e cargaOEM. Não há AC-in.
    """
    ac, dc = potencias_interface(spec)
    if not {'house_ac_kw', 'dc12_kw'}.issubset(data.columns):
        raise ValueError('CargasAC eDC12 separadas obrigatórias')
    if (not np.isfinite(data[['house_ac_kw', 'dc12_kw']]).all().all()
            or (data[['house_ac_kw', 'dc12_kw']] < 0).any().any()):
        raise ValueError('Cargas não negativas finitas obrigatórias')
    eta = spec['inverter']['efficiency_assumed']*spec['charge']['onboard_efficiency_assumed']
    if abs(c['transfer_efficiency_assumed']-eta) > 1e-12:
        raise ValueError('Perdas de transferência inconsistentes')
    dt = _validate_inputs(data, c, powers, initial, final, driving_cap_h, float(dc.max()))
    if target_km is not None and (not np.isfinite(target_km) or target_km < 0):
        raise ValueError('Distância alvo inválida')
    states, edges, drive, teardown_end = _states(c, dt)
    n, k, m, levels = len(data), len(states), len(drive), len(dc)
    hb, tb = n*k, n*k+n*m
    sb, qb, cb, lb = tb+n, tb+2*n, tb+3*n, tb+4*n
    count = lb+n*levels
    low, high = np.zeros(count), np.full(count, np.inf)
    high[:hb], high[hb:tb], high[lb:] = 1, dt, 1
    tc, sc = c['traction_capacity_kwh'], c['service_capacity_kwh']
    low[tb:sb], high[tb:sb] = tc*c['traction_min_soc'], tc
    low[sb:qb], high[sb:qb] = sc*c['service_min_soc'], sc
    low[sb-1] = high[sb-1] = final*tc
    low[qb-1] = high[qb-1] = c['service_final_soc']*sc
    high[qb:cb] = dc.max()
    high[cb:lb] = data['fixed_kw'].to_numpy()+data['portable_kw'].to_numpy()
    for j, state in enumerate(states):
        if ('stowed', state) not in edges:
            high[j] = 0
        if state not in ['stowed', teardown_end, *drive]:
            high[(n-1)*k+j] = 0
    for t, (_, inputs) in enumerate(data.iterrows()):
        for j in range(levels):
            apparent = ac[j]/spec['charge']['power_factor_assumed']+inputs['house_ac_kw']/spec['inverter']['household_power_factor_assumed']
            if (ac[j]+inputs['house_ac_kw'] > spec['inverter']['continuous_power_kw_at40c']+1e-9
                    or apparent > spec['inverter']['apparent_power_kva_at25c']+1e-9
                    or inputs['dc12_kw'] > spec['household']['dc12_power_limit_kw']+1e-9):
                high[lb+t*levels+j] = 0
    objective, integer = np.zeros(count), np.zeros(count)
    objective[hb:tb] = np.tile(-np.array(c['speed_modes_km_h']), n)
    integer[:hb] = integer[lb:] = 1
    days = sorted(set(data.index.date))
    mat = lil_matrix((n*(k+m+7)+len(days)+1, count))
    lo, hi = np.full(mat.shape[0], -np.inf), np.full(mat.shape[0], np.inf)
    row = 0
    for t in range(n):
        z, hs = slice(t*k, (t+1)*k), slice(hb+t*m, hb+(t+1)*m)
        mat[row, z], lo[row], hi[row] = 1, 1, 1
        row += 1
        for j, state in enumerate(states):
            if t:
                mat[row, t*k+j] = 1
                for prev, old in enumerate(states):
                    if (old, state) in edges:
                        mat[row, (t-1)*k+prev] = -1
                hi[row] = 0
            row += 1
        for j, state in enumerate(drive):
            mat[row, hb+t*m+j], mat[row, t*k+states.index(state)] = 1, -dt
            hi[row] = 0
            row += 1
        mat[row, tb+t], mat[row, qb+t], mat[row, hs] = 1, -dt*eta, powers
        if t:
            mat[row, tb+t-1] = -1
        lo[row] = hi[row] = initial*tc if not t else 0
        row += 1
        mat[row, sb+t], mat[row, qb+t], mat[row, cb+t] = 1, dt, dt
        mat[row, t*k+states.index('deployed')] = -dt*data.iloc[t]['portable_kw']
        if t:
            mat[row, sb+t-1] = -1
        lo[row] = hi[row] = dt*(data.iloc[t]['fixed_kw']-data.iloc[t]['house_kw'])+(c['service_initial_soc']*sc if not t else 0)
        row += 1
        mat[row, cb+t], mat[row, t*k+states.index('deployed')] = 1, -data.iloc[t]['portable_kw']
        hi[row] = data.iloc[t]['fixed_kw']
        row += 1
        mat[row, qb+t] = 1
        for state in drive:
            mat[row, t*k+states.index(state)] = dc.max()
        hi[row] = dc.max()
        row += 1
        ls = slice(lb+t*levels, lb+(t+1)*levels)
        mat[row, ls], lo[row], hi[row] = 1, 1, 1
        row += 1
        mat[row, qb+t], mat[row, ls] = 1, -dc
        lo[row] = hi[row] = 0
        row += 1
    for day in days:
        for t, start in enumerate(data.index):
            if start.date() == day:
                mat[row, hb+t*m:hb+(t+1)*m] = 1
        hi[row] = driving_cap_h
        row += 1
    if target_km is not None:
        mat[row, hb:tb] = np.tile(c['speed_modes_km_h'], n)
        lo[row] = hi[row] = target_km
    r = milp(objective, integrality=integer, bounds=Bounds(low, high),
             constraints=LinearConstraint(mat.tocsr(), lo, hi),
             options={'time_limit': c['solver_time_limit_s'], 'mip_rel_gap': 1e-6})
    out = {'feasible': r.x is not None, 'optimal_in_grid': r.status == 0,
           'solver_status': int(r.status), 'message': r.message, 'vehicle_validated': False}
    if r.x is None:
        return out
    rows = []
    for t, start in enumerate(data.index):
        state = states[int(np.argmax(r.x[t*k:(t+1)*k]))]
        j = drive.index(state) if state in drive else None
        rows.append({'start': start.isoformat(), 'state': state,
                     'driving_h': float(r.x[hb+t*m:hb+(t+1)*m].sum()),
                     'speed_km_h': float(c['speed_modes_km_h'][j]) if j is not None else 0.,
                     'drive_kw': float(powers[j]) if j is not None else 0.,
                     'fixed_kw': float(data.iloc[t]['fixed_kw']),
                     'portable_kw': float(data.iloc[t]['portable_kw']) if state == 'deployed' else 0.,
                     'house_kw': float(data.iloc[t]['house_kw']), 'transfer_kw': float(r.x[qb+t]),
                     'curtailed_kw': float(r.x[cb+t]), 'traction_kwh': float(r.x[tb+t]),
                     'service_kwh': float(r.x[sb+t]),
                     'charge_current_a': float(spec['charge']['current_modes_a_assumed'][int(np.argmax(r.x[lb+t*levels:lb+(t+1)*levels]))])})
    verification = verificar_interface(rows, data, c, powers, spec, initial, final, driving_cap_h)
    if target_km is not None and abs(verification['distance_km']-target_km) > 1e-5:
        raise ValueError('Distância alvo divergente')
    return dict(out, schedule=rows, verification=verification, distance_km=verification['distance_km'],
                mip_gap=float(r.mip_gap), distance_upper_bound_km=float(-r.mip_dual_bound))
