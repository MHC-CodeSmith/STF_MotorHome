"""Item 32: carga de A/C com proteção solar interna no para-brisa.

Reaproveita o balanço do I32 (`cabine_31_32_reexecutada.json`) e o acoplamento da vazão
de CO2 (`ventilacao_mecanica_sensibilidade/resumo.json`). Só o ganho pelo vidro frontal
muda: com a cortina fechada ele é multiplicado pelo IAC.
"""
import argparse
import csv
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "config/protecao_solar_cabine.yaml")
    parser.add_argument("--destino", type=Path,
                        default=ROOT / "entregas/integrado_maxeon1560/i32_protecao_solar")
    args = parser.parse_args()
    cfg = yaml.safe_load(args.config.read_text())
    cabine = json.loads(
        (ROOT / "entregas/etapa_pos_dec061/cabine_31_32_reexecutada.json").read_text())
    ventilacao = json.loads(
        (ROOT / "entregas/integrado_maxeon1560/ventilacao_mecanica_sensibilidade/resumo.json")
        .read_text())["hvac_ventilation_coupling"]["design_flow_occupant_cases"]
    frente = next(s for s in cabine["surfaces"] if s["surface"] == "front")
    ganho_parabrisa = frente["noon_glass_solar_gain_w"]
    capacidade = cfg["capacity_claim_w"]

    casos = []
    for v in ventilacao:
        base_30 = v["baseline_hvac_demand_w_at_30m3h"]
        demandas = {
            "30 m3/h": (30.0, base_30),
            "CO2 1000 ppm": (v["co2_balance_flow_m3_h"], v["updated_hvac_demand_w"]),
        }
        for nome, (vazao, demanda) in demandas.items():
            for iac in [1.0, *cfg["iac"]["sweep"]]:
                reducao = ganho_parabrisa * (1 - iac)
                total = demanda - reducao
                casos.append({
                    "occupants": v["occupants"],
                    "ventilation_case": nome,
                    "fresh_air_m3_h": vazao,
                    "iac": iac,
                    "windshield_gain_w": ganho_parabrisa * iac,
                    "cooling_required_w": total,
                    "margin_w": capacidade - total,
                })

    args.destino.mkdir(parents=True, exist_ok=True)
    with (args.destino / "casos.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, list(casos[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(casos)

    def caso(pessoas, ventil, iac):
        return next(c for c in casos if c["occupants"] == pessoas
                    and c["ventilation_case"] == ventil and c["iac"] == iac)

    projeto = [c for c in casos if c["occupants"] == 2
               and c["ventilation_case"] == "CO2 1000 ppm"]
    com_protecao = [c for c in projeto if c["iac"] < 1]
    resumo = {
        "script": "scripts/calcular_i32_protecao_parabrisa.py",
        "device": cfg["device"]["model"],
        "windshield_glass_area_m2": frente["glass_area_m2"],
        "windshield_noon_poa_w_m2": frente["noon_poa_w_m2"],
        "windshield_gain_unshaded_w": ganho_parabrisa,
        "windshield_share_of_design_load": ganho_parabrisa / caso(2, "CO2 1000 ppm", 1.0)[
            "cooling_required_w"],
        "design_case_unshaded_w": caso(2, "CO2 1000 ppm", 1.0)["cooling_required_w"],
        "design_case_nominal_iac_w": caso(2, "CO2 1000 ppm", cfg["iac"]["nominal"])[
            "cooling_required_w"],
        "design_case_range_w": [min(c["cooling_required_w"] for c in com_protecao),
                                max(c["cooling_required_w"] for c in com_protecao)],
        "design_margin_range_w": [min(c["margin_w"] for c in com_protecao),
                                  max(c["margin_w"] for c in com_protecao)],
        "all_shaded_cases_within_capacity_claim": all(c["margin_w"] > 0 for c in com_protecao),
        "iac_nominal": cfg["iac"]["nominal"],
        "iac_sweep": cfg["iac"]["sweep"],
        "capacity_claim_w": capacidade,
        "operation": cfg["operation"],
        "capacity_at_33c_25c_demonstrated": False,
        "product_iac_measured": False,
    }
    (args.destino / "resumo.json").write_text(
        json.dumps(resumo, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(resumo, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
