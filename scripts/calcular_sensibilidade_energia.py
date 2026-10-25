"""Curvas I21/22/25/26 condicionadas, sem alegar autonomia máxima resolvida."""

import argparse
import csv
import hashlib
import json
import sys
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import yaml

from motorhome.dinamica import forca_aerodinamica, forca_rolamento
from motorhome.sistemas_termicos import numero


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config', type=Path, required=True)
    p.add_argument('--solar', type=Path, required=True)
    p.add_argument('--destino', type=Path, required=True)
    args = p.parse_args()
    c = yaml.safe_load(args.config.read_text())
    solar = json.loads(args.solar.read_text())
    if c['status'] != 'ESTIMATIVA_CONDICIONADA_NAO_VALIDADA':
        raise ValueError('Esta rotina não publica resultados finais')
    for name in ['mass_kg', 'frontal_area_m2', 'air_density_kg_m3']:
        numero(c[name], name, 0, True)
    numero(c['driving_auxiliary_power_w'], 'auxiliares', 0)
    rows = []
    for cd, cr, eta in product(c['drag_coefficients'], c['rolling_coefficients'], c['traction_efficiencies']):
        numero(cd, 'Cd', 0)
        numero(cr, 'Cr', 0)
        if not 0 < eta <= 1:
            raise ValueError('Eficiência inválida')
        for kmh in c['speed_km_h']:
            numero(kmh, 'velocidade', 0, True)
            v = kmh/3.6
            aero = forca_aerodinamica(c['air_density_kg_m3'], cd, c['frontal_area_m2'], v)
            roll = forca_rolamento(cr, c['mass_kg'])
            wheels = (aero+roll)*v
            terminal = wheels/eta+c['driving_auxiliary_power_w']
            efficiency = kmh/(terminal/1000)
            row = {'speed_km_h': kmh, 'cd_pilot': cd, 'cr_assumed': cr, 'eta_assumed': eta,
                   'aerodynamic_force_n': aero, 'rolling_force_n': roll, 'wheel_power_w': wheels,
                   'battery_terminal_power_w': terminal, 'km_per_kwh': efficiency}
            for n in ['2', '3']:
                row[f'solar_only_assumed_{n}_panels_km'] = solar['arrays'][n]['terminal_energy_assumed_kwh']*efficiency
            rows.append(row)
    args.destino.mkdir(parents=True, exist_ok=False)
    out = args.destino
    with (out/'sensibilidade.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n'); w.writeheader(); w.writerows(rows)
    fig, axes = plt.subplots(2, 1, figsize=(10, 8), layout='constrained')
    speeds = np.array(c['speed_km_h'])
    for col, ax, label in [('km_per_kwh', axes[0], 'km/kWh na bateria'),
                           ('solar_only_assumed_2_panels_km', axes[1], 'Distância com solar do dia [km]')]:
        vals = np.array([[r[col] for r in rows if r['speed_km_h'] == s] for s in speeds])
        ax.fill_between(speeds, vals.min(axis=1), vals.max(axis=1), color='#9fc2da', alpha=.65, label='Faixa de hipóteses Cd/Cr/eta')
        ax.plot(speeds, np.median(vals, axis=1), color='#255e84', label='Mediana da grade, não valor aprovado')
        ax.set(xlabel='Velocidade constante [km/h]', ylabel=label)
        ax.legend(); ax.grid(alpha=.3)
    fig.suptitle('Aurora Solar — sensibilidade provisória\nMassa-cenário 4250 kg; auxiliares assumidos 800 W; sem validação física')
    fig.savefig(out/'sensibilidade_energia.png', dpi=160)
    plt.close(fig)
    summary = {'status': c['status'], 'script': 'scripts/calcular_sensibilidade_energia.py',
               'config_sha256': hashlib.sha256(args.config.read_bytes()).hexdigest(),
               'solar_sha256': hashlib.sha256(args.solar.read_bytes()).hexdigest(), 'assumptions': c,
               'scenario_count': len(rows), 'official_vehicle_results': False,
               'urban_road_ranges': {str(speed): {col: [min(r[col] for r in rows if r['speed_km_h'] == speed),
                                                       max(r[col] for r in rows if r['speed_km_h'] == speed)]
                                                 for col in ['km_per_kwh', 'solar_only_assumed_2_panels_km']}
                                     for speed in [40, 80]},
               'trip_optimized': False, 'item27_optimized_vehicle': False}
    (out/'resumo_sensibilidade.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(json.dumps(summary['urban_road_ranges'], ensure_ascii=False))


if __name__ == '__main__':
    main()
