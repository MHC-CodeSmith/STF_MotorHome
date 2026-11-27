"""Report two-grid sensitivity without claiming physical validation or GCI."""

import argparse
import csv
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--inicial", type=Path, required=True)
    p.add_argument("--refinada", type=Path, required=True)
    p.add_argument("--destino", type=Path, required=True)
    a = p.parse_args()
    coarse = json.loads(a.inicial.read_text())
    fine = json.loads(a.refinada.read_text())
    if not coarse["complete_six_cases"] or not fine["complete_six_cases"]:
        raise RuntimeError("Both six-case phases must finish before comparing grids")
    rows = []
    for c in coarse["cases"]:
        f = next(r for r in fine["cases"] if r["case"] == c["case"])
        rows.append(
            {
                "case": c["case"],
                "coarse_cells": c["cells"],
                "fine_cells": f["cells"],
                "coarse_cd": c["cd_diagnostic"],
                "fine_cd": f["cd_diagnostic"],
                "coarse_cda_m2": c["cda_m2"],
                "fine_cda_m2": f["cda_m2"],
                "cda_change_percent": 100 * (f["cda_m2"] / c["cda_m2"] - 1),
                "drag_change_n": f["drag_n"] - c["drag_n"],
                "both_iterative_checks_passed": c["iterative_check_passed"]
                and f["iterative_check_passed"],
            }
        )
    panel_rows = []
    for c in coarse["panel_comparisons"]:
        f = next(r for r in fine["panel_comparisons"] if r["geometry"] == c["geometry"])
        panel_rows.append(
            {
                "geometry": c["geometry"],
                "coarse_panel_delta_cda_m2": c["delta_cda_m2"],
                "fine_panel_delta_cda_m2": f["delta_cda_m2"],
                "change_in_panel_delta_cda_m2": f["delta_cda_m2"] - c["delta_cda_m2"],
                "increment_sign_changed": f["delta_cda_m2"] * c["delta_cda_m2"] < 0,
            }
        )
    a.destino.mkdir(parents=True, exist_ok=True)
    with (a.destino / "sensibilidade_malha.csv").open("w") as stream:
        writer = csv.DictWriter(stream, list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (a.destino / "sensibilidade_malha.json").write_text(
        json.dumps(
            {
                "cases": rows,
                "panel_increment_sensitivity": panel_rows,
                "physical_validation": False,
                "grid_independence_claimed": False,
                "gci": None,
                "limitation": "Two grid levels alone do not establish asymptotic convergence or physical accuracy.",
            },
            indent=2,
        )
        + "\n"
    )


if __name__ == "__main__":
    main()
