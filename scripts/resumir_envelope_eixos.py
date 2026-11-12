"""Summarize the existing full-factorial axle/CG sensitivity grid.

This is a deterministic envelope over explicitly enumerated study assumptions,
not a probability model and not an OEM axle-load compliance check.
"""

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "entregas/integrado_maxeon1540/integracao/massa_cg_eixos_sensibilidade.csv"
OUT = ROOT / "entregas/integrado_maxeon1540/integracao/envelope_cargas_eixos"
FACTORS = (
    "estimated_mass_factor",
    "oem_rear_fraction_assumed",
    "oem_cg_height_assumed_m",
    "water_clean_grey_black_l",
)
METRICS = (
    "mass_kg",
    "cg_x_m",
    "cg_y_m",
    "cg_z_m",
    "front_kg",
    "rear_kg",
    "pbt_margin_kg",
    "geometric_ay_g",
)


def load_rows() -> list[dict[str, str]]:
    with INPUT.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    expected = 2 * 3**4
    if len(rows) != expected:
        raise ValueError(f"Esperadas {expected} combinações fatoriais; encontradas {len(rows)}")
    return rows


def main_effect_shares(rows: list[dict[str, str]], metric: str) -> dict[str, float]:
    """Balanced-grid main-effect variance shares; interactions remain pooled."""
    values = [float(row[metric]) for row in rows]
    mean = sum(values) / len(values)
    total_ss = sum((value - mean) ** 2 for value in values)
    if total_ss == 0:
        return {factor: 0.0 for factor in ("layout", *FACTORS)}
    shares: dict[str, float] = {}
    for factor in ("layout", *FACTORS):
        grouped: dict[str, list[float]] = defaultdict(list)
        for row in rows:
            grouped[row[factor]].append(float(row[metric]))
        ss = sum(len(group) * (sum(group) / len(group) - mean) ** 2 for group in grouped.values())
        shares[factor] = ss / total_ss
    shares["interactions_and_residual"] = max(0.0, 1.0 - sum(shares.values()))
    return shares


def main() -> None:
    rows = load_rows()
    OUT.mkdir(parents=True, exist_ok=True)
    layouts = sorted({row["layout"] for row in rows})
    summary: dict[str, object] = {
        "source": str(INPUT.relative_to(ROOT)),
        "scenario": "maxeon1540_independente",
        "method": "envelope_fatorial_finito; sem interpretação probabilística",
        "cases": len(rows),
        "factor_levels": {factor: sorted({row[factor] for row in rows}) for factor in ("layout", *FACTORS)},
        "limits": {
            "pbt_kg": 4250.0,
            "axle_ratings_kg": None,
            "base_axle_distribution_source": "OEM indisponível; frações traseiras 0,35/0,42/0,50 são hipóteses",
            "physical_validation": False,
        },
        "by_layout": {},
    }
    envelope_rows: list[dict[str, object]] = []
    by_layout = summary["by_layout"]
    assert isinstance(by_layout, dict)
    for layout in layouts:
        subset = [row for row in rows if row["layout"] == layout]
        extrema: dict[str, object] = {}
        for metric in METRICS:
            low = min(subset, key=lambda row: float(row[metric]))
            high = max(subset, key=lambda row: float(row[metric]))
            extrema[metric] = {
                "min": float(low[metric]),
                "min_case": {key: low[key] for key in ("estimated_mass_factor", "oem_rear_fraction_assumed", "oem_cg_height_assumed_m", "water_clean_grey_black_l")},
                "max": float(high[metric]),
                "max_case": {key: high[key] for key in ("estimated_mass_factor", "oem_rear_fraction_assumed", "oem_cg_height_assumed_m", "water_clean_grey_black_l")},
            }
        by_layout[layout] = {
            "cases": len(subset),
            "envelope": extrema,
            "main_effect_variance_shares": {metric: main_effect_shares(subset, metric) for metric in ("front_kg", "rear_kg", "cg_x_m", "cg_z_m")},
            "pbt_all_grid_cases_below_4250kg": all(float(row["mass_kg"]) <= 4250.0 for row in subset),
            "minimum_grid_pbt_margin_kg": min(float(row["pbt_margin_kg"]) for row in subset),
            "axle_compliance": "indeterminada; limites OEM por eixo ausentes",
        }
        for row in subset:
            envelope_rows.append({"layout": layout, **{key: row[key] for key in (*FACTORS, *METRICS)}})

    (OUT / "resumo.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (OUT / "casos.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=envelope_rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(envelope_rows)
    print(json.dumps({"cases": len(rows), "output": str(OUT.relative_to(ROOT)), "by_layout": {name: data["envelope"] for name, data in by_layout.items()}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
