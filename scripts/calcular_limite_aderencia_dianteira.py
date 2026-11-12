"""Traction-only acceleration envelope for the front-drive study vehicle.

The result is an upper bound set by tire adhesion, not a motor/transmission
performance prediction. Friction coefficients are sensitivities, not tire data.
"""

import csv
import json
from math import atan, cos, isfinite, sin
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "entregas/integrado_maxeon1540/integracao/massa_cg_eixos_sensibilidade.csv"
OUT = ROOT / "entregas/integrado_maxeon1540/integracao/limite_aderencia_tracao_dianteira"
G = 9.80665
MU_GRID = (0.2, 0.3, 0.5, 0.7, 0.9)
GRADE_GRID_PERCENT = (-6.0, 0.0, 6.0)


def front_drive_traction_limit(mass_kg: float, cg_x_m: float, cg_z_m: float,
                               wheelbase_m: float, mu: float,
                               grade_percent: float) -> dict[str, float | bool]:
    """Solve force balance and front-axle normal load at the adhesion limit."""
    values = (mass_kg, cg_x_m, cg_z_m, wheelbase_m, mu, grade_percent)
    if any(not isfinite(value) for value in values):
        raise ValueError("Inputs must be finite")
    if mass_kg <= 0 or cg_z_m <= 0 or wheelbase_m <= 0 or mu <= 0:
        raise ValueError("Mass, CG height, wheelbase and mu must be positive")
    if not 0 < cg_x_m < wheelbase_m:
        raise ValueError("Longitudinal CG must lie between axles")
    theta = atan(grade_percent / 100.0)
    front_static_fraction = (wheelbase_m - cg_x_m) / wheelbase_m
    numerator = mu * cos(theta) * front_static_fraction - sin(theta)
    acceleration_g = numerator / (1.0 + mu * cg_z_m / wheelbase_m)
    can_hold_grade = numerator >= 0
    front_normal_n = mass_kg * G * (
        cos(theta) * front_static_fraction - acceleration_g * cg_z_m / wheelbase_m
    )
    tire_force_n = mu * front_normal_n
    gravity_along_grade_n = mass_kg * G * sin(theta)
    residual_n = tire_force_n - gravity_along_grade_n - mass_kg * acceleration_g * G
    return {
        "acceleration_limit_g": acceleration_g,
        "acceleration_limit_m_s2": acceleration_g * G,
        "front_normal_load_kg_equivalent": front_normal_n / G,
        "front_tire_force_limit_n": tire_force_n,
        "grade_resistance_n": gravity_along_grade_n,
        "force_balance_residual_n": residual_n,
        "can_hold_grade_at_zero_acceleration": can_hold_grade,
    }


def main() -> None:
    params = yaml.safe_load((ROOT / "config/parametros_globais.yaml").read_text(encoding="utf-8"))
    wheelbase = float(params["parameters"]["wheelbase_m"]["value"])
    with INPUT.open(newline="", encoding="utf-8") as stream:
        source_rows = list(csv.DictReader(stream))
    if len(source_rows) != 162:
        raise ValueError(f"Expected 162 mass/CG cases; found {len(source_rows)}")

    rows: list[dict[str, object]] = []
    for source in source_rows:
        for mu in MU_GRID:
            for grade in GRADE_GRID_PERCENT:
                result = front_drive_traction_limit(
                    float(source["mass_kg"]), float(source["cg_x_m"]),
                    float(source["cg_z_m"]), wheelbase, mu, grade,
                )
                rows.append({
                    "layout": source["layout"],
                    "estimated_mass_factor": source["estimated_mass_factor"],
                    "oem_rear_fraction_assumed": source["oem_rear_fraction_assumed"],
                    "oem_cg_height_assumed_m": source["oem_cg_height_assumed_m"],
                    "water_clean_grey_black_l": source["water_clean_grey_black_l"],
                    "mass_kg": float(source["mass_kg"]),
                    "cg_x_m": float(source["cg_x_m"]),
                    "cg_z_m": float(source["cg_z_m"]),
                    "wheelbase_m": wheelbase,
                    "mu_sensitivity": mu,
                    "grade_percent": grade,
                    **result,
                })

    OUT.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0])
    with (OUT / "casos.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    by_condition = {}
    for mu in MU_GRID:
        for grade in GRADE_GRID_PERCENT:
            subset = [r for r in rows if r["mu_sensitivity"] == mu and r["grade_percent"] == grade]
            key = f"mu={mu:g};grade={grade:g}%"
            by_condition[key] = {
                "cases": len(subset),
                "acceleration_limit_g_range": [
                    min(float(r["acceleration_limit_g"]) for r in subset),
                    max(float(r["acceleration_limit_g"]) for r in subset),
                ],
                "cases_unable_to_hold_grade": sum(not bool(r["can_hold_grade_at_zero_acceleration"]) for r in subset),
                "max_abs_force_balance_residual_n": max(abs(float(r["force_balance_residual_n"])) for r in subset),
            }
    summary = {
        "method": "quasi_static_front_axle_adhesion_limit; grade equilibrium; no torque/power cap",
        "source_cases": len(source_rows),
        "cases": len(rows),
        "drive_axle": "front; published for the studied SK MY25 reference sheet",
        "mu_values": MU_GRID,
        "mu_scope": "dimensionless sensitivities only; not measured Continental tire-road coefficients",
        "grade_percent_values": GRADE_GRID_PERCENT,
        "equation_acceleration_g": "(mu*cos(theta)*(L-xcg)/L - sin(theta))/(1+mu*zcg/L), theta=atan(grade_percent/100)",
        "ignored": ["motor torque map", "gear reduction", "inverter limits", "tire transient behavior", "suspension compliance", "aerodynamic drag", "rolling resistance"],
        "physical_validation": False,
        "oem_acceleration_prediction": False,
        "by_condition": by_condition,
    }
    (OUT / "resumo.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"cases": len(rows), "by_condition": by_condition}, ensure_ascii=False))


if __name__ == "__main__":
    main()
