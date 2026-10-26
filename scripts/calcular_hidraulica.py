"""I35: ponto de operação e equilíbrio térmico condicionados, curva Bosch real."""

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
from motorhome.hidraulica import Circuito, perda, ponto_operacao
from motorhome.radiador_cruzado import efetividade_integral, resolver


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config', type=Path, default=Path('config/hidraulica_proposta.yaml'))
    p.add_argument('--destino', type=Path, required=True)
    args = p.parse_args()
    cfg = yaml.safe_load(args.config.read_text())
    a, pump = cfg['assumed'], cfg['pump']
    args.destino.mkdir(parents=True, exist_ok=False)
    c = Circuito(a['hose_length_m'], a['hose_internal_diameter_m'], a['roughness_m'],
                 a['minor_loss_k'], a['density_kg_m3'], a['dynamic_viscosity_pa_s'],
                 a['component_reference_flow_m3_s'], sum(a['component_drop_pa_at_reference'].values()))
    curve = np.array(pump['curve_l_h_kpa_a'])
    q, pressure, current = curve[:, 0]/3.6e6, curve[:, 1]*1000, curve[:, 2]
    r = ponto_operacao(c, q, pressure, current, pump['voltage_v'])
    uncertainty = [ponto_operacao(c, q, pressure, current, pump['voltage_v'], delta)
                   for delta in [-pump['pressure_reading_uncertainty_pa'], pump['pressure_reading_uncertainty_pa']]]
    ch = r['mass_flow_kg_s']*a['cp_j_kgk']
    cc = a['air_mass_flow_kg_s']*a['air_cp_j_kgk']
    eff = efetividade_integral(a['radiator_ua_w_k']/min(ch, cc), min(ch, cc)/max(ch, cc))
    thermal = []
    for eta in a['combined_efficiencies']:
        loss = a['max_motor_mechanical_w']*(1/eta-1)
        total = loss+r['electric_power_w']  # conservador: toda energia da bomba vira calor neste circuito
        hot = a['ambient_k']+total/(eff*min(ch, cc))
        fields = resolver(a['radiator_ua_w_k'], ch, cc, hot, a['ambient_k'])
        thermal.append({'combined_efficiency_assumed': eta, 'motor_inverter_loss_w': loss,
                        'pump_heat_assumed_w': r['electric_power_w'], 'radiator_load_w': total,
                        'hot_inlet_k': hot, 'coolant_outlet_k': hot-total/ch,
                        'air_outlet_k': a['ambient_k']+total/cc,
                        'coolant_rise_k': total/ch,
                        'field_heat_residual_to_load_w': fields['calor_w']-total})
        if eta == .9:
            for name, field in [('quente', fields['quente_k']), ('frio', fields['fria_k'])]:
                np.savetxt(args.destino/f'campo_{name}_k.csv', field, delimiter=',')
            fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout='constrained')
            for ax, field, label in zip(axes, [fields['quente_k'], fields['fria_k']], ['Refrigerante', 'Ar'], strict=True):
                im = ax.imshow(field-273.15, origin='lower', cmap='inferno', aspect='auto')
                ax.set(title=label, xlabel='Coordenada do escoamento quente', ylabel='Coordenada do ar')
                fig.colorbar(im, ax=ax, label='°C')
            fig.savefig(args.destino/'campos_equilibrio.png', dpi=160); plt.close(fig)
    system = [{'flow_l_h': float(flow*3.6e6), **perda(c, flow)} for flow in np.linspace(q[0], q[-1], 251)]
    for name, rows in [('curva_sistema.csv', system), ('equilibrios_termicos.csv', thermal)]:
        with (args.destino/name).open('w') as f:
            w = csv.DictWriter(f, list(rows[0]), lineterminator='\n'); w.writeheader(); w.writerows(rows)
    fig, ax = plt.subplots(figsize=(8, 4.5), layout='constrained')
    ax.plot(curve[:, 0], curve[:, 1], 'o-', label='Bosch: leitura aproximada da ficha')
    ax.fill_between(curve[:, 0], curve[:, 1]-3, curve[:, 1]+3, alpha=.15, label='±3 kPa: leitura')
    ax.plot([s['flow_l_h'] for s in system], [s['total_pa']/1000 for s in system], label='Circuito proposto (perdas assumidas)')
    ax.plot(r['flow_m3_s']*3.6e6, r['pump_pressure_pa']/1000, 'ko', label='Interseção')
    ax.set(xlabel='Vazão (L/h)', ylabel='Pressão diferencial (kPa)', title='I35 • ponto hidráulico condicionado • bomba a 12 V')
    ax.legend(); ax.grid(alpha=.2)
    fig.savefig(args.destino/'ponto_operacao.png', dpi=160); plt.close(fig)
    summary = {'status': cfg['status'], 'revision': cfg['revision'],
               'generated_utc': datetime.now(timezone.utc).isoformat(), 'operating_point': r,
               'pressure_reading_sensitivity': uncertainty, 'thermal_equilibria': thermal,
               'effectiveness': eff, 'pump_source': pump, 'limits': cfg['limits'],
               'inputs_sha256': {str(f): hashlib.sha256(f.read_bytes()).hexdigest() for f in
                                [args.config, Path(__file__), Path('src/motorhome/hidraulica.py'), Path('src/motorhome/radiador_cruzado.py')]}}
    (args.destino/'resumo_hidraulica.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps({'operating_point': r, 'thermal_equilibria': thermal}, indent=2))


if __name__ == '__main__':
    main()
