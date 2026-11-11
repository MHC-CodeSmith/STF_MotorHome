"""Sizing sensitivity for a provisional ventilation fallback; no fan is selected."""

from __future__ import annotations

import hashlib
import itertools
import json
import os
from pathlib import Path

import pandas as pd

from motorhome.cenarios import carregar_configuracao, diretorio_entregas

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    os.environ["MOTORHOME_SCENARIO"] = "maxeon1540_independente"
    config = carregar_configuracao(ROOT)
    study = config["development"]["ventilation_study"]
    occupants = [1, 2]
    targets_ppm = [800, 1000, 1200]
    generation_l_h_person = [12, 18, 24]
    pressure_drop_pa = [20, 50, 100]
    fan_efficiency = [0.2, 0.35]
    indoor_outdoor_delta_k = [0, 8, 15]
    operation_h_day = [8, 24]
    air_density = 1.2
    air_cp = 1005.0
    co2_outside_ppm = float(study["outside_co2_ppm"])
    rows = []

    for people, target, generation, pressure, efficiency, delta_k, hours in itertools.product(
        occupants,
        targets_ppm,
        generation_l_h_person,
        pressure_drop_pa,
        fan_efficiency,
        indoor_outdoor_delta_k,
        operation_h_day,
    ):
        if target <= co2_outside_ppm:
            raise ValueError("CO2 target must exceed the assumed outdoor concentration")
        co2_generation_m3_h = people * generation / 1000
        required_flow_m3_h = co2_generation_m3_h / ((target - co2_outside_ppm) * 1e-6)
        flow_m3_s = required_flow_m3_h / 3600
        fan_power_w = flow_m3_s * pressure / efficiency
        sensible_load_w = air_density * flow_m3_s * air_cp * delta_k
        baseline_flow = 30.0
        baseline_co2_ppm = co2_outside_ppm + co2_generation_m3_h / baseline_flow * 1e6
        rows.append(
            {
                "occupants": people,
                "co2_target_study_ppm": target,
                "co2_outside_assumed_ppm": co2_outside_ppm,
                "co2_generation_l_h_person_assumed": generation,
                "required_outdoor_air_m3_h_for_co2_balance": required_flow_m3_h,
                "baseline_flow_30_m3_h_equilibrium_co2_ppm": baseline_co2_ppm,
                "baseline_30_m3_h_meets_study_target": baseline_co2_ppm <= target,
                "pressure_drop_assumed_pa": pressure,
                "fan_total_efficiency_assumed": efficiency,
                "fan_electrical_power_estimate_w": fan_power_w,
                "fan_energy_estimate_kwh_day": fan_power_w * hours / 1000,
                "operation_h_day_assumed": hours,
                "indoor_outdoor_delta_k_assumed": delta_k,
                "ventilation_sensible_load_estimate_w": sensible_load_w,
                "latent_load_included": False,
            }
        )

    frame = pd.DataFrame(rows)
    output = diretorio_entregas(ROOT) / "ventilacao_mecanica_sensibilidade"
    output.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output / "envelope_ventilacao.csv", index=False)
    nominal = frame[
        (frame.occupants == 2)
        & (frame.co2_target_study_ppm == 1000)
        & (frame.co2_generation_l_h_person_assumed == 18)
    ]
    nominal_summary = {
        "two_occupants_target_1000ppm_reference_flow_m3_h": float(
            nominal.required_outdoor_air_m3_h_for_co2_balance.iloc[0]
        ),
        "baseline_30_m3_h_equilibrium_co2_ppm": float(
            nominal.baseline_flow_30_m3_h_equilibrium_co2_ppm.iloc[0]
        ),
        "fan_power_range_w": [
            float(frame.fan_electrical_power_estimate_w.min()),
            float(frame.fan_electrical_power_estimate_w.max()),
        ],
        "fan_energy_range_kwh_day": [
            float(frame.fan_energy_estimate_kwh_day.min()),
            float(frame.fan_energy_estimate_kwh_day.max()),
        ],
        "two_occupants_delta8k_sensible_load_w": float(
            nominal[nominal.indoor_outdoor_delta_k_assumed == 8]
            .ventilation_sensible_load_estimate_w.iloc[0]
        ),
    }
    summary = {
        "scenario": config["_execution"]["scenario"],
        "source_config_sha256": config["_execution"]["source_sha256"],
        "resolved_config_sha256": config["_execution"]["resolved_sha256"],
        "script": "scripts/sensibilizar_ventilacao_mecanica.py",
        "cases": len(frame),
        "co2_balance_model": "well-mixed steady state: Q = occupants * generation / (target - outdoor concentration)",
        "nominal_study_case": nominal_summary,
        "natural_ventilation_remains_priority": True,
        "mechanical_fallback_selected_or_installed": False,
        "regulatory_minimum_claimed": False,
        "physical_validation": False,
        "limits": [
            "CO2 targets, generation rates, duct pressure drops, fan efficiencies and operation hours are study sensitivities, not a cited ventilation code or measured design.",
            "Steady, well-mixed CO2 balance excludes transient cabin concentration and leakage.",
            "Sensible ventilation load uses fixed air density and heat capacity; latent load is excluded because outdoor humidity and cabin moisture control are unknown.",
            "No fan, duct, grille, acoustic treatment, electrical protection or installation is selected or approved.",
            "The 30 m3/h comparison is the existing model input, not a demonstrated installed airflow.",
        ],
        "configuration_file_sha256": hashlib.sha256(
            (ROOT / "config/parametros_globais.yaml").read_bytes()
        ).hexdigest(),
    }
    (output / "resumo.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps({"cases": len(frame), **nominal_summary}, ensure_ascii=False))


if __name__ == "__main__":
    main()
