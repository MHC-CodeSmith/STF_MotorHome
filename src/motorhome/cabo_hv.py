"""Contorno térmico de cabos HV: convecção, radiação, conduíte, agrupamento e transitório.

Reaproveita o campo r–θ de `cabos_polares.resolver` (volumes finitos validados) e
concentra aqui apenas o que o solver não representa: ar e entorno radiativo
distintos, confinamento em conduíte, agrupamento de fases e perdas AC.

Todas as hipóteses de contorno são explícitas e não substituem dados de
fabricante. O caso `n_fases=1`, `fator_confinamento=1`, `fator_forma=1`,
`t_radiante=t_ar` e `fator_perda_ac=1` reproduz exatamente o contorno anterior
(Churchill–Chu + radiação linearizada contra o próprio ar).
"""

from dataclasses import dataclass

import numpy as np

from .cabos_polares import Cabo, resolver

SIGMA = 5.670374419e-8
G = 9.81

# Ar seco a 1 atm (Incropera, Tabela A.4): T [K], k [W/m K], nu [m2/s], Pr
AIR = np.array([
    [300, 0.0263, 15.89e-6, 0.707], [350, 0.0300, 20.92e-6, 0.700],
    [400, 0.0338, 26.41e-6, 0.690], [450, 0.0373, 32.39e-6, 0.686],
    [500, 0.0407, 38.79e-6, 0.684], [550, 0.0439, 45.57e-6, 0.683],
    [600, 0.0469, 52.69e-6, 0.685],
])

# Propriedades térmicas assumidas (hipóteses, não ficha do produto).
COBRE_RHO_KG_M3 = 8960.
COBRE_CP_J_KGK = 385.
ISOLACAO_RHO_KG_M3 = 1200.
ISOLACAO_CP_J_KGK = 1700.

# Fração do perímetro exposta ao ar/entorno quando as fases correm encostadas.
# Valor assumido; a sensibilidade é varrida na análise. Fases iguais em
# temperatura não trocam calor líquido entre si, então o agrupamento reduz a
# área efetiva de troca em vez de criar uma fonte adicional.
FRACAO_EXPOSTA_POR_FASE = {1: 1.0, 2: 0.85, 3: 0.80}


def _finito_positivo(valor, nome, zero=False):
    if isinstance(valor, bool) or not np.isfinite(valor) or valor < 0 or (valor == 0 and not zero):
        raise ValueError(f'{nome}: finito positivo obrigatório')


@dataclass(frozen=True)
class CondicoesContorno:
    """Contorno térmico externo de um cabo ou grupo de cabos.

    t_ar_c: temperatura do ar.
    t_radiante_c: temperatura média das superfícies vizinhas (paredes, cofre).
    fator_forma_radiacao: 1 = visão plena do entorno; 0 = radiação bloqueada.
    fator_confinamento_conveccao: 1 = convecção livre; <1 = conduíte/fechamento.
    n_fases: cabos encostados; reduz a área exposta por `fracao_perimetro_exposto`.
    fator_perda_ac: multiplicador de perda Joule (skin/proximidade/PWM).
    """

    t_ar_c: float = 25.0
    t_radiante_c: float = 25.0
    emissividade: float = 0.9
    fator_forma_radiacao: float = 1.0
    fator_confinamento_conveccao: float = 1.0
    n_fases: int = 1
    fator_perda_ac: float = 1.0
    fracao_perimetro_exposto: float | None = None

    def __post_init__(self):
        for nome in ('t_ar_c', 't_radiante_c'):
            valor = getattr(self, nome)
            if not np.isfinite(valor) or valor <= -273.15:
                raise ValueError(f'{nome}: temperatura absoluta inválida')
        if not np.isfinite(self.emissividade) or not 0 <= self.emissividade <= 1:
            raise ValueError('emissividade deve estar em [0,1]')
        for nome in ('fator_forma_radiacao', 'fator_confinamento_conveccao'):
            valor = getattr(self, nome)
            if not np.isfinite(valor) or not 0 <= valor <= 1:
                raise ValueError(f'{nome} deve estar em [0,1]')
        if isinstance(self.n_fases, bool) or not isinstance(self.n_fases, int) or self.n_fases < 1:
            raise ValueError('n_fases: inteiro >=1 obrigatório')
        _finito_positivo(self.fator_perda_ac, 'fator_perda_ac')
        if self.fator_perda_ac < 1:
            raise ValueError('fator_perda_ac: perdas AC não podem reduzir a resistência')
        if self.fracao_perimetro_exposto is not None:
            fracao = self.fracao_perimetro_exposto
            if not np.isfinite(fracao) or not 0 < fracao <= 1:
                raise ValueError('fracao_perimetro_exposto deve estar em (0,1]')

    @property
    def fracao_exposta(self):
        if self.fracao_perimetro_exposto is not None:
            return self.fracao_perimetro_exposto
        return FRACAO_EXPOSTA_POR_FASE.get(self.n_fases, 0.75)

    @property
    def t_ar_k(self):
        return self.t_ar_c + 273.15

    @property
    def t_radiante_k(self):
        return self.t_radiante_c + 273.15


def propriedades_ar(t_k):
    """k [W/m K], nu [m²/s] e Pr do ar, interpolados em T."""
    return tuple(float(np.interp(t_k, AIR[:, 0], AIR[:, i])) for i in (1, 2, 3))


def h_conveccao(t_sup_k, t_ar_k, diametro_m):
    """Convecção natural em cilindro horizontal (Churchill–Chu)."""
    if not np.isfinite(diametro_m) or diametro_m <= 0:
        raise ValueError('diâmetro deve ser positivo')
    t_filme = (t_sup_k + t_ar_k)/2
    k, nu, pr = propriedades_ar(t_filme)
    alfa = nu/pr
    ra = G*(1/t_filme)*max(t_sup_k - t_ar_k, 1e-6)*diametro_m**3/(nu*alfa)
    nu_d = (0.60 + 0.387*ra**(1/6)/(1 + (0.559/pr)**(9/16))**(8/27))**2
    return nu_d*k/diametro_m


def h_radiacao(t_sup_k, t_radiante_k, emissividade, fator_forma=1.0):
    """Coeficiente radiativo linearizado para um sink distinto do ar."""
    return (emissividade*fator_forma*SIGMA*(t_sup_k**2 + t_radiante_k**2)
            *(t_sup_k + t_radiante_k))


def coeficientes(t_sup_k, cabo, contorno):
    """Retorna (h_total, t_sink_equivalente) para um único Robin.

    A soma de convecção e radiação com sinks diferentes é exata para a
    linearização em `t_sup_k` se usarmos o sink ponderado
    `(h_conv*t_ar + h_rad*t_rad)/(h_conv+h_rad)`. Ambas as parcelas são
    multiplicadas pela fração de perímetro exposta do grupo.
    """
    fracao = contorno.fracao_exposta
    h_conv = (h_conveccao(t_sup_k, contorno.t_ar_k, 2*cabo.raio_externo_m)
              * contorno.fator_confinamento_conveccao*fracao)
    h_rad = h_radiacao(t_sup_k, contorno.t_radiante_k,
                       contorno.emissividade, contorno.fator_forma_radiacao)*fracao
    total = h_conv + h_rad
    if total <= 0:
        raise ValueError('Coeficientes de troca nulos: contorno sem convecção nem radiação')
    t_sink = (h_conv*contorno.t_ar_k + h_rad*contorno.t_radiante_k)/total
    return total, t_sink, h_conv, h_rad


def resolver_estacionario(cabo, corrente_a, contorno, nr=32, nt=128,
                          max_iteracoes=200, tolerancia_k=1e-6):
    """Campo r–θ estacionário com contorno completo (ar, entorno, conduíte, fases)."""
    if not np.isfinite(corrente_a) or corrente_a < 0:
        raise ValueError('corrente deve ser finita e não negativa')
    # Perdas AC entram como corrente equivalente: I_eff²R == f_ac·I²R.
    corrente_efetiva = corrente_a*np.sqrt(contorno.fator_perda_ac)
    t_sup = contorno.t_ar_k + 30.0
    for _ in range(max_iteracoes):
        h_total, t_sink, h_conv, h_rad = coeficientes(t_sup, cabo, contorno)
        r = resolver(cabo, corrente_efetiva, nr, nt, h_total, t_sink)
        t_nova = float(np.mean(r['temperatura_superficie_k']))
        if abs(t_nova - t_sup) < tolerancia_k:
            t_sup = t_nova
            break
        t_sup = 0.5*t_sup + 0.5*t_nova
    else:
        raise RuntimeError('Iteração da temperatura de superfície não convergiu')
    return {'temperatura_max_k': float(r['temperatura_max_k']),
            'temperatura_media_feixe_k': float(r['temperatura_media_feixe_k']),
            'temperatura_superficie_k': t_sup,
            'joule_w_m': float(r['joule_w_m']),
            'removido_w_m': float(r['removido_w_m']),
            'residuo_w_m': float(r['residuo_w_m']),
            'h_conveccao_w_m2k': h_conv, 'h_radiacao_w_m2k': h_rad,
            't_sink_k': t_sink, 'corrente_efetiva_a': corrente_efetiva,
            'fracao_exposta': contorno.fracao_exposta, 'campo': r}


def resolver_fases(cabos, correntes, contorno):
    """Resolve um grupo de cabos com o mesmo contorno externo.

    Fases com a mesma corrente ficam à mesma temperatura e não trocam calor
    líquido entre si; o agrupamento já está em `fracao_perimetro_exposto`.
    Correntes diferentes são resolvidas individualmente, sem transferência
    lateral inventada.
    """
    if len(cabos) != len(correntes) or not cabos:
        raise ValueError('cabos e correntes devem ter o mesmo tamanho não nulo')
    if not isinstance(contorno, CondicoesContorno):
        raise ValueError('contorno inválido')
    grupo = CondicoesContorno(**{**contorno.__dict__, 'n_fases': 1,
                                 'fracao_perimetro_exposto': contorno.fracao_exposta})
    return [resolver_estacionario(cabo, corrente, grupo)
            for cabo, corrente in zip(cabos, correntes, strict=True)]


def _area_cobre(cabo):
    """Área de cobre coerente com a resistência do modelo: A = rho20/R20."""
    return 1.724e-8/cabo.resistencia20_ohm_m


def _capacidade(cabo):
    """Capacidade térmica por metro [J/(m K)] do cobre e da isolação."""
    a_cobre = _area_cobre(cabo)
    a_total = np.pi*cabo.raio_externo_m**2
    a_isolacao = max(a_total - np.pi*cabo.raio_feixe_m**2, 0.0)
    return COBRE_RHO_KG_M3*COBRE_CP_J_KGK*a_cobre + ISOLACAO_RHO_KG_M3*ISOLACAO_CP_J_KGK*a_isolacao


def resolver_transiente(cabo, corrente_continua_a, corrente_pico_a, contorno,
                        duracao_pico_s, t_limite_k=None, passo_s=1.0, max_passos=200000):
    """Sobretemperatura de um pico sobre o regime, por capacidade concentrada.

    Parte do estacionário em `corrente_continua_a`, aplica `corrente_pico_a`
    por `duracao_pico_s` e devolve a constante de tempo, o pico de temperatura
    e (se `t_limite_k` for dado) a duração máxima admissível do pico.
    A condutância é calibrada no próprio estacionário, então o modelo reproduz
    o solver r–θ no limite t→∞.
    """
    _finito_positivo(duracao_pico_s, 'duracao_pico_s')
    _finito_positivo(passo_s, 'passo_s')
    regime = resolver_estacionario(cabo, corrente_continua_a, contorno)
    capacidade = _capacidade(cabo)
    delta = regime['temperatura_max_k'] - contorno.t_ar_k
    if delta <= 0:
        raise ValueError('Regime sem sobretemperatura: corrente contínua nula?')
    condutancia = regime['joule_w_m']/delta
    tau = capacidade/condutancia

    def joule(temperatura):
        fator = 1 + cabo.alpha_por_k*(temperatura - cabo.referencia_k)
        return (corrente_pico_a**2*contorno.fator_perda_ac
                *cabo.resistencia20_ohm_m*max(fator, 0.0))

    # Integração explícita estável para o passo escolhido.
    limite_dt = capacidade/condutancia
    if passo_s > limite_dt:
        raise ValueError('passo_s excede o limite de estabilidade do modelo concentrado')
    passos = int(np.ceil(duracao_pico_s/passo_s))
    if passos > max_passos:
        raise ValueError('número de passos excede o limite')
    temperatura = regime['temperatura_max_k']
    historico = [(0.0, temperatura)]
    for n in range(1, passos + 1):
        temperatura += passo_s*(joule(temperatura)
                                - condutancia*(temperatura - contorno.t_ar_k))/capacidade
        if not np.isfinite(temperatura):
            raise ValueError('Temperatura não finita no transitório')
        historico.append((n*passo_s, temperatura))

    duracao_admissivel = None
    if t_limite_k is not None:
        duracao_admissivel = _duracao_ate_limite(cabo, contorno, regime, joule,
                                                 condutancia, capacidade, t_limite_k)
    return {'tau_s': tau, 'capacidade_j_mk': capacidade,
            'condutancia_w_mk': condutancia,
            'temperatura_regime_k': regime['temperatura_max_k'],
            'temperatura_pico_k': max(temperatura, max(t for _, t in historico)),
            'historico': historico, 'duracao_pico_s': duracao_pico_s,
            'duracao_maxima_admissivel_s': duracao_admissivel}


def _duracao_ate_limite(cabo, contorno, regime, joule, condutancia, capacidade, t_limite_k):
    """Tempo até a temperatura atingir `t_limite_k` (None se nunca atinge)."""
    if regime['temperatura_max_k'] >= t_limite_k:
        return 0.0
    if joule(t_limite_k)/condutancia + contorno.t_ar_k <= t_limite_k:
        return None
    # Como dT/dt = (q(T) - G(T-Ta))/C, integrar até cruzar o limite.
    dt = 0.5
    temperatura, tempo = regime['temperatura_max_k'], 0.0
    while tempo < 1e6:
        temperatura += dt*(joule(temperatura) - condutancia*(temperatura - contorno.t_ar_k))/capacidade
        tempo += dt
        if temperatura >= t_limite_k:
            return tempo
    return None
