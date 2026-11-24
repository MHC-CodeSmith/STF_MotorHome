"""Figura do item 32: cortina refletiva no para-brisa e efeito na carga de A/C.

Uso (na raiz do repositório):
    .venv/bin/python relatorio/figura_cortina_i32.py

Esquerda: cabine do modelo exterior do projeto com a cortina plissada desenhada 3 cm atrás do
para-brisa (representação esquemática, não a geometria do produto). Direita: carga de projeto
(2 pessoas, 62 m³/h) sem e com a cortina, lida de entregas/integrado_maxeon1540/i32_protecao_solar.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import montagem_cad as M
import numpy as np
import renderizar_cad as R
from matplotlib.patches import Patch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ROOT = Path(__file__).resolve().parents[1]
I32 = ROOT / "entregas/integrado_maxeon1540/i32_protecao_solar/resumo.json"
VIDRO = "Exterior_Static_313fb3"        # malha única com todos os vidros do exterior (material Body_Glass)
RECUO = 0.03                            # cortina 3 cm atrás do vidro
PREGAS = 14                             # faixas horizontais alternadas para sugerir o plissado
PRATA = ((1.0, 1.0, 1.0), (0.86, 0.88, 0.91))


def para_brisa(tri):
    """Triângulos do vidro voltados para a frente na região da cabine."""
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    return (np.abs(n[:, 0]) > 0.45) & (tri.mean(1)[:, 0] > 1.0), n


def cortina(tri, n):
    """Cópia do para-brisa deslocada para dentro e dividida em pregas horizontais."""
    dentro = np.where((n[:, 0] > 0)[:, None], -n, n)         # normal apontando para o interior (-x)
    t = R.fatiar(tri + RECUO * dentro[:, None, :], 0.05)
    z = t.mean(1)[:, 2]
    faixa = np.floor((z - z.min()) / (np.ptp(z) + 1e-9) * PREGAS).astype(int) % 2
    return [(f"prega_{k}", t[faixa == k], PRATA[k]) for k in (0, 1)]


def render(ax):
    pecas = M.exterior()
    vidro = next(p for p in pecas if p.nome == VIDRO)
    sel, n = para_brisa(vidro.tri)
    resto = [(p.nome, p.tri, p.rgb) for p in pecas if p.nome != VIDRO and not p.nome.startswith(("Wheel_0_0", "Brake"))]
    itens = resto + [("vidro", vidro.tri[~sel], vidro.rgb)] + cortina(vidro.tri[sel], n[sel])
    itens += [("para_brisa", vidro.tri[sel], (0.55, 0.65, 0.75))]
    # recorta a dianteira (cabine) para enquadrar
    itens = [(k, t[t.mean(1)[:, 0] > 0.6], c) for k, t, c in itens]
    itens = [(k, t, c) for k, t, c in itens if len(t)]
    tri = desenhar(ax, itens, alfa={"para_brisa": 0.07})
    R.enquadrar(ax, tri, 12, 24, margem=0.02, zoom=1.22)
    ax.set_title("Cortina plissada refletiva atrás do para-brisa\n(representação no modelo do projeto)", fontsize=12)


def desenhar(ax, itens, alfa):
    """Como renderizar_cad.desenhar, sem antialiasing: evita as emendas claras entre triângulos."""
    tris, cores = [], []
    for nome, tri, rgb in itens:
        tri = R.fatiar(tri, 0.15)
        n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
        luz = 0.42 + 0.58 * np.abs(n @ R.LUZ)
        if nome.startswith("prega"):      # tecido metalizado: claro em qualquer orientação
            luz = 0.85 + 0.15 * np.abs(n @ R.LUZ)
        c = np.clip(np.asarray(rgb)[None, :] * luz[:, None], 0, 1)
        tris.append(tri)
        cores.append(np.hstack([c, np.full((len(tri), 1), alfa.get(nome, 1.0))]))
    tri = np.concatenate(tris)
    ax.add_collection3d(Poly3DCollection(tri, facecolors=np.concatenate(cores), edgecolors="none",
                                         linewidths=0, antialiased=False))
    return tri


def barras(ax):
    r = json.loads(I32.read_text())
    sem, com = r["design_case_unshaded_w"] / 1e3, r["design_case_nominal_iac_w"] / 1e3
    vidro = r["windshield_gain_unshaded_w"] / 1e3
    outras = sem - vidro
    lo, hi = (x / 1e3 for x in r["design_case_range_w"])
    cap = r["capacity_claim_w"] / 1e3
    x = np.arange(2)
    ax.bar(x, [outras, outras], color="#adb5bd")
    ax.bar(x, [vidro, com - outras], bottom=outras, color=["#e8590c", "#f4a261"])
    ax.errorbar(1.47, com, yerr=[[com - lo], [hi - com]], fmt="none", ecolor="k", capsize=5, lw=1)
    ax.axhline(cap, color="#1f5fbf", ls="--", lw=1.2)
    ax.text(2.12, cap + 0.05, f"FreshWell 3000: {cap:.1f} kW".replace(".", ","), color="#1f5fbf", fontsize=10.5, ha="right")
    for xi, v in zip(x, (sem, com)):
        ax.text(xi, v + 0.06, f"{v:.2f} kW".replace(".", ","), ha="center", fontsize=11.5, fontweight="bold")
    ax.text(1.54, com, f"IAC 0,3–0,7:\n{lo:.2f}–{hi:.2f} kW".replace(".", ","), fontsize=10, va="center")
    ax.set_xticks(x, ["sem cortina", "com cortina\n(IAC = 0,5)"])
    ax.set_ylabel("carga de refrigeração [kW]", fontsize=11)
    ax.tick_params(labelsize=10.5)
    ax.set_ylim(0, 3.4)
    ax.set_xlim(-0.6, 2.15)
    ax.legend(handles=[Patch(color="#e8590c", label="sol pelo para-brisa\n(sem cortina)"),
                       Patch(color="#f4a261", label="sol pelo para-brisa\n(com cortina)"),
                       Patch(color="#adb5bd", label="demais parcelas: condução, sol nas\noutras faces, pessoas,\nequipamentos e ventilação")],
              fontsize=10, loc="upper left", bbox_to_anchor=(1.0, 1.0), frameon=False)
    ax.set_title("Carga de projeto ao meio-dia (2 pessoas, 62 m³/h)", fontsize=12)
    ax.spines[["top", "right"]].set_visible(False)


def main() -> None:
    fig = plt.figure(figsize=(9.6, 4.2), facecolor="white")
    ax3 = fig.add_axes([0.0, 0.0, 0.37, 0.88], projection="3d", computed_zorder=False)
    ax2 = fig.add_axes([0.455, 0.15, 0.29, 0.72])
    render(ax3)
    barras(ax2)
    R.salvar(fig, "i32_cortina.png")


if __name__ == "__main__":
    main()
