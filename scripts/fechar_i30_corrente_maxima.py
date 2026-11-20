"""I30: temperatura do cabo de alimentação do motor na potência máxima.

Revisão de 2026-11-20: o contorno térmico deixou de ser "cabo isolado em ar parado
a 25 °C com radiação plena". Passa a cobrir ar e entorno radiativo distintos,
confinamento em conduíte, agrupamento das três fases e perdas AC, além do regime
transitório no pico. O solver r–θ (`motorhome.cabos_polares`) não foi alterado.

O contorno "referencia_antiga" reproduz exatamente o resultado anterior
(85,37 °C em 1×120 mm² a 489 A) e serve de regressão.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import yaml
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from motorhome.cabo_hv import (
    CondicoesContorno,
    resolver_estacionario,
    resolver_transiente,
)
from motorhome.cabos_polares import Cabo


def _cabo_de_bitola(bitola, modelo):
    """Cabo a partir da tabela canônica `development.cable_hv`."""
    return Cabo(bitola["condutor_mm"] / 2000, bitola["externo_mm"] / 2000,
                modelo["bundle_k_assumed_w_mk"], modelo["insulation_k_assumed_w_mk"],
                bitola["r20_ohm_km"] / 1000, modelo["alpha_assumed_per_k"],
                modelo["reference_k"])


def _corrente_fase(potencia_w, eta, pf, v_dc):
    """I_fase a partir do limite de modulação linear SVPWM: V_LL,rms = V_dc/sqrt(2)."""
    return potencia_w / (eta * np.sqrt(3) * v_dc / np.sqrt(2) * pf)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "config/cabos_tracao_proposta.yaml")
    parser.add_argument("--destino", type=Path,
                        default=ROOT / "entregas/integrado_maxeon1540/i30_corrente_maxima")
    args = parser.parse_args()
    modelo = yaml.safe_load(args.config.read_text())["model"]
    globais = yaml.safe_load((ROOT / "config/parametros_globais.yaml").read_text())
    params = {k: v["value"] for k, v in globais["parameters"].items()}
    cabos_cfg = globais["development"]["cable_hv"]
    p_mech = params["motor_peak_kw"] * 1000
    v_dc_nom = params["traction_voltage_v"]
    modo_normal_w = params["motor_mode_power_kw"]["normal"] * 1000

    bitolas = {b["area_mm2"]: _cabo_de_bitola(b, modelo) for b in cabos_cfg["bitolas"]}
    nominal = {"eta": 0.95, "pf": 0.90, "vdc": v_dc_nom}
    i_pico = _corrente_fase(p_mech, nominal["eta"], nominal["pf"], nominal["vdc"])
    i_normal = _corrente_fase(modo_normal_w, nominal["eta"], nominal["pf"], nominal["vdc"])

    contornos = {
        "referencia_antiga": CondicoesContorno(**cabos_cfg["contorno_referencia_antiga"]),
        "rota_protegida": CondicoesContorno(**cabos_cfg["contorno_rota_protegida"]),
        "hot_spot": CondicoesContorno(**cabos_cfg["contorno_projeto"]),
    }

    # 1) Matriz contorno × bitola × ponto de operação.
    rows = []
    for (nome_contorno, contorno), area, potencia in itertools.product(
            contornos.items(), bitolas, (modo_normal_w, p_mech)):
        corrente = _corrente_fase(potencia, nominal["eta"], nominal["pf"], nominal["vdc"])
        r = resolver_estacionario(bitolas[area], corrente, contorno)
        rows.append({"contorno": nome_contorno, "potencia_w": potencia, "corrente_a": corrente,
                     "area_mm2": area,
                     "temperatura_max_c": r["temperatura_max_k"] - 273.15,
                     "temperatura_superficie_c": r["temperatura_superficie_k"] - 273.15,
                     "h_conveccao_w_m2k": r["h_conveccao_w_m2k"],
                     "h_radiacao_w_m2k": r["h_radiacao_w_m2k"],
                     "joule_w_m": r["joule_w_m"], "removido_w_m": r["removido_w_m"],
                     "residuo_w_m": r["residuo_w_m"],
                     "acima_125c": r["temperatura_max_k"] > cabos_cfg["t_max_projeto_c"] + 273.15,
                     "acima_150c": r["temperatura_max_k"] > cabos_cfg["t_falha_c"] + 273.15})

    # 2) Corrente máxima para o critério de projeto em cada contorno.
    def temperatura(area, corrente, contorno):
        """Temperatura máxima; fuga térmica (sem solução física) conta como exceder."""
        try:
            return resolver_estacionario(bitolas[area], corrente, contorno, nr=24, nt=96)[
                "temperatura_max_k"] - 273.15
        except (ValueError, RuntimeError):
            return 1e5

    t_limite = cabos_cfg["t_max_projeto_c"]
    limites = []
    for nome_contorno, contorno in contornos.items():
        for area in bitolas:
            def excesso(corrente, area=area, contorno=contorno):
                return temperatura(area, corrente, contorno) - t_limite
            if excesso(5.0) > 0:
                imax = 0.0
            elif excesso(900.0) < 0:
                imax = 900.0
            else:
                imax = brentq(excesso, 5.0, 900.0, xtol=1.0)
            limites.append({"contorno": nome_contorno, "area_mm2": area,
                            "corrente_max_125c_a": imax,
                            "potencia_equivalente_kw": imax * (nominal["eta"] * np.sqrt(3)
                                                               * nominal["vdc"] / np.sqrt(2)
                                                               * nominal["pf"]) / 1000})

    # 3) Transitório: pico de 205 kW partindo do regime normal.
    transitorio = []
    for nome_contorno, contorno in contornos.items():
        for area, cabo in bitolas.items():
            tr = resolver_transiente(cabo, i_normal, i_pico, contorno,
                                     duracao_pico_s=180.0,
                                     t_limite_k=cabos_cfg["t_max_projeto_c"] + 273.15,
                                     passo_s=2.0)
            hist = dict(tr["historico"])
            transitorio.append({"contorno": nome_contorno, "area_mm2": area,
                                "temperatura_regime_c": tr["temperatura_regime_k"] - 273.15,
                                "tau_s": tr["tau_s"],
                                "temperatura_apos_60s_c": hist[60.0] - 273.15,
                                "temperatura_apos_180s_c": hist[180.0] - 273.15,
                                "duracao_maxima_admissivel_s": tr["duracao_maxima_admissivel_s"]})

    # 4) Decisão: menor bitola que atende no ponto de projeto.
    def atende(contorno, area):
        return not next(r for r in rows if r["contorno"] == contorno
                        and r["area_mm2"] == area
                        and r["potencia_w"] == modo_normal_w)["acima_125c"]

    bitola_minima = next((a for a in sorted(bitolas) if atende("hot_spot", a)), None)
    bitola_rota = next((a for a in sorted(bitolas) if atende("rota_protegida", a)), None)

    args.destino.mkdir(parents=True, exist_ok=True)
    for nome, dados in (("sensibilidade.csv", rows), ("limites_bitola.csv", limites),
                         ("transitorio_pico.csv", transitorio)):
        with (args.destino / nome).open("w", newline="") as f:
            w = csv.DictWriter(f, list(dados[0]), lineterminator="\n")
            w.writeheader()
            w.writerows(dados)

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4), layout="constrained")
    for ax, potencia, titulo in (
            (axes[0], modo_normal_w,
             f"Modo normal ({modo_normal_w/1000:.0f} kW, {i_normal:.0f} A)"),
            (axes[1], p_mech,
             f"Pico em regime permanente ({p_mech/1000:.0f} kW, {i_pico:.0f} A)")):
        for nome_contorno, estilo in zip(contornos, ("o-", "s-", "^-"), strict=True):
            sel = [r for r in rows if r["contorno"] == nome_contorno
                   and r["potencia_w"] == potencia]
            ax.plot([r["area_mm2"] for r in sel], [r["temperatura_max_c"] for r in sel],
                    estilo, label=nome_contorno)
        ax.axhline(cabos_cfg["t_max_projeto_c"], ls="--", c="k", lw=0.8)
        ax.axhline(cabos_cfg["t_falha_c"], ls=":", c="r", lw=0.8)
        ax.set(xlabel="bitola [mm²]", ylabel="temperatura máxima [°C]", title=titulo)
        ax.grid(alpha=.25); ax.legend(fontsize=8)
    axes[0].text(0.3, cabos_cfg["t_max_projeto_c"]+2, "critério 125 °C", fontsize=8)
    axes[0].text(0.3, cabos_cfg["t_falha_c"]+2, "ficha RADOX 150 °C (3000 h)", fontsize=8)
    fig.savefig(args.destino / "campo_corrente_maxima.png", dpi=150)
    plt.close(fig)

    resumo = {
        "script": "scripts/fechar_i30_corrente_maxima.py",
        "revisao": "2026-11-20-contorno-completo",
        "method": "I_fase = P/(eta*sqrt(3)*V_LL*FP), V_LL,rms = V_dc/sqrt(2) (limite SVPWM linear); "
                  "campo r-theta por volumes finitos; contorno = Churchill-Chu + radiação com sink "
                  "distinto + conduíte + agrupamento de fases + fator de perda AC; transitório por "
                  "capacidade concentrada calibrada no estacionário",
        "motor_peak_mechanical_w": p_mech, "motor_normal_mechanical_w": modo_normal_w,
        "nominal": {**nominal, "corrente_normal_a": i_normal, "corrente_pico_a": i_pico},
        "regressao_referencia_antiga_c": {
            area: next(r for r in rows if r["contorno"] == "referencia_antiga"
                       and r["area_mm2"] == area
                       and r["potencia_w"] == p_mech)["temperatura_max_c"]
            for area in bitolas},
        "temperatura_modo_normal_c": {
            contorno: {area: next(r for r in rows if r["contorno"] == contorno
                                  and r["area_mm2"] == area
                                  and r["potencia_w"] == modo_normal_w)["temperatura_max_c"]
                       for area in bitolas} for contorno in contornos},
        "temperatura_100_pct_pico_c": {
            contorno: {area: next(r for r in rows if r["contorno"] == contorno
                                  and r["area_mm2"] == area
                                  and r["potencia_w"] == p_mech)["temperatura_max_c"]
                       for area in bitolas} for contorno in contornos},
        "limites_125c": limites,
        "transitorio": transitorio,
        "criterio": {
            "t_max_projeto_c": cabos_cfg["t_max_projeto_c"],
            "t_falha_c": cabos_cfg["t_falha_c"],
            "corrente_projeto": "modo normal",
            "bitola_minima_hot_spot_mm2": bitola_minima,
            "bitola_minima_rota_protegida_mm2": bitola_rota,
            "bitola_referencia_config_mm2": cabos_cfg["bitola_referencia_mm2"],
        },
        "max_abs_residuo_w_m": max(abs(r["residuo_w_m"]) for r in rows),
        "limits": [
            ("Bitolas 185/240 são derivadas por geometria calibrada nos pontos de catálogo "
             "(erro <1%); exigem confirmação na ficha do fabricante antes de qualquer compra."),
            ("Convecção/conduíte/fator de forma/agrupamento são hipóteses explicitadas em "
             "config/parametros_globais.yaml (development.cable_hv); não são medições."),
            "Perda AC entra como corrente equivalente; efeito pelicular não é resolvido.",
            "Não há condução axial, terminais/contatos, chicote completo nem EMC.",
            ("Nenhuma modificação física do chicote HV OEM é autorizada (DEC-001/DEC-040): o "
             "resultado é requisito de verificação e, se não comprovado, limite de potência contínua."),
        ],
    }
    (args.destino / "resumo.json").write_text(
        json.dumps(resumo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"normal": resumo["temperatura_modo_normal_c"],
                      "criterio": resumo["criterio"]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
