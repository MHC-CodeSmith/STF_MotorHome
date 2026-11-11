"""Sensitivity of the conditional I29 replay to temporal discretization.

Re-evaluates a narrow neighborhood of the existing dense-search leaders at
15-minute and 5-minute steps. This is a finite local comparison under the
existing hypothetical DC interface; it is not a global optimizer or proof of
physical feasibility.
"""

from __future__ import annotations

import copy
import hashlib
import itertools
import json
import os
import sys
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from motorhome.cenarios import carregar_configuracao, diretorio_entregas
from motorhome.reconciliacao import consumo_plano, simular_missao
from motorhome.solar import simular_dia


def main() -> None:
    os.environ["MOTORHOME_SCENARIO"] = "maxeon1540_independente"
    config = carregar_configuracao(ROOT)
    params = {key: value["value"] for key, value in config["parameters"].items()}
    grid = config["development"]["mission_grid"]
    solar_template = yaml.safe_load((ROOT / "config/solar_proposta.yaml").read_text())
    solar_template["scenario"].update(
        date=params["reference_day"], latitude_deg=params["latitude_deg"],
        longitude_deg=params["longitude_deg"], altitude_m=params["altitude_m"],
        ambient_temperature_c=params["ambient_c"], wind_speed_m_s=params["wind_m_s"],
        relative_humidity_percent=params["rh_percent"],
    )
    solar_template["module"].update(
        p_stc_w=params["roof_power_48v_study_wp"], gamma_pdc_per_k=params["pv_gamma"]
    )
    solar_template["array"].update(
        module_counts=[1], tilt_deg=0, azimuth_deg=0, albedo=params["pv_albedo"]
    )
    solar_template["assumptions"].update(
        converter_efficiency=1, other_losses_fraction=params["pv_other_loss"],
        faiman_u0_w_m2k=params["pv_faiman_u0"], faiman_u1_w_s_m3k=params["pv_faiman_u1"],
    )

    # The 5-minute grid resolves start phase and PV ramps more finely while
    # keeping the study local to the published 18 h / ~20 km/h leaders.
    starts_h = [17.5, 17.75, 18.0, 18.25, 18.5, 18.75, 19.0]
    speeds_kmh = [19.6, 19.8, 20.0, 20.2, 20.4, 20.6, 20.8]
    reserves = [(0.1, 0.2), (0.2, 0.3)]
    aux_w = 700
    candidate_rows: list[dict] = []

    for step_min in (15, 5, 1):
        dt_h = step_min / 60
        solar = copy.deepcopy(solar_template)
        roof_power = simular_dia(solar, step_min)["terminal_assumed_1_modules_w"].to_numpy()
        # simular_missao receives mean interval power in kW and applies dt.
        roof = (roof_power[:-1] + roof_power[1:]) / 2000
        portable_candidates = []
        for tilt, azimuth in itertools.product(range(0, 76, 15), (0, 90, 180, 270)):
            candidate = copy.deepcopy(solar)
            candidate["array"].update(tilt_deg=tilt, azimuth_deg=azimuth)
            candidate["module"].update(
                p_stc_w=params["portable_wp"], gamma_pdc_per_k=params["portable_gamma"]
            )
            watts = simular_dia(candidate, step_min)["terminal_assumed_1_modules_w"].to_numpy()
            portable_candidates.append((tilt, azimuth, (watts[:-1] + watts[1:]) / 2000))

        slot_hours = np.arange(len(roof)) * dt_h + dt_h / 2
        ac_kwh = sum(
            load["energy_ac_or_dc_kwh_day"]["base"]
            for load in config["loads"] if load["side"] == "AC"
        )
        dc_kwh = sum(
            load["energy_ac_or_dc_kwh_day"]["base"]
            for load in config["loads"] if load["side"] == "DC"
        )
        service_day = ac_kwh / params["eta_inverter"] + dc_kwh / params["eta_lv"]
        service_day += params["inverter_idle_w"] * 24 / 1000

        for start_h, speed, reserve in itertools.product(starts_h, speeds_kmh, reserves):
            driving = (slot_hours - start_h) % 24 < 8.0
            since_park = (slot_hours - (start_h + 8.0)) % 24
            usable = (~driving) & (since_park >= params["pv_setup_h"])
            usable &= since_park < 16.0 - params["pv_teardown_h"]
            tilt, azimuth, portable_curve = max(
                portable_candidates, key=lambda item: float((item[2] * usable).sum())
            )
            portable = portable_curve * usable
            consumption = consumo_plano(
                speed, params["assembled_typical_mass_kg"], params["cd_range"][1],
                params["area_m2"], params["crr_range"][1], params["rho_range"][1],
                params["eta_traction_range"][1], aux_traction_kw=aux_w / 1000,
            )
            result = simular_missao(
                roof.tolist(), portable.tolist(), driving.tolist(), speed_kmh=speed,
                kwh_km=consumption["kwh_km"],
                service_kwh_day=service_day,
                traction_capacity_kwh=params["traction_usable_kwh"], service_capacity_kwh=14.4,
                reserve_traction=reserve[0], reserve_service=reserve[1], mode=grid["mode"],
                min_dc_kw=grid["hypothetical_min_dc_kw"], max_days=grid["max_days"],
                eta_dc=params["eta_dc"],
            )
            result.pop("trace", None)
            result.pop("daily", None)
            candidate_rows.append({
                "time_step_min": step_min, "start_hour": start_h,
                "driving_window_h": 8.0, "speed_kmh": speed,
                "reserve_traction": reserve[0], "reserve_service": reserve[1],
                "auxiliary_traction_w_assumed": aux_w,
                "portable_tilt_deg": tilt, "portable_azimuth_deg": azimuth,
                "kwh_per_km": consumption["kwh_km"], **result,
            })

    output = diretorio_entregas(ROOT) / "otimizacao_resolucao_temporal"
    output.mkdir(parents=True, exist_ok=True)
    candidate_rows.sort(key=lambda row: (row["time_step_min"], row["reserve_traction"],
                                         row["reserve_service"], row["elapsed_days"]))
    (output / "candidatos.json").write_text(
        json.dumps(candidate_rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    leaders = []
    for step_min, rt, rs in itertools.product((15, 5, 1), (0.1, 0.2), (0.2, 0.3)):
        if (rt, rs) not in reserves:
            continue
        eligible = [row for row in candidate_rows if row["time_step_min"] == step_min
                    and row["reserve_traction"] == rt and row["reserve_service"] == rs
                    and row["status"] == "chegada_condicional"]
        if eligible:
            leaders.append(min(eligible, key=lambda row: (row["elapsed_days"],
                                                           row["start_hour"], row["speed_kmh"])))
    summary = {
        "scenario": config["_execution"]["scenario"],
        "source_config_sha256": config["_execution"]["source_sha256"],
        "resolved_config_sha256": config["_execution"]["resolved_sha256"],
        "script": "scripts/refinar_resolucao_missao.py",
        "method": "comparação local em 15, 5 e 1 minuto; sete horários (17,5–19 h), sete velocidades (19,6–20,8 km/h), dois pares de reservas; horários e velocidades não cobrem todo o domínio",
        "candidate_count": len(candidate_rows), "steps_min": [15, 5, 1],
        "speed_domain_kmh": [min(speeds_kmh), max(speeds_kmh)],
        "start_domain_h": [min(starts_h), max(starts_h)],
        "auxiliary_traction_w_assumed": aux_w,
        "hypothetical_dc_interface": True, "physical_mission_demonstrated": False,
        "global_optimum_claimed": False,
        "best_local_by_resolution_and_reserve": leaders,
        "max_abs_energy_residual_kwh": max(abs(row["energy_residual_kwh"]) for row in candidate_rows),
        "configuration_file_sha256": hashlib.sha256(
            (ROOT / "config/parametros_globais.yaml").read_bytes()
        ).hexdigest(),
    }
    (output / "resumo.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
