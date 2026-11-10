"""Modelos de integração dimensional, estrutural e hídrica, SI.

Hipóteses e dados de cenário pertencem ao YAML canônico. Nenhuma função
homologa instalação ou fornece parâmetros proprietários OEM.
"""
import math

import numpy as np


def caixa_intersecao(a, b, tol=1e-9):
    """Volume de interseção AABB em m³; encostar não é colisão."""
    lo = np.maximum(a['position_m'], b['position_m'])
    hi = np.minimum(np.array(a['position_m'])+a['dimensions_m'],
                    np.array(b['position_m'])+b['dimensions_m'])
    delta = hi-lo
    return float(np.prod(delta)) if np.all(delta > tol) else 0.


def centro_massa(parts):
    masses = np.asarray([p['mass_kg'] for p in parts], dtype=float)
    coords = np.asarray([p['cg_m'] for p in parts], dtype=float)
    if not np.isfinite(masses).all() or (masses < 0).any() or masses.sum() <= 0:
        raise ValueError('Massas inválidas')
    if coords.shape != (len(parts), 3) or not np.isfinite(coords).all():
        raise ValueError('Coordenadas inválidas')
    return float(masses.sum()), (masses @ coords/masses.sum()).tolist()


def viga_fem(length_m, elastic_pa, inertia_m4, load_n_m, elements=16):
    """Euler-Bernoulli, biapoiada, carga uniforme; 2 DOF/nó, carga consistente.

    Elementos Hermite cúbicos. Retorna deslocamentos/rotações e reações.
    Deslocamento positivo no sentido da carga; sem cisalhamento/torção/juntas.
    """
    if min(length_m, elastic_pa, inertia_m4) <= 0 or elements < 2 or not math.isfinite(load_n_m):
        raise ValueError('Parâmetro de viga inválido')
    h = length_m/elements
    k = elastic_pa*inertia_m4/h**3*np.array([
        [12,6*h,-12,6*h], [6*h,4*h*h,-6*h,2*h*h],
        [-12,-6*h,12,-6*h], [6*h,2*h*h,-6*h,4*h*h]])
    f = load_n_m*np.array([h/2,h*h/12,h/2,-h*h/12])
    matrix = np.zeros((2*(elements+1),)*2)
    force = np.zeros(2*(elements+1))
    for i in range(elements):
        idx = np.arange(2*i,2*i+4)
        matrix[np.ix_(idx,idx)] += k
        force[idx] += f
    free = np.setdiff1d(np.arange(len(force)), [0,2*elements])
    u = np.zeros_like(force)
    u[free] = np.linalg.solve(matrix[np.ix_(free,free)],force[free])
    reaction = matrix@u-force
    reference = 5*load_n_m*length_m**4/(384*elastic_pa*inertia_m4)
    return {'x_m': np.linspace(0,length_m,elements+1).tolist(),
            'displacement_m': u[::2].tolist(), 'rotation_rad': u[1::2].tolist(),
            'max_displacement_m': float(max(abs(u[::2]))),
            'analytic_max_m': abs(reference),
            'force_residual_n': float(reaction[0]+reaction[-2]+force[::2].sum()),
            'reactions_n': [-float(reaction[0]),-float(reaction[-2])],
            'strain_energy_j': float(.5*u@matrix@u)}


def consumir_agua(state, clean_draw_l, black_fraction=0., evaporated_l=0.):
    """Transfere água entre tanques, sem inventar massa ou exceder capacidade."""
    if clean_draw_l < 0 or not 0 <= black_fraction <= 1 or not 0 <= evaporated_l <= clean_draw_l:
        raise ValueError('Consumo hídrico inválido')
    out = dict(state)
    if clean_draw_l > out['clean_l']+1e-9:
        raise ValueError('Água limpa insuficiente')
    waste = clean_draw_l-evaporated_l
    out['clean_l'] -= clean_draw_l
    out['black_l'] += waste*black_fraction
    out['grey_l'] += waste*(1-black_fraction)
    if out['black_l'] > 20+1e-9 or out['grey_l'] > 70+1e-9:
        raise ValueError('Capacidade de resíduos excedida')
    before = sum(state[k] for k in ['clean_l','grey_l','black_l'])
    after = sum(out[k] for k in ['clean_l','grey_l','black_l'])
    out['residual_l'] = before-after-evaporated_l
    return out


def vazao_chamine(area_low_m2, area_high_m2, height_m, inside_c, outside_c, cd=.6):
    """Aberturas em série, vento nulo; vazão volumétrica em m³/s."""
    if min(area_low_m2,area_high_m2,height_m) <= 0 or min(inside_c,outside_c) <= -273.15 or not 0 < cd <= 1:
        raise ValueError('Aberturas/temperaturas inválidas')
    effective = 1/math.sqrt(area_low_m2**-2+area_high_m2**-2)
    return cd*effective*math.sqrt(2*9.80665*height_m*abs(inside_c-outside_c)/(273.15+(inside_c+outside_c)/2))
