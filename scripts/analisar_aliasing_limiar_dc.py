"""Diagnose interval aliasing at the hypothetical minimum-DC-power threshold.

Compares the existing all-or-zero interval gate against exact threshold-crossing
integration of a piecewise-linear 1-minute clear-sky PV profile. This is a
numerical integration diagnostic, not an EVSE behavior or mission prediction.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from motorhome.cenarios import carregar_configuracao
from motorhome.solar import simular_dia

DATES = ("2026-03-20", "2026-06-21", "2026-09-22", "2026-12-21")
STEPS_MIN = (1, 5, 15, 30, 60)
DRIVE_START_H = 18.0
DRIVE_WINDOW_H = 8.0
PORTABLE_TILT_DEG = 45.0
PORTABLE_AZIMUTH_DEG = 0.0


def integrate_linear_above_threshold_kwh(y0_kw: float, y1_kw: float,
                                         duration_h: float,
                                         threshold_kw: float) -> float:
    """Integrate linearly interpolated power only where it reaches threshold."""
    values = (y0_kw, y1_kw, duration_h, threshold_kw)
    if not all(np.isfinite(x) for x in values):
        raise ValueError("inputs must be finite")
    if duration_h <= 0 or threshold_kw < 0:
        raise ValueError("duration must be positive and threshold nonnegative")
    a, b, threshold = y0_kw, y1_kw, threshold_kw
    if a >= threshold and b >= threshold:
        return 0.5 * (a + b) * duration_h
    if a < threshold and b < threshold:
        return 0.0
    if a < threshold <= b:
        above_fraction = (b - threshold) / (b - a)
        return 0.5 * (threshold + b) * above_fraction * duration_h
    above_fraction = (a - threshold) / (a - b)
    return 0.5 * (threshold + a) * above_fraction * duration_h


def interval_gate_energy_kwh(y0_kw: float, y1_kw: float, duration_h: float,
                             threshold_kw: float, efficiency: float) -> float:
    """Existing policy: pass full interval surplus iff its mean clears threshold."""
    if not 0 < efficiency <= 1:
        raise ValueError("efficiency must be in (0, 1]")
    mean_power = 0.5 * (y0_kw + y1_kw)
    return mean_power * duration_h * efficiency if mean_power >= threshold_kw else 0.0


def main() -> None:
    os.environ["MOTORHOME_SCENARIO"] = "maxeon1540_independente"
    config = carregar_configuracao(ROOT)
    p = {key: value["value"] for key, value in config["parameters"].items()}
    grid = config["development"]["mission_grid"]
    threshold_kw = float(grid["hypothetical_min_dc_kw"])
    eta_dc = float(p["eta_dc"])
    service_kwh_day = sum(
        load["energy_ac_or_dc_kwh_day"]["base"]
        / (p["eta_inverter"] if load["side"] == "AC" else p["eta_lv"])
        for load in config["loads"]
    ) + p["inverter_idle_w"] * 24 / 1000
    service_kw = service_kwh_day / 24

    template = yaml.safe_load((ROOT / "config/solar_proposta.yaml").read_text())
    template["scenario"].update(
        latitude_deg=p["latitude_deg"], longitude_deg=p["longitude_deg"],
        altitude_m=p["altitude_m"], ambient_temperature_c=p["ambient_c"],
        wind_speed_m_s=p["wind_m_s"], relative_humidity_percent=p["rh_percent"],
    )
    template["array"].update(
        module_counts=[1], tilt_deg=0, azimuth_deg=0, albedo=p["pv_albedo"]
    )
    template["assumptions"].update(
        converter_efficiency=1, other_losses_fraction=p["pv_other_loss"],
        faiman_u0_w_m2k=p["pv_faiman_u0"], faiman_u1_w_s_m3k=p["pv_faiman_u1"],
    )

    rows: list[dict[str, object]] = []
    for date in DATES:
        template["scenario"]["date"] = date
        roof_cfg = yaml.safe_load(yaml.safe_dump(template))
        roof_cfg["module"].update(
            p_stc_w=p["roof_power_48v_study_wp"], gamma_pdc_per_k=p["pv_gamma"]
        )
        roof_w = simular_dia(roof_cfg, 1)["terminal_assumed_1_modules_w"].to_numpy()
        portable_cfg = yaml.safe_load(yaml.safe_dump(template))
        portable_cfg["array"].update(
            tilt_deg=PORTABLE_TILT_DEG, azimuth_deg=PORTABLE_AZIMUTH_DEG
        )
        portable_cfg["module"].update(
            p_stc_w=p["portable_wp"], gamma_pdc_per_k=p["portable_gamma"]
        )
        portable_w = simular_dia(portable_cfg, 1)["terminal_assumed_1_modules_w"].to_numpy()
        if len(roof_w) != 1441 or len(portable_w) != 1441:
            raise ValueError("1-minute profile must include 1440 intervals and both endpoints")

        for step_min in STEPS_MIN:
            stride = step_min
            dt_h = step_min / 60
            for i in range(0, 1440, stride):
                mid_h = (i + 0.5 * stride) / 60
                driving = (mid_h - DRIVE_START_H) % 24 < DRIVE_WINDOW_H
                since_park = (mid_h - (DRIVE_START_H + DRIVE_WINDOW_H)) % 24
                portable_usable = (
                    not driving
                    and since_park >= p["pv_setup_h"]
                    and since_park < 24 - DRIVE_WINDOW_H - p["pv_teardown_h"]
                )
                port0 = portable_w[i] if portable_usable else 0.0
                port1 = portable_w[i + stride] if portable_usable else 0.0
                pv0_kw = (roof_w[i] + port0) / 1000
                pv1_kw = (roof_w[i + stride] + port1) / 1000
                surplus0 = pv0_kw - service_kw
                surplus1 = pv1_kw - service_kw
                if driving:
                    continue
                rows.append({
                    "date": date, "step_min": step_min, "interval_index": i // stride,
                    "portable_usable": portable_usable,
                    "pv_start_kw": pv0_kw, "pv_end_kw": pv1_kw,
                    "service_power_uniform_kw_assumed": service_kw,
                    "surplus_start_kw": surplus0, "surplus_end_kw": surplus1,
                    "minimum_dc_output_kw_hypothetical": threshold_kw,
                    "minimum_dc_input_kw_hypothetical": threshold_kw / eta_dc,
                    "existing_interval_gate_energy_kwh": interval_gate_energy_kwh(
                        surplus0, surplus1, dt_h, threshold_kw / eta_dc, eta_dc
                    ),
                    "linear_threshold_integral_energy_kwh": eta_dc
                    * integrate_linear_above_threshold_kwh(
                        surplus0, surplus1, dt_h, threshold_kw / eta_dc
                    ),
                    "solar_energy_kwh": 0.5 * (pv0_kw + pv1_kw) * dt_h,
                    "driving": False,
                })

    frame = pd.DataFrame(rows)
    out = ROOT / "entregas/integrado_maxeon1540/otimizacao_resolucao_temporal/aliasing_limiar_dc"
    out.mkdir(parents=True, exist_ok=True)
    frame.to_csv(out / "intervalos.csv", index=False, lineterminator="\n")
    daily_rows = []
    for date, group in frame.groupby("date", sort=True):
        reference = float(group.loc[group.step_min == 1,
                                    "linear_threshold_integral_energy_kwh"].sum())
        for step, data in group.groupby("step_min", sort=True):
            current = float(data.existing_interval_gate_energy_kwh.sum())
            daily_rows.append({
                "date": date, "step_min": int(step),
                "intervals": len(data),
                "existing_interval_gate_dc_kwh": current,
                "piecewise_linear_threshold_reference_dc_kwh": reference,
                "difference_current_minus_reference_kwh": current - reference,
                "relative_difference_current_percent": (
                    100 * (current - reference) / reference if reference else None
                ),
                "reference_1min_profile_energy_kwh": float(data.solar_energy_kwh.sum()),
            })
    daily = pd.DataFrame(daily_rows)
    daily.to_csv(out / "resumo_por_data_passo.csv", index=False, lineterminator="\n")
    summary = {
        "scenario": config["_execution"]["scenario"],
        "source_config_sha256": config["_execution"]["source_sha256"],
        "resolved_config_sha256": config["_execution"]["resolved_sha256"],
        "script": "scripts/analisar_aliasing_limiar_dc.py",
        "dates": DATES, "steps_min": STEPS_MIN,
        "drive_start_h_assumed": DRIVE_START_H,
        "drive_window_h_assumed": DRIVE_WINDOW_H,
        "roof_wp_assumed": p["roof_power_48v_study_wp"],
        "portable_wp_assumed": p["portable_wp"],
        "portable_tilt_deg_assumed": PORTABLE_TILT_DEG,
        "portable_azimuth_deg_assumed": PORTABLE_AZIMUTH_DEG,
        "service_kwh_day_assumed": service_kwh_day,
        "service_load_uniform_kw_assumed": service_kw,
        "minimum_dc_output_kw_hypothetical": threshold_kw,
        "dc_efficiency_assumed": eta_dc,
        "intervals_non_driving": len(frame),
        "method": "the current all-or-zero per-interval minimum-power gate compared with threshold-crossing integration over linearly interpolated 1-minute clear-sky PV endpoints",
        "linear_1min_curve_is_physical_truth": False,
        "physical_charger_behavior_demonstrated": False,
        "physical_mission_demonstrated": False,
        "global_optimum_claimed": False,
        "limits": [
            "Minimum DC output is hypothetical and has no OEM authorization.",
            "Clear-sky modeled PV is not measured weather; clouds and shade are absent.",
            "The study applies the existing 18:00-02:00 driving window and 45-degree portable-panel hypothesis.",
            "The service load is spread uniformly over 24 hours; real timing and battery state coupling are not represented in this diagnostic.",
            "The piecewise-linear reference is an integration benchmark from a 1-minute model profile, not observed charger response or a physical upper/lower bound.",
            "No mission duration is recalculated; results diagnose numerical threshold sensitivity only.",
        ],
        "configuration_file_sha256": hashlib.sha256(
            (ROOT / "config/parametros_globais.yaml").read_bytes()
        ).hexdigest(),
        "daily_results": daily.to_dict("records"),
    }
    (out / "resumo.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    pivot = daily.pivot(index="step_min", columns="date",
                        values="difference_current_minus_reference_kwh")
    fig, ax = plt.subplots(figsize=(8.0, 4.8), layout="constrained")
    for date in pivot.columns:
        ax.plot(pivot.index, pivot[date], marker="o", linewidth=2, label=date)
    ax.axhline(0, color="#333333", linewidth=1)
    ax.set(
        title="I29: aliasing do mínimo DC pela duração do intervalo",
        xlabel="Duração do intervalo [min]",
        ylabel="Energia aceita pela regra atual − referência linear [kWh/dia]",
    )
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, title="Dia de céu limpo")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.text(
        0.5, -0.01,
        "Referência integra os cruzamentos de 1 kW de saída em perfil PV modelado a 1 min; "
        "não representa carregador nem clima medidos.",
        ha="center", fontsize=8,
    )
    fig.savefig(out / "aliasing_limiar_dc.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(json.dumps({
        "intervals": len(frame), "daily_comparisons": len(daily),
        "max_abs_difference_kwh_day": float(
            daily.difference_current_minus_reference_kwh.abs().max()
        ),
        "output": str(out.relative_to(ROOT)),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
