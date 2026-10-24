"""Adaptação autoral mensurável; não reconstrói CAD de fabricante."""

import numpy as np


def mapa_linear_trechos(valores, origem, destino):
    """Interpola marcos monotônicos e extrapola por translação nos extremos."""
    x = np.asarray(valores, dtype=float)
    a, b = np.asarray(origem, dtype=float), np.asarray(destino, dtype=float)
    if (a.ndim != 1 or len(a) < 2 or a.shape != b.shape
            or not all(np.isfinite(v).all() for v in (x, a, b))
            or (np.diff(a) <= 0).any() or (np.diff(b) <= 0).any()):
        raise ValueError('Marcos finitos, crescentes e de mesmo tamanho obrigatórios')
    return np.where(x < a[0], x+b[0]-a[0],
                    np.where(x > a[-1], x+b[-1]-a[-1], np.interp(x, a, b)))


def adaptar_vertices(vertices, mapa_x, mapa_z, deslocamento_rigido=None):
    """Rodas e componentes escolhidos recebem só translação, sem deformação."""
    v = np.array(vertices, dtype=float, copy=True)
    if v.ndim != 2 or v.shape[1] != 3 or not np.isfinite(v).all():
        raise ValueError('Vértices Nx3 finitos obrigatórios')
    if deslocamento_rigido is not None:
        d = np.asarray(deslocamento_rigido, dtype=float)
        if d.shape != (3,) or not np.isfinite(d).all():
            raise ValueError('Translação deve ter três componentes finitas')
        return v+d
    v[:, 0] = mapa_linear_trechos(v[:, 0], *mapa_x)
    v[:, 2] = mapa_linear_trechos(v[:, 2], *mapa_z)
    return v
