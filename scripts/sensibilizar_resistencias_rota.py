"""Road-load sensitivity to grade and wind; no OEM motor map is inferred."""

from __future__ import annotations

import hashlib
import itertools
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from motorhome.cenarios import carregar_configuracao, diretorio_entregas


def main() -> None:
    os.environ["MOTORHOME_SCENARIO"] = "maxeon1540_independente"
    config = carregar_configuracao(ROOT)
    p = {key: value["value"] for key, value in config["parameters"].items()}

    # Transparent parametric envelope. Wind is positive headwind and negative
    # tailwind. These values are study sensitivities, not a route forecast.
    masses = [p["assembled_typical_mass_kg"], p["oem_pbt_kg"]]
    speeds_kmh = [10, 20, 40, 60, 80, 90]
    grades_percent = [-6, -3, 0, 3, 6]
    headwinds_m_s = [-10, -5, 0, 5, 10]
    crr_values = p["crr_range"]
    cd_values = p["cd_range"]
    rho_values = p["rho_range"]
    eta = p["eta_traction_range"][1]
    auxiliary_kw = p["traction_aux_assumed_w"] / 1000
    g = 9.80665
    area = p["area_m2"]
    rows = []

    for mass, speed_kmh, grade_pct, wind, crr, cd, rho in itertools.product(
        masses, speeds_kmh, grades_percent, headwinds_m_s, crr_values, cd_values, rho_values
    ):
        speed = speed_kmh / 3.6
        angle = np.arctan(grade_pct / 100)
        rolling_n = crr * mass * g * np.cos(angle)
        grade_n = mass * g * np.sin(angle)
        air_relative_m_s = speed + wind
        aerodynamic_n = 0.5 * rho * cd * area * air_relative_m_s * abs(air_relative_m_s)
        total_n = rolling_n + grade_n + aerodynamic_n
        wheel_kw_signed = total_n * speed / 1000
        positive_wheel_kw = max(0.0, wheel_kw_signed)
        brake_demand_kw = max(0.0, -wheel_kw_signed)
        battery_kw = positive_wheel_kw / eta + auxiliary_kw
        rows.append({
            "mass_kg": mass, "speed_kmh": speed_kmh, "grade_percent": grade_pct,
            "headwind_m_s": wind, "crr_assumed": crr, "cd_assumed": cd,
            "air_density_kg_m3": rho, "traction_efficiency_assumed": eta,
            "traction_auxiliary_kw_assumed": auxiliary_kw,
            "rolling_force_n": rolling_n, "grade_force_n": grade_n,
            "aerodynamic_force_n": aerodynamic_n, "relative_air_speed_m_s": air_relative_m_s,
            "total_road_load_n": total_n, "wheel_power_signed_kw": wheel_kw_signed,
            "positive_wheel_demand_kw": positive_wheel_kw,
            "mechanical_braking_demand_kw_no_regen_credit": brake_demand_kw,
            "estimated_battery_demand_kw_no_regen_credit": battery_kw,
            "estimated_battery_kwh_per_km_no_regen_credit": battery_kw / speed_kmh,
        })

    frame = pd.DataFrame(rows)
    out = diretorio_entregas(ROOT) / "dinamica_resistiva_sensibilidade"
    out.mkdir(parents=True, exist_ok=True)
    frame.to_csv(out / "envelope_grade_vento.csv", index=False)
    highest = frame.loc[frame["positive_wheel_demand_kw"].idxmax()].to_dict()
    lowest = frame.loc[frame["wheel_power_signed_kw"].idxmin()].to_dict()
    flat = frame[(frame.grade_percent == 0) & (frame.headwind_m_s == 0)
                 & (frame.mass_kg == masses[0]) & (frame.crr_assumed == p["crr_range"][1])
                 & (frame.cd_assumed == p["cd_range"][1]) & (frame.air_density_kg_m3 == p["rho_range"][1])]
    summary = {
        "scenario": config["_execution"]["scenario"],
        "source_config_sha256": config["_execution"]["source_sha256"],
        "resolved_config_sha256": config["_execution"]["resolved_sha256"],
        "script": "scripts/sensibilizar_resistencias_rota.py",
        "method": "equilíbrio longitudinal em velocidade constante: rolamento + gravidade da rampa + arrasto relativo ao ar; sem mapas OEM e sem crédito de regeneração",
        "cases": len(frame), "mass_kg": masses, "speed_kmh": speeds_kmh,
        "grade_percent": grades_percent, "headwind_m_s_positive_headwind": headwinds_m_s,
        "crr_assumed": crr_values, "cd_assumed": cd_values, "air_density_kg_m3": rho_values,
        "traction_efficiency_assumed": eta, "traction_auxiliary_kw_assumed": auxiliary_kw,
        "max_positive_wheel_demand": highest,
        "max_signed_braking_demand_without_regen": lowest,
        "flat_reference_mass_kg": masses[0],
        "flat_reference_kwh_per_km_by_speed": flat[["speed_kmh", "estimated_battery_kwh_per_km_no_regen_credit"]].to_dict("records"),
        "road_grade_or_wind_is_approved_mission_input": False,
        "oem_motor_map_used": False,
        "physical_validation": False,
        "limits": [
            "Grade, wind, Crr, Cd, density, and efficiency are explicit sensitivities, not measured conditions.",
            "Constant-speed model omits transient acceleration, tire limits, shifting, and thermal derating.",
            "Negative wheel power is reported as braking demand; no regenerative energy is credited.",
            "The combined traction efficiency and auxiliary draw do not substitute for motor/inverter maps.",
            "OEM continuous power, reduction ratio, and axle limits are unavailable; no performance approval is implied.",
        ],
        "configuration_file_sha256": hashlib.sha256(
            (ROOT / "config/parametros_globais.yaml").read_bytes()
        ).hexdigest(),
    }
    (out / "resumo.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "cases": len(frame), "max_positive_wheel_kw": highest["positive_wheel_demand_kw"],
        "max_braking_demand_kw": lowest["mechanical_braking_demand_kw_no_regen_credit"],
        "physical_validation": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
