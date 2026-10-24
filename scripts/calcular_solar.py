"""Estima geração de projeto, com fontes e hipóteses; não valida integração HV."""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pvlib
import yaml

from motorhome.solar import integrar_kwh, simular_dia


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config', type=Path, required=True)
    p.add_argument('--destino', type=Path, required=True)
    args = p.parse_args()
    c = yaml.safe_load(args.config.read_text())
    r, coarse = simular_dia(c, 1), simular_dia(c, 5)
    summary = {}
    for n in c['array']['module_counts']:
        col = f'terminal_assumed_{n}_modules_w'
        energy, energy5 = integrar_kwh(r[col]), integrar_kwh(coarse[col])
        summary[str(n)] = {'p_stc_array_w': n*c['module']['p_stc_w'],
                           'area_modules_m2': n*c['module']['length_m']*c['module']['width_m'],
                           'mass_modules_kg': n*c['module']['mass_kg'],
                           'dc_energy_kwh': integrar_kwh(r[f'dc_{n}_modules_w']),
                           'terminal_energy_assumed_kwh': energy,
                           'timestep_difference_1min_5min_fraction': abs(energy-energy5)/energy,
                           'peak_terminal_assumed_w': float(r[col].max())}
    args.destino.mkdir(parents=True, exist_ok=False)
    out = args.destino
    r.to_csv(out/'pv_timeseries.csv', index_label='local_time')
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), layout='constrained')
    hour = np.arange(len(r))/60
    axes[0].plot(hour, r.poa_w_m2, label='Plano horizontal')
    axes[0].set(xlabel='Hora local [h]', ylabel='Irradiância [W/m²]', title='São Carlos A711, 21/06/2026 — céu limpo Ineichen')
    for n in c['array']['module_counts']:
        axes[1].plot(hour, r[f'terminal_assumed_{n}_modules_w'], label=f'{n} módulos: {summary[str(n)]["terminal_energy_assumed_kwh"]:.2f} kWh/dia')
    axes[1].set(xlabel='Hora local [h]', ylabel='Potência após perdas assumidas [W]', title='Estimativa condicionada — conversão HV e montagem ainda não validadas')
    for ax in axes:
        ax.legend()
        ax.grid(alpha=.3)
        ax.set_xlim(0, 24)
    fig.savefig(out/'solar_proposta.png', dpi=160)
    plt.close(fig)
    result = {'revision': c['revision'], 'tipo': c['status'], 'data_utc': datetime.now(timezone.utc).isoformat(),
              'script': 'scripts/calcular_solar.py', 'config_sha256': hashlib.sha256(args.config.read_bytes()).hexdigest(),
              'pvlib_version': pvlib.__version__, 'local': c['scenario'], 'hypotheses': c['assumptions'],
              'global_horizontal_irradiation_kwh_m2': integrar_kwh(r.ghi_w_m2),
              'max_module_temperature_c': float(r.temperature_module_c.max()), 'arrays': summary,
              'approved_vehicle_result': False, 'hv_conversion_verified': False}
    (out/'resumo_solar.json').write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
