"""I24: total material cost in BRL including Brazilian import taxes.

Reads config/custos_brl_i24.yaml (public list/retail prices with URLs and an
access date). Imported lines go through the import cascade (CIF, II, IPI,
PIS/COFINS-Importação, ICMS grossed up); domestic retail prices already carry
taxes and are summed as published. Lines marked as estimates carry a declared
low/nominal/high range. The result is a reference budget, not a quotation.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import yaml

ROOT = Path(__file__).resolve().parents[1]
CASES = ("baixo", "nominal", "alto")


def escolher(valor, k: int):
    return valor[k] if isinstance(valor, list) else valor


def importar(cif: float, ii: float, ipi: float, t: dict) -> dict:
    tax_ii = ii * cif
    tax_ipi = ipi * (cif + tax_ii)
    pis, cofins = t["pis"] * cif, t["cofins"] * cif
    base = cif + tax_ii + tax_ipi + pis + cofins
    icms = t["icms"] / (1 - t["icms"]) * base
    return {"cif": cif, "ii": tax_ii, "ipi": tax_ipi, "pis": pis, "cofins": cofins, "icms": icms,
            "total": base + icms}


def main() -> None:
    cfg = yaml.safe_load((ROOT / "config/custos_brl_i24.yaml").read_text())
    fx = {"BRL": 1.0, "USD": cfg["cambio"]["usd_brl"]["value"], "EUR": cfg["cambio"]["eur_brl"]["value"]}
    trib = cfg["tributos_importacao"]
    rows, totals = [], {c: 0.0 for c in CASES}
    for item in cfg["itens"]:
        for k, case in enumerate(CASES):
            if "faixa" in item:
                fob = item["faixa"][k] * item["qtd"]
            else:
                fob = item["preco"] * item["qtd"] * fx[item["moeda"]]
            line = {"id": item["id"], "caso": case, "descricao": item["descricao"], "qtd": item["qtd"],
                    "moeda": item["moeda"], "valor_origem_brl": fob, "fonte": item["fonte"]}
            if item["importado"]:
                rule = trib[item["importado"]]
                tax = importar(fob * (1 + trib["frete_seguro"][k]), escolher(rule["ii"], k), escolher(rule["ipi"], k), trib)
                line.update({f"{n}_brl": v for n, v in tax.items()})
                line["total_brl"] = tax["total"]
            else:
                line["total_brl"] = fob
            totals[case] += line["total_brl"]
            rows.append(line)

    out = ROOT / "entregas/integrado_maxeon1560/i24_custo_brl"
    out.mkdir(parents=True, exist_ok=True)
    fields = ["id", "caso", "descricao", "qtd", "moeda", "valor_origem_brl", "cif_brl", "ii_brl", "ipi_brl",
              "pis_brl", "cofins_brl", "icms_brl", "total_brl", "fonte"]
    with (out / "custo_por_linha.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fields, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    nominal = [r for r in rows if r["caso"] == "nominal"]
    veic = next(r for r in nominal if r["id"] == "veiculo")
    tributos = sum(r.get(k, 0.0) for r in nominal for k in ("ii_brl", "ipi_brl", "pis_brl", "cofins_brl", "icms_brl"))
    resumo = {
        "script": "scripts/calcular_custo_brl_i24.py", "config": "config/custos_brl_i24.yaml",
        "cambio": {k: v for k, v in cfg["cambio"].items()},
        "total_brl": totals,
        "nominal_veiculo_importado_brl": veic["total_brl"],
        "nominal_conversao_brl": totals["nominal"] - veic["total_brl"],
        "nominal_tributos_importacao_brl": tributos,
        "is_quotation": False,
        "limits": ["Preços de lista/varejo públicos, não cotação; IVA europeu não deduzido dos preços de varejo (conservador).",
                   "II/IPI de componentes por faixa declarada; NCM não classificada item a item.",
                   "Linhas de estimativa (isolamento, marcenaria, elétrica/hidráulica, montagem) são faixas, não preços."],
    }
    (out / "resumo.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    groups = {}
    for r in nominal:
        g = "Veículo base importado" if r["id"] == "veiculo" else ("Sistema solar e baterias" if r["id"] in (
            "modulos_maxeon", "bateria_servicos", "inversor_servicos", "mppt_teto", "mppt_portateis", "pv_portatil")
            else "Interior, conforto e montagem")
        groups[g] = groups.get(g, 0.0) + r["total_brl"]
    fig, ax = plt.subplots(figsize=(7, 3))
    names = list(groups)
    ax.barh(names, [groups[n] / 1000 for n in names], color=["#4c6ef5", "#f08c00", "#2b8a3e"])
    for i, n in enumerate(names):
        ax.text(groups[n] / 1000, i, f" {groups[n] / 1000:,.0f} mil".replace(",", "."), va="center", fontsize=9)
    ax.set_xlabel("custo nominal com impostos [mil R$]")
    ax.set_title(f"I24 — total nominal R$ {totals['nominal'] / 1000:,.0f} mil".replace(",", "."))
    ax.set_xlim(0, max(groups.values()) / 1000 * 1.25)
    fig.tight_layout()
    fig.savefig(out / "custo_por_grupo.png", dpi=150)
    print(json.dumps({k: resumo[k] for k in ("total_brl", "nominal_veiculo_importado_brl", "nominal_conversao_brl",
                                              "nominal_tributos_importacao_brl")}, indent=1))


if __name__ == "__main__":
    main()
