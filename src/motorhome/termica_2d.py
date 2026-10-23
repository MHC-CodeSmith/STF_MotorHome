"""Difusão térmica 2D por volumes finitos, Euler explícito conservativo.

Malha cartesiana uniforme, sólido homogêneo, espessura constante, faces em z
adiabáticas, fonte fixa no tempo. Não representa disco/cabo real automaticamente.
"""

from dataclasses import dataclass
from math import ceil

import numpy as np

from .sistemas_termicos import numero, temperatura


@dataclass(frozen=True)
class Material:
    k_w_mk: float
    rho_kg_m3: float
    cp_j_kgk: float

    def __post_init__(self):
        for nome in ('k_w_mk', 'rho_kg_m3', 'cp_j_kgk'):
            numero(getattr(self, nome), nome, 0, True)


@dataclass(frozen=True)
class Malha:
    lx_m: float
    ly_m: float
    espessura_m: float
    nx: int
    ny: int

    def __post_init__(self):
        for nome in ('lx_m', 'ly_m', 'espessura_m'):
            numero(getattr(self, nome), nome, 0, True)
        for nome in ('nx', 'ny'):
            v = getattr(self, nome)
            if isinstance(v, bool) or not isinstance(v, int) or v < 2:
                raise ValueError(f'{nome}: inteiro >= 2 obrigatório')

    @property
    def dx(self):
        return self.lx_m/self.nx

    @property
    def dy(self):
        return self.ly_m/self.ny

    def centros(self):
        return np.meshgrid((np.arange(self.nx)+.5)*self.dx,
                           (np.arange(self.ny)+.5)*self.dy)


@dataclass(frozen=True)
class Contorno:
    tipo: str
    temperatura_k: float | None = None
    h_w_m2k: float | None = None
    fluxo_entrada_w_m2: float | None = None

    def __post_init__(self):
        esperados = {'isolado': (False, False, False),
                     'temperatura': (True, False, False),
                     'conveccao': (True, True, False), 'fluxo': (False, False, True)}
        fornecidos = tuple(v is not None for v in
                           (self.temperatura_k, self.h_w_m2k, self.fluxo_entrada_w_m2))
        if self.tipo not in esperados or fornecidos != esperados[self.tipo]:
            raise ValueError('Tipo/campos de contorno incompatíveis')
        if self.temperatura_k is not None:
            temperatura(self.temperatura_k)
        if self.h_w_m2k is not None:
            numero(self.h_w_m2k, 'h [W/m² K]', 0)
        if self.fluxo_entrada_w_m2 is not None:
            numero(self.fluxo_entrada_w_m2, 'fluxo [W/m²]')


def _campo(valor, formato, nome, positivo=False):
    bruto = np.asarray(valor)
    if bruto.dtype.kind not in 'iuf':
        raise ValueError(f'{nome}: números reais obrigatórios')
    arr = np.array(bruto, dtype=float, copy=True)
    if arr.ndim == 0:
        arr = np.full(formato, float(arr))
    if arr.shape != formato or not np.isfinite(arr).all():
        raise ValueError(f'{nome}: formato {formato} e valores finitos obrigatórios')
    if positivo and (arr <= 0).any():
        raise ValueError(f'{nome}: temperatura absoluta deve ser positiva')
    return arr


def resolver(malha, material, inicial_k, geracao_w_m3, contornos, duracao_s,
             passo_s=None, seguranca=.8, max_passos=1_000_000, saidas=20):
    """Retorna campo final, históricos e resíduo global de energia em J.

    Contornos exigidos: esquerda/direita/inferior/superior. G na face convectiva
    inclui resistência de meia célula e filme. dt <= Ccel/soma(G) mantém pesos
    não negativos. Fonte negativa deve preservar T>0. Sem radiação/não linearidade.
    """
    tempo = numero(duracao_s, 'duração [s]', 0, True)
    safety = numero(seguranca, 'segurança', 0, True)
    if safety > 1:
        raise ValueError('Segurança deve estar em (0,1]')
    for v, nome in [(max_passos, 'max_passos'), (saidas, 'saidas')]:
        if isinstance(v, bool) or not isinstance(v, int) or v < 1:
            raise ValueError(f'{nome}: inteiro positivo obrigatório')
    lados = {'esquerda', 'direita', 'inferior', 'superior'}
    if set(contornos) != lados or not all(isinstance(b, Contorno) for b in contornos.values()):
        raise ValueError('Fornecer exatamente quatro contornos válidos')
    nx, ny = malha.nx, malha.ny
    t = _campo(inicial_k, (ny, nx), 'inicial', True)
    inicial = t.copy()
    fonte = _campo(geracao_w_m3, (ny, nx), 'geração')
    dx, dy, z = malha.dx, malha.dy, malha.espessura_m
    volume = dx*dy*z
    ccel = material.rho_kg_m3*material.cp_j_kgk*volume
    gx, gy = material.k_w_mk*dy*z/dx, material.k_w_mk*dx*z/dy
    diag = np.zeros_like(t)
    diag[:, :-1] += gx
    diag[:, 1:] += gx
    diag[:-1, :] += gy
    diag[1:, :] += gy
    faces = [('esquerda', (slice(None), 0), dy*z, dx),
             ('direita', (slice(None), -1), dy*z, dx),
             ('inferior', (0, slice(None)), dx*z, dy),
             ('superior', (-1, slice(None)), dx*z, dy)]
    termos = []
    for lado, indice, area, distancia in faces:
        bc = contornos[lado]
        g, entrada = 0., 0.
        if bc.tipo == 'temperatura':
            g = 2*material.k_w_mk*area/distancia
            entrada = g*bc.temperatura_k
        elif bc.tipo == 'conveccao' and bc.h_w_m2k > 0:
            g = area/(distancia/(2*material.k_w_mk)+1/bc.h_w_m2k)
            entrada = g*bc.temperatura_k
        elif bc.tipo == 'fluxo':
            entrada = area*bc.fluxo_entrada_w_m2
        diag[indice] += g
        termos.append((indice, g, entrada))
    limite = ccel/float(diag.max())
    dt_alvo = safety*limite if passo_s is None else numero(passo_s, 'dt [s]', 0, True)
    if dt_alvo > limite*(1+1e-14):
        raise ValueError(f'Passo instável: dt={dt_alvo}, limite={limite} s')
    passos = ceil(tempo/dt_alvo)
    if passos > max_passos:
        raise ValueError(f'{passos} passos excedem limite {max_passos}')
    dt = tempo/passos
    potencia_fonte = fonte*volume
    energia_fonte = energia_contorno = 0.
    historico = []
    intervalo = max(1, passos//saidas)

    def estado(n):
        armazenada = ccel*float(np.sum(t-inicial))
        return {'tempo_s': n*dt, 'min_k': float(t.min()), 'max_k': float(t.max()),
                'media_k': float(t.mean()), 'armazenada_j': armazenada,
                'fonte_j': energia_fonte, 'contorno_entrada_j': energia_contorno,
                'residuo_j': armazenada-energia_fonte-energia_contorno}

    historico.append(estado(0))
    for n in range(1, passos+1):
        potencia = potencia_fonte.copy()
        fx = gx*(t[:, 1:]-t[:, :-1])
        fy = gy*(t[1:, :]-t[:-1, :])
        potencia[:, :-1] += fx
        potencia[:, 1:] -= fx
        potencia[:-1, :] += fy
        potencia[1:, :] -= fy
        pb = 0.
        for indice, g, entrada in termos:
            fluxo = entrada-g*t[indice]
            potencia[indice] += fluxo
            pb += float(np.sum(fluxo))
        t += (dt/ccel)*potencia
        if not np.isfinite(t).all() or (t <= 0).any():
            raise ValueError('Campo calculado não finito ou temperatura <= 0 K')
        energia_fonte += dt*float(potencia_fonte.sum())
        energia_contorno += dt*pb
        if n % intervalo == 0 or n == passos:
            historico.append(estado(n))
    return {'temperatura_k': t, 'historico': historico, 'passos': passos,
            'passo_s': dt, 'limite_passo_s': limite}
