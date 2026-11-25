"""Montagem CAD detalhada do Aurora Solar no referencial do veículo (x para a frente, y para a esquerda, z para cima).

Usada por renderizar_cad.py (figuras do relatório) e pelo visualizador 3D.

Referencial: o mesmo de todo o projeto (config/equipamentos_interior.yaml, gerar_visualizador.py): a face
interna traseira da caixa de carga fica em x = -3,35 m, o piso acabado em z = 0,68 m e a largura é centrada
em y = 0. O deck solar segue a geometria do CFD (40 mm acima do teto, 25 mm da traseira).

Os layouts A/B de integrado_maxeon1560 são caixas; aqui eles ganham os detalhes do interior equipado de
24/10 (geladeira, lava e seca, A/C, sanitário, porta do banheiro, ducha, pia, travesseiros, bolsas dos
portáteis), encaixados exatamente na caixa de cada equipamento do layout final. O trem de tração e os
bancos da cabine são os do conceito de 24/10 (componentes OEM, não mudaram).
"""
from __future__ import annotations

import itertools
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "entregas"
PARCIAL = E / "parcial_2026-10-24"

TRASEIRA_X, PISO_Z = -3.35, 0.68                 # face interna traseira e piso acabado (referencial do projeto)
CARGA = np.array([TRASEIRA_X, 0.0, PISO_Z])
LARGURA = 1.794                                  # largura interna (1,87 m - 2 x 38 mm de revestimento)
DECK = np.array([-3.482, -0.91, 0.648])          # deck: mesma posição do pvdeck.stl do CFD (I19)
TETO_Z = 2.612                                   # topo do teto da carroceria
ARCO = (0.85, 0.224, 0.35)                       # caixa de roda (config/parametros_globais.yaml, geometry)
# O banco US5000 dos layouts (piso a 0,72 m) invadia ~7 cm a caixa de roda esquerda posta sobre o eixo real.
# Layout A: o banco sobe e apoia sobre a caixa de roda (topo a 1,543 m, abaixo do estrado a 1,66 m).
# Layout B: o banco do sofá fica a 1,26 m, então o banco de baterias entra 18,5 cm para o centro e o tanque
# de água limpa recua 4,5 cm (as alças do banco ficam a 1 cm dele).
SUBIDA_BANCO = PISO_Z + ARCO[2] + 0.01 - 0.72
RECUO_BANCO_B = (LARGURA / 2 - ARCO[1] - 0.005) - 0.853
AVANCO_BANCO_A = 0.006                           # tira o banco do poste traseiro da cama (folga de 1 mm; 2 mm ao acesso do inversor)
RECUO_COOKTOP = 0.06                             # para dentro da gaveta, layout A e B
RAIO_TUBO, RAIO_CABO = 0.007, 0.007

CORES = {
    "energia": (0.20, 0.42, 0.78), "agua": (0.22, 0.70, 0.82), "eletro": (0.93, 0.55, 0.20),
    "clima": (0.82, 0.25, 0.25), "movel": (0.80, 0.66, 0.47), "banho": (0.92, 0.92, 0.95),
    "solar": (0.10, 0.16, 0.30), "bolsa": (0.35, 0.38, 0.42), "cama": (0.62, 0.70, 0.55),
}
MATERIAIS = {"Body": (0.94, 0.95, 0.96), "Body_Glass": (0.16, 0.22, 0.30), "Black_Plastic": (0.20, 0.21, 0.23),
             "Tire": (0.09, 0.09, 0.10), "Chrome": (0.78, 0.79, 0.82), "Metal": (0.70, 0.71, 0.74),
             "Metal_Dark": (0.30, 0.30, 0.32)}
DETALHE = {  # cor por palavra-chave das peças de detalhe (interior de 24/10)
    "vidro": (0.25, 0.35, 0.45), "aro": (0.75, 0.76, 0.78), "display": (0.10, 0.12, 0.14), "seletor": (0.75, 0.76, 0.78),
    "porta": (0.93, 0.93, 0.94), "puxador": (0.70, 0.71, 0.74), "carcaca": (0.94, 0.94, 0.95), "grelha": (0.35, 0.36, 0.38),
    "saida_duto": (0.55, 0.56, 0.58), "assento": (0.95, 0.95, 0.96), "tampa": (0.95, 0.95, 0.96),
    "tanque": (0.90, 0.90, 0.92), "coluna": (0.78, 0.79, 0.82), "chuveiro": (0.78, 0.79, 0.82),
    "porta_correr": (0.72, 0.78, 0.82), "bica": (0.78, 0.79, 0.82), "torneira": (0.78, 0.79, 0.82),
    "cuba": (0.80, 0.81, 0.83), "travesseiro": (0.96, 0.96, 0.94), "degrau": (0.55, 0.56, 0.58),
    "poste": (0.55, 0.56, 0.58), "bolsa": (0.25, 0.27, 0.30), "cinta": (0.12, 0.12, 0.13), "alca": (0.12, 0.12, 0.13),
    "encosto": (0.22, 0.23, 0.25), "almofada": (0.22, 0.23, 0.25), "base_assento": (0.15, 0.15, 0.16),
    "aleta": (0.12, 0.30, 0.55), "envelope": (0.15, 0.36, 0.66), "etiqueta": (0.95, 0.95, 0.96),
}
TRACAO = {"pack_tracao": (0.30, 0.33, 0.37), "motor_tracao": (0.45, 0.47, 0.50), "redutor": (0.40, 0.42, 0.45),
          "inversor_tracao": (0.55, 0.57, 0.60), "carregador_oem": (0.55, 0.57, 0.60), "radiador_tracao": (0.35, 0.37, 0.40),
          "arrefecimento": (0.20, 0.55, 0.85), "rotas_hv": (0.95, 0.50, 0.10)}


@dataclass
class Peca:
    grupo: str
    nome: str
    v: np.ndarray       # vértices n x 3 no referencial do veículo
    f: np.ndarray       # faces m x 3
    rgb: tuple
    dono: str = ""      # equipamento a que o detalhe pertence (peças do mesmo dono não contam como colisão)

    def __post_init__(self):
        self.dono = self.dono or self.nome

    @property
    def tri(self) -> np.ndarray:
        return self.v[self.f]

    @property
    def caixa(self):
        return self.v.min(0), self.v.max(0)


def _nome(no: str) -> str:
    return no.split("_", 1)[1] if no[:1].isdigit() and "_" in no else no


def ler(caminho: Path, desloc=(0.0, 0.0, 0.0)):
    """[(nome, vértices, faces, geometria)] de um GLB, já transformados para o referencial global."""
    import trimesh

    cena = trimesh.load(caminho)
    if isinstance(cena, trimesh.Trimesh):
        return [("malha", cena.vertices + desloc, np.asarray(cena.faces), cena)]
    saida = []
    for no in cena.graph.nodes_geometry:
        matriz, g = cena.graph[no]
        geo = cena.geometry[g]
        saida.append((_nome(no), trimesh.transform_points(geo.vertices, matriz) + desloc, np.asarray(geo.faces), geo))
    return saida


def cor_material(geo) -> tuple:
    m = getattr(geo.visual, "material", None)
    nome = getattr(m, "name", None)
    if nome in MATERIAIS:
        return MATERIAIS[nome]
    c = getattr(m, "baseColorFactor", None)
    if c is not None:
        c = np.asarray(c, float)[:3]
        return tuple(np.clip(c / 255.0 if c.max() > 1 else c, 0.08, 1.0))
    return (0.80, 0.82, 0.85)


def categoria(nome: str) -> str:
    for chave, cat in (("US5000", "energia"), ("inversor", "energia"), ("tanque", "agua"), ("boiler", "agua"),
                       ("bomba", "agua"), ("geladeira", "eletro"), ("cooktop", "eletro"), ("lava", "eletro"),
                       ("hvac", "clima"), ("MAXEON", "solar"), ("bolsa", "bolsa"), ("cama", "cama"),
                       ("assento", "cama"), ("cassete", "banho"), ("banho", "banho")):
        if chave in nome:
            return cat
    return "movel"


def cor_detalhe(nome: str, padrao=(0.85, 0.86, 0.88)) -> tuple:
    for chave in sorted(DETALHE, key=len, reverse=True):
        if chave in nome:
            return DETALHE[chave]
    return padrao


def caixa_malha(v_lo, v_hi):
    """Caixa (8 vértices, 12 triângulos) entre dois cantos."""
    import trimesh

    b = trimesh.creation.box(bounds=np.array([v_lo, v_hi]))
    return np.asarray(b.vertices), np.asarray(b.faces)


def caixas_unidas(cantos):
    """Uma malha com várias caixas [(lo, hi), ...]."""
    vs, fs, n = [], [], 0
    for a, b in cantos:
        v, f = caixa_malha(a, b)
        vs.append(v); fs.append(f + n); n += len(v)
    return np.vstack(vs), np.vstack(fs)


def limpar(n: str) -> str:
    return re.sub(r"^\d+_", "", n.split("__")[-1])


def cilindro(p0, p1, r, secoes=14):
    import trimesh

    c = trimesh.creation.cylinder(radius=r, segment=np.array([p0, p1]), sections=secoes)
    return np.asarray(c.vertices), np.asarray(c.faces)


def encaixar(itens, destino, giro=0):
    """Leva peças (nome, v, f) da caixa que elas ocupam para a caixa `destino` (lo, hi).

    giro: 0, 90 ou -90 graus em torno de z antes de escalar (para acertar a face de acesso)."""
    v_all = np.vstack([v for _, v, _ in itens])
    centro = (v_all.min(0) + v_all.max(0)) / 2
    ang = np.radians(giro)
    R = np.array([[np.cos(ang), -np.sin(ang), 0], [np.sin(ang), np.cos(ang), 0], [0, 0, 1]])
    girados = [(n, (v - centro) @ R.T, f) for n, v, f in itens]
    g_all = np.vstack([v for _, v, _ in girados])
    lo, hi = g_all.min(0), g_all.max(0)
    d_lo, d_hi = map(np.asarray, destino)
    esc = (d_hi - d_lo) / np.maximum(hi - lo, 1e-9)
    return [(n, (v - lo) * esc + d_lo, f) for n, v, f in girados]


# ---------------------------------------------------------------- blocos
def exterior() -> list[Peca]:
    return [Peca("exterior", n, v, f, cor_material(g)) for n, v, f, g in ler(PARCIAL / "aurora_L3H2_proposta_m.glb")]


def caixas_de_roda(ext: list[Peca]) -> list[Peca]:
    """Caixas de roda internas sobre os pneus traseiros reais (dimensões do config; posição do pneu do CAD)."""
    saida = []
    for p in ext:
        if p.nome.startswith("Wheel_1_") and "_" in p.nome and cor_material_nome(p) == "Tire":
            lo, hi = p.caixa
            xc = (lo[0] + hi[0]) / 2
            lado = 1 if lo[1] > 0 else -1
            y_int = lado * (LARGURA / 2 - ARCO[1])
            y_ext = lado * LARGURA / 2
            v, f = caixa_malha([xc - ARCO[0] / 2, min(y_int, y_ext), PISO_Z], [xc + ARCO[0] / 2, max(y_int, y_ext), PISO_Z + ARCO[2]])
            saida.append(Peca("arcos", f"caixa_roda_{'esquerda' if lado > 0 else 'direita'}", v, f, (0.62, 0.64, 0.67)))
    return saida


def cor_material_nome(p: Peca) -> str:
    return {v: k for k, v in MATERIAIS.items()}.get(tuple(p.rgb), "")


def cabine_oem() -> list[Peca]:
    return [Peca("cabine", n, v, f, cor_detalhe(n)) for n, v, f, _ in ler(PARCIAL / "interior_equipado.glb")
            if n.startswith("assentos_oem")]


def tracao_oem() -> list[Peca]:
    saida = []
    for n, v, f, _ in ler(PARCIAL / "tracao_e_servicos.glb"):
        pref = n.split("__")[0]
        if pref in TRACAO:
            saida.append(Peca("tracao", n, v, f, TRACAO[pref]))
    return saida


def deck_solar(ext: list[Peca] | None = None) -> list[Peca]:
    """4 módulos Maxeon com moldura e células, sobre trilhos e pés no vão de 40 mm."""
    saida = []
    mods = ler(E / "desenvolvimento_2026-11-09/teto_maxeon/alternativa1540_plana.glb", DECK)
    for n, v, _, _ in mods:
        lo, hi = v.min(0), v.max(0)
        m = 0.022
        for k, (a, b) in enumerate((([lo[0], lo[1], lo[2]], [hi[0], lo[1] + m, hi[2]]),
                                    ([lo[0], hi[1] - m, lo[2]], [hi[0], hi[1], hi[2]]),
                                    ([lo[0], lo[1], lo[2]], [lo[0] + m, hi[1], hi[2]]),
                                    ([hi[0] - m, lo[1], lo[2]], [hi[0], hi[1], hi[2]]))):
            vv, ff = caixa_malha(a, b)
            saida.append(Peca("teto", f"{n}_moldura_{k}", vv, ff, (0.72, 0.74, 0.77)))
        vv, ff = caixa_malha([lo[0] + m, lo[1] + m, hi[2] - 0.006], [hi[0] - m, hi[1] - m, hi[2] - 0.002])
        saida.append(Peca("teto", f"{n}_vidro", vv, ff, (0.07, 0.10, 0.20)))
        # 8 x 13 células (Maxeon 3, 104 células)
        nx, ny, folga = 8, 13, 0.004
        dx, dy = (hi[0] - lo[0] - 2 * m) / nx, (hi[1] - lo[1] - 2 * m) / ny
        cantos = [([lo[0] + m + i * dx + folga, lo[1] + m + j * dy + folga, hi[2] - 0.002],
                   [lo[0] + m + (i + 1) * dx - folga, lo[1] + m + (j + 1) * dy - folga, hi[2] - 0.0005])
                  for i in range(nx) for j in range(ny)]
        vv, ff = caixas_unidas(cantos)
        saida.append(Peca("teto", f"{n}_celulas", vv, ff, (0.12, 0.17, 0.32)))
    v_all = np.vstack([v for _, v, _, _ in mods])
    lo, hi = v_all.min(0), v_all.max(0)
    teto = altura_teto(ext) if ext is not None else (lambda x, y: TETO_Z)
    trilho_z0 = lo[2] - 0.025
    for yy in (-0.62, 0.62):  # trilhos longitudinais 25 mm sob o deck; pés do teto (abaulado) até o trilho
        vv, ff = caixa_malha([lo[0] + 0.05, yy - 0.02, trilho_z0], [hi[0] - 0.05, yy + 0.02, lo[2]])
        saida.append(Peca("teto", "trilho", vv, ff, (0.60, 0.62, 0.65)))
        for xx in np.linspace(lo[0] + 0.15, hi[0] - 0.15, 6):
            vv, ff = caixa_malha([xx - 0.04, yy - 0.04, teto(xx, yy) - 0.004], [xx + 0.04, yy + 0.04, trilho_z0])
            saida.append(Peca("teto", "pe_trilho", vv, ff, (0.20, 0.21, 0.23)))
    return saida


def altura_teto(ext: list[Peca]):
    """z do teto da carroceria em (x, y), pela amostra dos vértices da pintura (material Body)."""
    v = np.vstack([p.v for p in ext if p.rgb == MATERIAIS["Body"] and not p.nome.startswith("Door")])
    v = v[v[:, 2] > 2.3]

    def z(x, y):
        perto = v[(np.abs(v[:, 0] - x) < 0.12) & (np.abs(v[:, 1] - y) < 0.12)]
        return float(perto[:, 2].max()) if len(perto) else TETO_Z
    return z


def portateis_solo() -> list[Peca]:
    return [Peca("solo", n, v, f, CORES["solar"]) for n, v, f, _ in ler(PARCIAL / "solar_portatil_solo.glb")]


# ---------------------------------------------------------------- interior
def _detalhes_24_10():
    """Peças do interior equipado de 24/10 agrupadas por equipamento."""
    grupos: dict[str, list] = {}
    for n, v, f, _ in ler(PARCIAL / "interior_equipado.glb"):
        pref = n.split("__")[0]
        grupos.setdefault(pref, []).append((n, v, f))
    for n, v, f, _ in ler(PARCIAL / "solar_portatil_transporte.glb"):
        k = re.search(r"pv_(\d)", n).group(1)
        grupos.setdefault(f"bolsa_{k}", []).append((n, v, f))
    return grupos


def interior(layout: str, arcos: list[Peca] | None = None) -> list[Peca]:
    """layout 'A' (cama fixa, escolhido) ou 'B' (cama conversível)."""
    arquivo = {"A": "A_fixa.glb", "B": "B_conversivel_noite.glb"}[layout]
    grupo = f"layout{layout}"
    caixas = {n: (v, f) for n, v, f, _ in ler(E / "integrado_maxeon1560/integracao" / arquivo, CARGA)
              if "MAXEON" not in n}
    # ajustes de encaixe sobre os dados do layout (colisões dos próprios dados, 12 mm a 10 cm):
    for k, (v, f) in list(caixas.items()):
        if k.endswith("cooktop_armazenado"):          # atravessava a divisória 3.02: volta 6 cm para dentro da gaveta
            caixas[k] = (v + [-RECUO_COOKTOP, 0, 0], f)
        if layout == "B" and k.endswith("divisoria_2.54"):  # no B a lava e seca vai até 2,64: divisória logo depois
            caixas[k] = (v + [0.112, 0, 0], f)
        if "US5000" in k:                                  # fora da caixa de roda (ver SUBIDA_BANCO)
            caixas[k] = (v + ([AVANCO_BANCO_A, 0, SUBIDA_BANCO] if layout == "A" else [0, RECUO_BANCO_B, 0]), f)
        if layout == "B" and k.endswith("tanque_limpa"):
            caixas[k] = (v + [0, -0.045, 0], f)
    det = _detalhes_24_10()
    saida: list[Peca] = []
    substituidas = set()

    def lim(chave):
        v = caixas[chave][0]
        return v.min(0), v.max(0)

    def achar(sufixo):
        return next(k for k in caixas if k.endswith(sufixo))

    def por(itens, destino, giro=0, dono=""):
        for n, v, f in encaixar(itens, destino, giro):
            saida.append(Peca(grupo, limpar(n), v, f, cor_detalhe(n), dono))

    def filtro(pref, *palavras):
        return [x for x in det[pref] if any(p in x[0] for p in palavras)] if palavras else det[pref]

    # equipamentos com modelo detalhado: a caixa do layout final manda; o detalhe é encaixado nela
    k = achar("geladeira_AC"); por(det["geladeira"], lim(k), dono="geladeira_AC"); substituidas.add(k)
    k = achar("lava_seca")
    lo, hi = lim(k)
    por(det["lava_seca"], (lo, hi), giro=-90 if layout == "A" else 0, dono="lava_seca"); substituidas.add(k)  # porta para o corredor
    k = achar("hvac"); por(det["hvac"], lim(k), giro=90, dono="hvac"); substituidas.add(k)
    k = achar("cassete"); por(det["sanitario"], lim(k), giro=-90, dono="cassete"); substituidas.add(k)
    for i in range(1, 5):
        k = achar(f"portatil_bolsa_{i}"); lo, hi = lim(k)
        por(det[f"bolsa_{i}"], (lo, hi), dono=f"portatil_bolsa_{i}"); substituidas.add(k)
    k = achar("inversor"); lo, hi = lim(k)
    if hi[2] - lo[2] > hi[0] - lo[0]:      # parede (layout A); no B o inversor está deitado: fica a caixa
        tr = ler(PARCIAL / "tracao_e_servicos.glb")
        inv = [(n, v, f) for n, v, f, _ in tr if n.startswith("inversor_servicos")]
        por(inv, (lo, hi), dono="inversor"); substituidas.add(k)

    # banheiro: porta de correr, coluna da ducha e chuveiro do banheiro de 24/10 na caixa do banheiro final
    paredes = [k for k in caixas if "banho" in k]
    b_lo = np.min([lim(k)[0] for k in paredes], axis=0)
    b_hi = np.max([lim(k)[1] for k in paredes], axis=0)
    b_hi[2] = max(b_hi[2], PISO_Z + 1.78)
    banho = filtro("banheiro")
    ref = encaixar(banho, (b_lo, b_hi))
    for n, v, f in ref:
        if any(p in n for p in ("porta_correr", "coluna_ducha", "chuveiro")):
            saida.append(Peca(grupo, limpar(n), v, f, cor_detalhe(n), "banho"))

    # cama: travesseiros sobre o colchão final e postes até o estrado
    k = next(k for k in caixas if "colchao" in k)
    c_lo, c_hi = lim(k)
    trav = filtro("cama", "travesseiro")
    t_lo = np.vstack([v for _, v, _ in trav]).min(0)
    for n, v, f in trav:
        v2 = v + np.array([c_lo[0] + 0.06 - t_lo[0], 0.0, c_hi[2] - t_lo[2]])
        if layout == "A":
            saida.append(Peca(grupo, "travesseiro", v2, f, cor_detalhe(n), "cama_colchao"))
    if layout == "A":
        est = lim(next(k for k in caixas if k.endswith("estrado")))
        for n, v, f in filtro("cama", "poste"):
            lo, hi = v.min(0), v.max(0)
            v2 = v.copy()
            v2[:, 2] = PISO_Z + (v[:, 2] - lo[2]) / max(hi[2] - lo[2], 1e-9) * (est[0][2] - PISO_Z)
            saida.append(Peca(grupo, "poste_cama", v2, f, cor_detalhe("poste"), "estrado"))
        for n, v, f in filtro("cama", "degrau"):
            saida.append(Peca(grupo, "degrau_retratil", v, f, cor_detalhe("degrau")))

    # cozinha: pia rasa na ponta da linha de água (x = -0,35 m), frente de gaveta/porta entre divisórias
    tampo = lim(achar("tampo"))
    pia = filtro("pia")
    p_all = np.vstack([v for _, v, _ in pia])
    cuba = [x for x in pia if "cuba" in x[0]]
    cu_all = np.vstack([v for _, v, _ in cuba])
    yc = (tampo[0][1] + tampo[1][1]) / 2
    # a linha de água sobe em x = -0,35 m, junto à divisória; a cuba fica no vão livre (sem geladeira) mais próximo
    divs = sorted(lim(k)[0][0] for k in caixas if "divisoria" in k)
    vaos = [(a + 0.012, b) for a, b in itertools.pairwise(divs)
            if not any(lim(k)[0][0] < b and lim(k)[1][0] > a and "geladeira" in k for k in caixas)]
    a, b = min(vaos, key=lambda ab: min(abs(ab[0] + 0.35), abs(ab[1] + 0.35)))
    dx = (a + b) / 2 - (cu_all.min(0)[0] + cu_all.max(0)[0]) / 2
    dy = yc - (cu_all.min(0)[1] + cu_all.max(0)[1]) / 2
    dz = tampo[1][2] - cu_all.max(0)[2]
    fundo = tampo[1][2] - 0.11           # cuba de 11 cm: acima do cooktop guardado
    xc = (a + b) / 2
    esc = min(1.0, (b - a - 0.03) / (cu_all.max(0)[0] - cu_all.min(0)[0]))   # cuba cabe no vão
    for n, v, f in pia:
        v2 = v + [dx, dy, dz]
        v2[:, 0] = xc + (v2[:, 0] - xc) * esc
        if "cuba" in n:
            v2[:, 2] = np.maximum(v2[:, 2], fundo)
        saida.append(Peca(grupo, limpar(n), v2, f, cor_detalhe(n), "tampo"))
    cu = np.vstack([p.v for p in saida if p.dono == "tampo" and "cuba" in p.nome])
    t = tampo[1][2]
    lo_c, hi_c = cu.min(0), cu.max(0)
    # bancada com recorte para a cuba (sem faces coplanares: o matplotlib não tem z-buffer) e aro inox no recorte
    k_tampo = achar("tampo")
    r_lo, r_hi = lo_c - 0.015, hi_c + 0.015
    t_lo, t_hi = tampo
    vv, ff = caixas_unidas([([t_lo[0], t_lo[1], t_lo[2]], [r_lo[0], t_hi[1], t_hi[2]]),
                            ([r_hi[0], t_lo[1], t_lo[2]], [t_hi[0], t_hi[1], t_hi[2]]),
                            ([r_lo[0], t_lo[1], t_lo[2]], [r_hi[0], r_lo[1], t_hi[2]]),
                            ([r_lo[0], r_hi[1], t_lo[2]], [r_hi[0], t_hi[1], t_hi[2]])])
    caixas[k_tampo] = (vv, ff)
    vv, ff = caixas_unidas([([r_lo[0], r_lo[1], t - 0.004], [r_hi[0], lo_c[1], t + 0.003]),
                            ([r_lo[0], hi_c[1], t - 0.004], [r_hi[0], r_hi[1], t + 0.003]),
                            ([r_lo[0], lo_c[1], t - 0.004], [lo_c[0], hi_c[1], t + 0.003]),
                            ([hi_c[0], lo_c[1], t - 0.004], [r_hi[0], hi_c[1], t + 0.003])])
    saida.append(Peca(grupo, "borda_cuba", vv, ff, (0.80, 0.81, 0.83), "tampo"))
    del p_all
    yf = tampo[1][1]
    for a, b in itertools.pairwise(divs):
        a, b = a + 0.014, b - 0.002
        ocupado = any(lim(k)[0][0] < b and lim(k)[1][0] > a and ("geladeira" in k or "lava" in k) for k in caixas)
        if ocupado or b - a < 0.15:
            continue
        for z0, z1, nome in ((PISO_Z + 0.04, tampo[0][2] - 0.22, "porta_gabinete"), (tampo[0][2] - 0.20, tampo[0][2] - 0.02, "gaveta")):
            vv, ff = caixa_malha([a, yf, z0], [b, yf + 0.018, z1])
            saida.append(Peca(grupo, nome, vv, ff, (0.86, 0.74, 0.56), f"frente_{a:.2f}"))
            zc = z1 - 0.05 if nome == "porta_gabinete" else (z0 + z1) / 2
            vv, ff = caixa_malha([(a + b) / 2 - 0.08, yf + 0.018, zc - 0.008], [(a + b) / 2 + 0.08, yf + 0.032, zc + 0.008])
            saida.append(Peca(grupo, "puxador", vv, ff, (0.70, 0.71, 0.74), f"frente_{a:.2f}"))

    # US5000: frente de rack com alças e LEDs voltada para o centro do veículo
    for k in [k for k in caixas if "US5000" in k]:
        lo, hi = lim(k)
        frente_y = lo[1] if abs(lo[1]) < abs(hi[1]) else hi[1]
        s = -1 if frente_y == lo[1] else 1
        vv, ff = caixa_malha([lo[0], lo[1], lo[2]], [hi[0], hi[1], hi[2]])
        saida.append(Peca(grupo, limpar(k), vv, ff, (0.30, 0.31, 0.34), limpar(k)))
        y0, y1 = sorted([frente_y, frente_y + s * 0.006])
        vv, ff = caixa_malha([lo[0] + 0.02, y0, lo[2] + 0.012], [hi[0] - 0.02, y1, hi[2] - 0.012])
        saida.append(Peca(grupo, "US5000_frente", vv, ff, (0.82, 0.83, 0.85), limpar(k)))
        for xa in (lo[0] + 0.035, hi[0] - 0.035):
            y0, y1 = sorted([frente_y + s * 0.006, frente_y + s * 0.03])
            vv, ff = caixa_malha([xa - 0.01, y0, lo[2] + 0.03], [xa + 0.01, y1, hi[2] - 0.03])
            saida.append(Peca(grupo, "US5000_alca", vv, ff, (0.20, 0.21, 0.23), limpar(k)))
        y0, y1 = sorted([frente_y + s * 0.006, frente_y + s * 0.009])
        vv, ff = caixa_malha([lo[0] + 0.12, y0, hi[2] - 0.05], [lo[0] + 0.24, y1, hi[2] - 0.035])
        saida.append(Peca(grupo, "US5000_led", vv, ff, (0.20, 0.80, 0.35), limpar(k)))
        substituidas.add(k)
    # Layout A: o banco sobe 0,36 m e só os 7 cm da frente apoiam na caixa de roda. O resto vai sobre um
    # pedestal de cantoneiras de aço até o piso (quatro montantes, quadro superior e travessa inferior),
    # parafusado às chapas de fixação do item 15; a massa está na reserva de suportes elétricos.
    if layout == "A":
        lo = np.min([lim(k)[0] for k in caixas if "US5000" in k], axis=0)
        hi = np.max([lim(k)[1] for k in caixas if "US5000" in k], axis=0)
        arco = [p for p in arcos or [] if p.nome == "caixa_roda_esquerda"]
        x1 = min(hi[0], arco[0].caixa[0][0] - 0.005) if arco else hi[0]
        aco, c = (0.45, 0.47, 0.50), 0.03
        for xa in (lo[0], x1 - c):
            for ya in (lo[1], hi[1] - c):
                vv, ff = caixa_malha([xa, ya, PISO_Z], [xa + c, ya + c, lo[2]])
                saida.append(Peca(grupo, "pedestal_montante", vv, ff, aco, "pedestal_banco"))
        for z0 in (PISO_Z, lo[2] - c):
            for ya in (lo[1], hi[1] - c):
                vv, ff = caixa_malha([lo[0], ya, z0], [x1, ya + c, z0 + c])
                saida.append(Peca(grupo, "pedestal_travessa", vv, ff, aco, "pedestal_banco"))
        vv, ff = caixa_malha([lo[0], lo[1], lo[2] - 0.004], [x1, hi[1], lo[2]])
        saida.append(Peca(grupo, "pedestal_chapa", vv, ff, aco, "pedestal_banco"))

    # cooktop guardado: vidro preto
    k = achar("cooktop_armazenado"); v, f = caixas[k]
    saida.append(Peca(grupo, "cooktop_armazenado", v, f, (0.08, 0.08, 0.09))); substituidas.add(k)

    for k, (v, f) in caixas.items():
        if k in substituidas:
            continue
        nome = limpar(k)
        saida.append(Peca(grupo, nome, v, f, CORES[categoria(nome)]))
    return saida


def tubo(pontos, raio, nome, rgb, grupo="rotas"):
    """Polilinha de cilindros (um por trecho) com esferas nas curvas."""
    import trimesh

    saida = []
    p = [np.asarray(q, float) for q in pontos]
    for i, (a, b) in enumerate(itertools.pairwise(p)):
        if np.linalg.norm(b - a) < 1e-6:
            continue
        v, f = cilindro(a, b, raio, 12)
        saida.append(Peca(grupo, f"{nome}_{i}", v, f, rgb))
    for i, q in enumerate(p[1:-1]):
        e = trimesh.creation.icosphere(subdivisions=1, radius=raio)
        saida.append(Peca(grupo, f"{nome}_curva{i}", np.asarray(e.vertices) + q, np.asarray(e.faces), rgb))
    return saida


def rotas() -> list[Peca]:
    def cor(n):
        if "cabo_positivo" in n:
            return (0.85, 0.12, 0.12)
        if "cabo_retorno" in n:
            return (0.10, 0.10, 0.10)
        if any(k in n for k in ("tanque_bomba", "bomba_boiler", "principal_pia")):
            return (0.15, 0.55, 0.95)
        return (0.78, 0.80, 0.84)
    desloc = CARGA + np.array([0.0, -LARGURA / 2, 0.0])
    saida = []
    for n, v, f, _ in ler(E / "integrado_maxeon1560/rotas_instalacoes/layoutA_rotas_reserva.glb", desloc):
        if n.startswith("eletrico__") or "principal_pia" in n:
            continue                                   # refeitos abaixo, sem colisão
        if "US5000" in n:
            v = v + [AVANCO_BANCO_A, 0, SUBIDA_BANCO]
        if n.endswith("cooktop_armazenado"):
            v = v + [-RECUO_COOKTOP, 0, 0]
        saida.append(Peca("rotas", n, v, f, cor(n)))
    # 48 V: da frente do banco (y = 0,433, agora sobre a caixa de roda) pela frente do inversor até a base dele
    z_banco = 0.72 + SUBIDA_BANCO + 0.30
    for nome, dx, rgb in (("eletrico__cabo_positivo", 0.0, (0.85, 0.12, 0.12)), ("eletrico__cabo_retorno", 0.03, (0.10, 0.10, 0.10))):
        x0 = -2.93 + dx
        x1 = -2.62 + dx
        saida += tubo([(x0, 0.433, z_banco), (x0, 0.395, z_banco), (x1, 0.395, z_banco), (x1, 0.395, 0.925),
                       (x1, 0.58, 0.925), (x1, 0.58, 0.96)], RAIO_CABO, nome, rgb)
    # água para a pia: desce ao lado da bomba (fora do A/C), corre sob o piso e sobe atrás do gabinete até a torneira
    z_sob = PISO_Z - 0.07
    saida += tubo([(-2.15, 0.253, 1.03), (-2.15, 0.40, 1.03), (-2.15, 0.40, z_sob), (-0.684, 0.40, z_sob),
                   (-0.684, -0.86, z_sob), (-0.684, -0.86, 1.575), (-0.684, -0.807, 1.575), (-0.684, -0.807, 1.61)],
                  RAIO_TUBO, "hidraulica__principal_pia_sob_piso",
                  (0.15, 0.55, 0.95))
    return saida


def montagem() -> dict[str, list[Peca]]:
    ext = exterior()
    arcos = caixas_de_roda(ext)
    return {"exterior": ext, "arcos": arcos, "cabine": cabine_oem(), "tracao": tracao_oem(),
            "teto": deck_solar(ext), "layoutA": interior("A", arcos), "layoutB": interior("B", arcos), "rotas": rotas(),
            "solo": portateis_solo()}
