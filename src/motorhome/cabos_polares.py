"""Seção de cabo r–theta: volumes finitos estacionários, dois materiais.

Por metro axial, sem condução axial/contatos/radiação/efeitos AC. Fonte Joule
homogeneizada no feixe, corrente espacialmente uniforme e R(T) linear.
As temperaturas são em K; a resistência elétrica de entrada é por metro.
"""

from dataclasses import dataclass

import numpy as np
from scipy.sparse import coo_matrix, diags
from scipy.sparse.linalg import spsolve


@dataclass(frozen=True)
class Cabo:
    raio_feixe_m: float
    raio_externo_m: float
    k_feixe_w_mk: float
    k_isolamento_w_mk: float
    resistencia20_ohm_m: float
    alpha_por_k: float = .00393
    referencia_k: float = 293.15

    def __post_init__(self):
        values = vars(self)
        if any(not np.isfinite(v) or v <= 0 for k, v in values.items() if k != 'alpha_por_k'):
            raise ValueError('Geometria e propriedades devem ser positivas e finitas')
        if not 0 <= self.alpha_por_k < 1 or self.raio_feixe_m >= self.raio_externo_m:
            raise ValueError('Coeficiente ou raios incompatíveis')


def resolver(cabo, corrente_a, nr=24, ntheta=64, h_w_m2k=10., ambiente_k=298.15):
    """Resolve K(T-Ta)=Joule(T), com Robin externo e periodicidade angular.

    nr é a quantidade de anéis EM CADA material. h e Ta aceitam vetores de
    ntheta setores. A lei afim de resistividade é acoplada diretamente na
    matriz; nenhuma temperatura do condutor é prescrita como resultado.
    Rejeita solução não física de aquecimento (instabilidade da lei linear).
    """
    if any(isinstance(n, bool) or not isinstance(n, int) or n < 3 for n in (nr, ntheta)):
        raise ValueError('Malha exige inteiros >=3')
    if not np.isfinite(corrente_a) or corrente_a < 0:
        raise ValueError('Corrente deve ser finita e não negativa')
    h = np.broadcast_to(np.asarray(h_w_m2k, dtype=float), (ntheta,))
    ta = np.broadcast_to(np.asarray(ambiente_k, dtype=float), (ntheta,))
    if np.any(~np.isfinite(h)) or np.any(h <= 0) or np.any(~np.isfinite(ta)) or np.any(ta <= 0):
        raise ValueError('Filme e temperatura ambiente devem ser positivos e finitos')
    rf = np.r_[np.linspace(0, cabo.raio_feixe_m, nr+1),
               np.linspace(cabo.raio_feixe_m, cabo.raio_externo_m, nr+1)[1:]]
    rc = (rf[1:]+rf[:-1])/2
    dtheta = 2*np.pi/ntheta
    theta = (np.arange(ntheta)+.5)*dtheta
    k = np.r_[np.full(nr, cabo.k_feixe_w_mk), np.full(nr, cabo.k_isolamento_w_mk)]
    area = np.broadcast_to((.5*np.diff(rf**2)*dtheta)[:, None], (2*nr, ntheta)).copy()
    size = 2*nr*ntheta
    diagonal = np.zeros(size)
    rows, cols, values = [], [], []

    def face(a, b, g):
        rows.extend([a, b])
        cols.extend([b, a])
        values.extend([-g, -g])
        diagonal[a] += g
        diagonal[b] += g

    for i in range(2*nr):
        for j in range(ntheta):
            a = i*ntheta+j
            if i+1 < 2*nr:
                # Resistências radiais logarítmicas em série, inclusive interface.
                g = dtheta/(np.log(rf[i+1]/rc[i])/k[i]
                            + np.log(rc[i+1]/rf[i+1])/k[i+1])
                face(a, a+ntheta, g)
            # Cada face angular é inserida uma única vez; fluxo nulo em r=0.
            g = k[i]*(rf[i+1]-rf[i])/(rc[i]*dtheta)
            face(a, i*ntheta+(j+1) % ntheta, g)
    gb = dtheta/(np.log(rf[-1]/rc[-1])/k[-1]+1/(h*rf[-1]))
    diagonal[-ntheta:] += gb
    rows.extend(range(size))
    cols.extend(range(size))
    values.extend(diagonal)
    conduction = coo_matrix((values, (rows, cols)), shape=(size, size)).tocsr()
    # A soma de s0 é I²R20 [W/m]; área do feixe inclui vazios, não A_nominal.
    s0 = np.zeros_like(area)
    s0[:nr] = corrente_a**2*cabo.resistencia20_ohm_m*area[:nr]/(np.pi*cabo.raio_feixe_m**2)
    slope = cabo.alpha_por_k*s0.ravel()
    # Subtrair uma referência reduz cancelamento por grandes valores absolutos.
    baseline = float(ta.min())
    rhs = s0.ravel()*(1+cabo.alpha_por_k*(baseline-cabo.referencia_k))
    rhs[-ntheta:] += gb*(ta-baseline)
    matrix = conduction-diags(slope)
    delta = spsolve(matrix, rhs)
    temp = (delta+baseline).reshape(area.shape)
    factor = 1+cabo.alpha_por_k*(temp-cabo.referencia_k)
    if np.any(~np.isfinite(temp)) or np.min(delta) < -1e-6 or np.min(factor[:nr]) <= 0:
        raise ValueError('Sem solução estacionária física para a lei/contornos adotados')
    joule = s0*factor
    generated = float(joule.sum())
    removed = float(np.sum(gb*(temp[-1]-ta)))
    surface = ta+gb*(temp[-1]-ta)/(h*rf[-1]*dtheta)
    residual = matrix@delta-rhs
    return {'r_m': rc, 'faces_r_m': rf, 'theta_rad': theta, 'area_m2': area,
            'temperatura_k': temp, 'joule_w_m': generated, 'removido_w_m': removed,
            'residuo_w_m': generated-removed,
            'residuo_max_celula_w_m': float(np.max(np.abs(residual))),
            'temperatura_media_feixe_k': float(np.sum(temp[:nr]*area[:nr])/area[:nr].sum()),
            'temperatura_max_k': float(temp.max()),
            'temperatura_superficie_k': surface,
            'variacao_angular_superficie_k': float(np.ptp(surface))}


def perfil_analitico_sem_feedback(cabo, corrente_a, h_w_m2k, ambiente_k, r_m):
    """Referência independente: fonte uniforme, alpha=0, Robin uniforme."""
    r = np.asarray(r_m)
    a, b = cabo.raio_feixe_m, cabo.raio_externo_m
    q = corrente_a**2*cabo.resistencia20_ohm_m
    ts = ambiente_k+q/(2*np.pi*b*h_w_m2k)
    interface = ts+q*np.log(b/a)/(2*np.pi*cabo.k_isolamento_w_mk)
    return np.where(r <= a, interface+q*(1-(r/a)**2)/(4*np.pi*cabo.k_feixe_w_mk),
                    ts+q*np.log(b/r)/(2*np.pi*cabo.k_isolamento_w_mk))
