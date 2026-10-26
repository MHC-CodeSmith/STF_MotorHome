"""Circuito fechado: curva publicada interpolada e Darcy–Weisbach em SI."""

from dataclasses import dataclass

import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq


@dataclass(frozen=True)
class Circuito:
    comprimento_m: float
    diametro_m: float
    rugosidade_m: float
    soma_k: float
    rho_kg_m3: float
    mu_pa_s: float
    vazao_referencia_m3_s: float
    perda_componentes_referencia_pa: float

    def __post_init__(self):
        for key, value in vars(self).items():
            if not np.isfinite(value) or value < 0:
                raise ValueError(f'{key}: valor inválido')
        if min(self.diametro_m, self.rho_kg_m3, self.mu_pa_s, self.vazao_referencia_m3_s) <= 0:
            raise ValueError('Diâmetro, propriedades e vazão de referência positivos')


def fator_darcy(reynolds, rugosidade_relativa):
    """64/Re laminar; Haaland turbulento; transição2300–4000 interpolada."""
    if not np.isfinite(reynolds) or reynolds <= 0 or not np.isfinite(rugosidade_relativa) or rugosidade_relativa < 0:
        raise ValueError('Re e rugosidade inválidos')
    laminar = 64/reynolds
    turbulent = (-1.8*np.log10((rugosidade_relativa/3.7)**1.11+6.9/reynolds))**-2
    weight = np.clip((reynolds-2300)/1700, 0, 1)
    return float((1-weight)*laminar+weight*turbulent)


def perda(circuito, vazao_m3_s):
    if not np.isfinite(vazao_m3_s) or vazao_m3_s < 0:
        raise ValueError('Vazão deve ser finita e não negativa')
    if vazao_m3_s == 0:
        return {'total_pa': 0., 'tubos_pa': 0., 'singularidades_pa': 0., 'componentes_pa': 0., 're': 0., 'f_darcy': 0.}
    c = circuito
    vel = vazao_m3_s/(np.pi*c.diametro_m**2/4)
    re = c.rho_kg_m3*vel*c.diametro_m/c.mu_pa_s
    f = fator_darcy(re, c.rugosidade_m/c.diametro_m)
    dynamic = c.rho_kg_m3*vel**2/2
    pipe = f*c.comprimento_m/c.diametro_m*dynamic
    minor = c.soma_k*dynamic
    components = c.perda_componentes_referencia_pa*(vazao_m3_s/c.vazao_referencia_m3_s)**2
    return {'total_pa': float(pipe+minor+components), 'tubos_pa': float(pipe),
            'singularidades_pa': float(minor), 'componentes_pa': float(components), 're': float(re), 'f_darcy': f}


def ponto_operacao(circuito, vazoes_m3_s, pressoes_pa, correntes_a, tensao_v=12., deslocamento_curva_pa=0.):
    q, p, i = [np.asarray(v, dtype=float) for v in (vazoes_m3_s, pressoes_pa, correntes_a)]
    if q.ndim != 1 or len(q) < 3 or p.shape != q.shape or i.shape != q.shape:
        raise ValueError('Curvas com formas incompatíveis')
    if any(np.any(~np.isfinite(v)) or np.any(v < 0) for v in (q, p, i)) or np.any(np.diff(q) <= 0):
        raise ValueError('Curva inválida ou vazões não crescentes')
    if not np.isfinite(tensao_v) or tensao_v <= 0 or not np.isfinite(deslocamento_curva_pa):
        raise ValueError('Tensão/deslocamento inválidos')
    pressure = PchipInterpolator(q, p, extrapolate=False)
    current = PchipInterpolator(q, i, extrapolate=False)
    def residual(flow):
        return float(pressure(flow))+deslocamento_curva_pa-perda(circuito, flow)['total_pa']
    if residual(q[0]) <= 0 or residual(q[-1]) >= 0:
        raise ValueError('Sem interseção demonstrada no domínio publicado; não extrapolar')
    # Circuito crescente e curva decrescente na região operacional; checar unicidade.
    sample = np.array([residual(x) for x in np.linspace(q[0], q[-1], 1001)])
    if np.count_nonzero(np.diff(np.sign(sample)) < 0) != 1:
        raise ValueError('Interseção não única/demonstrada')
    flow = brentq(residual, q[0], q[-1], xtol=1e-14)
    dp = perda(circuito, flow)
    amps = float(current(flow))
    return {'flow_m3_s': flow, 'flow_l_min': flow*60000,
            'mass_flow_kg_s': flow*circuito.rho_kg_m3,
            'pump_pressure_pa': float(pressure(flow))+deslocamento_curva_pa,
            'current_a': amps, 'electric_power_w': amps*tensao_v,
            'hydraulic_power_w': flow*dp['total_pa'],
            'pump_electrohydraulic_efficiency': flow*dp['total_pa']/(amps*tensao_v),
            'pressure_residual_pa': residual(flow), 'system': dp}
