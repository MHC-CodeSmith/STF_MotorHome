"""I33: disco ventilado simplificado, energia, campo r–z e convergência."""

import argparse
import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from motorhome.freios_axisimetricos import Pista, placa_analitica, resolver


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=Path('config/freios_proposta.yaml'))
    parser.add_argument('--destino', type=Path, required=True)
    args = parser.parse_args()
    config = yaml.safe_load(args.config.read_text())
    a, o, m = config['assumed'], config['official'], config['material_reference']
    p = Pista(a['inner_ring_radius_m'], config['reference_component']['diameter_m']/2,
              a['plate_thickness_m'], a['pad_track_inner_radius_m'], a['pad_track_outer_radius_m'],
              m['density_kg_m3'], m['cp_j_kgk'], m['conductivity_w_mk'])
    args.destino.mkdir(parents=True, exist_ok=False)
    defaults = {'massa_kg': a['vehicle_mass_kg'], 'fracao_eixo': a['front_axle_energy_fraction'],
                'fracao_disco': a['disc_heat_fraction'], 'fracao_regenerada': a['regeneration_fraction'],
                'duracao_s': o['braking_duration_s'], 'vi_m_s': o['initial_speed_m_s'],
                'vf_m_s': o['final_speed_m_s'], 'ambiente_k': o['initial_temperature_k'],
                'h_externo_w_m2k': a['outside_h_w_m2k'], 'h_canal_w_m2k': a['channel_h_w_m2k']}

    def run(nr=96, nz=32, dt_s=.005, **kw):
        return resolver(p, nr=nr, nz=nz, dt_s=dt_s, **(defaults | kw))

    grid = []
    for nr, nz in [(12, 4), (24, 8), (48, 16), (96, 32)]:
        r = run(nr, nz)
        grid.append({'nr': nr, 'nz': nz, 'dt_s': r['dt_real_s'],
                     'final_max_cell_k': float(r['temperatura_k'].max()),
                     'peak_surface_k': r['pico_superficie_k'], 'residual_j': r['residuo_disco_j']})
    r = run()
    temporal = []
    for dt in [.08, .04, .02, .01]:
        rt = run(dt_s=dt)
        temporal.append({'requested_dt_s': dt, 'actual_dt_s': rt['dt_real_s'],
                         'final_max_cell_k': float(rt['temperatura_k'].max()),
                         'error_to_dt005_k': float(np.max(np.abs(rt['temperatura_k']-r['temperatura_k'])))})
    analytical = []
    pa = Pista(contato_interno_m=.09, contato_externo_m=.15)
    q0 = 4250*4*30*.7*.9/4/(np.pi*(.15**2-.09**2))
    for nz in [16, 32, 64]:
        ra = resolver(pa, nr=3, nz=nz, dt_s=.002, h_externo_w_m2k=0, h_canal_w_m2k=0)
        exact = placa_analitica(.008, nz, 5, q0, 4/30)
        analytical.append({'nz': nz, 'max_error_to_series_k': float(np.max(np.abs(ra['temperatura_k'][0]-298.15-exact)))})
    sensitivity = []
    for fraction in [.6, .7, .8]:
        for disc in [.8, .9, 1.]:
            rs = run(48, 16, .02, fracao_eixo=fraction, fracao_disco=disc)
            sensitivity.append({'front_fraction': fraction, 'disc_fraction': disc,
                                'peak_surface_k': rs['pico_superficie_k'],
                                'disc_input_j': rs['energia_entrada_disco_j']})
    convection = []
    for h in [0., 20., 50., 100.]:
        rh = run(48, 16, .02, h_externo_w_m2k=h, h_canal_w_m2k=h)
        convection.append({'h_both_faces_w_m2k': h, 'peak_surface_k': rh['pico_superficie_k'],
                           'disc_output_j': rh['energia_saida_disco_j']})
    for name, rows in [('convergencia_malha.csv', grid), ('convergencia_tempo.csv', temporal),
                       ('verificacao_analitica.csv', analytical), ('sensibilidade_particao.csv', sensitivity),
                       ('sensibilidade_conveccao.csv', convection), ('historico.csv', r['historico'])]:
        with (args.destino/name).open('w') as f:
            writer = csv.DictWriter(f, list(rows[0]), lineterminator='\n')
            writer.writeheader(); writer.writerows(rows)
    field = [{'r_m': float(rad), 'z_m': float(z), 'temperature_k': float(r['temperatura_k'][i, j])}
             for i, rad in enumerate(r['r_m']) for j, z in enumerate(r['z_m'])]
    with (args.destino/'campo_rz.csv').open('w') as f:
        w = csv.DictWriter(f, list(field[0]), lineterminator='\n'); w.writeheader(); w.writerows(field)
    fig, ax = plt.subplots(figsize=(8, 4.5), layout='constrained')
    image = ax.pcolormesh(r['r_m']*1000, r['z_m']*1000, (r['temperatura_k']-273.15).T, shading='nearest', cmap='inferno')
    fig.colorbar(image, ax=ax, label='Temperatura (°C)')
    ax.set(xlabel='Raio (mm)', ylabel='Espessura de uma placa (mm)',
           title='I33 • campo r–z aos 5 s • geometria e partição condicionadas')
    fig.savefig(args.destino/'campo_freio.png', dpi=160); plt.close(fig)
    trace = r['historico']
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout='constrained')
    times = [x['tempo_s'] for x in trace]
    axes[0].plot(times, [x['tmax_superficie_k']-273.15 for x in trace], label='Superfície reconstruída')
    axes[0].plot(times, [x['tmax_celula_k']-273.15 for x in trace], label='Centro de célula')
    axes[0].set(xlabel='Tempo (s)', ylabel='Temperatura (°C)'); axes[0].legend()
    for key, label in [('energia_entrada_placa_j', 'Entrada'), ('energia_armazenada_placa_j', 'Armazenada'), ('energia_saida_placa_j', 'Convecção')]:
        axes[1].plot(times, [2*x[key]/1000 for x in trace], label=label)
    axes[1].set(xlabel='Tempo (s)', ylabel='Energia de um disco (kJ)'); axes[1].legend()
    fig.savefig(args.destino/'historico_freio.png', dpi=160); plt.close(fig)
    summary = {key: value for key, value in r.items() if np.isscalar(value)}
    summary.update(status=config['status'], generated_utc=datetime.now(timezone.utc).isoformat(),
                   scenario_revision=config['revision'], config=str(args.config),
                   final_max_cell_k=float(r['temperatura_k'].max()), final_max_surface_k=float(r['superficie_k'].max()),
                   grid=grid, time_convergence=temporal, analytical_verification=analytical,
                   sources=[config['reference_component'], config['material_reference']], limits=config['limits'])
    summary['inputs_sha256'] = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in
                               [args.config, Path(__file__), Path('src/motorhome/freios_axisimetricos.py')]}
    (args.destino/'resumo_freios.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps({k: v for k, v in summary.items() if np.isscalar(v)}, indent=2))


if __name__ == '__main__':
    main()
