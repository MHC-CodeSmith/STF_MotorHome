"""Estudo I30 condicionado com campo r–theta, malhas e referências analíticas."""
import argparse
import csv
import hashlib
import json
import sys
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from motorhome.cabos_polares import Cabo, perfil_analitico_sem_feedback, resolver


def resumo(r):
    return {k: v for k, v in r.items() if np.isscalar(v)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config', type=Path, default=Path('config/cabos_tracao_proposta.yaml'))
    p.add_argument('--destino', type=Path, required=True)
    a = p.parse_args()
    config = yaml.safe_load(a.config.read_text())
    m = config['model']
    c = Cabo(m['bundle_radius_m'], m['outer_radius_m'], m['bundle_k_assumed_w_mk'],
             m['insulation_k_assumed_w_mk'], m['resistance20_ohm_m'], m['alpha_assumed_per_k'],
             m['reference_k'])
    a.destino.mkdir(parents=True, exist_ok=False)
    dc_i = m['dc_example_motor_mechanical_w']/(m['dc_example_voltage_v']*m['dc_example_combined_efficiency_assumed'])
    cases = []
    for circuit, currents in [('fase_RMS_hipotetica', m['phase_rms_currents_assumed_a']), ('DC_exemplo_eta90', [dc_i])]:
        for current in currents:
            for h in m['h_assumed_w_m2k']:
                result = resolver(c, current, 32, 128, h, m['ambient_k'])
                cases.append({'circuito': circuit, 'corrente_a': current, 'h_w_m2k': h,
                              'temperatura_max_c': result['temperatura_max_k']-273.15,
                              'acima_referencia_150c': bool(result['temperatura_max_k'] > 423.15),
                              'extrapolacao_material': bool(result['temperatura_max_k'] > 423.15),
                              **resumo(result)})
    alternative_data = config['alternative_manufacturer_same_table']
    alternatives = []
    for name, candidate, parallel in [
        ('1x120_por_condutor', c, 1),
        ('1x150_por_condutor', replace(c, raio_feixe_m=alternative_data['conductor_diameter_max_mm']/2000,
                                      raio_externo_m=alternative_data['cable_diameter_nominal_mm']/2000,
                                      resistencia20_ohm_m=alternative_data['resistance20_max_ohm_km']/1000), 1),
        ('2x120_por_condutor_resfriamento_independente', c, 2),
    ]:
        for current in [dc_i, 600.]:
            for h in m['h_assumed_w_m2k']:
                r = resolver(candidate, current/parallel, 32, 128, h, m['ambient_k'])
                alternatives.append({'alternativa': name, 'corrente_total_a': current,
                    'corrente_por_cabo_a': current/parallel, 'cabos_por_condutor': parallel,
                    'h_assumido_w_m2k': h, 'temperatura_max_c': r['temperatura_max_k']-273.15,
                    'joule_total_por_condutor_w_m': parallel*r['joule_w_m'],
                    'acima_referencia_150c': bool(r['temperatura_max_k'] > 423.15)})
    grids = []
    analytic, harmonic = [], []
    final = None
    for nr, nt in zip(m['radial_cells_per_material'], m['angular_cells'], strict=True):
        theta = (np.arange(nt)+.5)*2*np.pi/nt
        h = m['asymmetric_h_mean_assumed_w_m2k']*(1+m['asymmetric_h_sine_fraction_assumed']*np.sin(theta))
        final = resolver(c, m['asymmetric_case_current_assumed_a'], nr, nt, h, m['ambient_k'])
        grids.append({'nr_por_material': nr, 'ntheta': nt, 'celulas': 2*nr*nt, **resumo(final)})
        no_feedback = replace(c, alpha_por_k=0, k_feixe_w_mk=3.)
        test = resolver(no_feedback, 100, nr, nt, 10, m['ambient_k'])
        exact = perfil_analitico_sem_feedback(no_feedback, 100, 10, m['ambient_k'], test['r_m'])
        analytic.append(float(np.max(abs(test['temperatura_k']-exact[:, None]))))
        uniform = replace(no_feedback, k_isolamento_w_mk=3.)
        outside = 300+2*(1+2*3/(1000*c.raio_externo_m))*np.cos(2*theta)
        test = resolver(uniform, 0, nr, nt, 1000, outside)
        exact = 300+2*(test['r_m'][:, None]/c.raio_externo_m)**2*np.cos(2*theta)
        harmonic.append(float(np.sqrt(np.mean((test['temperatura_k']-exact)**2))))
    sensitivity = []
    theta = final['theta_rad']
    h = m['asymmetric_h_mean_assumed_w_m2k']*(1+m['asymmetric_h_sine_fraction_assumed']*np.sin(theta))
    for kb in [100, 200, 385]:
        for ki in [.15, .2, .3]:
            result = resolver(replace(c, k_feixe_w_mk=kb, k_isolamento_w_mk=ki),
                              m['asymmetric_case_current_assumed_a'], 32, 128, h, m['ambient_k'])
            sensitivity.append({'k_feixe_assumida_w_mk': kb, 'k_isolamento_assumida_w_mk': ki,
                                'temperatura_max_c': result['temperatura_max_k']-273.15})
    r, t = np.meshgrid(final['r_m'], final['theta_rad'], indexing='ij')
    data = np.c_[r.ravel(), t.ravel(), (r*np.cos(t)).ravel(), (r*np.sin(t)).ravel(),
                 final['temperatura_k'].ravel()]
    np.savetxt(a.destino/'campo_temperatura.csv', data, delimiter=',',
               header='r_m,theta_rad,x_m,y_m,temperatura_k', comments='')
    for name, rows in [('cenarios.csv', cases), ('convergencia.csv', grids), ('sensibilidade_k.csv', sensitivity), ('alternativas.csv', alternatives)]:
        with (a.destino/name).open('w') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.8), layout='constrained')
    theta_edges = np.linspace(0, 2*np.pi, len(final['theta_rad'])+1)
    rr, tt = np.meshgrid(final['faces_r_m'], theta_edges, indexing='ij')
    img = axes[0].pcolormesh(rr*np.cos(tt)*1000, rr*np.sin(tt)*1000,
                             final['temperatura_k']-273.15, shading='flat', cmap='inferno')
    axes[0].add_patch(plt.Circle((0, 0), c.raio_feixe_m*1000, fill=False, color='cyan', linewidth=.8))
    axes[0].set(aspect='equal', xlabel='x [mm]', ylabel='y [mm]', title='450 A RMS hipotéticos; h = 10(1 + 0,5 sen θ)')
    fig.colorbar(img, ax=axes[0], label='Temperatura estacionária [°C]')
    for current in m['phase_rms_currents_assumed_a']:
        sub = [row for row in cases if row['circuito'] == 'fase_RMS_hipotetica' and row['corrente_a'] == current]
        axes[1].plot([row['h_w_m2k'] for row in sub], [row['temperatura_max_c'] for row in sub], 'o-', label=f'{current} A RMS hipotéticos')
    axes[1].axhline(150, color='red', linestyle='--', label='Referência 3000 h da ficha: 150 °C')
    axes[1].set(xlabel='h assumido [W/(m² K)]', ylabel='Temperatura máxima [°C]',
                title='Sensibilidade; extrapolações não qualificam o cabo')
    axes[1].set_ylim(0, 250)
    axes[1].text(.98, .98, 'Ponto 600 A / h=5: >1000 °C extrapolados;\nfora da faixa física do material e do gráfico',
                 transform=axes[1].transAxes, ha='right', va='top', fontsize=8)
    axes[1].legend(fontsize=8, loc='center right')
    axes[1].grid(alpha=.25)
    fig.savefig(a.destino/'campo_e_sensibilidade.png', dpi=165)
    plt.close(fig)
    source_paths = [a.config, Path(__file__), Path('src/motorhome/cabos_polares.py')]
    result = {'status': config['status'], 'revision': config['revision'],
              'generated_utc': datetime.now(timezone.utc).isoformat(), 'script': str(Path(__file__).relative_to(Path.cwd())),
              'inputs_sha256': {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in source_paths},
              'manufacturer': config['manufacturer'], 'assumptions_and_limits': m['limitations'],
              'dc_current_example_a': dc_i, 'cases': cases, 'mesh_study_asymmetric': grids,
              'finest_max_change_k': abs(grids[-1]['temperatura_max_k']-grids[-2]['temperatura_max_k']),
              'analytical_verification_synthetic': {'radial_max_error_k': analytic, 'harmonic_2d_rms_error_k': harmonic,
                   'radial_observed_orders': np.log2(np.array(analytic[:-1])/analytic[1:]).tolist(),
                   'harmonic_observed_orders': np.log2(np.array(harmonic[:-1])/harmonic[1:]).tolist()},
              'alternatives_independent_cooling_equal_current_assumed': alternatives,
              'conductivity_sensitivity': sensitivity}
    (a.destino/'resumo_cabos.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps({'dc_i_a': dc_i, 'mesh': grids, 'verification': result['analytical_verification_synthetic']}, indent=2))


if __name__ == '__main__':
    main()
