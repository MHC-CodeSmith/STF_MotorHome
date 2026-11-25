"""Gera e reúne as figuras do relatório a partir dos resultados versionados.

Uso (na raiz do repositório): .venv/bin/python relatorio/gerar_figuras.py
Lê somente arquivos em entregas/ e equipe/; grava em relatorio/figuras/.
"""

from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "entregas/integrado_maxeon1560"
OUT = ROOT / "relatorio/figuras"
plt.rcParams.update({"figure.dpi": 110, "savefig.dpi": 180, "font.size": 9, "axes.grid": True,
                     "grid.alpha": 0.3, "axes.spines.top": False, "axes.spines.right": False})
C = {"azul": "#1f5fbf", "laranja": "#e8590c", "verde": "#2b8a3e", "cinza": "#868e96", "roxo": "#7048e8"}


def ler(p: Path) -> list[dict]:
    with p.open() as f:
        return list(csv.DictReader(f))


def col(rows, k):
    return np.array([float(r[k]) for r in rows])


def salvar(fig, nome):
    fig.tight_layout()
    fig.savefig(OUT / nome)
    plt.close(fig)


def solar():
    """I08: teto, portáteis e soma hora a hora nos quatro casos de operação do mesmo dia."""
    pasta = E / "p5_geracao_portateis"
    rows = ler(pasta / "horario_casos.csv")
    res = json.loads((pasta / "resumo.json").read_text())["casos"]
    wp = json.loads((E / "solar/resumo.json").read_text())["roof_wp"]
    titulos = {"so_teto": "só teto", "parado_dia_todo": "parado o dia todo (portáteis prontos antes do amanhecer)",
               "conducao_08_16": "condução diurna, 08–16 h", "conducao_18_02": "condução no fim da tarde, 18–02 h"}
    fig, axs = plt.subplots(2, 2, figsize=(9, 5.2), sharex=True, sharey=True)
    for ax, (caso, tit) in zip(axs.flat, titulos.items()):
        r = [x for x in rows if x["caso"] == caso]
        h, teto, port, tot = col(r, "hora"), col(r, "teto_kw"), col(r, "portateis_kw"), col(r, "total_kw")
        ab = np.array([x["abertos"] == "True" for x in r])
        janela = res[caso]["janela_conducao_h"]
        if janela and janela[0] != janela[1]:
            ini, fim = janela
            for a, b in ([(ini, fim)] if fim > ini else [(ini, 24), (0, fim)]):
                ax.axvspan(a, b, color=C["cinza"], alpha=0.15, lw=0)
        if ab.any() and not ab.all():
            for t0 in h[1:][np.diff(ab.astype(int)) != 0]:
                ax.axvline(t0, color=C["azul"], ls=":", lw=0.8)
        ax.fill_between(h, teto, color=C["laranja"], alpha=0.35, lw=0)
        ax.plot(h, teto, color=C["laranja"], lw=1.2, label=f"teto {wp} Wp")
        ax.plot(h, port, color=C["azul"], lw=1.2, label="portáteis 1600 Wp")
        ax.plot(h, tot, color="k", lw=1.6, label="soma")
        ax.set_title(f"{tit}\nteto {res[caso]['teto_kwh']:.2f} + portáteis {res[caso]['portateis_kwh']:.2f} = "
                     f"{res[caso]['total_kwh']:.2f} kWh".replace(".", ","), fontsize=8.5)
        ax.set(xlim=(0, 24), xticks=range(0, 25, 4))
    axs[0, 0].legend(loc="upper left", fontsize=7.5)
    for ax in axs[1]:
        ax.set_xlabel("hora local (21/06, São Carlos, céu limpo)")
    for ax in axs[:, 0]:
        ax.set_ylabel("potência CC [kW]")
    salvar(fig, "i08_geracao_solar.png")


def dinamica():
    rows = [r for r in ler(E / "integracao/dinamica_massa_integrada.csv")
            if r["layout"] == "A_fixa" and r["mass_case"] == "tipica_estimada"]
    v = col(rows, "speed_kmh"); fa = col(rows, "aerodinamica_n"); fr = col(rows, "rolamento_n")
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ax.plot(v, fa, color=C["azul"], label="arrasto aerodinâmico")
    ax.plot(v, fr, color=C["verde"], label="resistência ao rolamento")
    ax.plot(v, fa + fr, color="k", lw=2, label="total")
    ax.set(xlabel="velocidade [km/h]", ylabel="força [N]", xlim=(0, 90))
    ax.legend()
    salvar(fig, "i21_forcas_resistivas.png")
    pw = col(rows, "rodas_kw"); pb = col(rows, "bateria_kw")
    ms = v / 3.6
    cfg = json.loads((E / "parametros_resolvidos.json").read_text())
    perf = cfg["development"]["performance_envelope"]
    eta_red = min(perf["gear_efficiency"], key=lambda x: abs(x-.97))
    ratio = min(perf["gear_ratio"], key=lambda x: abs(x-10))
    available = eta_red*np.minimum(perf["peak_torque_nm"]*ratio*ms/perf["wheel_radius_m"], perf["peak_motor_w"])/1000
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.3))
    ax = axes[0]
    ax.plot(v, fa * ms / 1000, color=C["azul"], label="aerodinâmica")
    ax.plot(v, fr * ms / 1000, color=C["verde"], label="rolamento")
    ax.plot(v, pw, color="k", lw=2, label="demanda nas rodas")
    ax.plot(v, pb, color=C["laranja"], lw=2, ls="--", label="demanda na bateria")
    ax.set(xlabel="velocidade [km/h]", ylabel="potência [kW]", xlim=(0,90), title="Demanda em regime")
    ax.legend(fontsize=7)
    ax = axes[1]
    ax.plot(np.r_[0,v], np.r_[0,available], color=C["roxo"], label="pico disponível nas rodas")
    ax.plot(v,pw,color="k",label="demanda nas rodas")
    ax.set(xlabel="velocidade [km/h]",ylabel="potência [kW]",xlim=(0,90),title="Envelope do motor e redutor")
    ax.legend(fontsize=7)
    salvar(fig, "i22_potencias.png")
    fig, ax = plt.subplots(figsize=(6.4, 3))
    km = col(rows, "km_kwh")
    ax.plot(v, km, color=C["roxo"], lw=2)
    for vv in (40, 80):
        k = float(np.interp(vv, v, km))
        ax.plot(vv, k, "o", color=C["laranja"]); ax.annotate(f"{k:.2f} km/kWh", (vv, k), textcoords="offset points", xytext=(6, 6))
    ax.set(xlabel="velocidade [km/h]", ylabel="consumo [km/kWh]", xlim=(0, 90))
    salvar(fig, "i26_km_kwh.png")


def autonomia_solar():
    linhas = ler(E / "despacho_i25/melhores_por_velocidade.csv")
    todas = [r for r in linhas if r["services_cyclic"] == "False"]
    # passo mais fino que cobre toda a faixa 10–90 km/h
    passos = sorted({int(r["step_min"]) for r in todas})
    passo = next(s for s in passos if len({r["speed_kmh"] for r in todas if int(r["step_min"]) == s}) > 10)
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    mininos = sorted({float(r["hypothetical_dc_min_input_kw"]) for r in todas if float(r["hypothetical_dc_min_input_kw"]) > 0})
    piso = mininos[0] if mininos else 1.0
    rotulo_piso = f"{piso:g}".replace(".", ",")
    # Compara o piso como número: o CSV grava 0.0/0.38/3.0 quando a varredura tem valor fracionário.
    casos = (("False", 0.0, C["cinza"], "--", "sem habitação, interface ideal (sem mínimo)"),
             ("False", piso, C["laranja"], "-", f"sem habitação, mínimo de {rotulo_piso} kW na saída"),
             ("True", piso, C["azul"], "-", f"com a habitação (7,23 kWh/dia), mínimo de {rotulo_piso} kW"))
    for serv, dc, cor, ls, lab in casos:
        sel = sorted((r for r in linhas if r["services_cyclic"] == serv and float(r["hypothetical_dc_min_input_kw"]) == dc
                      and int(r["step_min"]) == passo), key=lambda r: float(r["speed_kmh"]))
        v, d = col(sel, "speed_kmh"), col(sel, "distance_km")
        ax.plot(v, d, color=cor, ls=ls, label=lab)
        if dc == piso:
            fino = [r for r in linhas if r["services_cyclic"] == serv and float(r["hypothetical_dc_min_input_kw"]) == dc
                    and r["step_min"] == "5"]
            for vv in (40, 80):
                k = next(float(r["distance_km"]) for r in fino if float(r["speed_kmh"]) == vv)
                ax.plot(vv, k, "o", color=cor)
                ax.annotate(f"{k:.1f} km".replace(".", ","), (vv, k), textcoords="offset points", xytext=(5, 5), color=cor)
    ax.set(xlabel="velocidade [km/h]", ylabel="distância com o sol do dia [km]", xlim=(10, 90), ylim=(0, None))
    ax.set_title(f"curvas com passo de {passo} min; pontos a 40 e 80 km/h com passo de 5 min", fontsize=8)
    ax.legend(fontsize=7.5)
    salvar(fig, "i25_autonomia_solar.png")


def i27():
    # Cada linha guarda o valor do intervalo que termina naquele instante (steps-pre).
    fig, axs = plt.subplots(1, 3, figsize=(9, 2.8))
    for nome, cor, lab in (("I27_SOC1_otimo_ate24h.csv", C["azul"], "ótimo (até 24 h)"),
                           ("I27_SOC1_8h.csv", C["laranja"], "janela de 8 h")):
        r = ler(E / "energia_sistemas" / nome)
        t, v = col(r, "time_h"), col(r, "speed_kmh")
        pb, pw, soc = col(r, "battery_power_kw"), col(r, "wheels_power_kw"), col(r, "soc_traction")
        if t[-1] < 24:
            t, v, pb, pw, soc = (np.append(t, 24.0), np.append(v, 0.0), np.append(pb, 0.0),
                                 np.append(pw, 0.0), np.append(soc, soc[-1]))
        axs[0].plot(t, v, color=cor, label=lab, drawstyle="steps-pre")
        axs[1].plot(t, pb, color=cor, drawstyle="steps-pre")
        eta_red = 0.97  # hipótese de rendimento do redutor do item5
        axs[1].plot(t, pw/eta_red, color=cor, ls="--", drawstyle="steps-pre")
        axs[2].plot(t, 100 * soc, color=cor)
    axs[0].set(xlabel="tempo [h]", ylabel="velocidade [km/h]", xlim=(0, 24)); axs[0].legend(fontsize=7)
    axs[1].set(xlabel="tempo [h]", ylabel="potência [kW]", title="— bateria   - - motor (ηred=0,97)", ylim=(0, None), xlim=(0, 24))
    axs[2].axhline(30, color="k", lw=0.8, ls=":"); axs[2].set(xlabel="tempo [h]", ylabel="SOC tração [%]", xlim=(0, 24))
    salvar(fig, "i27_perfil.png")


def i28():
    mass = json.loads((E / "integracao/layouts_massas.json").read_text())["layouts"]["A_fixa"]["nominal"]["mass_kg"]
    r = ler(E / f"mecanica_termica/aceleracao_{mass:.2f}_10_0.97_0.8.csv")
    t, v = col(r, "time_s"), col(r, "speed_kmh")
    fig, ax = plt.subplots(figsize=(6.4, 3))
    ax.plot(t, v, color=C["azul"], lw=2)
    ax.axhline(90, color=C["laranja"], ls="--", lw=1); ax.text(0.3, 92, "limitador eletrônico 90 km/h", color=C["laranja"])
    ax.axhline(100, color=C["cinza"], ls=":", lw=1); ax.text(0.3, 102, "100 km/h (não alcançado)", color=C["cinza"])
    t90 = float(np.interp(89.99, v, t))
    ax.annotate(f"0–90 km/h em {t90:.1f} s", (t90, 90), textcoords="offset points", xytext=(-90, -30), arrowprops={"arrowstyle": "->"})
    ax.set(xlabel="tempo [s]", ylabel="velocidade [km/h]", ylim=(0, 110), xlim=(0, max(t)))
    salvar(fig, "i28_aceleracao.png")


def vistas_exterior():
    """I17: vistas ortográficas cotadas e isométrica da geometria externa usada no CFD."""
    import trimesh
    from matplotlib.collections import PolyCollection
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    tri = ROOT / "entregas/aero_equipado1540/malha_adicional_1/case/constant/triSurface"
    corpo, deck = trimesh.load(tri / "aurora.stl"), trimesh.load(tri / "pvdeck.stl")
    tudo = trimesh.util.concatenate([corpo, deck])
    lo, hi = tudo.bounds
    comp, larg, alt = hi - lo
    v = corpo.vertices
    tras = v[v[:, 0] < lo[0] + 0.7 * comp]          # atrás dos espelhos
    larg_corpo = float(np.ptp(tras[:, 1]))
    teto = float(corpo.bounds[1][2])
    fig = plt.figure(figsize=(10, 6.2))
    vistas = [("Vista lateral", (0, 2), (0.05, 0.50, 0.55, 0.40)), ("Vista superior", (0, 1), (0.05, 0.04, 0.55, 0.38)),
              ("Vista frontal", (1, 2), (0.66, 0.50, 0.30, 0.40))]
    for titulo, (a, b), pos in vistas:
        ax = fig.add_axes(pos)
        for malha, cor in ((corpo, "#c5d3e8"), (deck, "#e8590c")):
            pol = malha.vertices[malha.faces][:, :, [a, b]]
            ax.add_collection(PolyCollection(pol, facecolor=cor, edgecolor="none"))
        ax.set_aspect("equal"); ax.set_title(titulo, fontsize=9)
        ax.set_xlim(lo[a] - 0.4, hi[a] + 0.4); ax.set_ylim(lo[b] - 0.55, hi[b] + 0.45)
        if (a, b) != (0, 2):
            ax.set_xlabel("m")
        ax.grid(alpha=0.2)

        def cota(ax, p0, p1, txt, off, horiz=True):
            ax.annotate("", p0, p1, arrowprops={"arrowstyle": "<->", "lw": 0.8})
            mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
            ax.text(mx + (0 if horiz else off), my + (off if horiz else 0), txt, ha="center", va="center", fontsize=8,
                    rotation=0 if horiz else 90, bbox={"fc": "white", "ec": "none", "pad": 1})
        if (a, b) == (0, 2):
            cota(ax, (lo[0], lo[2] - 0.3), (hi[0], lo[2] - 0.3), f"comprimento {comp:.3f} m", 0)
            cota(ax, (hi[0] + 0.25, lo[2]), (hi[0] + 0.25, hi[2]), f"altura c/ FV {alt:.3f} m", 0, False)
            ax.text(lo[0] + 0.1, hi[2] + 0.2, f"teto da carroceria {teto:.3f} m; entre-eixos 4,035 m (dado OEM)", fontsize=7)
        elif (a, b) == (0, 1):
            cota(ax, (hi[0] + 0.25, lo[1]), (hi[0] + 0.25, hi[1]), f"c/ espelhos {larg:.3f} m", 0, False)
            cota(ax, (lo[0] + 0.3, -larg_corpo / 2), (lo[0] + 0.3, larg_corpo / 2), f"carroceria {larg_corpo:.3f} m", 0, False)
            db = deck.bounds
            ax.text(db[0][0], hi[1] + 0.15, f"teto FV {db[1][0] - db[0][0]:.2f} × {db[1][1] - db[0][1]:.2f} m (4 Maxeon, 1560 Wp)",
                    fontsize=7, color="#e8590c")
        else:
            cota(ax, (-larg_corpo / 2, lo[2] - 0.3), (larg_corpo / 2, lo[2] - 0.3), f"{larg_corpo:.3f} m", 0)
    ax3 = fig.add_axes((0.62, 0.02, 0.36, 0.48), projection="3d")
    for malha, cor in ((corpo, "#9fb4d6"),
                       (deck, "#e8590c")):
        ax3.add_collection3d(Poly3DCollection(malha.vertices[malha.faces], facecolor=cor, edgecolor="#5c6f8f",
                                              linewidths=0.05, alpha=1.0))
    ax3.set_xlim(lo[0], hi[0]); ax3.set_ylim(lo[1] - 1.9, hi[1] + 1.9); ax3.set_zlim(lo[2], lo[2] + comp * 0.5)
    ax3.set_box_aspect((comp, larg + 3.8, comp * 0.5)); ax3.view_init(18, -125); ax3.set_axis_off()
    fig.suptitle("Aurora Solar — geometria externa (modelo equivalente do CFD, Fiat E-Ducato L3H2 + teto FV)", fontsize=10, y=0.995)
    fig.savefig(OUT / "i17_vistas_exterior.png")
    plt.close(fig)


def vistas_layout():
    """Planta dos envelopes do layout A e níveis das baterias na montagem final."""
    if __package__:
        from . import montagem_cad as cad
    else:
        import montagem_cad as cad

    from matplotlib.patches import Rectangle
    from matplotlib.ticker import FuncFormatter

    config = json.loads((E / "parametros_resolvidos.json").read_text())["development"]
    geometria = config["geometry"]
    comp, largura, _ = np.array(geometria["cargo_outer_m"]) - 2 * geometria["lining_each_side_m"]
    volumes = {}
    for item in config["layout_equipment"]["A_fixa"]:
        nome = item["id"]
        pos = np.array(item["position_m"], dtype=float)
        if nome.startswith("US5000_"):
            pos[2] += cad.SUBIDA_BANCO
        elif nome == "cooktop_armazenado":
            pos[0] -= cad.RECUO_COOKTOP
        volumes[nome] = pos, np.array(item["dimensions_m"])

    equipamentos = [
        ("cama_colchao", "Cama", "#e3e6dc"),
        ("portatil_bolsa_1", "Portáteis", "#c9c1ab"),
        ("tanque_limpa", "", "#b0d5d9"), ("tanque_cinza", "", "#b0d5d9"),
        ("boiler", "", "#b0d5d9"), ("bomba", "", "#b0d5d9"),
        ("inversor", "", "#a4b6c4"), ("hvac", "", "#c5c5da"),
        ("lava_seca", "Lava e seca", "#dcd5c9"), ("geladeira_AC", "Geladeira", "#dcd5c9"),
        ("cooktop_armazenado", "", "#dcd5c9"), ("cassete", "Cassete", "#dbd6cf"),
        ("US5000_1", "Banco", "#5789ab"),
    ]
    fig, (plan, elev) = plt.subplots(1, 2, figsize=(9.2, 3.6),
                                     gridspec_kw={"width_ratios": [1.45, 1]})
    fig.subplots_adjust(left=.068, right=.98, top=.85, bottom=.19, wspace=.14)
    plan.add_patch(Rectangle((0, 0), comp, largura, fc="white", ec="#455058"))
    for nome, rotulo, cor in equipamentos:
        pos, tam = volumes[nome]
        if nome == "portatil_bolsa_1":
            pos_final, tam_final = volumes["portatil_bolsa_4"]
            tam = pos_final + tam_final - pos
        plan.add_patch(Rectangle(pos[:2], *tam[:2], lw=.65, fc=cor, ec="#5a676a"))
        if rotulo:
            cx, cy = pos[:2] + tam[:2] / 2
            if nome == "cama_colchao":
                cx, cy = 1.65, 1.17
            plan.text(cx, cy, rotulo, fontsize=8, ha="center", va="center")
    # As superfícies se sobrepõem na projeção. Os números ocupam áreas visíveis
    # das peças e a chave identifica os equipamentos de menor dimensão.
    for number, (x, y) in enumerate([(.19,.90), (.43,1.06), (.73,.82), (1.30,1.38),
                                      (.77,1.47), (1.12,.95), (2.83,.21)], start=1):
        plan.text(x, y, str(number), ha="center", va="center", fontsize=7)
    fig.text(.5, .01, "1  Água limpa     2  Água cinza     3  Boiler     4  Bomba     "
             "5  Inversor     6  Ar-condicionado     7  Cooktop", ha="center", fontsize=8)
    plan.set(xlim=(-.03, comp+.03), ylim=(-.025, largura+.025), aspect="equal",
             xlabel="Distância à face interna traseira [m]", ylabel="Largura interna [m]")
    plan.set_xticks([0, 1, 2, 3, comp])
    plan.set_yticks([0, .6, 1.2, largura])
    fmt = FuncFormatter(lambda v, _: f"{v:.3f}".rstrip("0").rstrip(".").replace(".", ","))
    plan.xaxis.set_major_formatter(fmt)
    plan.yaxis.set_major_formatter(fmt)
    plan.set_title("Planta dos equipamentos · layout A", fontsize=11, pad=10)
    plan.grid(False)

    azul = "#235b7e"
    modulos = [volumes[n] for n in sorted(volumes) if n.startswith("US5000_")]
    topo = max(pos[2] + tamanho[2] for pos, tamanho in modulos)
    nivel_piso = cad.PISO_Z
    for i, (pos, tamanho) in enumerate(modulos, 1):
        elev.add_patch(Rectangle((.10, pos[2]), .44, tamanho[2], ec=azul, fc="#b8cfdd", lw=.8))
        elev.text(.32, pos[2] + tamanho[2]/2, f"US5000 · {i}", color="#133d56",
                  va="center", ha="center", fontsize=8)
    elev.add_patch(Rectangle((.10, 0), .44, cad.ARCO[2], ec="#5a676a", fc="#e2e5e5", lw=.65))
    elev.text(.32, cad.ARCO[2]/2, "Caixa de roda", va="center", ha="center", fontsize=8)
    elev.hlines([0, topo], [.04, .10], [.75, .75], colors="#48535b", linewidth=.85)
    elev.annotate("", (.70, topo), (.70, 0), arrowprops={"arrowstyle":"<->", "lw":1, "color":azul})
    metros = lambda z: f"{z:.3f}".replace(".", ",") + " m"
    elev.text(.76, topo/2, f"{metros(topo)}\nacima do piso", va="center", color=azul, fontsize=8.5)
    elev.text(.10, topo+.055, f"Topo do banco · {metros(nivel_piso+topo)} do solo", fontsize=9)
    elev.text(.10, -.11, f"Piso acabado · {metros(nivel_piso)} do solo", fontsize=9)
    elev.set(xlim=(0, 1.35), ylim=(-.18, 1.11), title="Níveis do banco de serviços")
    elev.axis("off")
    fig.savefig(OUT / "i17_layout_interno.png", dpi=210, bbox_inches="tight", pad_inches=.06)
    plt.close(fig)


def motor():
    """I04: envelope de torque/potência (picos OEM 410 N m, 205 kW) e mapa de eficiência de um
    modelo paramétrico de perdas calibrado para eta = 0,95 no ponto de canto. Não é mapa OEM."""
    t_max, p_max = 410.0, 205e3
    w_b = p_max / t_max                         # 500 rad/s
    rpm = np.linspace(1, 12000, 400)
    w = rpm * 2 * np.pi / 60
    torque = np.minimum(t_max, p_max / w)
    perda_canto = p_max * (1 / 0.95 - 1)
    kc, ki, km, p0 = (0.60 * perda_canto / t_max**2, 0.25 * perda_canto / w_b**1.5,
                      0.10 * perda_canto / w_b, 0.05 * perda_canto)
    W, T = np.meshgrid(w, np.linspace(1, t_max, 300))
    pm = T * W
    eta = pm / (pm + kc * T**2 + ki * W**1.5 + km * W + p0)
    eta[T > np.minimum(t_max, p_max / W)] = np.nan
    rpm90 = 25.0 / 0.361262 * 10 * 60 / (2 * np.pi)
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.4))
    ax = axs[0]
    ax.plot(rpm, torque, color=C["azul"], lw=2, label="torque máximo [N m]")
    ax.set(xlabel="rotação do motor [rpm]", ylabel="torque [N m]", ylim=(0, 450), xlim=(0, 12000))
    ax2 = ax.twinx()
    ax2.plot(rpm, torque * w / 1000, color=C["laranja"], lw=2, label="potência máxima [kW]")
    ax2.set_ylabel("potência [kW]"); ax2.set_ylim(0, 225); ax2.grid(False)
    ax.axvline(rpm90, color="k", ls=":", lw=1); ax.text(rpm90 + 100, 30, f"90 km/h\n(i = 10)\n{rpm90:.0f} rpm", fontsize=7)
    ax.axvline(w_b * 60 / (2 * np.pi), color=C["cinza"], ls="--", lw=0.8)
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="center right", fontsize=7)
    ax.set_title("Envelope de pico (dados OEM: 205 kW, 410 N m)", fontsize=9)
    cs = axs[1].contourf(W * 60 / (2 * np.pi), T, 100 * eta, levels=[70, 80, 85, 88, 90, 92, 93, 94, 95, 96, 97], cmap="viridis")
    axs[1].contour(W * 60 / (2 * np.pi), T, 100 * eta, levels=[90, 94, 96], colors="w", linewidths=0.6)
    axs[1].plot(rpm, torque, color="k", lw=1)
    axs[1].set(xlabel="rotação do motor [rpm]", ylabel="torque [N m]", xlim=(0, 12000))
    axs[1].set_title("Eficiência — modelo paramétrico de perdas (não OEM)", fontsize=9)
    fig.colorbar(cs, ax=axs[1], label="η motor [%]")
    salvar(fig, "i04_motor.png")
    return {"eta_max_modelo": float(np.nanmax(eta)), "rpm_base": float(w_b * 60 / (2 * np.pi)), "rpm_90kmh_i10": rpm90}



def freios_integrados():
    """I33: campos e históricos da mesma massa usada no texto atual."""
    mass = json.loads((E / "integracao/layouts_massas.json").read_text())["layouts"]["A_fixa"]["nominal"]["mass_kg"]
    pasta = E / "freios_integrados"
    field = np.load(pasta / f"campo_{mass:.3f}kg_regen0kw.npz")
    fig, ax = plt.subplots(figsize=(5.8, 3.3))
    im = ax.pcolormesh(field["r_m"]*1000, field["z_m"]*1000, field["temperature_k"].T-273.15,
                       shading="nearest", cmap="inferno")
    fig.colorbar(im, ax=ax, label="temperatura [°C]")
    ax.set(xlabel="raio [mm]", ylabel="espessura z [mm]", title=f"Massa nominal {mass:.1f} kg; sem regeneração")
    salvar(fig, "i33_campo.png")
    fig, ax = plt.subplots(figsize=(5.8, 3.3))
    for m, regen, label in [(mass,0,"nominal, sem regeneração"), (mass,40,"nominal, regeneração 40 kW"),
                            (mass,80,"nominal, regeneração 80 kW"), (4250,0,"PBT, sem regeneração")]:
        rows = ler(pasta / f"temperatura_tempo_{m:.3f}kg_regen{regen}kw.csv")
        ax.plot(col(rows,"tempo_s"), col(rows,"tmax_superficie_k")-273.15, label=label)
    ax.set(xlabel="tempo [s]", ylabel="pico superficial [°C]", xlim=(0,5))
    ax.legend(fontsize=7)
    salvar(fig, "i33_historico.png")

COPIAS = {
    "i24_custo.png": E / "i24_custo_brl/custo_por_grupo.png",
    "i30_cabos.png": E / "i30_corrente_maxima/campo_corrente_maxima.png",
    "i31_cabine.png": ROOT / "entregas/desenvolvimento_2026-11-09/cabine_transiente/campo_temperatura_velocidade.png",
    "i34_bateria.png": ROOT / "equipe/P7_arrefecimento/I34_temperatura_da_bateria_em_carga/resultados/carga_bateria.png",
    "i35_radiador.png": ROOT / "equipe/P7_arrefecimento/I35_bomba_radiador_e_vazao/resultados/hidraulica_campos_equilibrio.png",
    "i35_ponto_operacao.png": ROOT / "entregas/desenvolvimento_2026-11-09/arrefecimento/ponto_operacao.png",
    "i19_gci.png": ROOT / "entregas/aero_equipado1540/familia_gci/gci_cd.png",
    "i29_missao.png": E / "i29_fechamento/missao_lider.png",
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for f in (solar, dinamica, autonomia_solar, i27, i28, vistas_exterior, vistas_layout, freios_integrados):
        f()
    print(json.dumps(motor()))
    faltando = []
    for nome, origem in COPIAS.items():
        if origem.exists():
            shutil.copy2(origem, OUT / nome)
        else:
            faltando.append(str(origem.relative_to(ROOT)))
    print(json.dumps({"figuras": sorted(p.name for p in OUT.glob("*.png")), "faltando": faltando}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
