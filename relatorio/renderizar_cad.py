"""Renderiza as imagens de CAD e de CFD do relatório a partir da geometria do projeto.

Uso (na raiz do repositório):
    .venv/bin/python relatorio/renderizar_cad.py \
        --cfd-vtk /home/mhc/motorhome_referencias_tarefas/cfd-familia-gci-20261116/bg_55x20x10/case/VTK/case_344

A montagem vem de relatorio/montagem_cad.py: exterior L3H2 adaptado (derivado de razor24/Dogan Ulus,
MPL-2.0 e CC-BY-4.0), layouts A/B detalhados no referencial do projeto (face traseira interna em
x = -3,35 m, piso em z = 0,68 m), tração e bancos OEM, deck Maxeon na posição do CFD, rotas e painéis
portáteis. Banco de serviços e chapas de fixação vêm dos STEP (malhados com gmsh).
Renderização por sombreamento de Lambert em matplotlib (sem dependência de GPU).
"""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import montagem_cad as M
import numpy as np
import trimesh
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "entregas"
OUT = ROOT / "relatorio/figuras"
LUZ = np.array([-0.35, -0.55, 0.76]) / np.linalg.norm([-0.35, -0.55, 0.76])
CORES = M.CORES

ROTULOS = {
    "geladeira_AC": "geladeira", "cassete": "cassete", "boiler": "boiler", "inversor": "inversor",
    "tanque_limpa": "água limpa", "tanque_cinza": "água cinza", "US5000_2": "banco 48 V (sob a cama)",
    "lava_seca": "lava e seca", "hvac": "A/C", "cama_colchao": "cama", "cama_conversivel_colchao": "cama conversível",
    "portatil_bolsa_2": "painéis portáteis", "banho": "banho", "tampo": "bancada",
}
ROTULOS_INTERIOR = {"lava_seca", "geladeira_AC", "cassete", "tampo", "cama_colchao", "cama_conversivel_colchao",
                    "US5000_2", "tanque_limpa", "banho"}
NOMES_CATEGORIA = {"energia": "energia 48 V", "agua": "água", "eletro": "eletrodomésticos", "clima": "A/C",
                   "movel": "mobiliário", "banho": "banheiro", "bolsa": "portáteis guardados", "cama": "cama/assentos"}


def lista(pecas):
    """Peças da montagem no formato (dono, triângulos, rgb) usado no desenho."""
    return [(p.dono, p.tri, p.rgb) for p in pecas]


def partes_step(caminho: Path, cor):
    malha = trimesh.load(step_para_stl(caminho))
    return [("malha", np.asarray(malha.vertices)[np.asarray(malha.faces)], cor)]


def step_para_stl(caminho: Path) -> Path:
    import gmsh

    destino = Path(tempfile.gettempdir()) / (caminho.stem + "_render.stl")
    if destino.exists():
        return destino
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.option.setNumber("Mesh.MeshSizeMax", 0.03)
    gmsh.open(str(caminho))
    gmsh.model.mesh.generate(2)
    gmsh.write(str(destino))
    gmsh.finalize()
    return destino


def fatiar(tri: np.ndarray, lim: float = 0.15) -> np.ndarray:
    """Divide triângulos pela aresta mais longa até todas ficarem abaixo de `lim` (m).

    O matplotlib não tem z-buffer: ordena polígonos inteiros pela profundidade média. Um triângulo
    longo (piso de 3,6 m, divisória) recebe uma profundidade só e é pintado por cima do que está à
    frente dele, aparecendo como uma cunha diagonal. Triângulos pequenos ordenam corretamente."""
    prontos = []
    while len(tri):
        e = np.stack([np.linalg.norm(tri[:, (i + 1) % 3] - tri[:, i], axis=1) for i in range(3)], axis=1)
        longo = e.max(1) > lim
        prontos.append(tri[~longo])
        t, k = tri[longo], e[longo].argmax(1)
        a = t[np.arange(len(t)), k]
        b = t[np.arange(len(t)), (k + 1) % 3]
        c = t[np.arange(len(t)), (k + 2) % 3]
        m = (a + b) / 2
        tri = np.concatenate([np.stack([a, m, c], 1), np.stack([m, b, c], 1)])
    return np.concatenate(prontos) if prontos else tri


def desenhar(ax, lista, alfa=None, aresta=None, lim=0.15):
    tris, cores = [], []
    for nome, tri, rgb in lista:
        if lim:
            tri = fatiar(tri, lim)
        n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
        luz = 0.42 + 0.58 * np.abs(n @ LUZ)
        c = np.clip(np.asarray(rgb)[None, :] * luz[:, None], 0, 1)
        a = np.full((len(tri), 1), 1.0 if alfa is None else alfa.get(nome, 1.0) if isinstance(alfa, dict) else alfa)
        tris.append(tri)
        cores.append(np.hstack([c, a]))
    tri = np.concatenate(tris)
    pc = Poly3DCollection(tri, facecolors=np.concatenate(cores), edgecolors=aresta or "none",
                          linewidths=0.15 if aresta else 0)
    ax.add_collection3d(pc)
    return tri


def enquadrar(ax, tri, elev, azim, margem=0.05, zoom=1.0):
    lo, hi = tri.reshape(-1, 3).min(0), tri.reshape(-1, 3).max(0)
    centro, faixa = (lo + hi) / 2, (hi - lo) * (1 + margem)
    for f, c, r in ((ax.set_xlim, centro[0], faixa[0]), (ax.set_ylim, centro[1], faixa[1]), (ax.set_zlim, centro[2], faixa[2])):
        f(c - r / 2, c + r / 2)
    aspecto = faixa.copy()
    if elev >= 89:          # vista superior: a altura não aparece, achatar para não sobrar margem
        aspecto[2] = 0.02 * faixa[:2].max()
    ax.set_box_aspect(aspecto, zoom=zoom)
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()


def figura_3d(n=1, tamanho=(9, 5)):
    fig = plt.figure(figsize=tamanho, facecolor="white")
    axs = [fig.add_subplot(1, n, i + 1, projection="3d", computed_zorder=False) for i in range(n)]
    fig.subplots_adjust(left=0, right=1, bottom=0, top=0.93, wspace=0)
    return fig, axs


def salvar(fig, nome, aparar=False, dpi=170):
    fig.savefig(OUT / nome, dpi=dpi, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    if aparar:              # vistas laterais em 3D deixam muito branco dentro do eixo: corta as margens
        from PIL import Image, ImageChops

        img = Image.open(OUT / nome).convert("RGB")
        caixa = ImageChops.difference(img, Image.new("RGB", img.size, "white")).getbbox()
        if caixa:
            img.crop((max(caixa[0] - 12, 0), max(caixa[1] - 12, 0), caixa[2] + 12, caixa[3] + 12)).save(OUT / nome)
    print("ok", nome)


def legenda(ax, extra=()):
    from matplotlib.patches import Patch

    itens = [Patch(color=CORES[k], label=v) for k, v in NOMES_CATEGORIA.items()]
    itens += [Patch(color=c, label=r) for r, c in extra]
    ax.legend(handles=itens, loc="lower left", fontsize=7, frameon=False, ncol=2)


def rotular(ax, pecas, deslocamento_z=0.12, so=None):
    """Um rótulo por equipamento (dono), no topo da caixa que reúne as suas peças."""
    caixas: dict[str, list] = {}
    for p in pecas:
        dono = "banho" if "banho" in p.dono else p.dono
        if dono in ROTULOS and (so is None or dono in so):
            caixas.setdefault(dono, []).append(p.v)
    for dono, vs in caixas.items():
        v = np.vstack(vs)
        c = (v.min(0) + v.max(0)) / 2
        ax.text(c[0], c[1], v[:, 2].max() + deslocamento_z, ROTULOS[dono], fontsize=7, ha="center",
                zorder=10, bbox={"fc": "white", "ec": "0.6", "lw": 0.4, "pad": 1.2, "alpha": 0.85})


def translucido(pecas, a=0.35):
    return {p.dono: a for p in pecas if "cama" in p.dono or p.dono in ("estrado", "ponte_cama", "travesseiro")}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cfd-vtk", type=Path)
    ap.add_argument("--so-cfd", action="store_true", help="refaz só as figuras de CFD")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if not args.so_cfd:
        cad()
    if args.cfd_vtk:
        cfd(args.cfd_vtk)


def cad() -> None:
    G = M.montagem()
    exterior = lista(G["exterior"])
    sob = lista([p for p in G["teto"] if p.nome in ("trilho", "pe_trilho")])      # desenhados antes dos módulos
    teto = lista([p for p in G["teto"] if p.nome not in ("trilho", "pe_trilho")])
    oem = G["cabine"] + G["tracao"] + G["arcos"]

    # 1. exterior com teto solar, duas vistas
    fig, axs = figura_3d(2, (12, 4.6))
    for ax, azim, tit in ((axs[0], 32, "dianteira"), (axs[1], -140, "traseira")):
        tri = desenhar(ax, exterior)
        desenhar(ax, sob)
        desenhar(ax, teto)
        enquadrar(ax, tri, 16, azim, zoom=1.25)
        ax.set_title(f"Vista {tit}", fontsize=9)
    fig.suptitle("Aurora Solar — exterior com teto de 4 módulos Maxeon (1560 Wp)", fontsize=10)
    salvar(fig, "cad_exterior.png")

    # 2. estacionado, portáteis abertos no solo
    fig, axs = figura_3d(1, (9, 5.4))
    tri = desenhar(axs[0], lista(G["solo"]) + exterior)
    desenhar(axs[0], sob)
    desenhar(axs[0], teto)
    enquadrar(axs[0], tri, 28, -62, zoom=1.3)
    axs[0].set_title("Estacionado: teto 1560 Wp + 4 painéis portáteis de 400 W abertos (≈ 14,5 kWh/dia em 21/06)", fontsize=9)
    salvar(fig, "cad_estacionado.png")

    # 3. interiores em corte (carroceria fantasma), com tração sob o piso e bancos da cabine
    fantasma = [(n, t, (0.55, 0.60, 0.68)) for n, t, _ in exterior]
    for nome_fig, chave, titulo in (("cad_interior_A.png", "layoutA", "Layout A (cama fixa) — escolhido"),
                                    ("cad_interior_B.png", "layoutB", "Layout B (cama conversível) — comparador")):
        lay = G[chave]
        fig, axs = figura_3d(1, (10, 5.6))
        alfa = {n: 0.045 for n, _, _ in fantasma}
        alfa.update(translucido(lay))
        tri = desenhar(axs[0], fantasma + lista(oem) + lista(lay), alfa=alfa)
        enquadrar(axs[0], tri, 34, -58, zoom=1.2)
        rotular(axs[0], lay, so=ROTULOS_INTERIOR)
        legenda(axs[0], extra=(("tração OEM (sob o piso)", M.TRACAO["pack_tracao"]),))
        axs[0].set_title(f"{titulo}: interior em corte, carroceria transparente", fontsize=9)
        salvar(fig, nome_fig)

    # 4. plantas A e B
    fig = plt.figure(figsize=(10, 6.6), facecolor="white")
    axs = [fig.add_subplot(2, 1, i + 1, projection="3d", computed_zorder=False) for i in range(2)]
    fig.subplots_adjust(left=0, right=1, bottom=0, top=0.95, hspace=0.02)
    for ax, chave, tit in ((axs[0], "layoutA", "Layout A"), (axs[1], "layoutB", "Layout B")):
        lay = G[chave]
        tri = desenhar(ax, lista(G["arcos"] + lay), alfa=translucido(lay, 0.3), aresta=(0.2, 0.2, 0.2, 0.35))
        enquadrar(ax, tri, 90, -90, zoom=1.4)
        ax.set_proj_type("ortho")
        rotular(ax, lay, 0.05, so=(ROTULOS_INTERIOR - {"banho"}) | {"boiler", "inversor", "hvac", "tanque_cinza"})
        ax.set_title(f"{tit} — planta (frente do veículo à direita, cama transparente)", fontsize=9)
    legenda(axs[1])
    salvar(fig, "cad_plantas.png")

    # 5. rotas de cabos e água
    rotas = G["rotas"]
    instal = lambda n: any(k in n for k in ("cabo", "tanque_bomba", "bomba_boiler", "principal_pia"))
    alfa = {p.nome: 0.35 for p in rotas if not instal(p.nome)}
    fig, axs = figura_3d(1, (10, 5))
    sob_piso = lambda p: instal(p.nome) and p.v[:, 2].max() < M.PISO_Z - 0.02
    piso = [p for p in G["layoutA"] if p.nome == "piso"]
    pack = [p for p in G["tracao"] if p.nome.startswith("pack_tracao")]
    t_pack = desenhar(axs[0], [(p.nome, p.tri, p.rgb) for p in pack], alfa=0.25)
    desenhar(axs[0], [(p.nome, p.tri, p.rgb) for p in rotas if sob_piso(p)])          # sob o piso: antes dele
    tri = desenhar(axs[0], [(p.nome, p.tri, p.rgb) for p in piso], alfa=0.45)
    tri = np.concatenate([tri, desenhar(axs[0], [(p.nome, p.tri, p.rgb) for p in rotas if not instal(p.nome)], alfa=alfa)])
    desenhar(axs[0], [(p.nome, p.tri, p.rgb) for p in rotas if instal(p.nome) and not sob_piso(p)])
    enquadrar(axs[0], np.concatenate([tri, t_pack]), 30, -55, zoom=1.15)
    caixas = [M.Peca("rotas", p.nome, p.v, p.f, p.rgb, M.limpar(p.nome)) for p in rotas]
    rotular(axs[0], caixas)
    axs[0].set_title("Rotas: cabos 48 V (vermelho +, preto −) e água (azul), layout A; linha da pia sob o piso", fontsize=9)
    salvar(fig, "cad_rotas.png")

    # 6. teto em planta
    fig, axs = figura_3d(1, (10, 3.6))
    tri = desenhar(axs[0], exterior)
    desenhar(axs[0], sob)
    desenhar(axs[0], teto)
    enquadrar(axs[0], tri, 90, -90, zoom=1.1)
    axs[0].set_proj_type("ortho")
    axs[0].set_title("Teto: 4× SPR-MAX3-390 (1560 Wp, 2S2P), deck de 4,24 × 1,69 m a 40 mm do teto", fontsize=9)
    salvar(fig, "cad_teto.png")

    # 7. corte longitudinal: metade esquerda da carroceria, interior A, tração sob o piso e deck sobre trilhos
    meia = [(n, t[t[:, :, 1].mean(1) > 0.05], c) for n, t, c in exterior if not n.startswith(("Wheel_0_0", "Wheel_1_0"))]
    meia = [(n, t, c) for n, t, c in meia if len(t)]
    fig, axs = figura_3d(1, (12, 4.4))
    lay = G["layoutA"]
    alfa = {n: 0.55 for n, _, _ in meia}
    tri = desenhar(axs[0], meia + lista(G["tracao"] + G["cabine"] + G["arcos"] + lay) + sob, alfa=alfa)
    desenhar(axs[0], teto)
    enquadrar(axs[0], tri, 6, -90, margem=0.02, zoom=1.05)
    axs[0].set_proj_type("ortho")
    rotular(axs[0], lay, 0.06, so={"cama_colchao", "cassete", "geladeira_AC", "lava_seca", "US5000_2", "tampo"})
    salvar(fig, "cad_corte.png", aparar=True, dpi=400)     # título vai na legenda do relatório

    # 8. banco de serviços na montagem final (sobre a caixa de roda, sob o estrado) e chapas de fixação
    modulos = [p for p in lay if p.dono.startswith("US5000")]
    vb = np.vstack([p.v for p in modulos])
    lo, hi = vb.min(0) - [0.45, 0.35, 0], vb.max(0) + [0.45, 0.35, 0]
    perto = [p for p in G["arcos"] + lay if not p.dono.startswith("US5000")
             and p.dono in {"estrado", "cama_colchao", "piso", "pedestal_banco"} | {a.dono for a in G["arcos"]}
             and np.all(p.v.max(0)[:2] >= lo[:2]) and np.all(p.v.min(0)[:2] <= hi[:2])]
    corte = []
    for p in perto:
        t = fatiar(p.tri, 0.04)
        corte.append((p.dono, t[np.all((t[..., :2] >= lo[:2]) & (t[..., :2] <= hi[:2]), axis=(1, 2))], p.rgb))
    corte = [c for c in corte if len(c[1])]
    chapas = partes_step(E / "desenvolvimento_2026-11-09/fixacoes_redimensionadas/chapas_locais_condicionais.step",
                         (0.62, 0.64, 0.68))
    fig, axs = figura_3d(2, (12, 4.2))
    tri = desenhar(axs[0], corte, alfa={"estrado": 0.35, "cama_colchao": 0.2}, lim=None)
    desenhar(axs[0], lista(modulos), aresta=(0.1, 0.1, 0.15, 0.25))
    enquadrar(axs[0], tri, 18, -55, zoom=1.15)
    topo = vb.max(0)
    axs[0].text(vb[:, 0].max() + 0.05, vb[:, 1].mean(), topo[2] - 0.2, "3× US5000\n(banco 48 V)", fontsize=8,
                ha="left", zorder=50, bbox={"fc": "white", "ec": "0.6", "lw": 0.4, "pad": 1.5})
    for dono, txt, desloc in (("estrado", "estrado da cama", (0, 0, 0)), ("caixa_roda_esquerda", "caixa de roda", (0.25, 0, -0.12)),
                              ("pedestal_banco", "pedestal de aço", (-0.12, 0, -0.22))):
        vs = [p.v for p in perto if p.dono == dono]
        if vs:
            v = np.vstack(vs)
            v = v[np.all((v[:, :2] >= lo[:2]) & (v[:, :2] <= hi[:2]), axis=1)]
            if len(v):
                v = v[v[:, 2] >= v[:, 2].max() - 0.02]
                axs[0].text(*v.mean(0) + [0, 0, 0.06] + np.asarray(desloc), txt, fontsize=8, ha="center", zorder=50,
                            bbox={"fc": "white", "ec": "0.6", "lw": 0.4, "pad": 1.5})
    axs[0].set_title("Banco de serviços: 3× US5000 no pedestal e na caixa de roda, sob o estrado", fontsize=9)
    tri = desenhar(axs[1], chapas, aresta=(0.1, 0.1, 0.15, 0.25))
    enquadrar(axs[1], tri, 30, -50, zoom=1.2)
    axs[1].set_title("18 chapas de fixação dimensionadas (STEP, 33,1 kg)", fontsize=9)
    salvar(fig, "cad_banco_fixacoes.png")


def cfd(pasta: Path) -> None:
    import vtk
    from vtk.util.numpy_support import vtk_to_numpy

    u_inf = 22.222222

    def ler_vtp(arquivo):
        r = vtk.vtkXMLPolyDataReader()
        r.SetFileName(str(arquivo))
        r.Update()
        tri = vtk.vtkTriangleFilter()
        tri.SetInputData(r.GetOutput())
        tri.Update()
        c2p = vtk.vtkCellDataToPointData()
        c2p.SetInputData(tri.GetOutput())
        c2p.Update()
        pd = tri.GetOutput()
        pts = vtk_to_numpy(pd.GetPoints().GetData())
        cel = vtk_to_numpy(pd.GetPolys().GetData()).reshape(-1, 4)[:, 1:]
        p = vtk_to_numpy(pd.GetCellData().GetArray("p"))
        return pts[cel], p

    tri_c, p_c = ler_vtp(pasta / "boundary/aurora.vtp")
    tri_d, p_d = ler_vtp(pasta / "boundary/pvdeck.vtp")
    tri = np.concatenate([tri_c, tri_d])
    cp = np.concatenate([p_c, p_d]) / (0.5 * u_inf**2)
    norm = matplotlib.colors.Normalize(-1.0, 1.0)
    cmap = plt.get_cmap("turbo")
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    luz = 0.55 + 0.45 * np.abs(n @ LUZ)
    cores = cmap(norm(cp))
    cores[:, :3] *= luz[:, None]
    fig, axs = figura_3d(2, (12, 4.4))
    for ax, azim, tit in ((axs[0], 35, "frente"), (axs[1], -145, "traseira")):
        el, az = np.radians(18), np.radians(azim)
        olho = np.array([np.cos(el) * np.cos(az), np.cos(el) * np.sin(az), np.sin(el)])
        # normais dos patches do OpenFOAM apontam para fora do fluido, isto é, para dentro do veículo
        vis = n @ olho < 0
        ax.add_collection3d(Poly3DCollection(tri[vis], facecolors=cores[vis], edgecolors="none"))
        enquadrar(ax, tri, 18, azim, zoom=1.25)
        ax.set_title(f"$C_p$ na superfície — {tit}", fontsize=9)
    sm = matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap)
    fig.colorbar(sm, ax=axs, shrink=0.6, label="$C_p = p/(\\frac{1}{2}U_\\infty^2)$", pad=0.01)
    salvar(fig, "cfd_cp.png")

    r = vtk.vtkXMLUnstructuredGridReader()
    r.SetFileName(str(pasta / "internal.vtu"))
    r.Update()
    plano = vtk.vtkPlane()
    plano.SetOrigin(0, 0.001, 0)
    plano.SetNormal(0, 1, 0)
    corte = vtk.vtkCutter()
    corte.SetCutFunction(plano)
    corte.SetInputConnection(r.GetOutputPort())
    corte.Update()
    tf = vtk.vtkTriangleFilter()
    tf.SetInputData(corte.GetOutput())
    tf.Update()
    pd = tf.GetOutput()
    pts = vtk_to_numpy(pd.GetPoints().GetData())
    cel = vtk_to_numpy(pd.GetPolys().GetData()).reshape(-1, 4)[:, 1:]
    u = vtk_to_numpy(pd.GetCellData().GetArray("U"))
    umag = np.linalg.norm(u, axis=1) / u_inf
    fig, ax = plt.subplots(figsize=(11, 3.4))
    tc = ax.tripcolor(pts[:, 0], pts[:, 2], cel, facecolors=umag, cmap="viridis", vmin=0, vmax=1.3, shading="flat")
    ax.set_facecolor("0.78")   # sem células dentro do veículo: o fundo cinza é a silhueta
    ax.set(xlim=(-10, 5), ylim=(0, 4.5), xlabel="x [m] (escoamento da direita para a esquerda)", ylabel="z [m]", aspect="equal")
    ax.set_title("Velocidade no plano de simetria, $|U|/U_\\infty$ (80 km/h, malha fina)", fontsize=9)
    fig.colorbar(tc, ax=ax, label="$|U|/U_\\infty$", pad=0.01)
    fig.tight_layout()
    fig.savefig(OUT / "cfd_plano.png", dpi=170)
    plt.close(fig)
    print("ok cfd_plano.png")


if __name__ == "__main__":
    main()
