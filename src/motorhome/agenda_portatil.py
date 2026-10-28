"""Agenda condicionada com duas baterias, portátil estacionado e montagem.

MILP diário: um estado físico por intervalo, um trecho inicial de condução de
duração variável por estado de velocidade. Serviços -> tração é uma hipótese
explícita, nunca a soma das capacidades. Unidades internas: h, kW, kWh, km.
"""

import math

import numpy as np
import pandas as pd
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix


def _states(c, dt):
    setup = [f'setup_{i}' for i in range(math.ceil(c['setup_minutes_assumed']/60/dt))]
    teardown = [f'teardown_{i}' for i in range(math.ceil(c['teardown_minutes_assumed']/60/dt))]
    drive = [f'drive_{v:g}' for v in c['speed_modes_km_h']]
    states = ['stowed', *setup, 'deployed', *teardown, *drive]
    edges = {(a, b) for a in ['stowed', *drive] for b in ['stowed', setup[0], *drive]}
    edges.update(zip(setup, [*setup[1:], 'deployed']))
    edges.update({('deployed', 'deployed'), ('deployed', teardown[0])})
    edges.update(zip(teardown, [*teardown[1:], 'stowed']))
    edges.update((teardown[-1], b) for b in drive)
    return states, edges, drive, teardown[-1]


def _validate_inputs(data, c, drive_kw, initial_soc, final_soc, driving_limit_h, transfer_kw):
    required = ['fixed_kw', 'portable_kw', 'house_kw']
    if (not isinstance(data.index, pd.DatetimeIndex) or data.index.tz is None
            or len(data) < 2 or not all(k in data for k in required)):
        raise ValueError('Série com fuso e potências obrigatória')
    values = data[required].to_numpy()
    dt = float((data.index[1]-data.index[0]).total_seconds()/3600)
    if (not np.isfinite(values).all() or (values < 0).any() or dt <= 0
            or not np.allclose((data.index[1:]-data.index[:-1]).total_seconds()/3600, dt)):
        raise ValueError('Potências não negativas finitas e grade contínua obrigatórias')
    ends = data.index+pd.to_timedelta(dt, unit='h')
    if any(a.date() != (b-pd.Timedelta(nanoseconds=1)).date() for a, b in zip(data.index, ends)):
        raise ValueError('Intervalos não podem cruzar meias-noites')
    positive = [c[k] for k in ['setup_minutes_assumed', 'teardown_minutes_assumed',
                             'traction_capacity_kwh', 'service_capacity_kwh', 'solver_time_limit_s']]
    if any(not np.isfinite(x) or x <= 0 for x in [*positive, driving_limit_h]):
        raise ValueError('Durações e capacidades positivas obrigatórias')
    fractions = [initial_soc, final_soc, c['traction_min_soc'], c['service_min_soc'],
                 c['service_initial_soc'], c['service_final_soc'], c['transfer_efficiency_assumed']]
    if any(not np.isfinite(x) or not 0 <= x <= 1 for x in fractions):
        raise ValueError('SOC e eficiência devem ser frações finitas')
    if (min(initial_soc, final_soc) < c['traction_min_soc']
            or min(c['service_initial_soc'], c['service_final_soc']) < c['service_min_soc']
            or c['transfer_efficiency_assumed'] <= 0):
        raise ValueError('SOC abaixo da reserva ou eficiência nula')
    speeds, powers = np.asarray(c['speed_modes_km_h']), np.asarray(drive_kw)
    if (speeds.ndim != 1 or not len(speeds) or powers.shape != speeds.shape
            or not np.isfinite(speeds).all() or not np.isfinite(powers).all()
            or (speeds <= 0).any() or (powers <= 0).any()
            or len(set(speeds)) != len(speeds) or not np.isfinite(transfer_kw) or transfer_kw < 0):
        raise ValueError('Modos de velocidade/potência e transferência inválidos')
    return dt


def otimizar_dia(data, c, drive_kw, initial_soc, final_soc, driving_limit_h,
                 transfer_kw, target_km=None):
    """Maximiza distância; se target_km fornecido, constrói dia com distância exata.

    Retorna incumbente verificado e gap/limite do solver. Não promete ótimo quando
    o tempo acaba. Instalação/desinstalação ocupam estados inteiros, sem geração.
    Transferência é bloqueada em todo intervalo que contém condução, mesmo parcial.
    """
    dt = _validate_inputs(data, c, drive_kw, initial_soc, final_soc, driving_limit_h, transfer_kw)
    if target_km is not None and (not np.isfinite(target_km) or target_km < 0):
        raise ValueError('Distância alvo não negativa finita obrigatória')
    states, edges, drive, teardown_end = _states(c, dt)
    n, k, m = len(data), len(states), len(drive)
    hbase, tbase = n*k, n*k+n*m
    sbase, qbase, cutbase = tbase+n, tbase+2*n, tbase+3*n
    count = cutbase+n
    lower, upper = np.zeros(count), np.full(count, np.inf)
    upper[:hbase], upper[hbase:tbase] = 1, dt
    tc, sc = c['traction_capacity_kwh'], c['service_capacity_kwh']
    lower[tbase:sbase], upper[tbase:sbase] = tc*c['traction_min_soc'], tc
    lower[sbase:qbase], upper[sbase:qbase] = sc*c['service_min_soc'], sc
    lower[sbase-1] = upper[sbase-1] = final_soc*tc
    lower[qbase-1] = upper[qbase-1] = c['service_final_soc']*sc
    upper[qbase:cutbase] = transfer_kw
    upper[cutbase:] = data['fixed_kw'].to_numpy()+data['portable_kw'].to_numpy()
    # Começar com portátil guardado; terminar guardado ou concluindo recolhimento.
    for j, state in enumerate(states):
        if ('stowed', state) not in edges:
            upper[j] = 0
        if state not in ['stowed', teardown_end, *drive]:
            upper[(n-1)*k+j] = 0
    objective = np.zeros(count)
    objective[hbase:tbase] = np.tile(-np.array(c['speed_modes_km_h']), n)
    integrality = np.zeros(count)
    integrality[:hbase] = 1
    days = sorted(set(data.index.date))
    mat = lil_matrix((n*(k+m+5)+len(days)+1, count))
    lo, hi = np.full(mat.shape[0], -np.inf), np.full(mat.shape[0], np.inf)
    row = 0
    for t in range(n):
        z, hs = slice(t*k, (t+1)*k), slice(hbase+t*m, hbase+(t+1)*m)
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
            mat[row, hbase+t*m+j], mat[row, t*k+states.index(state)] = 1, -dt
            hi[row] = 0
            row += 1
        mat[row, tbase+t], mat[row, qbase+t], mat[row, hs] = 1, -dt*c['transfer_efficiency_assumed'], drive_kw
        if t:
            mat[row, tbase+t-1] = -1
        lo[row] = hi[row] = initial_soc*tc if not t else 0
        row += 1
        mat[row, sbase+t], mat[row, qbase+t], mat[row, cutbase+t] = 1, dt, dt
        mat[row, t*k+states.index('deployed')] = -dt*data.iloc[t]['portable_kw']
        if t:
            mat[row, sbase+t-1] = -1
        lo[row] = hi[row] = dt*(data.iloc[t]['fixed_kw']-data.iloc[t]['house_kw'])+(c['service_initial_soc']*sc if not t else 0)
        row += 1
        # Não cortar energia de bateria: corte <= geração fisicamente disponível.
        mat[row, cutbase+t], mat[row, t*k+states.index('deployed')] = 1, -data.iloc[t]['portable_kw']
        hi[row] = data.iloc[t]['fixed_kw']
        row += 1
        mat[row, qbase+t] = 1
        for state in drive:
            mat[row, t*k+states.index(state)] = transfer_kw
        hi[row] = transfer_kw
        row += 1
    for day in days:
        for t, start in enumerate(data.index):
            if start.date() == day:
                mat[row, hbase+t*m:hbase+(t+1)*m] = 1
        hi[row] = driving_limit_h
        row += 1
    if target_km is not None:
        mat[row, hbase:tbase] = np.tile(c['speed_modes_km_h'], n)
        lo[row] = hi[row] = target_km
    result = milp(objective, integrality=integrality, bounds=Bounds(lower, upper),
                  constraints=LinearConstraint(mat.tocsr(), lo, hi),
                  options={'time_limit': c['solver_time_limit_s'], 'mip_rel_gap': 1e-6})
    out = {'feasible': result.x is not None, 'optimal_in_grid': result.status == 0,
           'solver_status': int(result.status), 'message': result.message,
           'transfer_kw_assumed': transfer_kw, 'vehicle_validated': False}
    if result.x is None:
        return out
    rows = []
    for t, start in enumerate(data.index):
        state = states[int(np.argmax(result.x[t*k:(t+1)*k]))]
        hours = result.x[hbase+t*m:hbase+(t+1)*m]
        j = drive.index(state) if state in drive else None
        rows.append({'start': start.isoformat(), 'state': state,
                     'driving_h': float(hours.sum()),
                     'speed_km_h': float(c['speed_modes_km_h'][j]) if j is not None else 0.,
                     'drive_kw': float(drive_kw[j]) if j is not None else 0.,
                     'fixed_kw': float(data.iloc[t]['fixed_kw']),
                     'portable_kw': float(data.iloc[t]['portable_kw']) if state == 'deployed' else 0.,
                     'house_kw': float(data.iloc[t]['house_kw']),
                     'transfer_kw': float(result.x[qbase+t]), 'curtailed_kw': float(result.x[cutbase+t]),
                     'traction_kwh': float(result.x[tbase+t]), 'service_kwh': float(result.x[sbase+t])})
    out.update(schedule=rows, distance_km=sum(r['speed_km_h']*r['driving_h'] for r in rows),
               mip_gap=float(result.mip_gap), distance_upper_bound_km=float(-result.mip_dual_bound))
    out['verification'] = verificar_agenda(rows, data, c, drive_kw, initial_soc, final_soc,
                                          driving_limit_h, transfer_kw)
    if target_km is not None and abs(out['distance_km']-target_km) > 1e-5:
        raise ValueError('Distância alvo divergente')
    return out


def verificar_agenda(rows, data, c, drive_kw, initial_soc, final_soc, driving_limit_h, transfer_kw):
    """Reconstitui cronologia/energia, incluindo o ponto em que a condução termina.

    Não usa SOC do solver como entrada de integração; compara com os valores
    exportados. Solar/corte/cargas constantes. Condução ocorre no início do passo:
    verificar também esse estado evita saldo médio que esconda déficit ou excesso.
    """
    dt = _validate_inputs(data, c, drive_kw, initial_soc, final_soc, driving_limit_h, transfer_kw)
    states, edges, drive, teardown_end = _states(c, dt)
    tc, sc = c['traction_capacity_kwh'], c['service_capacity_kwh']
    et, es, previous, residual = initial_soc*tc, c['service_initial_soc']*sc, 'stowed', 0.
    daily, totals = {}, {'distance_km': 0., 'solar_kwh': 0., 'house_kwh': 0., 'transfer_input_kwh': 0.,
                        'drive_kwh': 0., 'curtailed_kwh': 0.}
    if len(rows) != len(data):
        raise ValueError('Agenda incompleta')
    for t, r in enumerate(rows):
        state, h = r['state'], r['driving_h']
        if (pd.Timestamp(r['start']) != data.index[t] or state not in states
                or (previous, state) not in edges or not -1e-7 <= h <= dt+1e-7):
            raise ValueError('Cronologia, estado ou montagem inválidos')
        j = drive.index(state) if state in drive else None
        expected = {'fixed_kw': data.iloc[t]['fixed_kw'], 'house_kw': data.iloc[t]['house_kw'],
                    'portable_kw': data.iloc[t]['portable_kw'] if state == 'deployed' else 0.,
                    'speed_km_h': c['speed_modes_km_h'][j] if j is not None else 0.,
                    'drive_kw': drive_kw[j] if j is not None else 0.}
        if (not all(np.isfinite(v) for v in r.values() if isinstance(v, (int, float)))
                or any(abs(r[key]-value) > 1e-7 for key, value in expected.items())
                or (j is None and abs(h) > 1e-7)):
            raise ValueError('Potência, velocidade ou geração divergentes')
        q, cut = r['transfer_kw'], r['curtailed_kw']
        if (not -1e-7 <= q <= (0 if j is not None else transfer_kw)+1e-7
                or not -1e-7 <= cut <= r['fixed_kw']+r['portable_kw']+1e-7):
            raise ValueError('Transferência ou corte inválidos')
        rt = q*c['transfer_efficiency_assumed']
        rs = r['fixed_kw']+r['portable_kw']-r['house_kw']-q-cut
        # Nas etapas de condução q=0; energia de tração cai primeiro e fica constante.
        for hours in [h, dt]:
            traction = et+rt*hours-r['drive_kw']*min(hours, h)
            service = es+rs*hours
            if (not tc*c['traction_min_soc']-1e-6 <= traction <= tc+1e-6
                    or not sc*c['service_min_soc']-1e-6 <= service <= sc+1e-6):
                raise ValueError('Energia fora dos limites, inclusive dentro do intervalo')
        et, es = et+rt*dt-r['drive_kw']*h, es+rs*dt
        residual = max(residual, abs(et-r['traction_kwh']), abs(es-r['service_kwh']))
        day = data.index[t].date().isoformat()
        daily[day] = daily.get(day, 0.)+h
        totals['distance_km'] += r['speed_km_h']*h
        for key, power in [('solar_kwh', r['fixed_kw']+r['portable_kw']), ('house_kwh', r['house_kw']),
                           ('transfer_input_kwh', q), ('curtailed_kwh', cut)]:
            totals[key] += power*dt
        totals['drive_kwh'] += r['drive_kw']*h
        previous = state
    if (previous not in ['stowed', teardown_end, *drive] or residual > 1e-5
            or abs(et-final_soc*tc) > 1e-5 or abs(es-c['service_final_soc']*sc) > 1e-5
            or max(daily.values()) > driving_limit_h+1e-6):
        raise ValueError('SOC final, balanço ou condução diária divergentes')
    return dict(totals, max_balance_residual_kwh=residual, daily_driving_h=daily,
                traction_final_soc=et/tc, service_final_soc=es/sc,
                transfer_loss_kwh=totals['transfer_input_kwh']*(1-c['transfer_efficiency_assumed']),
                external_charge_kwh=0., independently_feasible_in_model=True)
