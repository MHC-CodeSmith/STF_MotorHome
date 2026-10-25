"""Triagens geométricas de envelopes; não substituem colisão de sólidos reais."""

import numpy as np


def verificar_caixas(caixas, dimensoes):
    """Envelopes axis-aligned em SI; encostar é permitido, sobrepor volume não."""
    dim = np.asarray(dimensoes, dtype=float)
    if dim.shape != (3,) or not np.isfinite(dim).all() or (dim <= 0).any():
        raise ValueError('Dimensões positivas finitas em três eixos')
    bounds = []
    fora = []
    ids = set()
    for box in caixas:
        name = box['id']
        if name in ids:
            raise ValueError('Identificador duplicado')
        ids.add(name)
        lo = np.asarray(box['position_xyz_m'], dtype=float)
        size = np.asarray(box['dimensions_xyz_m'], dtype=float)
        if (lo.shape != (3,) or size.shape != (3,) or not np.isfinite(lo).all()
                or not np.isfinite(size).all() or (size <= 0).any()):
            raise ValueError('Envelope inválido')
        hi = lo+size
        if (lo < -1e-9).any() or (hi > dim+1e-9).any():
            fora.append(name)
        bounds.append((name, lo, hi))
    overlaps = []
    for i, (name, lo, hi) in enumerate(bounds):
        for other, low, high in bounds[i+1:]:
            if (np.minimum(hi, high)-np.maximum(lo, low) > 1e-9).all():
                overlaps.append([name, other])
    return {'outside': fora, 'overlaps': overlaps, 'envelope_check_passed': not fora and not overlaps}


def arranjos_em_grade(comprimento, largura, modulo_x, modulo_y, folga, margem):
    """Enumera grades sem obstáculos, ambas orientações, sem presumir teto plano."""
    vals = np.asarray([comprimento, largura, modulo_x, modulo_y, folga, margem], dtype=float)
    if not np.isfinite(vals).all() or (vals[:4] <= 0).any() or (vals[4:] < 0).any():
        raise ValueError('Dimensões positivas e folgas não negativas')
    result = []
    for x, y in [(modulo_x, modulo_y), (modulo_y, modulo_x)]:
        nx = max(0, int(np.floor((comprimento-2*margem+folga)/(x+folga)+1e-10)))
        ny = max(0, int(np.floor((largura-2*margem+folga)/(y+folga)+1e-10)))
        result.append({'nx': nx, 'ny': ny, 'count': nx*ny, 'module_x_m': x, 'module_y_m': y})
    return result
