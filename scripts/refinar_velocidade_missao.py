"""Refinamento local de velocidade para o I29, sem alegar ótimo global.

Mantém a política temporal líder (20:00–04:00), alocação flexível e carga DC
direta hipotética. Busca por varredura de 1 km/h e refinamento de 0,1 km/h.
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


def main():
    os.environ["MOTORHOME_SCENARIO"] = "maxeon1540_independente"
    c = carregar_configuracao(ROOT)
    out = diretorio_entregas(ROOT) / "otimizacao_refinada_velocidade"
    out.mkdir(parents=True, exist_ok=True)
    p = {k: v["value"] for k, v in c["parameters"].items()}
    grid = c["development"]["mission_grid"]
    base = yaml.safe_load((ROOT / "config/solar_proposta.yaml").read_text())
    base["scenario"].update(
        date=p["reference_day"], latitude_deg=p["latitude_deg"],
        longitude_deg=p["longitude_deg"], altitude_m=p["altitude_m"],
        ambient_temperature_c=p["ambient_c"], wind_speed_m_s=p["wind_m_s"],
        relative_humidity_percent=p["rh_percent"],
    )
    base["module"].update(
        p_stc_w=p["roof_power_48v_study_wp"], gamma_pdc_per_k=p["pv_gamma"],
    )
    base["array"].update(module_counts=[1], tilt_deg=0, azimuth_deg=0, albedo=p["pv_albedo"])
    base["assumptions"].update(
        converter_efficiency=1, other_losses_fraction=p["pv_other_loss"],
        faiman_u0_w_m2k=p["pv_faiman_u0"], faiman_u1_w_s_m3k=p["pv_faiman_u1"],
    )
    roof_power = simular_dia(base, 15)["terminal_assumed_1_modules_w"].to_numpy()
    roof = (roof_power[:-1] + roof_power[1:]) / 2000
    portable_candidates = []
    for tilt, azimuth in itertools.product(range(0, 76, 15), [0, 90, 180, 270]):
        candidate = copy.deepcopy(base)
        candidate["array"].update(tilt_deg=tilt, azimuth_deg=azimuth)
        candidate["module"].update(
            p_stc_w=p["portable_wp"], gamma_pdc_per_k=p["portable_gamma"],
        )
        watts = simular_dia(candidate, 15)["terminal_assumed_1_modules_w"].to_numpy()
        curve = (watts[:-1] + watts[1:]) / 2000
        portable_candidates.append((tilt, azimuth, curve))

    dt = 0.25
    hours = np.arange(96) * dt + dt / 2
    start, window = 20, 8
    driving = (hours - start) % 24 < window
    since_park = (hours - (start + window)) % 24
    usable = (~driving) & (since_park >= p["pv_setup_h"]) & (
        since_park < 24 - window - p["pv_teardown_h"]
    )
    tilt, azimuth, portable_curve = max(
        portable_candidates,
        key=lambda item: float((item[2] * usable).sum()),
    )
    portable = portable_curve * usable
    ac = sum(x["energy_ac_or_dc_kwh_day"]["base"] for x in c["loads"] if x["side"] == "AC")
    dc = sum(x["energy_ac_or_dc_kwh_day"]["base"] for x in c["loads"] if x["side"] == "DC")
    service_day = ac / p["eta_inverter"] + dc / p["eta_lv"] + p["inverter_idle_w"] * 24 / 1000

    def evaluate(speed, reserve, aux_w):
        consumption = consumo_plano(
            speed, p["assembled_typical_mass_kg"], p["cd_range"][1],
            p["area_m2"], p["crr_range"][1], p["rho_range"][1],
            p["eta_traction_range"][1], aux_traction_kw=aux_w / 1000,
        )
        result = simular_missao(
            roof.tolist(), portable.tolist(), driving.tolist(),
            speed_kmh=float(speed), kwh_km=consumption["kwh_km"],
            service_kwh_day=service_day, traction_capacity_kwh=p["traction_usable_kwh"],
            service_capacity_kwh=14.4, reserve_traction=reserve[0],
            reserve_service=reserve[1], mode=grid["mode"],
            min_dc_kw=grid["hypothetical_min_dc_kw"],
            max_days=grid["max_days"], eta_dc=p["eta_dc"],
        )
        result.pop("trace")
        result.pop("daily")
        return result, consumption

    rows = []
    for reserve, aux_w in itertools.product(grid["reserves"], grid["auxiliary_sweep_w"]):
        coarse = []
        for speed in np.arange(10.0, 90.0001, 1.0):
            result, consumption = evaluate(speed, reserve, aux_w)
            row = {
                "reserve_traction": reserve[0], "reserve_service": reserve[1],
                "auxiliary_traction_w_assumed": aux_w, "speed_kmh": float(speed),
                "kwh_per_km": consumption["kwh_km"], **result,
            }
            rows.append(row)
            if result["status"] == "chegada_condicional":
                coarse.append(row)
        if coarse:
            center = min(coarse, key=lambda x: x["elapsed_days"])["speed_kmh"]
            for speed in np.arange(max(10.0, center - 1), min(90.0, center + 1) + 1e-9, 0.1):
                result, consumption = evaluate(speed, reserve, aux_w)
                rows.append({
                    "reserve_traction": reserve[0], "reserve_service": reserve[1],
                    "auxiliary_traction_w_assumed": aux_w, "speed_kmh": round(float(speed), 3),
                    "kwh_per_km": consumption["kwh_km"], **result,
                })

    df = pd.DataFrame(rows)
    df.to_csv(out / "varredura_velocidade.csv", index=False)
    feasible = df[df.status == "chegada_condicional"].copy()
    best = []
    for (rt, rs, aux), group in feasible.groupby(
        ["reserve_traction", "reserve_service", "auxiliary_traction_w_assumed"]
    ):
        result = group.sort_values(["elapsed_days", "speed_kmh"]).iloc[0].to_dict()
        best.append(result)
    summary = {
        "scope": "Refinamento local de velocidade para política fixa 20:00–04:00; "
                 "não reotimiza horário/janela e não prova ótimo global.",
        "scenario": c["_execution"]["scenario"],
        "source_config_sha256": c["_execution"]["source_sha256"],
        "resolved_config_sha256": c["_execution"]["resolved_sha256"],
        "script": "scripts/refinar_velocidade_missao.py",
        "speed_domain_kmh": [10, 90],
        "coarse_step_kmh": 1.0,
        "local_refinement_step_kmh": 0.1,
        "time_step_h": dt,
        "fixed_start_h": start,
        "fixed_driving_window_h": window,
        "portable_angle_deg": {"tilt": tilt, "azimuth": azimuth},
        "hypothetical_dc_interface": True,
        "physical_mission_demonstrated": False,
        "best_by_reserve_and_auxiliary": best,
        "rows": len(df),
        "max_abs_energy_residual_kwh": float(df.energy_residual_kwh.abs().max()),
    }
    (out / "resumo.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
