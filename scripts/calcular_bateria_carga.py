"""I34: SOC/temperaturas em carga20/80kW e sensibilidades explícitas."""

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
from motorhome.bateria_carga import resolver


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config', type=Path, default=Path('config/bateria_termica_proposta.yaml'))
    p.add_argument('--destino', type=Path, required=True)
    args = p.parse_args()
    cfg = yaml.safe_load(args.config.read_text())
    c = cfg['assumed'] | cfg['official']
    args.destino.mkdir(parents=True, exist_ok=False)
    nominal, sensitivity, convergence = [], [], []
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), layout='constrained')
    for power in cfg['official']['charger_powers_w']:
        r = resolver(c, power)
        h = r.pop('history')
        nominal.append({'requested_power_w': power, **r})
        with (args.destino/f'historico_{power//1000}kw.csv').open('w') as f:
            w = csv.DictWriter(f, list(h[0]), lineterminator='\n'); w.writeheader(); w.writerows(h)
        time = np.array([row['time_s'] for row in h])/3600
        axes[0].plot(time, [row['battery_k']-273.15 for row in h], label=f'{power//1000} kW • bateria')
        axes[0].plot(time, [row['coolant_k']-273.15 for row in h], '--', label=f'{power//1000} kW • refrigerante')
        axes[1].plot(time, [row['soc']*100 for row in h], label=f'{power//1000} kW')
        ref = resolver(c, power, rtol=1e-10, max_step_s=5)
        for step in [120, 60, 30]:
            rc = resolver(c, power, rtol=1e-7, max_step_s=step)
            convergence.append({'power_w': power, 'max_step_s': step,
                                'duration_error_to_reference_s': abs(rc['duration_s']-ref['duration_s']),
                                'temperature_error_to_reference_k': abs(rc['final_battery_k']-ref['final_battery_k'])})
        for resistance in cfg['sensitivities']['resistance_ref_ohm']:
            for entropy in cfg['sensitivities']['pack_entropy_v_k']:
                rs = resolver(c | {'resistance_ref_ohm': resistance, 'pack_entropy_v_k': entropy}, power)
                rs.pop('history')
                sensitivity.append({'power_w': power, 'resistance_ref_ohm': resistance, 'entropy_v_k': entropy, **rs})
        adiabatic = resolver(c | {'battery_coolant_ua_w_k': 0, 'cooler_ambient_ua_w_k': 0}, power)
        adiabatic.pop('history')
        sensitivity.append({'power_w': power, 'resistance_ref_ohm': c['resistance_ref_ohm'],
                            'entropy_v_k': c['pack_entropy_v_k'], **adiabatic, 'case': 'adiabatic'})
    for ax in axes:
        ax.legend(); ax.grid(alpha=.2); ax.set_xlabel('Tempo (h)')
    axes[0].set(ylabel='Temperatura (°C)', title='Dois nós térmicos • parâmetros hipotéticos')
    axes[1].set(ylabel='SOC equivalente (%)', title='Protocolo proposto 20 → 80%')
    fig.savefig(args.destino/'carga_bateria.png', dpi=160); plt.close(fig)
    for name, rows in [('sensibilidade.csv', sensitivity), ('convergencia.csv', convergence)]:
        keys = list(dict.fromkeys(key for row in rows for key in row))
        with (args.destino/name).open('w') as f:
            w = csv.DictWriter(f, keys, lineterminator='\n'); w.writeheader(); w.writerows(rows)
    summary = {'status': cfg['status'], 'revision': cfg['revision'], 'nominal': nominal,
               'generated_utc': datetime.now(timezone.utc).isoformat(), 'convergence': convergence,
               'sources': cfg['sources'], 'limits': cfg['limits'],
               'inputs_sha256': {str(f): hashlib.sha256(f.read_bytes()).hexdigest() for f in
                                [args.config, Path(__file__), Path('src/motorhome/bateria_carga.py')]}}
    (args.destino/'resumo_bateria_carga.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps(nominal, indent=2))


if __name__ == '__main__':
    main()
