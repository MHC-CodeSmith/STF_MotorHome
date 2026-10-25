"""Reservas de ocupação autorais no retângulo OEM; sem alegar montagem aprovada."""

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import yaml
from matplotlib.patches import Rectangle


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config', type=Path, required=True)
    p.add_argument('--destino', type=Path, required=True)
    args = p.parse_args()
    c = yaml.safe_load(args.config.read_text())
    length, width, height = c['cargo_m']
    zones = c['floor_zones']
    for z in zones:
        if (min(z['x_m'], z['y_m']) < 0 or min(z['length_m'], z['width_m'], z['height_m']) <= 0
                or z['x_m']+z['length_m'] > length+1e-9
                or z['y_m']+z['width_m'] > width+1e-9 or z['height_m'] > height):
            raise ValueError(f'Reserva fora do retângulo máximo OEM: {z["id"]}')
    for i, a in enumerate(zones):
        for b in zones[i+1:]:
            dx = min(a['x_m']+a['length_m'], b['x_m']+b['length_m'])-max(a['x_m'], b['x_m'])
            dy = min(a['y_m']+a['width_m'], b['y_m']+b['width_m'])-max(a['y_m'], b['y_m'])
            if dx > 1e-8 and dy > 1e-8:
                raise ValueError(f'Reservas se sobrepõem: {a["id"]} / {b["id"]}')
    roof = c['roof']
    roof_end = roof['start_x_m']+roof['modules']*roof['module_length_x_m']+(roof['modules']-1)*roof['gap_m']
    if roof_end > length or roof['module_width_y_m'] > width:
        raise ValueError('Módulos não cabem no retângulo de referência')
    args.destino.mkdir(parents=True, exist_ok=False)
    fig, axes = plt.subplots(2, 1, figsize=(11, 8), layout='constrained')
    labels = ['Cama longitudinal\n1,95 × 1,35 m\nlava-seca/HVAC sob estrado', 'Geladeira / pia\nindução elétrica', 'Banheiro\n0,90 × 0,70 m\nH 1,80 m', 'Mesa\nrebatível']
    colors = ['#b6d7a8', '#f4c99b', '#a2c4c9', '#c9b8d9']
    for z, label, color in zip(zones, labels, colors):
        axes[0].add_patch(Rectangle((z['x_m'], z['y_m']), z['length_m'], z['width_m'], facecolor=color, edgecolor='black'))
        axes[0].text(z['x_m']+z['length_m']/2, z['y_m']+z['width_m']/2, label, ha='center', va='center', fontsize=9)
    axes[0].text(2.55, .855, 'Corredor\n0,48 m', ha='center', va='center', fontsize=9)
    for i in range(roof['modules']):
        x = roof['start_x_m']+i*(roof['module_length_x_m']+roof['gap_m'])
        y = (width-roof['module_width_y_m'])/2
        axes[1].add_patch(Rectangle((x, y), roof['module_length_x_m'], roof['module_width_y_m'], facecolor='#274d75', edgecolor='black'))
        axes[1].text(x+roof['module_length_x_m']/2, width/2, 'JA Solar\n450 W\n22 kg', ha='center', va='center', color='white')
    cab = roof['cab_module']
    axes[1].add_patch(Rectangle((cab['start_x_m'], (width-cab['width_y_m'])/2), cab['length_x_m'], cab['width_y_m'], facecolor='#497598', edgecolor='black'))
    axes[1].text(cab['start_x_m']+cab['length_x_m']/2, width/2, 'Victron\n190 W\n10,5 kg', color='white', ha='center', va='center', fontsize=9)
    axes[1].axvline(length, color='gray', ls='--', alpha=.8)
    for ax, title in zip(axes, ['Planta de integração: cama elevada, itens identificados e mesa rebatível', 'Teto: 1540 W expostos recolhidos; até2890 W com extensão aberta (não desenhada nesta planta)']):
        ax.add_patch(Rectangle((0, 0), length, width, fill=False, linewidth=2))
        ax.set(xlim=(-.1, length+.1), ylim=(-.1, width+.1), aspect='equal', xlabel='X — traseira → cabine [m]', ylabel='Y [m]', title=title)
    axes[1].set_xlim(-.1, cab['start_x_m']+cab['length_x_m']+.1)
    fig.suptitle('Aurora Solar — estudo preliminar para duas pessoas\nEnvelope máximo OEM; caixas de roda, acabamentos e fixações ainda precisam de conferência')
    fig.savefig(args.destino/'layout_proposto.png', dpi=160)
    plt.close(fig)
    report = {'status': c['status'], 'config_sha256': hashlib.sha256(args.config.read_bytes()).hexdigest(),
              'script': 'scripts/gerar_layout_proposto.py', 'zones': zones,
              'no_rectangle_overlap': True, 'roof_modules_rectangular_fit': True,
              'roof_length_occupied_m': roof_end-roof['start_x_m'],
              'height_increment_support_and_module_m': roof['support_height_m']+roof['module_thickness_m'],
              'verified_interference_free_vehicle': False, 'assumptions': c['assumptions']}
    (args.destino/'resumo_layout.json').write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
