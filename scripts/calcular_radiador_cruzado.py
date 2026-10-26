"""I35: perfis cruzados e capacidade condicionada, sem curvas OEM inventadas."""

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
from motorhome.radiador_cruzado import efetividade_integral, resolver


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config', type=Path, default=Path('config/arrefecimento_proposta.yaml'))
    p.add_argument('--destino', type=Path, required=True)
    a = p.parse_args()
    config = yaml.safe_load(a.config.read_text())
    platform_path = Path('config/arquitetura_eletrica_proposta.yaml')
    power = yaml.safe_load(platform_path.read_text())['motor']['peak_power_W']
    m = config['assumed']
    a.destino.mkdir(parents=True, exist_ok=False)
    def run(ua, mh, mc, n):
        return resolver(ua, mh*m['coolant_cp_j_kgk'], mc*m['air_cp_j_kgk'],
                        m['hot_coolant_inlet_k'], m['air_inlet_k'], n, n)
    rows = []
    for mh in m['coolant_mass_flow_kg_s']:
        for mc in m['air_mass_flow_kg_s']:
            for ua in m['ua_w_k']:
                r = run(ua, mh, mc, 64)
                rows.append({'coolant_mass_flow_kg_s': mh, 'air_mass_flow_kg_s': mc,
                    'ua_assumed_w_k': ua, **{k: v for k, v in r.items() if np.isscalar(v)}})
    nc = m['nominal_field_case']
    mh, mc, ua = nc['coolant_mass_flow_kg_s'], nc['air_mass_flow_kg_s'], nc['ua_w_k']
    ch, cc = mh*m['coolant_cp_j_kgk'], mc*m['air_cp_j_kgk']
    exact = efetividade_integral(ua/min(ch, cc), min(ch, cc)/max(ch, cc))
    grid = []
    for n in [16, 32, 64]:
        r = run(ua, mh, mc, n)
        grid.append({'n': n, 'cells': n*n, 'effectiveness': r['efetividade'],
                     'error_against_integral': abs(r['efetividade']-exact),
                     'heat_w': r['calor_w'], 'residual_w': r['residuo_w']})
    r = run(ua, mh, mc, 64)
    losses = [{'eta_combined_assumed': eta, 'mechanical_peak_w': power,
               'combined_loss_w': power*(1/eta-1),
               'coolant_delta_t_if_all_loss_here_k': power*(1/eta-1)/ch,
               'capacity_margin_w_at_assumed_inlet_temperatures': r['calor_w']-power*(1/eta-1)}
              for eta in m['combined_motor_inverter_efficiencies']]
    for filename, data in [('cenarios.csv', rows), ('convergencia.csv', grid), ('perdas_condicionadas.csv', losses)]:
        with (a.destino/filename).open('w') as f:
            writer = csv.DictWriter(f, fieldnames=list(data[0]), lineterminator='\n')
            writer.writeheader()
            writer.writerows(data)
    np.savetxt(a.destino/'campo_quente_k.csv', r['quente_k'], delimiter=',')
    np.savetxt(a.destino/'campo_frio_k.csv', r['fria_k'], delimiter=',')
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), layout='constrained')
    for ax, field, label in zip(axes, [r['quente_k'], r['fria_k']],
                                ['Refrigerante: fluxo em +x', 'Ar: fluxo em +y'], strict=True):
        im = ax.imshow(field-273.15, origin='lower', extent=[0, 1, 0, 1], aspect='auto',
                       vmin=25, vmax=80, cmap='inferno')
        ax.set(xlabel='x / L', ylabel='y / H', title=label)
        fig.colorbar(im, ax=ax, label='Temperatura [°C]')
    fig.suptitle('Estudo condicionado: UA=1000 W/K; refrigerante 0,5 kg/s; ar 1 kg/s')
    fig.savefig(a.destino/'campos_radiador.png', dpi=160)
    plt.close(fig)
    paths = [a.config, platform_path, Path(__file__), Path('src/motorhome/radiador_cruzado.py')]
    result = {'status': config['status'], 'revision': config['revision'],
              'generated_utc': datetime.now(timezone.utc).isoformat(),
              'inputs_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
              'method_source': config['method'], 'assumptions': m, 'unknown': config['unknown'],
              'limits': config['limits'], 'nominal_conditioned': {k: v for k, v in r.items() if np.isscalar(v)},
              'mesh_study': grid, 'reference_integral_effectiveness': exact,
              'conditional_combined_losses': losses, 'sensitivity': rows}
    (a.destino/'resumo_radiador.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps({'nominal': result['nominal_conditioned'], 'mesh': grid, 'losses': losses}, indent=2))


if __name__ == '__main__':
    main()
