"""Finite coarse + local search over daily departure windows for I29.

All physics and the hypothetical direct-DC interface follow the existing I29
model. The result is a bounded-grid study, never a global optimum or validation.
"""

import copy
import itertools
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
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
    solar = yaml.safe_load((ROOT / "config/solar_proposta.yaml").read_text())
    solar["scenario"].update(
        date=params["reference_day"], latitude_deg=params["latitude_deg"],
        longitude_deg=params["longitude_deg"], altitude_m=params["altitude_m"],
        ambient_temperature_c=params["ambient_c"], wind_speed_m_s=params["wind_m_s"],
        relative_humidity_percent=params["rh_percent"],
    )
    solar["module"].update(
        p_stc_w=params["roof_power_48v_study_wp"], gamma_pdc_per_k=params["pv_gamma"]
    )
    solar["array"].update(module_counts=[1], tilt_deg=0, azimuth_deg=0, albedo=params["pv_albedo"])
    solar["assumptions"].update(
        converter_efficiency=1, other_losses_fraction=params["pv_other_loss"],
        faiman_u0_w_m2k=params["pv_faiman_u0"], faiman_u1_w_s_m3k=params["pv_faiman_u1"],
    )
    roof_w = simular_dia(solar, 15)["terminal_assumed_1_modules_w"].to_numpy()
    roof = (roof_w[:-1] + roof_w[1:]) / 2000
    portable_candidates = []
    for tilt, azimuth in itertools.product(range(0, 76, 15), (0, 90, 180, 270)):
        candidate = copy.deepcopy(solar)
        candidate["array"].update(tilt_deg=tilt, azimuth_deg=azimuth)
        candidate["module"].update(
            p_stc_w=params["portable_wp"], gamma_pdc_per_k=params["portable_gamma"]
        )
        watts = simular_dia(candidate, 15)["terminal_assumed_1_modules_w"].to_numpy()
        portable_candidates.append((tilt, azimuth, (watts[:-1] + watts[1:]) / 2000))

    dt = 0.25
    hours = np.arange(96) * dt + dt / 2
    ac = sum(load["energy_ac_or_dc_kwh_day"]["base"] for load in config["loads"] if load["side"] == "AC")
    dc = sum(load["energy_ac_or_dc_kwh_day"]["base"] for load in config["loads"] if load["side"] == "DC")
    service_day = ac / params["eta_inverter"] + dc / params["eta_lv"] + params["inverter_idle_w"] * 24 / 1000

    dense = "--densa" in sys.argv[1:]
    cache: dict[float, tuple[np.ndarray, np.ndarray, int, int]] = {}

    def schedule(start: float) -> tuple[np.ndarray, np.ndarray, int, int]:
        key = round(start % 24, 4)
        if key in cache:
            return cache[key]
        driving = (hours - key) % 24 < 8.0
        since_park = (hours - (key + 8.0)) % 24
        usable = (~driving) & (since_park >= params["pv_setup_h"]) & (
            since_park < 16.0 - params["pv_teardown_h"]
        )
        tilt, azimuth, curve = max(portable_candidates, key=lambda item: float((item[2] * usable).sum()))
        entry = (driving, curve * usable, tilt, azimuth)
        cache[key] = entry
        return entry

    def evaluate(start: float, speed: float, reserve: tuple[float, float], aux_w: int) -> dict:
        driving, portable, tilt, azimuth = schedule(start)
        consumption = consumo_plano(
            speed, params["assembled_typical_mass_kg"], params["cd_range"][1],
            params["area_m2"], params["crr_range"][1], params["rho_range"][1],
            params["eta_traction_range"][1], aux_traction_kw=aux_w / 1000,
        )
        result = simular_missao(
            roof.tolist(), portable.tolist(), driving.tolist(), speed_kmh=float(speed),
            kwh_km=consumption["kwh_km"], service_kwh_day=service_day,
            traction_capacity_kwh=params["traction_usable_kwh"], service_capacity_kwh=14.4,
            reserve_traction=reserve[0], reserve_service=reserve[1], mode=grid["mode"],
            min_dc_kw=grid["hypothetical_min_dc_kw"], max_days=grid["max_days"], eta_dc=params["eta_dc"],
        )
        result.pop("trace", None)
        result.pop("daily", None)
        return {
            "reserve_traction": reserve[0], "reserve_service": reserve[1],
            "auxiliary_traction_w_assumed": aux_w, "start_hour": key_hour(start),
            "driving_window_h": 8.0, "speed_kmh": float(speed), "kwh_per_km": consumption["kwh_km"],
            "portable_tilt_deg": tilt, "portable_azimuth_deg": azimuth, **result,
        }

    cases: list[dict] = []
    best_coarse: dict[tuple[float, float, int], dict] = {}
    coarse_starts = np.arange(0, 24, 2.0 if dense else 3.0)
    coarse_speeds = np.arange(10, 90.0001, 2.0 if dense else 4.0)
    # Optimize at the documented central auxiliary estimate; evaluate the
    # other auxiliary values as sensitivities at the selected policies.
    aux_central = min(grid["auxiliary_sweep_w"], key=lambda value: abs(value - 700))
    optimized_aux = grid["auxiliary_sweep_w"] if dense else [aux_central]
    for reserve, aux_w in itertools.product(grid["reserves"], optimized_aux):
        key = (reserve[0], reserve[1], aux_w)
        group = [evaluate(start, speed, reserve, aux_w) for start in coarse_starts for speed in coarse_speeds]
        cases.extend(group)
        feasible = [row for row in group if row["status"] == "chegada_condicional"]
        if feasible:
            best_coarse[key] = min(feasible, key=lambda row: (row["elapsed_days"], row["speed_kmh"]))

    refined_cases = 0
    for (rt, rs, aux_w), center in best_coarse.items():
        reserve = (rt, rs)
        start_radius, start_step = (2.0, 0.5) if dense else (3.0, 0.75)
        speed_radius, speed_step = (2.0, 0.2) if dense else (4.0, 0.5)
        start_values = np.arange(center["start_hour"] - start_radius, center["start_hour"] + start_radius + 1e-9, start_step)
        speed_values = np.arange(max(10, center["speed_kmh"] - speed_radius), min(90, center["speed_kmh"] + speed_radius) + 1e-9, speed_step)
        refined = [evaluate(start, speed, reserve, aux_w) for start in start_values for speed in speed_values]
        cases.extend(refined)
        refined_cases += len(refined)

    optimized = [row for row in cases if row["status"] == "chegada_condicional"]
    selected_by_reserve: dict[tuple[float, float], dict] = {}
    for row in optimized:
        key = (row["reserve_traction"], row["reserve_service"])
        if key not in selected_by_reserve or row["elapsed_days"] < selected_by_reserve[key]["elapsed_days"]:
            selected_by_reserve[key] = row
    if not dense:
        for (rt, rs), selected in selected_by_reserve.items():
            for aux_w in grid["auxiliary_sweep_w"]:
                if aux_w != aux_central:
                    cases.append(evaluate(selected["start_hour"], selected["speed_kmh"], (rt, rs), aux_w))

    frame = pd.DataFrame(cases)
    output = diretorio_entregas(ROOT) / ("otimizacao_janela_missao_densa" if dense else "otimizacao_janela_missao")
    output.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output / "varredura_janela_velocidade.csv", index=False)
    feasible = frame[(frame.status == "chegada_condicional") & frame.auxiliary_traction_w_assumed.isin(optimized_aux)]
    best = []
    for keys, group in feasible.groupby(["reserve_traction", "reserve_service", "auxiliary_traction_w_assumed"]):
        selected = group.sort_values(["elapsed_days", "start_hour", "speed_kmh"]).iloc[0].to_dict()
        best.append(selected)
    summary = {
        "scenario": config["_execution"]["scenario"],
        "source_config_sha256": config["_execution"]["source_sha256"],
        "resolved_config_sha256": config["_execution"]["resolved_sha256"],
        "script": "scripts/otimizar_janela_missao.py",
        "method": "grade partida 2h/velocidade 2kmh; refinamento local partida 0,5h/velocidade 0,2kmh" if dense else "grade partida 3h/velocidade 4kmh; refinamento local partida 0,75h/velocidade 0,5kmh; sensitividades auxiliares avaliadas na política central",
        "time_step_h": dt,
        "driving_window_h": 8,
        "auxiliary_traction_w_optimized": optimized_aux,
        "coarse_cases": len(coarse_starts) * len(coarse_speeds) * len(grid["reserves"]) * len(optimized_aux),
        "refined_cases": refined_cases,
        "rows_total": len(frame),
        "hypothetical_dc_interface": True,
        "physical_mission_demonstrated": False,
        "global_optimum_claimed": False,
        "best_by_reserve_and_auxiliary": best,
        "auxiliary_sensitivities_at_selected_policy": [
            row for row in cases if row["auxiliary_traction_w_assumed"] != aux_central
        ],
        "max_abs_energy_residual_kwh": float(frame.energy_residual_kwh.abs().max()),
    }
    (output / "resumo.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(frame), "best": best}, ensure_ascii=False))


def key_hour(start: float) -> float:
    return round(start % 24, 4)


if __name__ == "__main__":
    main()
