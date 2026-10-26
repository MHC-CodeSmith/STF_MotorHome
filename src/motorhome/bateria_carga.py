"""ECM de carga com dois nós térmicos, SOC e balanços integrados.

Método reduzido autoral; parâmetros exigem calibração. Corrente positiva em
carga: P=Uoc*I+R*I² e Q=R*I²+I*T*dUoc/dT. Sem dinâmica RC/eletroquímica.
"""

import numpy as np
from scipy.integrate import solve_ivp


def corrente_carga(potencia_w, ocv_v, resistencia_ohm, limite_a, limite_v):
    vals = [potencia_w, ocv_v, resistencia_ohm, limite_a, limite_v]
    if any(not np.isfinite(v) for v in vals) or min(potencia_w, resistencia_ohm) < 0 or min(ocv_v, limite_a, limite_v) <= 0:
        raise ValueError('Parâmetros elétricos inválidos')
    current = 2*potencia_w/(ocv_v+np.sqrt(ocv_v**2+4*resistencia_ohm*potencia_w))
    if resistencia_ohm:
        current = min(current, max(0., (limite_v-ocv_v)/resistencia_ohm))
    elif ocv_v >= limite_v:
        current = 0.
    return min(current, limite_a)


def resolver(config, potencia_w, rtol=1e-8, max_step_s=30.):
    c = dict(config)
    required_positive = ['capacity_ah', 'reference_k', 'battery_mass_kg', 'battery_cp_j_kgk',
                         'coolant_mass_kg', 'coolant_cp_j_kgk', 'initial_battery_k',
                         'initial_coolant_k', 'maximum_current_a', 'maximum_voltage_v',
                         'temperature_stop_k', 'maximum_simulation_s', 'ambient_k']
    nonnegative = ['resistance_ref_ohm', 'resistance_soc_curvature', 'resistance_activation_over_r_k',
                   'battery_coolant_ua_w_k', 'cooler_ambient_ua_w_k']
    for name in required_positive+nonnegative:
        value = c[name]
        if not np.isfinite(value) or value < 0 or (name in required_positive and value == 0):
            raise ValueError(f'{name}: entrada inválida')
    if not 0 <= c['soc_initial'] < c['soc_final'] <= 1 or c['initial_battery_k'] >= c['temperature_stop_k']:
        raise ValueError('SOC ou temperatura inicial inválidos')
    if not np.isfinite(potencia_w) or potencia_w <= 0 or not np.isfinite(c['pack_entropy_v_k']):
        raise ValueError('Potência/entropia inválidas')
    zs, us = np.array(c['ocv_soc']), np.array(c['ocv_v'])
    if zs.ndim != 1 or len(zs) < 2 or zs.shape != us.shape or np.any(np.diff(zs) <= 0) or zs[0] > c['soc_initial'] or zs[-1] < c['soc_final'] or np.any(~np.isfinite(us)) or np.any(us <= 0):
        raise ValueError('CurvaOCV incompatível')
    cb = c['battery_mass_kg']*c['battery_cp_j_kgk']
    cc = c['coolant_mass_kg']*c['coolant_cp_j_kgk']

    def electrical(z, tb):
        u = float(np.interp(z, zs, us)+(tb-c['reference_k'])*c['pack_entropy_v_k'])
        r = c['resistance_ref_ohm']*(1+c['resistance_soc_curvature']*(z-.5)**2)*np.exp(c['resistance_activation_over_r_k']*(1/tb-1/c['reference_k']))
        i = corrente_carga(potencia_w, u, r, c['maximum_current_a'], c['maximum_voltage_v'])
        return u, r, i

    def rhs(t, y):
        z, tb, tc = y[:3]
        u, r, i = electrical(z, tb)
        ohmic = r*i*i
        rev = i*tb*c['pack_entropy_v_k']
        exchange = c['battery_coolant_ua_w_k']*(tb-tc)
        out = c['cooler_ambient_ua_w_k']*(tc-c['ambient_k'])
        return [i/(3600*c['capacity_ah']), (ohmic+rev-exchange)/cb, (exchange-out)/cc,
                (u+r*i)*i, u*i, ohmic, rev, out]

    def target(t, y):
        return y[0]-c['soc_final']
    target.terminal, target.direction = True, 1

    def hot(t, y):
        return y[1]-c['temperature_stop_k']
    hot.terminal, hot.direction = True, 1
    initial = [c['soc_initial'], c['initial_battery_k'], c['initial_coolant_k'], 0, 0, 0, 0, 0]
    solution = solve_ivp(rhs, [0, c['maximum_simulation_s']], initial, rtol=rtol,
                         atol=[1e-10, 1e-7, 1e-7, 1e-3, 1e-3, 1e-4, 1e-4, 1e-4],
                         max_step=max_step_s, events=[target, hot], dense_output=True)
    if not solution.success:
        raise ValueError(solution.message)
    end = float(solution.t[-1])
    times = np.unique(np.r_[np.arange(0, end, 30.), solution.t, end])
    values = solution.sol(times)
    rows = []
    for t, y in zip(times, values.T, strict=True):
        u, r, i = electrical(y[0], y[1])
        rows.append({'time_s': float(t), 'soc': float(y[0]), 'battery_k': float(y[1]),
                     'coolant_k': float(y[2]), 'current_a': i, 'terminal_v': u+r*i,
                     'accepted_power_w': (u+r*i)*i, 'ohmic_w': r*i*i,
                     'reversible_w': i*y[1]*c['pack_entropy_v_k']})
    y = values[:, -1]
    sensible = cb*(y[1]-initial[1])+cc*(y[2]-initial[2])
    return {'history': rows, 'stop': 'target_soc' if len(solution.t_events[0]) else ('temperature_limit' if len(solution.t_events[1]) else 'time_limit'),
            'duration_s': end, 'final_soc': float(y[0]), 'final_battery_k': float(y[1]),
            'max_battery_k': float(values[1].max()), 'terminal_energy_j': float(y[3]),
            'ocv_charge_integral_j': float(y[4]), 'ohmic_energy_j': float(y[5]),
            'reversible_energy_j': float(y[6]), 'cooling_energy_j': float(y[7]),
            'sensible_energy_j': float(sensible),
            'electrical_residual_j': float(y[3]-y[4]-y[5]),
            'thermal_residual_j': float(y[5]+y[6]-y[7]-sensible)}
