"""Menor tempo de viagem em grade de potências constantes, sem carga externa.

MILP: um modo por intervalo, última duração fracionária e distância exata.
O ótimo se refere à grade, não ao veículo físico nem a controle contínuo.
"""

import numpy as np
import pandas as pd
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix


def minimizar_tempo(inicios, duracao_s, velocidades_m_s, demandas_w, solar_w,
                    capacidade_j, soc_inicial, soc_minimo, distancia_m,
                    eficiencia_carga, eficiencia_descarga, limite_diario_s,
                    solar_durante_conducao, tempo_limite_s=30):
    """Chegada dentro do horizonte; reserva em todos os estados e até 8 h/dia.

    O primeiro início define a partida do relógio. Paradas antes da chegada
    consomem energia/tempo. Após chegar nada é contado. Solar e demandas são
    constantes em cada intervalo, inclusive no último intervalo fracionário.
    Não representa aceleração nem o perfil intraintervalo da irradiância.
    """
    if not isinstance(inicios, pd.DatetimeIndex) or inicios.tz is None or not len(inicios):
        raise ValueError('Índice temporal com fuso obrigatório')
    for x in [duracao_s, capacidade_j, distancia_m, limite_diario_s, tempo_limite_s]:
        if isinstance(x, bool) or not np.isfinite(x) or x <= 0:
            raise ValueError('Duração, energia, distância e limites devem ser positivos finitos')
    for x in [soc_inicial, soc_minimo, eficiencia_carga, eficiencia_descarga]:
        if isinstance(x, bool) or not np.isfinite(x) or not 0 <= x <= 1:
            raise ValueError('SOC/eficiências devem ser frações finitas')
    if soc_inicial < soc_minimo or min(eficiencia_carga, eficiencia_descarga) <= 0:
        raise ValueError('SOC inicial/eficiências incompatíveis')
    if not isinstance(solar_durante_conducao, bool):
        raise TypeError('Disponibilidade de solar em movimento deve ser explícita')
    v, p, pv = [np.asarray(x, dtype=float) for x in (velocidades_m_s, demandas_w, solar_w)]
    n = len(inicios)
    if (v.ndim != 1 or len(v) < 2 or p.shape != v.shape or pv.shape != (n,)
            or not all(np.isfinite(x).all() for x in (v, p, pv))
            or any((x < 0).any() for x in (v, p, pv)) or v[0] != 0 or not (v[1:] > 0).all()):
        raise ValueError('Modos parada/condução e geração não negativos obrigatórios')
    ends = inicios+pd.to_timedelta(duracao_s, unit='s')
    if n > 1 and not np.allclose((inicios[1:]-inicios[:-1]).total_seconds(), duracao_s):
        raise ValueError('Grade deve ser contínua')
    if any(t.date() != (e-pd.Timedelta(nanoseconds=1)).date() for t, e in zip(inicios, ends)):
        raise ValueError('Dividir intervalos nas meias-noites locais')
    k, dt = len(v), duracao_s/3600
    available = np.broadcast_to(pv[:, None], (n, k)).copy()
    if not solar_durante_conducao:
        available[:, 1:] = 0
    net = available-p[None, :]
    # SOC por hora de operação; evita coeficientes pequenos em segundos.
    rate = np.where(net >= 0, net*eficiencia_carga, net/eficiencia_descarga)*3600/capacidade_j
    positive = np.maximum(rate, 0)
    # z modo binário; h duração em horas; e SOC; c corte; a viagem ainda ativa.
    hbase, ebase, cbase, abase = n*k, 2*n*k, 2*n*k+n, 2*n*k+2*n
    count = abase+n+1
    lower, upper = np.zeros(count), np.full(count, np.inf)
    upper[:hbase], upper[hbase:ebase] = 1, dt
    lower[ebase:cbase], upper[ebase:cbase] = soc_minimo, 1
    upper[abase:] = 1
    lower[abase] = upper[abase] = 1
    upper[-1] = 0  # horizonte deve conter a chegada
    integrality = np.zeros(count)
    integrality[:hbase] = integrality[abase:] = 1
    objective = np.zeros(count)
    objective[hbase:ebase] = 1
    days = sorted({t.date() for t in inicios})
    mat = lil_matrix((n*(k+6)+len(days)+1, count))
    lo, hi = np.full(mat.shape[0], -np.inf), np.full(mat.shape[0], np.inf)
    row = 0
    for t in range(n):
        zs, hs = slice(t*k, (t+1)*k), slice(hbase+t*k, hbase+(t+1)*k)
        mat[row, zs], mat[row, abase+t] = 1, -1
        lo[row] = hi[row] = 0; row += 1
        for mode in range(k):
            mat[row, hbase+t*k+mode], mat[row, t*k+mode] = 1, -dt
            hi[row] = 0; row += 1
        # Duração integral antes da última etapa; parcial apenas na chegada.
        mat[row, hs], mat[row, abase+t] = 1, -dt
        hi[row] = 0; row += 1
        mat[row, hs], mat[row, abase+t+1] = 1, -dt
        lo[row] = 0; row += 1
        mat[row, abase+t+1], mat[row, abase+t] = 1, -1
        hi[row] = 0; row += 1
        mat[row, ebase+t], mat[row, cbase+t], mat[row, hs] = 1, 1, -rate[t]
        if t:
            mat[row, ebase+t-1] = -1
            lo[row] = hi[row] = 0
        else:
            lo[row] = hi[row] = soc_inicial
        row += 1
        mat[row, cbase+t], mat[row, hs] = 1, -positive[t]
        hi[row] = 0; row += 1
    for day in days:
        for t, start in enumerate(inicios):
            if start.date() == day:
                mat[row, hbase+t*k+1:hbase+(t+1)*k] = 1
        hi[row] = limite_diario_s/3600; row += 1
    mat[row, hbase:ebase] = np.tile(v*3.6, n)
    lo[row] = hi[row] = distancia_m/1000
    result = milp(objective, integrality=integrality, bounds=Bounds(lower, upper),
                  constraints=LinearConstraint(mat.tocsr(), lo, hi),
                  options={'time_limit': tempo_limite_s, 'mip_rel_gap': 1e-7})
    common = {'solver_status': int(result.status), 'message': result.message,
              'optimal_in_grid': result.status == 0, 'vehicle_validated': False,
              'scope': 'potências constantes por intervalo, modos discretos, chegada fracionária'}
    if result.x is None:
        return dict(common, feasible=False)
    h = result.x[hbase:ebase].reshape(n, k)
    states, cuts = result.x[ebase:cbase], result.x[cbase:abase]
    previous, residual, rows = soc_inicial, 0., []
    for t in range(n):
        residual = max(residual, abs(states[t]-previous-rate[t]@h[t]+cuts[t]))
        previous = states[t]
        if h[t].sum() < 1e-8:
            continue
        if np.sum(h[t] > 1e-7) != 1:
            raise ValueError('Solução mistura modos no mesmo intervalo')
        mode = int(np.argmax(h[t]))
        seconds = float(h[t, mode]*3600)
        rows.append({'start': inicios[t].isoformat(),
                     'end': (inicios[t]+pd.to_timedelta(seconds, unit='s')).isoformat(),
                     'duration_s': seconds, 'mode': mode, 'speed_m_s': float(v[mode]),
                     'terminal_demand_w': float(p[mode]), 'solar_w': float(available[t, mode]),
                     'soc_final': float(states[t]), 'curtailed_battery_charge_j': float(cuts[t]*capacidade_j)})
    actual_distance = float(np.sum(h*(v*3600)[None, :]))
    daily = {str(day): float(sum(h[t, 1:].sum()*3600 for t in range(n) if inicios[t].date() == day)) for day in days}
    if (residual > 1e-6 or abs(actual_distance-distancia_m) > max(1e-3, distancia_m*1e-7)
            or (states < soc_minimo-1e-6).any() or (states > 1+1e-6).any()
            or max(daily.values()) > limite_diario_s+1e-3):
        raise ValueError('Falha na verificação independente de energia/distância/limites')
    # Duração total precisa incluir todas as esperas, não apenas horas ao volante.
    elapsed = float(h.sum()*3600)
    arrival = pd.Timestamp(rows[-1]['end'])
    if abs((arrival-inicios[0]).total_seconds()-elapsed) > 1e-3:
        raise ValueError('Agenda com lacuna temporal antes da chegada')
    return dict(common, feasible=True, distance_m=actual_distance, elapsed_s=elapsed,
                arrival=arrival.isoformat(), final_soc=float(states[-1]), daily_driving_s=daily,
                max_soc_balance_residual=residual, schedule=rows,
                lower_bound_elapsed_s=float(result.mip_dual_bound*3600),
                mip_gap=float(result.mip_gap))
