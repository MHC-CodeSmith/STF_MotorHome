"""Item 19. Recalcula os extremos observados na família de malhas equipada.

Lê o histórico de forças, o y+ por superfície e os registros SIMPLE originais.
A área de referência é a declarada em forceCoeffs para ambas as superfícies.
O nome de arquivo histórico é mantido para quem já chama este script.
"""
import json
import math
import re
from statistics import fmean
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
FAMILIA = ROOT / "entregas/aero_equipado1540/familia_gci"
MALHAS = ("bg_55x20x10", "bg_44x16x8", "bg_33x12x6")  # Fina a grossa
NOMES = ("Fina", "Intermediária", "Grossa")
VOLUME = 55.0 * 20.0 * 10.0  # m³


def ler_caso(diretorio):
    dados = json.loads((diretorio / "resumo.json").read_text(encoding="utf-8"))
    if not dados.get("mesh_ok") or dados.get("solver_exit") != 0:
        raise ValueError(f"{diretorio.name}: verificar malha ou execução")
    log = (diretorio / "case/log.snappyHexMesh").read_text(errors="replace")
    if "reached limit" in log:
        raise ValueError(f"{diretorio.name}: refinamento atingiu o limite")
    case = diretorio / "case"
    check = (case / "log.checkMesh").read_text()
    n = int(re.search(r"^\s*cells:\s*(\d+)", check, re.M)[1])
    if "Mesh OK." not in check or n != dados["cell_count"]:
        raise ValueError(f"{diretorio.name}: contagem ou verificação da malha divergente")
    controle = (case / "system/controlDict").read_text()
    area = float(re.search(r"\bAref\s+([^;]+);", controle)[1])
    log_solver = (case / "log.simpleFoam").read_text()
    final = re.search(r"SIMPLE solution converged in (\d+) iterations", log_solver)
    if final is None or dados.get("solver_converged") is not True:
        raise ValueError(f"{diretorio.name}: convergência iterativa não confirmada")
    iteracao = int(final[1])
    arquivo = case / "postProcessing/forces1/0/coefficient.dat"
    tempos, historico = np.loadtxt(arquivo, usecols=(0, 1), unpack=True)
    if tempos[-1] != iteracao or len(historico) < 50 or not np.isfinite(historico).all():
        raise ValueError(f"{diretorio.name}: histórico de forças inválido")
    cd = float(historico[-1])
    if not math.isclose(cd, dados["last_cd_diagnostic"], rel_tol=1e-7):
        raise ValueError(f"{diretorio.name}: Cd do resumo diverge do histórico")
    fim = historico[-50:]
    span = float((max(fim) - min(fim)) / abs(fmean(fim)))
    yplus = {}
    for linha in (case / "postProcessing/yPlus/0/yPlus.dat").read_text().splitlines():
        if not linha.strip() or linha.startswith("#"):
            continue
        tempo, regiao, minimo, maximo, media = linha.split()
        if float(tempo) == iteracao:
            yplus[regiao] = [float(minimo), float(maximo), float(media)]
    if set(yplus) != {"ground", "aurora", "pvdeck"}:
        raise ValueError(f"{diretorio.name}: y+ ausente no último passo")
    return {"caso": diretorio.name, "celulas": n, "h_m": (VOLUME / n)**(1/3),
            "cd": cd, "area_ref_m2": area, "convergiu": True, "iteracoes": iteracao,
            "cd_span_50it": span, "yplus": yplus}


def comparar(casos, cd_energia):
    h1, h2, h3 = (c["h_m"] for c in casos)
    if not h1 < h2 < h3:
        raise ValueError("Ordem esperada: malha fina, intermediária e grossa")
    cd1, cd2, cd3 = (c["cd"] for c in casos)
    area = casos[0]["area_ref_m2"]
    if any(c["area_ref_m2"] != area for c in casos):
        raise ValueError("Os três coeficientes devem usar a mesma área de referência")
    delta21, delta32 = cd2 - cd1, cd3 - cd2
    razao = delta21 / delta32 if delta32 else None
    return {"script": "scripts/calcular_gci_aero.py", "casos": casos,
            "cenario": "maxeon1540_independente", "cd_fina": cd1, "cd_min": min(cd1, cd2, cd3),
            "cd_max": max(cd1, cd2, cd3), "cda_m2": cd1 * area, "area_ref_m2": area,
            "r21": h2 / h1, "r32": h3 / h2, "razao_convergencia_R": razao,
            "oscilatoria": razao is not None and razao < 0,
            "incerteza_absoluta_cd": None, "incerteza_relativa_cd": None,
            "cd_modelos_energia": cd_energia,
            "diferenca_relativa_modelos_energia": (cd_energia - cd1) / cd1,
            "physical_validation": False,
            "method": "Extremos observados nos três Cd finais; incerteza de malha não estimada"}


def gerar_figura(resumo, arquivo):
    casos = resumo["casos"]
    fig, ax = plt.subplots(figsize=(6.05, 2.95))
    fig.subplots_adjust(left=0.12, right=0.985, bottom=0.20, top=0.94)
    ax.axhspan(resumo["cd_min"], resumo["cd_max"], color="#4987b9", alpha=0.15,
               label="Faixa observada nas três malhas")
    cd_energia = resumo["cd_modelos_energia"]
    rotulo = f"Modelos de energia ({cd_energia:.3f})".replace(".", ",")
    ax.axhline(cd_energia, color="#ad501e", linestyle="--", linewidth=1, label=rotulo)
    ax.plot([c["h_m"] for c in casos], [c["cd"] for c in casos], "o-",
            color="#1b5791", linewidth=1, markersize=4.6)
    for c, nome in zip(casos, NOMES):
        ax.annotate(nome, (c["h_m"], c["cd"]), xytext=(0, 6),
                    textcoords="offset points", ha="center", fontsize=8)
    ax.margins(x=0.16, y=0.48)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.2f}".replace(".", ",")))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:.3f}".replace(".", ",")))
    ax.tick_params(labelsize=7.5)
    ax.set_xlabel(r"Tamanho representativo da célula, $h$ [m]", fontsize=9)
    ax.set_ylabel(r"Coeficiente de arrasto, $C_d$", fontsize=9)
    ax.grid(axis="y", linewidth=0.5, alpha=0.35)
    ax.legend(loc="lower center", ncol=2, fontsize=7, frameon=False)
    fig.savefig(arquivo, dpi=180)
    plt.close(fig)


def tex(resumo):
    def numero(valor, casas=4):
        return rf"\num{{{valor:.{casas}f}}}"
    faixa = numero(resumo["cd_min"]) + " a " + numero(resumo["cd_max"])
    razao = resumo["razao_convergencia_R"]
    linhas = [r"\begin{table}[H]\centering\small",
              r"\caption{Item 19 --- coeficiente de arrasto na família final de três malhas.}",
              r"\begin{tabular}{llrrr}\toprule",
              r"Malha & Malha de fundo & Células & $h$ [m] & $C_d$ \\ \midrule"]
    for nome, c in zip(NOMES, resumo["casos"]):
        fundo = c["caso"].removeprefix("bg_").replace("x", r"$\times$")
        linha = [nome, fundo, numero(c["celulas"], 0), numero(c["h_m"]), numero(c["cd"], 6)]
        linhas.append(" & ".join(linha) + r" \\")
    linhas.append(r"\bottomrule\end{tabular}\end{table}")
    return "\n".join([
        r"\newcommand{\CdValor}{" + numero(resumo["cd_fina"]) + "}",
        r"\newcommand{\CdFaixa}{" + faixa + "}",
        r"\newcommand{\CdGCI}{\textnormal{GCI indeterminado}}",  # Uso legado
        r"\newcommand{\CdA}{" + rf"\SI{{{resumo['cda_m2']:.2f}}}{{m^2}}" + "}",
        r"\newcommand{\CdOscilatoria}{" + str(int(razao is not None and razao < 0)) + "}",
        r"\newcommand{\GCItabela}{" + "\n".join(linhas) + "}",
    ]) + "\n"


def main():
    config = yaml.safe_load((ROOT / "config/parametros_globais.yaml").read_text())
    cd_energia = config["parameters"]["cd_range"]["value"][1]
    resumo = comparar([ler_caso(FAMILIA / nome) for nome in MALHAS], cd_energia)
    texto = json.dumps(resumo, ensure_ascii=False, indent=2, allow_nan=False)
    (FAMILIA / "resumo_gci.json").write_text(texto + "\n", encoding="utf-8")
    gerar_figura(resumo, FAMILIA / "gci_cd.png")
    (ROOT / "relatorio/valores_i19.tex").write_text(tex(resumo), encoding="utf-8")


if __name__ == "__main__":
    main()
