"""Envelope quase estático de transferência longitudinal para a grade massa/CG.

Não modela ABS, suspensão, pneus, aerodinâmica, transientes ou aprovação OEM.
Os limites comparativos são mantidos como referências de triagem separadas.
"""

import csv
import json
from math import isfinite
from pathlib import Path
from statistics import median

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import yaml

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "entregas/integrado_maxeon1540/integracao/massa_cg_eixos_sensibilidade.csv"
OUT = ROOT / "entregas/integrado_maxeon1540/integracao/envelope_frenagem_eixos"
G = 9.80665
DECEL_G = (0.0, 0.1, 0.2, 0.3, 0.4, 0.5)
# UK MY25.5 L3 comparator; not established for the studied Slovakia MY25 van.
AXLE_COMPARATOR_KG = {"front": 2100.0, "rear": 2400.0}


def loads_under_braking(mass_kg: float, cg_x_m: float, cg_z_m: float,
                        wheelbase_m: float, deceleration_g: float) -> tuple[float, float, float]:
    """Return front/rear reactions and transfer for level-ground quasi-static braking."""
    values = (mass_kg, cg_x_m, cg_z_m, wheelbase_m, deceleration_g)
    if any(not isfinite(value) for value in values):
        raise ValueError("Inputs must be finite")
    if any(value < 0 for value in values) or mass_kg == 0 or wheelbase_m == 0 or cg_z_m == 0:
        raise ValueError("Mass, wheelbase and CG height must be positive; other inputs nonnegative")
    if cg_x_m == 0 or cg_x_m >= wheelbase_m:
        raise ValueError("Longitudinal CG must lie between axles")
    # deceleration_g is already normalized by g; reactions are mass-equivalent kg.
    transfer = mass_kg * deceleration_g * cg_z_m / wheelbase_m
    front = mass_kg * (wheelbase_m - cg_x_m) / wheelbase_m + transfer
    return front, mass_kg - front, transfer


def main() -> None:
    params = yaml.safe_load((ROOT / "config/parametros_globais.yaml").read_text(encoding="utf-8"))
    wheelbase = float(params["parameters"]["wheelbase_m"]["value"])
    with INPUT.open(newline="", encoding="utf-8") as stream:
        source_rows = list(csv.DictReader(stream))
    if len(source_rows) != 162:
        raise ValueError(f"Expected 162 mass/CG cases; found {len(source_rows)}")

    rows: list[dict[str, object]] = []
    for source in source_rows:
        mass = float(source["mass_kg"])
        cg_x = float(source["cg_x_m"])
        cg_z = float(source["cg_z_m"])
        if mass <= 0 or not 0 < cg_x < wheelbase or cg_z <= 0:
            raise ValueError(f"Invalid mass/CG case: {source}")
        for decel_g in DECEL_G:
            front, rear, transfer = loads_under_braking(mass, cg_x, cg_z, wheelbase, decel_g)
            rows.append({
                "layout": source["layout"],
                "estimated_mass_factor": source["estimated_mass_factor"],
                "oem_rear_fraction_assumed": source["oem_rear_fraction_assumed"],
                "oem_cg_height_assumed_m": source["oem_cg_height_assumed_m"],
                "water_clean_grey_black_l": source["water_clean_grey_black_l"],
                "mass_kg": mass,
                "cg_x_m": cg_x,
                "cg_z_m": cg_z,
                "deceleration_g": decel_g,
                "load_transfer_to_front_kg": transfer,
                "front_dynamic_kg": front,
                "rear_dynamic_kg": rear,
                "axle_sum_error_kg": front + rear - mass,
                "front_over_2100_comparator": front > AXLE_COMPARATOR_KG["front"],
                "rear_over_2400_comparator": rear > AXLE_COMPARATOR_KG["rear"],
                "pbt_margin_kg": 4250.0 - mass,
            })

    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (OUT / "casos.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    by_deceleration = {}
    for decel_g in DECEL_G:
        subset = [row for row in rows if row["deceleration_g"] == decel_g]
        by_deceleration[str(decel_g)] = {
            "cases": len(subset),
            "front_load_range_kg": [min(r["front_dynamic_kg"] for r in subset), max(r["front_dynamic_kg"] for r in subset)],
            "rear_load_range_kg": [min(r["rear_dynamic_kg"] for r in subset), max(r["rear_dynamic_kg"] for r in subset)],
            "above_front_comparator_cases": sum(bool(r["front_over_2100_comparator"]) for r in subset),
            "above_rear_comparator_cases": sum(bool(r["rear_over_2400_comparator"]) for r in subset),
            "max_abs_axle_sum_error_kg": max(abs(float(r["axle_sum_error_kg"])) for r in subset),
        }
    summary = {
        "method": "quasi_static_longitudinal_load_transfer; level_ground; no suspension or tire dynamics",
        "source_cases": len(source_rows),
        "cases": len(rows),
        "wheelbase_m": wheelbase,
        "deceleration_grid_g": DECEL_G,
        "equation_transfer_kg": "mass_kg * deceleration_g * cg_z_m / wheelbase_m; deceleration_g is a multiple of g",
        "axle_rating_comparators_kg": AXLE_COMPARATOR_KG,
        "comparator_scope": "UK MY25.5 L3 listing only; not verified for studied Slovakia MY25 vehicle",
        "physical_validation": False,
        "oem_compliance": "indeterminate; exact variant axle limits and dynamic brake data unavailable",
        "by_deceleration": by_deceleration,
    }
    (OUT / "resumo.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.8), sharex=True, sharey=True, layout="constrained")
    for ax, column, color, title, comparator, comparator_label in (
        (axes[0], "front_dynamic_kg", "#4C72B0", "Eixo dianteiro", 2100.0, "Comparador estático publicado: 2.100 kg"),
        (axes[1], "rear_dynamic_kg", "#DD8452", "Eixo traseiro", 2400.0, "Comparador estático publicado: 2.400 kg"),
    ):
        medians, lows, highs = [], [], []
        for decel_g in DECEL_G:
            values = [float(r[column]) for r in rows if r["deceleration_g"] == decel_g]
            medians.append(median(values))
            lows.append(min(values))
            highs.append(max(values))
        ax.fill_between(DECEL_G, lows, highs, color=color, alpha=0.18, linewidth=0,
                        label="Faixa dos 162 casos")
        ax.plot(DECEL_G, medians, color=color, marker="o", linewidth=2,
                label="Mediana dos casos")
        ax.axhline(comparator, color="#222222", linestyle="--", linewidth=1.3,
                   label=comparator_label)
        ax.set_title(title)
        ax.set_xlabel("Desaceleração assumida [g]")
        ax.set_xticks(DECEL_G)
        ax.grid(axis="y", alpha=0.25)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.legend(frameon=False, fontsize=7.5, loc="best")
    axes[0].set_ylabel("Reação normal equivalente [kg]")
    fig.suptitle("Transferência longitudinal: envelope quase estático, não homologação", fontsize=12, weight="bold")
    fig.text(0.5, -0.015,
             "Piso nivelado; CG/massas hipotéticos. Linhas tracejadas são comparadores estáticos de UK/Polônia, não limites dinâmicos nem da variante SK MY25.",
             ha="center", fontsize=8)
    fig.savefig(OUT / "envelope_frenagem.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(json.dumps({"cases": len(rows), "deceleration_levels": len(DECEL_G),
                      "plot": str((OUT / "envelope_frenagem.png").relative_to(ROOT))}, ensure_ascii=False))


if __name__ == "__main__":
    main()
