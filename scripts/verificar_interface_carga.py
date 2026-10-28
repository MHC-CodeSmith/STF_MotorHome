"""Reabre a nova missão e confere barramentos, correntes e energia dos CSV."""

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))

import numpy as np
import pandas as pd
from calcular_agenda_portatil import load_solar

from motorhome.interface_carga import verificar_interface


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def auditar(pasta):
    root = Path(__file__).resolve().parents[1]
    s = json.loads((pasta/'resumo_interface_carga.json').read_text())
    for name, expected in s['inputs_sha256'].items():
        if sha(root/name) != expected:
            raise ValueError(f'Entrada mudou: {name}')
    for name, expected in s['output_csv_sha256'].items():
        if sha(pasta/name) != expected:
            raise ValueError(f'CSV mudou: {name}')
    c, spec, powers = s['configuration'], s['interface_specification'], s['traction_powers_kw']
    data = pd.read_csv(pasta/'entradas_interface.csv', index_col=0)
    data.index = pd.DatetimeIndex(pd.to_datetime(data.index, utc=True)).tz_convert('America/Sao_Paulo')
    original = root/'entregas/parcial_2026-10-24/expansao_solar.csv'
    # Confirma explicitamente as colunas dos barramentos; não basta o total diário.
    for key, source in [('fixed_kw', 'terminal_assumed_3_modules_w'),
                         ('excluded_12v_solar_kw', 'cab_190w_after_assumed_losses_w')]:
        expected = load_solar(original, source, 30)
        if not data.index.equals(expected.index) or not np.allclose(data[key], expected, atol=1e-10):
            raise ValueError('Solar de12/48V misturado ou deslocado no tempo')
    house = (data['house_ac_kw']/spec['inverter']['efficiency_assumed']
             +data['dc12_kw']/spec['household']['dc_dc_efficiency_assumed']
             +spec['inverter']['idle_power_kw_published'])
    if not np.allclose(house, data['house_kw'], atol=1e-10):
        raise ValueError('Perdas/standby residenciais divergentes')
    fields = ['start', 'state', 'driving_h', 'speed_km_h', 'drive_kw', 'fixed_kw', 'portable_kw',
              'house_kw', 'transfer_kw', 'curtailed_kw', 'traction_kwh', 'service_kwh', 'charge_current_a']
    checked = {}
    for name, case in s['cases'].items():
        if not case['feasible']:
            continue
        rows = pd.read_csv(pasta/f'{name}.csv')[fields].to_dict('records')
        initial = c['traction_initial_soc'] if name in ['i27', 'i29_primeiro'] else c['traction_final_soc_i27']
        v = verificar_interface(rows, data, c, powers, spec, initial, c['traction_final_soc_i27'],
                                24. if name == 'i27' else 8.)
        for key in ['distance_km', 'solar_kwh', 'house_kwh', 'drive_kwh', 'transfer_input_kwh', 'curtailed_kwh']:
            if abs(v[key]-case['verification'][key]) > 1e-5:
                raise ValueError(f'Resumo diverge do CSV: {name}/{key}')
        checked[name] = {k: v[k] for k in ['distance_km', 'max_balance_residual_kwh',
                                         'max_shared_active_kw', 'max_shared_apparent_kva', 'charging_starts']}
    if s['trip']['constructed']:
        rows = pd.read_csv(pasta/'viagem_7000km.csv')[fields].to_dict('records')
        repeated = pd.concat([data]*s['trip']['full_days_upper_bound'], ignore_index=True)
        repeated.index = pd.date_range(data.index[0], periods=len(repeated), freq='30min')
        v = verificar_interface(rows, repeated, c, powers, spec, c['traction_initial_soc'], c['traction_final_soc_i27'], 8.)
        if abs(v['distance_km']-7000) > 1e-4:
            raise ValueError('Distância da viagem divergente')
        checked['trip'] = {k: v[k] for k in ['distance_km', 'max_balance_residual_kwh',
                                            'max_shared_active_kw', 'max_shared_apparent_kva']}
        checked['trip']['max_driving_h_day'] = max(v['daily_driving_h'].values())
    return {'provenance_bus_separation_and_replay_passed': True, 'cases': checked,
            'interface_oem_verified': False, 'vehicle_validated': False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('resultado', type=Path)
    args = p.parse_args()
    print(json.dumps(auditar(args.resultado), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
