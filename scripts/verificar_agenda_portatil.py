"""Reabre CSV/JSON da etapa portátil e verifica energia/cronologia/proveniência."""

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))

import pandas as pd

from motorhome.agenda_portatil import verificar_agenda


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def auditar(pasta):
    root = Path(__file__).resolve().parents[1]
    summary = json.loads((pasta/'resumo_agenda_portatil.json').read_text())
    for name, expected in summary['inputs_sha256'].items():
        if sha(root/name) != expected:
            raise ValueError(f'Entrada mudou: {name}')
    for name, expected in summary['output_csv_sha256'].items():
        if sha(pasta/name) != expected:
            raise ValueError(f'CSV mudou: {name}')
    data = pd.read_csv(pasta/'entradas_grade.csv', index_col=0)
    data.index = pd.DatetimeIndex(pd.to_datetime(data.index, utc=True)).tz_convert('America/Sao_Paulo')
    c, powers = summary['configuration'], summary['traction_modes_kw']
    fields = ['start', 'state', 'driving_h', 'speed_km_h', 'drive_kw', 'fixed_kw', 'portable_kw',
              'house_kw', 'transfer_kw', 'curtailed_kw', 'traction_kwh', 'service_kwh']
    checked = {}
    for name, case in summary['cases'].items():
        if not case['feasible']:
            continue
        frame = pd.read_csv(pasta/f'{name}.csv')
        rows = frame[fields].to_dict('records')
        initial = c['traction_final_soc_i27'] if name in ['i29_dia_ciclico', 'i29_ultimo_dia'] else c['traction_initial_soc']
        verification = verificar_agenda(rows, data, c, powers, initial, c['traction_final_soc_i27'],
                                        24. if name.startswith('i27') else 8., case['transfer_kw_assumed'])
        for r, mechanical in zip(rows, frame['wheel_mechanical_kw']):
            mode = c['speed_modes_km_h'].index(r['speed_km_h']) if r['speed_km_h'] else None
            expected = summary['wheel_mechanical_modes_kw'][mode] if mode is not None else 0.
            if abs(mechanical-expected) > 1e-7:
                raise ValueError('Potência mecânica nas rodas divergente')
        if not frame['motor_shaft_kw'].isna().all():
            raise ValueError('Potência de eixo sem dados de transmissão')
        for key in ['distance_km', 'solar_kwh', 'house_kwh', 'drive_kwh', 'transfer_input_kwh', 'curtailed_kwh']:
            if abs(verification[key]-case['verification'][key]) > 1e-5:
                raise ValueError(f'Resumo divergente do CSV: {name}/{key}')
        checked[name] = {'distance_km': verification['distance_km'],
                         'max_balance_residual_kwh': verification['max_balance_residual_kwh']}
    trip = summary['trip_7000km']
    if trip['constructed']:
        rows = pd.read_csv(pasta/'i29_viagem_7000km.csv')[fields].to_dict('records')
        repeated = pd.concat([data]*trip['full_days'], ignore_index=True)
        repeated.index = pd.date_range(data.index[0], periods=len(repeated), freq=pd.Timedelta(minutes=c['step_minutes']))
        verification = verificar_agenda(rows, repeated, c, powers, c['traction_initial_soc'],
                                        c['traction_final_soc_i27'], 8., c['transfer_power_kw_assumed'])
        if abs(verification['distance_km']-trip['distance_target_km']) > 1e-4:
            raise ValueError('Viagem não atingiu distância alvo')
        checked['trip_7000km'] = {'distance_km': verification['distance_km'],
                                 'max_driving_h_day': max(verification['daily_driving_h'].values()),
                                 'max_balance_residual_kwh': verification['max_balance_residual_kwh']}
    return {'provenance_and_csv_replay_passed': True, 'cases': checked, 'vehicle_validated': False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('resultado', type=Path)
    args = p.parse_args()
    print(json.dumps(auditar(args.resultado), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
