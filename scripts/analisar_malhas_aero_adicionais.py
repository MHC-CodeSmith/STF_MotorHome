"""Consolidate diagnostics from additional equipped-aerodynamics CFD runs."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "entregas/aero_equipado1540"
CASES = [
    "malha_adicional_1",
    "malha_adicional_gradiente_solo_2",
    "malha_adicional_gradiente_solo_4",
    "malha_adicional_gradiente_solo_20",
    "malha_adicional_parede_1",
]


def main() -> None:
    rows: list[dict[str, object]] = []
    for name in CASES:
        path = BASE / name / "resumo.json"
        data = json.loads(path.read_text())
        yplus = data.get("yplus_summary") or {}
        residuals = data.get("parallel_last_completed_initial_residuals") or {}
        rows.append({
            "case": name,
            "cells": data.get("cell_count"),
            "mesh_ok": data.get("mesh_ok"),
            "solver_converged": data.get("parallel_solver_converged"),
            "solver_exit": data.get("parallel_solver_exit"),
            "last_completed_iteration": data.get("parallel_last_completed_iteration"),
            "solver_seconds": data.get("parallel_solver_seconds"),
            "cd_diagnostic": data.get("last_cd_diagnostic"),
            "cd_last50_relative_span": data.get("last50_cd_relative_span"),
            "uy_initial_residual": residuals.get("Uy"),
            "p_initial_residual": residuals.get("p"),
            "global_continuity_error": data.get("parallel_last_completed_global_continuity_error"),
            "ground_yplus_mean": (yplus.get("ground") or [None, None, None])[2],
            "pvdeck_yplus_mean": (yplus.get("pvdeck") or [None, None, None])[2],
            "body_yplus_mean": (yplus.get("aurora") or [None, None, None])[2],
            "validated_cd": data.get("validated_cd"),
            "physical_validation": data.get("physical_validation", False),
        })

    out = BASE / "comparacao_malhas_adicionais.csv"
    with out.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    cd_values = {row["case"]: row["cd_diagnostic"] for row in rows if row["cd_diagnostic"] is not None}
    reference = cd_values["malha_adicional_1"]
    comparisons = {
        name: {
            "absolute_difference": abs(value - reference),
            "relative_difference_vs_malha_adicional_1_pct": abs(value - reference) / abs(reference) * 100,
        }
        for name, value in cd_values.items()
        if name != "malha_adicional_1"
    }
    result = {
        "purpose": "Numerical diagnostics only; non-nested meshes and incomplete wall resolution do not support GCI or grid independence.",
        "reference_case": "malha_adicional_1",
        "cases": rows,
        "cd_diagnostic_pairwise_vs_reference": comparisons,
        "validated_cd": None,
        "grid_independence": False,
        "physical_validation": False,
    }
    (BASE / "comparacao_malhas_adicionais.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    )
    print(json.dumps({"csv": str(out.relative_to(ROOT)), "json": str((BASE / "comparacao_malhas_adicionais.json").relative_to(ROOT)), "pairwise": comparisons}, ensure_ascii=False))


if __name__ == "__main__":
    main()
