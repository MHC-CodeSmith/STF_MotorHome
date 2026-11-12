"""Conditional steady-climb envelope; not an OEM performance prediction.

Uses a published peak-power ceiling, explicit drivetrain-efficiency and tire
friction sensitivities, front-axle load, and road loads. No motor map/ratio,
continuous rating, thermal derating, or physical validation is inferred.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import os
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from motorhome.cenarios import carregar_configuracao, diretorio_entregas

G = 9.80665
SPEEDS_KMH = (20, 40, 60, 80, 90)
MU_VALUES = (0.3, 0.5, 0.7)
WIND_VALUES_M_S = (-10.0, 0.0, 10.0)
MAX_GRADE_RATIO = 0.50


def road_load_n(mass_kg: float, speed_m_s: float, grade_ratio: float,
                headwind_m_s: float, crr: float, cd: float, area_m2: float,
                rho_kg_m3: float) -> float:
    """Longitudinal steady road load; positive wind means headwind."""
    theta = np.arctan(grade_ratio)
    rolling = crr * mass_kg * G * np.cos(theta)
    grade = mass_kg * G * np.sin(theta)
    relative_air_speed = speed_m_s + headwind_m_s
    aero = 0.5 * rho_kg_m3 * cd * area_m2 * relative_air_speed * abs(relative_air_speed)
    return float(rolling + grade + aero)


def front_normal_n(mass_kg: float, cg_x_m: float, cg_z_m: float,
                   wheelbase_m: float, grade_ratio: float) -> float:
    """Static front normal force on a grade, with no acceleration transfer."""
    theta = np.arctan(grade_ratio)
    return float(mass_kg * G * (
        np.cos(theta) * (wheelbase_m - cg_x_m) / wheelbase_m
        - cg_z_m * np.sin(theta) / wheelbase_m
    ))


def solve_steady_climb(mass_kg: float, cg_x_m: float, cg_z_m: float,
                       wheelbase_m: float, speed_kmh: float, mu: float,
                       headwind_m_s: float, crr: float, cd: float,
                       area_m2: float, rho_kg_m3: float,
                       motor_peak_kw: float, drivetrain_efficiency: float) -> dict[str, float | bool | str]:
    """Find the greatest steady uphill grade allowed by power and adhesion."""
    values = (mass_kg, cg_x_m, cg_z_m, wheelbase_m, speed_kmh, mu,
              headwind_m_s, crr, cd, area_m2, rho_kg_m3, motor_peak_kw,
              drivetrain_efficiency)
    if not all(np.isfinite(v) for v in values):
        raise ValueError("inputs must be finite")
    if (mass_kg <= 0 or wheelbase_m <= 0 or not 0 < cg_x_m < wheelbase_m
            or cg_z_m <= 0 or speed_kmh <= 0 or mu <= 0 or crr < 0
            or cd < 0 or area_m2 <= 0 or rho_kg_m3 <= 0 or motor_peak_kw <= 0
            or not 0 < drivetrain_efficiency <= 1):
        raise ValueError("invalid vehicle, road, or drivetrain input")

    speed = speed_kmh / 3.6
    power_force = drivetrain_efficiency * motor_peak_kw * 1000.0 / speed

    def margin(grade: float) -> tuple[float, float, float]:
        normal = front_normal_n(mass_kg, cg_x_m, cg_z_m, wheelbase_m, grade)
        tire_force = mu * max(0.0, normal)
        available = min(power_force, tire_force)
        demand = road_load_n(mass_kg, speed, grade, headwind_m_s,
                             crr, cd, area_m2, rho_kg_m3)
        return available - demand, power_force, tire_force

    level_margin, _, level_tire = margin(0.0)
    if level_margin < 0:
        return {
            "maximum_grade_percent_in_model": 0.0,
            "level_motion_feasible_in_model": False,
            "grade_search_capped_at_50_percent": False,
            "limiting_mechanism_at_grade": "level_case_infeasible",
            "level_available_power_force_n": power_force,
            "level_front_adhesion_force_n": level_tire,
            "level_road_load_n": road_load_n(mass_kg, speed, 0.0, headwind_m_s,
                                               crr, cd, area_m2, rho_kg_m3),
            "force_balance_residual_n_at_limit": level_margin,
        }
    upper = MAX_GRADE_RATIO
    upper_margin, _, _ = margin(upper)
    if upper_margin >= 0:
        grade = upper
        capped = True
    else:
        lower = 0.0
        for _ in range(60):
            mid = 0.5 * (lower + upper)
            if margin(mid)[0] >= 0:
                lower = mid
            else:
                upper = mid
        grade = 0.5 * (lower + upper)
        capped = False

    residual, power_limit, tire_limit = margin(grade)
    mechanism = "potencia" if power_limit <= tire_limit else "aderencia_dianteira"
    return {
        "maximum_grade_percent_in_model": float(100.0 * grade),
        "level_motion_feasible_in_model": True,
        "grade_search_capped_at_50_percent": capped,
        "limiting_mechanism_at_grade": mechanism,
        "level_available_power_force_n": power_force,
        "level_front_adhesion_force_n": level_tire,
        "level_road_load_n": road_load_n(mass_kg, speed, 0.0, headwind_m_s,
                                           crr, cd, area_m2, rho_kg_m3),
        "force_balance_residual_n_at_limit": residual,
    }


def main() -> None:
    os.environ["MOTORHOME_SCENARIO"] = "maxeon1540_independente"
    config = carregar_configuracao(ROOT)
    p = {k: v["value"] for k, v in config["parameters"].items()}
    source = pd.read_csv(diretorio_entregas(ROOT) / "integracao/massa_cg_eixos_sensibilidade.csv")
    if len(source) != 162:
        raise ValueError(f"expected 162 mass/CG inputs, got {len(source)}")
    crr_values = p["crr_range"]
    efficiency_values = p["eta_traction_range"]
    cd = p["cd_range"][1]
    rho = p["rho_range"][1]
    cases = []
    for row, speed, mu, wind, crr, efficiency in itertools.product(
        source.to_dict("records"), SPEEDS_KMH, MU_VALUES, WIND_VALUES_M_S,
        crr_values, efficiency_values
    ):
        result = solve_steady_climb(
            float(row["mass_kg"]), float(row["cg_x_m"]), float(row["cg_z_m"]),
            float(p["wheelbase_m"]), speed, mu, wind, crr, cd, float(p["area_m2"]),
            rho, float(p["motor_peak_kw"]), efficiency,
        )
        cases.append({
            "layout": row["layout"], "estimated_mass_factor": row["estimated_mass_factor"],
            "mass_kg": float(row["mass_kg"]), "cg_x_m": float(row["cg_x_m"]),
            "cg_z_m": float(row["cg_z_m"]), "speed_kmh": speed,
            "mu_assumed": mu, "headwind_m_s": wind, "crr_assumed": crr,
            "cd_assumed_central": cd, "rho_assumed_central_kg_m3": rho,
            "motor_peak_kw_published_ceiling": p["motor_peak_kw"],
            "drivetrain_efficiency_assumed": efficiency, **result,
        })
    out = diretorio_entregas(ROOT) / "integracao/envelope_subida_condicional"
    out.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(cases)
    frame.to_csv(out / "casos.csv", index=False, lineterminator="\n")
    summary = {
        "scenario": config["_execution"]["scenario"],
        "source_config_sha256": config["_execution"]["source_sha256"],
        "resolved_config_sha256": config["_execution"]["resolved_sha256"],
        "source_mass_cg_cases": len(source), "cases": len(frame),
        "speeds_kmh": SPEEDS_KMH, "mu_sensitivities": MU_VALUES,
        "headwind_m_s": WIND_VALUES_M_S, "crr_sensitivities": crr_values,
        "drivetrain_efficiency_sensitivities": efficiency_values,
        "cd_central_assumed": cd, "rho_central_assumed_kg_m3": rho,
        "peak_power_kw_used_as_ceiling": p["motor_peak_kw"],
        "method": "steady longitudinal equilibrium; max grade by bisection; usable wheel force=min(eta*published peak power/v, mu*static front axle normal load on grade)",
        "maximum_grade_represents_continuous_oem_performance": False,
        "global_optimum_claimed": False, "physical_validation": False,
        "grouped_by_speed_mu": [],
        "limits": [
            "205 kW is used only as a documented peak-power ceiling for the study candidate; no continuous rating, map, torque-speed curve, or variant approval is inferred.",
            "Drivetrain efficiency, tire-road friction, rolling resistance, grade, and wind are sensitivities; Cd and air density use their central hypotheses here.",
            "Front-axle normal load is quasi-static with grade only; suspension, pitch transients, tire dynamics, and load variation are omitted.",
            "No gear ratio, motor speed limit, thermal derating, battery power limit, or startability at zero speed is modeled.",
            "This numerical envelope is not an OEM performance claim, road test, legal gradeability, or proof of sustained climbing.",
        ],
        "configuration_file_sha256": hashlib.sha256(
            (ROOT / "config/parametros_globais.yaml").read_bytes()
        ).hexdigest(),
    }
    for (speed, mu), group in frame.groupby(["speed_kmh", "mu_assumed"], sort=True):
        summary["grouped_by_speed_mu"].append({
            "speed_kmh": int(speed), "mu_assumed": float(mu),
            "grade_percent_in_model_range": [
                float(group.maximum_grade_percent_in_model.min()),
                float(group.maximum_grade_percent_in_model.max()),
            ],
            "grade_percent_in_model_median": float(group.maximum_grade_percent_in_model.median()),
            "cases_level_infeasible": int((~group.level_motion_feasible_in_model).sum()),
            "cases_capped": int(group.grade_search_capped_at_50_percent.sum()),
            "power_limited_fraction": float((group.limiting_mechanism_at_grade == "potencia").mean()),
            "max_abs_force_residual_n": float(group.force_balance_residual_n_at_limit.abs().max()),
        })
    (out / "resumo.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    pivot = frame.groupby(["speed_kmh", "mu_assumed"]).maximum_grade_percent_in_model.median().unstack()
    fig, ax = plt.subplots(figsize=(8.2, 5.0), layout="constrained")
    for mu in pivot.columns:
        ax.plot(pivot.index, pivot[mu], marker="o", linewidth=2, label=f"μ={mu:g} (hipótese)")
    ax.set(title="Subida em regime: envelope condicional potência × aderência",
           xlabel="Velocidade constante [km/h]", ylabel="Inclinação máxima calculada no modelo [%]")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, title="Aderência")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.text(0.5, -0.01,
             "Mediana dos 162 casos de massa/CG e sensibilidades Crr, vento e eficiência. "
             "Teto de pico 205 kW; sem mapa OEM, contínua, relação ou ensaio.",
             ha="center", fontsize=8)
    fig.savefig(out / "envelope_subida.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(json.dumps({
        "cases": len(frame), "summary": str((out / "resumo.json").relative_to(ROOT)),
        "median_grade_percent_at_mu_0_5": [
            next(x["grade_percent_in_model_median"] for x in summary["grouped_by_speed_mu"]
                 if x["speed_kmh"] == speed and x["mu_assumed"] == 0.5)
            for speed in SPEEDS_KMH
        ],
        "physical_validation": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
