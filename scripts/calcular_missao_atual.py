"""I25/I26/I29: energia do teto atual e limites necessários, sem alegar ótimo."""

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import yaml


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--destino', type=Path, required=True)
    args = p.parse_args()
    inputs = [Path('config/energia_sensibilidade.yaml'), Path('config/limites_operacionais_proposta.yaml'),
              Path('entregas/parcial_2026-10-24/resumo_expansao_solar.json')]
    e, limit = [yaml.safe_load(f.read_text()) for f in inputs[:2]]
    solar = json.loads(inputs[2].read_text())
    print('Campos de geração:', [k for k in solar if 'kwh' in k.lower() or 'energy' in k.lower()])
    args.destino.mkdir(parents=True, exist_ok=False)
    # São explicitamente limites matemáticos nas hipóteses anteriores, não nova curva OEM.
    speeds = np.arange(20, limit['speed_limiter_km_h']+1, 1)
    rows = []
    for speed in speeds:
        v = speed/3.6
        for cd in e['drag_coefficients']:
            for cr in e['rolling_coefficients']:
                for eta in e['traction_efficiencies']:
                    force = .5*e['air_density_kg_m3']*cd*e['frontal_area_m2']*v*v+cr*e['mass_kg']*9.80665
                    power = force*v/eta+e['driving_auxiliary_power_w']
                    rows.append({'speed_km_h': int(speed), 'cd_assumed': cd, 'cr_assumed': cr,
                                 'eta_assumed': eta, 'force_n': force, 'wheel_power_w': force*v,
                                 'battery_power_w': power, 'battery_km_kwh': speed/(power/1000)})
    with (args.destino/'consumo_velocidades.csv').open('w') as f:
        w = csv.DictWriter(f, list(rows[0]), lineterminator='\n'); w.writeheader(); w.writerows(rows)
    # A leitura dos campos de geração é explícita para impedir misturar cenários históricos.
    fixed = solar['energy_kwh']['mixed_stowed_w']
    house = solar['household_total_excluding_dryer_kwh_day']
    generation = {'fixed': fixed,
                  'extension_shading_geometric': solar['energy_kwh']['mixed_open_geometric_beam_shading_w'],
                  'extension_lower_string_disabled': solar['energy_kwh']['mixed_open_lower_string_off_if_shaded_w']}
    budget = []
    for layout, energy in generation.items():
        for house_eff in [.85, .9, .95, 1.]:
            net = energy-house/house_eff
            best = max(row['battery_km_kwh'] for row in rows)
            initial = 98+8.192
            # Necessário: D >= (E_viagem_min-E_inicial)/saldo_diario se saldo>0.
            min_energy = 7000/best
            necessary = max(0., (min_energy-initial)/net) if net > 0 else None
            budget.append({'layout': layout, 'pv_kwh_day': energy, 'house_consumption_kwh_day': house,
                           'aggregate_house_efficiency_assumed': house_eff, 'daily_surplus_before_traction_conversion_kwh': net,
                           'best_battery_km_kwh_in_grid': best, 'optimistic_initial_usable_kwh': initial,
                           'necessary_days_energy_lower_bound': necessary,
                           '7000km_energy_infeasible_in_repeated_day_model': bool(net <= 0 and min_energy > initial)})
    with (args.destino/'balanco_missao.csv').open('w') as f:
        w = csv.DictWriter(f, list(budget[0]), lineterminator='\n'); w.writeheader(); w.writerows(budget)
    curves = []
    for speed in [40, 80]:
        sub = [r for r in rows if r['speed_km_h'] == speed]
        curves.append({'speed_km_h': speed, 'battery_km_kwh_min': min(r['battery_km_kwh'] for r in sub),
                       'battery_km_kwh_max': max(r['battery_km_kwh'] for r in sub),
                       'fixed_pv_only_distance_km_min': fixed*min(r['battery_km_kwh'] for r in sub),
                       'fixed_pv_only_distance_km_max': fixed*max(r['battery_km_kwh'] for r in sub)})
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), layout='constrained')
    low = [min(r['battery_km_kwh'] for r in rows if r['speed_km_h'] == speed) for speed in speeds]
    high = [max(r['battery_km_kwh'] for r in rows if r['speed_km_h'] == speed) for speed in speeds]
    axes[0].fill_between(speeds, low, high, alpha=.3)
    axes[0].set(xlabel='Velocidade (km/h)', ylabel='km/kWh na bateria', title='I26 • grade condicionada até limite OEM')
    axes[1].fill_between(speeds, np.array(low)*fixed, np.array(high)*fixed, alpha=.3)
    axes[1].set(xlabel='Velocidade (km/h)', ylabel='Distância (km)', title='I25 • solar fixo do dia, antes da habitação')
    for ax in axes:
        ax.grid(alpha=.2)
    fig.savefig(args.destino/'autonomia_teto_atual.png', dpi=160); plt.close(fig)
    summary = {'status': 'LIMITES_CONDICIONADOS_NAO_AGENDA_OTIMA', 'generated_utc': datetime.now(timezone.utc).isoformat(),
               'case_40_80': curves, 'mission_daily_budgets': budget, 'speed_limit_km_h': limit['speed_limiter_km_h'],
               'notes': ['98kWh tração+8,192kWh de serviços compartilhados idealmente só para limite otimista; interligação não demonstrada.',
                         'Perdas da habitação são sensibilidades agregadas; auxiliares de tração800W ainda independentes, sem descontar suposta sobreposição.',
                         'Limite necessário de energia não é agenda, mínimo global ou previsão da rota; não inclui limite de8h/dia ou instalação da extensão.',
                         'Dia claro21jun repetido; expansão excede referência de teto na hipótese empilhada. Não arquitetura aprovada.',
                         'I25 antes da habitação mostra limite superior solar-only, não energia realmente disponível ao motor.',
                         'I27/I29 anteriores continuam históricos; este arquivo não substitui suas agendas por ótimo inventado.'],
               'inputs_sha256': {str(f): hashlib.sha256(f.read_bytes()).hexdigest() for f in [*inputs, Path(__file__)]}}
    (args.destino/'resumo_missao_atual.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps(curves, indent=2))


if __name__ == '__main__':
    main()
