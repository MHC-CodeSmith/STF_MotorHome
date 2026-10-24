"""Otimização MILP em grade temporal/modos discretos; não escolhe dados físicos.

Maximiza distância em horizonte fixo, respeitando energia em cada passo, reserva,
capacidade, SOC final e limite diário. Ótimo apenas na discretização fornecida.
"""

import numpy as np
import pandas as pd
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix


def maximizar_distancia(inicios, duracao_s, velocidades_m_s, demandas_w, solar_w,
                       capacidade_j, soc_inicial, soc_minimo, soc_final,
                       tolerancia_soc, eficiencia_carga, eficiencia_descarga,
                       limite_diario_s, solar_durante_conducao, tempo_limite_s=30):
    """Um modo (parada ou velocidade) por intervalo; potências constantes.

    Solar excedente pode ser cortado. Reservas avaliadas em todas as bordas; como
    o saldo é constante em cada passo, não há déficit intermediário oculto.
    Índice deve estar no fuso do projeto e os passos não podem cruzar meia-noite.
    Potências terminais por modo DEVEM vir de modelo validado ou caso sintético
    rotulado. Sem CC/CV, limites de corrente, acelerações ou carga externa.
    """
    if not isinstance(inicios, pd.DatetimeIndex) or inicios.tz is None or len(inicios) < 1:
        raise ValueError('Índice de inícios com fuso obrigatório')
    scalars = [duracao_s, capacidade_j, limite_diario_s, tempo_limite_s]
    if any(isinstance(x, bool) or not np.isfinite(x) or x <= 0 for x in scalars):
        raise ValueError('Duração, capacidade e limites devem ser positivos finitos')
    for x in [soc_inicial, soc_minimo, soc_final, tolerancia_soc, eficiencia_carga, eficiencia_descarga]:
        if isinstance(x, bool) or not np.isfinite(x) or not 0 <= x <= 1:
            raise ValueError('SOC, tolerância e eficiências devem ser frações finitas')
    if min(eficiencia_carga, eficiencia_descarga) <= 0 or soc_inicial < soc_minimo:
        raise ValueError('Eficiências positivas e SOC inicial acima da reserva obrigatórios')
    if not isinstance(solar_durante_conducao, bool):
        raise TypeError('Disponibilidade de solar em condução deve ser explícita')
    v, p, pv = (np.asarray(x, dtype=float) for x in [velocidades_m_s, demandas_w, solar_w])
    n, k = len(inicios), len(v)
    if (v.ndim != 1 or p.shape != v.shape or pv.shape != (n,) or k < 2
            or not all(np.isfinite(x).all() for x in [v, p, pv])
            or any((x < 0).any() for x in [v, p, pv]) or v[0] != 0 or not (v[1:] > 0).all()):
        raise ValueError('Modos parada/condução e série solar não negativos finitos obrigatórios')
    ends = inicios+pd.to_timedelta(duracao_s, unit='s')
    if n > 1 and not np.allclose((inicios[1:]-inicios[:-1]).total_seconds(), duracao_s):
        raise ValueError('Grade deve ser contínua')
    if any(t.date() != (e-pd.Timedelta(nanoseconds=1)).date() for t, e in zip(inicios, ends)):
        raise ValueError('Dividir intervalos nas meias-noites locais antes de otimizar')
    available = np.broadcast_to(pv[:, None], (n, k)).copy()
    if not solar_durante_conducao:
        available[:, 1:] = 0
    net = available-p[None, :]
    delta = np.where(net >= 0, net*eficiencia_carga, net/eficiencia_descarga)*duracao_s/capacidade_j
    positive = np.maximum(delta, 0)
    # Variáveis: z[t,modo] binária, estado[t] em fração, corte[t] em fração.
    count = n*k+2*n
    ebase, cbase = n*k, n*k+n
    objective = np.zeros(count)
    objective[:n*k] = np.tile(-v*duracao_s/1000, n)
    lower, upper = np.zeros(count), np.full(count, np.inf)
    upper[:n*k] = 1
    lower[ebase:cbase], upper[ebase:cbase] = soc_minimo, 1
    lower[cbase-1], upper[cbase-1] = max(soc_minimo, soc_final-tolerancia_soc), min(1, soc_final+tolerancia_soc)
    if lower[cbase-1] > upper[cbase-1]:
        raise ValueError('SOC final incompatível com reserva')
    integrality = np.zeros(count)
    integrality[:n*k] = 1
    days = sorted({t.date() for t in inicios})
    mat = lil_matrix((3*n+len(days), count))
    lo, hi = np.full(mat.shape[0], -np.inf), np.full(mat.shape[0], np.inf)
    for t in range(n):
        sl = slice(t*k, (t+1)*k)
        mat[t, sl], lo[t], hi[t] = 1, 1, 1
        row = n+t
        mat[row, ebase+t], mat[row, cbase+t] = 1, 1
        mat[row, sl] = -delta[t]
        if t:
            mat[row, ebase+t-1] = -1
            lo[row] = hi[row] = 0
        else:
            lo[row] = hi[row] = soc_inicial
        mat[2*n+t, cbase+t] = 1
        mat[2*n+t, sl] = -positive[t]
        hi[2*n+t] = 0
    for i, day in enumerate(days):
        row = 3*n+i
        for t, date in enumerate(inicios):
            if date.date() == day:
                mat[row, t*k+1:(t+1)*k] = duracao_s
        hi[row] = limite_diario_s
    result = milp(objective, integrality=integrality, bounds=Bounds(lower, upper),
                  constraints=LinearConstraint(mat.tocsr(), lo, hi),
                  options={'time_limit': tempo_limite_s, 'mip_rel_gap': 1e-7})
    if result.x is None:
        return {'feasible': False, 'solver_status': int(result.status), 'message': result.message,
                'optimal_in_grid': False, 'vehicle_validated': False}
    modes = np.argmax(result.x[:n*k].reshape(n, k), axis=1)
    states = result.x[ebase:cbase]
    cut = result.x[cbase:]*capacidade_j
    previous, max_residual, rows = soc_inicial, 0., []
    for t, mode in enumerate(modes):
        err = states[t]-previous-delta[t, mode]+cut[t]/capacidade_j
        max_residual = max(max_residual, abs(err))
        rows.append({'start': inicios[t].isoformat(), 'end': ends[t].isoformat(),
                     'mode': int(mode), 'speed_m_s': float(v[mode]), 'terminal_demand_w': float(p[mode]),
                     'available_solar_w': float(available[t, mode]), 'soc_final': float(states[t]),
                     'battery_charge_curtailed_j': float(cut[t])})
        previous = states[t]
    if max_residual > 1e-6 or (states < soc_minimo-1e-6).any() or (states > 1+1e-6).any():
        raise ValueError('Solução falhou na verificação independente de energia/limites')
    daily = {str(day): sum(duracao_s for t, mode in enumerate(modes) if inicios[t].date() == day and mode > 0) for day in days}
    return {'feasible': True, 'optimal_in_grid': result.status == 0, 'solver_status': int(result.status),
            'message': result.message, 'distance_m': float(np.sum(v[modes])*duracao_s),
            'daily_driving_s': daily, 'final_soc': float(states[-1]),
            'max_soc_balance_residual': max_residual, 'schedule': rows,
            'vehicle_validated': False, 'scope': 'horizonte e velocidades discretos; não prova ótimo contínuo I29'}
