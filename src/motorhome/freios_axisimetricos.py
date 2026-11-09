"""I33: condução transiente r–z em uma pista anular de disco ventilado.

Uma placa é resolvida; a placa oposta é idêntica. Aletas, cubo e pastilha
não são malhados. Fonte média na circunferência, propriedades constantes.
Volumetria cilíndrica exata; Crank–Nicolson e fluxos de face conservativos.
"""

from dataclasses import dataclass

import numpy as np
from scipy.sparse import coo_matrix, diags
from scipy.sparse.linalg import factorized


@dataclass(frozen=True)
class Pista:
    raio_interno_m: float = .09
    raio_externo_m: float = .15
    espessura_placa_m: float = .008
    contato_interno_m: float = .10
    contato_externo_m: float = .145
    densidade_kg_m3: float = 7100.
    cp_j_kgk: float = 500.
    k_w_mk: float = 51.

    def __post_init__(self):
        if any(not np.isfinite(v) or v <= 0 for v in vars(self).values()):
            raise ValueError('Propriedades devem ser positivas e finitas')
        if not self.raio_interno_m <= self.contato_interno_m < self.contato_externo_m <= self.raio_externo_m:
            raise ValueError('Anel de contato fora da pista')


def energia_frenagem(massa_kg, vi_m_s=30., vf_m_s=10., duracao_s=5.):
    """Energia translacional; não inclui inércias rotativas ou resistências."""
    vals = [massa_kg, vi_m_s, vf_m_s, duracao_s]
    if any(not np.isfinite(v) for v in vals) or massa_kg <= 0 or duracao_s <= 0 or not vi_m_s > vf_m_s >= 0:
        raise ValueError('Massa, velocidades ou duração inválidas')
    return .5*massa_kg*(vi_m_s**2-vf_m_s**2)


def placa_analitica(espessura_m, nz, tempo_s, fluxo_inicial_w_m2, declive_relativo_s,
                    densidade_kg_m3=7100., cp_j_kgk=500., k_w_mk=51., modos=1000):
    """Verificação independente: placa adiabática com q(t)=q0*(1-b*t).

    Série própria de cossenos para médias celulares axiais, face z=0 isolada
    e fluxo imposto em z=L. Retorna elevação em K. Sem usar matriz numérica.
    """
    n = np.arange(1, modos+1, dtype=float)
    lam = k_w_mk/(densidade_kg_m3*cp_j_kgk)*(n*np.pi/espessura_m)**2
    e = np.exp(-lam*tempo_s)
    integral = ((1-declive_relativo_s*tempo_s)*(-np.expm1(-lam*tempo_s))/lam
                + declive_relativo_s*(1-(1+lam*tempo_s)*e)/lam**2)
    coef = 2*(-1.)**n*fluxo_inicial_w_m2/(densidade_kg_m3*cp_j_kgk*espessura_m)*integral
    xf = np.linspace(0, 1, nz+1)
    averages = np.diff(np.sin(n[:, None]*np.pi*xf), axis=1)/(n[:, None]*np.pi/nz)
    mean = fluxo_inicial_w_m2*(tempo_s-.5*declive_relativo_s*tempo_s**2)/(densidade_kg_m3*cp_j_kgk*espessura_m)
    return mean+coef@averages


def resolver(pista, massa_kg=4250., fracao_eixo=.7, fracao_disco=.9,
             fracao_regenerada=0., nr=48, nz=16, dt_s=.01, duracao_s=5.,
             vi_m_s=30., vf_m_s=10., h_externo_w_m2k=20.,
             h_canal_w_m2k=50., ambiente_k=298.15,
             potencia_total_friccao_w=None):
    """Aquece duas faces de um disco; retorna a placa equivalente r–z.

    Potência de um disco = m*(-dv/dt)*v*(1-regen)*f_eixo*f_disco/2.
    Cada placa recebe metade. Fluxo uniforme no anel (desgaste uniforme).
    Robin nas faces axiais e raio externo; raio interno adiabático.
    Valores de h são hipóteses independentes, não função OEM de velocidade.
    Callback opcional(t) fornece potência total mecânica nos freios por atrito,
    já descontadas resistências e regeneração. Não combinar com fração regen.
    """
    energia = energia_frenagem(massa_kg, vi_m_s, vf_m_s, duracao_s)
    fractions = [fracao_eixo, fracao_disco, fracao_regenerada]
    if any(not np.isfinite(f) or not 0 <= f <= 1 for f in fractions):
        raise ValueError('Frações fora de [0,1]')
    if potencia_total_friccao_w is not None and (
            not callable(potencia_total_friccao_w) or fracao_regenerada != 0):
        raise ValueError('Perfil de atrito exige callback e regeneração já descontada')

    def potencia_placa(t):
        demand = massa_kg*(vi_m_s-vf_m_s)/duracao_s*(vi_m_s-(vi_m_s-vf_m_s)/duracao_s*t)
        if potencia_total_friccao_w is None:
            return demand*(1-fracao_regenerada)*fracao_eixo*fracao_disco/4
        friction = potencia_total_friccao_w(t)
        if not np.isfinite(friction) or not 0 <= friction <= demand+1e-6:
            raise ValueError('Potência de atrito fora da demanda mecânica')
        return friction*fracao_eixo*fracao_disco/4
    if any(isinstance(n, bool) or not isinstance(n, int) or n < 2 for n in (nr, nz)):
        raise ValueError('Malhas exigem inteiros >=2')
    if not np.isfinite(dt_s) or dt_s <= 0 or not np.isfinite(ambiente_k) or ambiente_k <= 0:
        raise ValueError('Passo e temperatura inválidos')
    if any(not np.isfinite(h) or h < 0 for h in (h_externo_w_m2k, h_canal_w_m2k)):
        raise ValueError('Convecção inválida')
    rf = np.linspace(pista.raio_interno_m, pista.raio_externo_m, nr+1)
    rc = (rf[:-1]+rf[1:])/2
    dz = pista.espessura_placa_m/nz
    zc = (np.arange(nz)+.5)*dz
    area = np.pi*np.diff(rf**2)
    volume = np.broadcast_to((area*dz)[:, None], (nr, nz)).copy()
    capacity = (volume*pista.densidade_kg_m3*pista.cp_j_kgk).ravel()
    size = nr*nz
    diagonal, robin = np.zeros(size), np.zeros(size)
    rows, cols, data = [], [], []

    def face(a, b, g):
        rows.extend([a, b]); cols.extend([b, a]); data.extend([-g, -g])
        diagonal[a] += g
        diagonal[b] += g

    k = pista.k_w_mk
    for i in range(nr):
        for j in range(nz):
            a = i*nz+j
            if i+1 < nr:
                face(a, a+nz, 2*np.pi*k*dz/np.log(rc[i+1]/rc[i]))
            if j+1 < nz:
                face(a, a+1, k*area[i]/dz)
        robin[i*nz] += area[i]/(1/h_canal_w_m2k+dz/(2*k)) if h_canal_w_m2k else 0.
        robin[i*nz+nz-1] += area[i]/(1/h_externo_w_m2k+dz/(2*k)) if h_externo_w_m2k else 0.
    if h_externo_w_m2k:
        robin[-nz:] += 2*np.pi*rf[-1]*dz/(1/h_externo_w_m2k+(rf[-1]-rc[-1])/k)
    matrix = coo_matrix((data, (rows, cols)), shape=(size, size)).tocsr()+diags(diagonal+robin)
    overlap = np.pi*np.maximum(0., np.minimum(rf[1:], pista.contato_externo_m)**2
                              - np.maximum(rf[:-1], pista.contato_interno_m)**2)
    weights = overlap/overlap.sum()
    resistance = dz/(2*k)
    source_factor = 1/(1+h_externo_w_m2k*resistance)
    source = np.zeros(size)
    source[nz-1::nz] = weights*source_factor
    steps = int(np.ceil(duracao_s/dt_s))
    dt = duracao_s/steps
    mass_matrix = diags(capacity/dt)
    solve = factorized((mass_matrix+.5*matrix).tocsc())
    rhs_matrix = mass_matrix-.5*matrix
    theta = np.zeros(size)
    cumulative_in, cumulative_out = 0., 0.
    trace = [{'tempo_s': 0., 'tmax_celula_k': ambiente_k, 'tmax_superficie_k': ambiente_k,
              'energia_entrada_placa_j': 0., 'energia_saida_placa_j': 0., 'energia_armazenada_placa_j': 0.}]
    peak_surface = ambiente_k
    surface = np.full(nr, ambiente_k)
    for step in range(steps):
        t = (step+1)*dt
        power = potencia_placa(t-dt/2)
        new = solve(rhs_matrix@theta+source*power)
        cumulative_in += power*dt
        # Robin inclui parcela da fonte que sai diretamente pela superfície.
        cumulative_out += (robin@(.5*(new+theta))+(1-source_factor)*power)*dt
        theta = new
        flux_end = potencia_placa(t)*weights/area
        surface = ambiente_k+(theta.reshape(nr, nz)[:, -1]+resistance*flux_end)*source_factor
        peak_surface = max(peak_surface, float(surface.max()))
        trace.append({'tempo_s': t, 'tmax_celula_k': float(theta.max()+ambiente_k),
                      'tmax_superficie_k': float(surface.max()),
                      'energia_entrada_placa_j': cumulative_in,
                      'energia_saida_placa_j': cumulative_out,
                      'energia_armazenada_placa_j': float(capacity@theta)})
    stored = float(capacity@theta)
    return {'temperatura_k': theta.reshape(nr, nz)+ambiente_k, 'r_m': rc, 'z_m': zc,
            'superficie_k': surface, 'historico': trace, 'dt_real_s': dt,
            'energia_translacional_j': energia, 'energia_entrada_disco_j': 2*cumulative_in,
            'energia_saida_disco_j': 2*cumulative_out, 'energia_armazenada_disco_j': 2*stored,
            'residuo_disco_j': 2*(cumulative_in-cumulative_out-stored),
            'massa_duas_placas_kg': float(2*volume.sum()*pista.densidade_kg_m3),
            'pico_superficie_k': peak_surface}
