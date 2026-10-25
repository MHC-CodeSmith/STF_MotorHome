"""Sombra geométrica de retângulos horizontais paralelos, direção solar explícita."""

from math import isfinite

from shapely.affinity import translate
from shapely.geometry import box
from shapely.ops import unary_union


def fracoes_sombreadas(inferiores, superiores, diferenca_altura_m, vetor_solar):
    """Retângulos (xmin,ymin,xmax,ymax); vetor aponta para o sol no mesmo referencial.

    Só bloqueio direto. Não representa perdas elétricas de diodos/strings nem
    obstrução de céu difuso. Quando o sol está abaixo do horizonte retorna zeros.
    """
    values = [diferenca_altura_m, *vetor_solar]
    if not all(isfinite(v) for v in values) or diferenca_altura_m < 0:
        raise ValueError('Geometria e vetor solar finitos, deltaZ não negativo')
    low, high = [], []
    for rectangles, target in [(inferiores, low), (superiores, high)]:
        for rect in rectangles:
            if len(rect) != 4 or not all(isfinite(v) for v in rect) or rect[2] <= rect[0] or rect[3] <= rect[1]:
                raise ValueError('Retângulos positivos e finitos')
            target.append(box(*rect))
    sx, sy, sz = vetor_solar
    if sz <= 0 or not high:
        return [0.]*len(low)
    shadow = unary_union([translate(poly, -diferenca_altura_m*sx/sz,
                                    -diferenca_altura_m*sy/sz) for poly in high])
    return [min(1., max(0., poly.intersection(shadow).area/poly.area)) for poly in low]
