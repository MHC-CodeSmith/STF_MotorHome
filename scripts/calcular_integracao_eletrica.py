"""Orçamento incremental e estimativas elétricas condicionadas da habitação."""

import argparse
import hashlib
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))

from motorhome.integracao_eletrica import analisar


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--destino', type=Path, required=True)
    p.add_argument('--solar', type=Path, default=Path('entregas/parcial_2026-10-24/resumo_expansao_solar.json'))
    a = p.parse_args()
    paths = [Path('config')/name for name in ['instalacoes_eletricas_proposta.yaml', 'equipamentos_interior.yaml']]
    e, i = [yaml.safe_load(path.read_text()) for path in paths]
    budget_path = Path('entregas/parcial_2026-10-24/orcamento_massa_parcial.json')
    budget = json.loads(budget_path.read_text())
    base_mass = (budget['oem_without_driver_kg']+sum(item['mass_kg'] or 0 for item in i['items'])
                 +budget['assumed_two_occupants_kg']+budget['assumed_total_water_kg']+budget['roof_fixed_estimate_kg'])
    expansion_path = a.solar
    expansion = json.loads(expansion_path.read_text())
    result = analisar(e, i)
    if result['equipment_pair_overlaps']:
        raise ValueError(result['equipment_pair_overlaps'])
    # Cabos de serviços apenas: resistividade/temperatura/comprimento são hipóteses.
    # Não substitui campo de temperatura multidimensional do cabo de tração I30.
    cases = []
    for v in [44.8, 51.2, 56.8]:
        for temp in [20, 60, 90]:
            current = 4000/(.90*v)
            resistance = 1.724e-8*(1+.00393*(temp-20))*4/(70e-6)
            cases.append({'battery_terminal_v': v, 'assumed_copper_temp_c': temp,
                          'current_a': current, 'two_pole_total_cable_length_m': 4,
                          'cross_section_mm2': 70, 'resistance_ohm': resistance,
                          'voltage_drop_v': current*resistance,
                          'joule_w': current**2*resistance})
    result.update(script='scripts/calcular_integracao_eletrica.py',
                  source_revision=e['revision'],
                  services_cable_sensitivity=cases,
                  cable_assumptions={'copper_rho20_ohm_m': 1.724e-8, 'copper_alpha_per_k': .00393,
                                     'inverter_efficiency_assumed': .90, 'ac_active_power_w': 4000,
                                     'not_measured_cable_properties': True},
                  service_useful_energy_at_assumed_80pct_dod_kwh=8.192,
                  autonomy_days_assumed_house_load_excluding_drying=8.192/expansion['household_total_excluding_dryer_kwh_day'],
                  autonomy_note='Quociente de energia DC/consumo agregado anterior, antes de perdas/standby; não autonomia AC ou da missão.',
                  base_known_mass_subtotal_kg=base_mass,
                  new_known_mass_subtotal_kg=base_mass+result['known_added_service_mass_kg'],
                  gross_limit_kg=4250,
                  unallocated_mass_kg=4250-base_mass-result['known_added_service_mass_kg'],
                  mass_budget_note='Subtotal conhecido/assumido; faltam móveis, suportes elétricos, quadro, cabos, tubos, fixações, bagagem, massas de itens sem ficha. Não massa final nem carga de eixos.',
                  inputs_sha256={str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in [*paths, budget_path, expansion_path]})
    a.destino.mkdir(parents=True, exist_ok=False)
    (a.destino/'resumo_integracao_eletrica.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'services_cable_sensitivity'}, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
