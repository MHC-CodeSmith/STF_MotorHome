"""Replay independente dos CSV de viagem: fonte solar, vias, reservas e energia."""

import argparse
import gzip
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))

import numpy as np
import pandas as pd
import yaml

from motorhome.viagem_rota import SolarRota


def bytes_csv(folder, filename):
    path = folder/filename
    return path.read_bytes() if path.exists() else gzip.decompress((folder/(filename+'.gz')).read_bytes())


def frame_csv(folder, filename):
    path = folder/filename
    return pd.read_csv(path if path.exists() else folder/(filename+'.gz'))


def verificar_case(frame, drive, case, steps, elevation, solar, config, battery, spec, dynamics):
    if not len(frame) or not len(drive):
        raise ValueError('Caso sem dados de viagem')
    start = pd.DatetimeIndex(pd.to_datetime(frame.start, utc=True, format='ISO8601'))
    end = pd.DatetimeIndex(pd.to_datetime(frame.end, utc=True, format='ISO8601'))
    dt = (end-start).total_seconds().to_numpy()/3600
    if (not np.allclose(dt, config['integration_minutes']/60)
            or not np.allclose((start[1:]-end[:-1]).total_seconds(), 0.)
            or not np.isfinite(frame.select_dtypes('number')).all().all()):
        raise ValueError('Agenda descontínua, duração ou valores inválidos')
    local = (start+pd.Timedelta(minutes=config['integration_minutes']/2)).tz_convert(config['timezone'])
    hours = local.hour+local.minute/60
    pos = frame.position_start_km.to_numpy()
    if (abs(pos[0]) > 1e-8 or not np.allclose(pos[1:], frame.position_end_km.to_numpy()[:-1], atol=1e-7)
            or (frame.position_end_km < frame.position_start_km-1e-7).any()):
        raise ValueError('Posição descontínua ou retrocedendo')
    # Recalcular a irradiância creditada a partir das fontes, não do resumo.
    si = solar.index
    weather_h = ((local.ceil('h')-si[0]).total_seconds()/3600).to_numpy(dtype=int)
    ni = np.clip(np.searchsorted(solar.distance, pos, side='right')-1, 0, len(solar.distance)-2)
    weight = (pos-solar.distance[ni])/(solar.distance[ni+1]-solar.distance[ni])
    table = solar.tables[case['scenario']]
    expected = table[ni, weather_h]*(1-weight[:, None])+table[ni+1, weather_h]*weight[:, None]
    available = expected[:, 0]+expected[:, 1]*((hours >= 6.5) & (hours < 21.5))
    if not np.allclose(frame.solar_kw, available, atol=1e-8) or not np.allclose(frame.roof48_kw, expected[:, 0], atol=1e-8):
        raise ValueError('Geração exportada diverge da fonte/data/posição')
    k = drive.step_index.to_numpy(int)
    speed = drive.speed_km_h.to_numpy()
    if (k < 0).any() or (k >= len(steps)).any():
        raise ValueError('Índice de trecho inválido')
    cap = np.minimum(case['cruise_cap_km_h'], steps.iloc[k].model_max_km_h.to_numpy())
    if (speed > cap+1e-7).any() or (speed <= 0).any():
        raise ValueError('Velocidade supera limite aproximado do trecho/veículo')
    distance = drive.end_km-drive.start_km
    if not np.allclose(distance, drive.duration_h*speed, atol=1e-7):
        raise ValueError('Velocidade/tempo/distância divergentes')
    if not np.allclose(drive.start_km.to_numpy()[1:], drive.end_km.to_numpy()[:-1], atol=1e-7):
        raise ValueError('Condução tem lacunas geográficas')
    z0 = np.interp(drive.start_km, elevation.distance_km, elevation.elevation_m)
    z1 = np.interp(drive.end_km, elevation.distance_km, elevation.elevation_m)
    grade = (z1-z0)/(distance*1000)
    if not np.allclose(grade, drive.grade_fraction, atol=1e-7):
        raise ValueError('Inclinação diverge doDEM')
    force = (.5*dynamics['air_density_kg_m3']*battery['drag_coefficient_assumed']*dynamics['frontal_area_m2']*(speed/3.6)**2
             + battery['rolling_coefficient_assumed']*dynamics['mass_kg']*9.80665*np.cos(np.arctan(grade))
             + dynamics['mass_kg']*9.80665*np.sin(np.arctan(grade)))
    wheel = force*speed/3.6/1000
    terminal = np.where(wheel >= 0, wheel/battery['traction_efficiency_assumed'], wheel*config['regeneration_efficiency_assumed'])+dynamics['driving_auxiliary_power_w']/1000
    if not np.allclose(terminal*drive.duration_h, drive.battery_kwh, atol=1e-7):
        raise ValueError('Consumo do trecho divergente')
    drive_start = pd.DatetimeIndex(pd.to_datetime(drive.start, utc=True, format='ISO8601'))
    drive_end = pd.DatetimeIndex(pd.to_datetime(drive.end, utc=True, format='ISO8601'))
    buckets = np.searchsorted(start.as_unit('ns').asi8, drive_start.as_unit('ns').asi8+1000, side='right')-1
    if (buckets < 0).any() or (buckets >= len(frame)).any():
        raise ValueError('Condução fora da agenda')
    if ((drive_end-end[buckets]).total_seconds() > 1e-5).any() or not np.allclose((drive_end-drive_start).total_seconds()/3600, drive.duration_h, atol=1e-7):
        raise ValueError('Horários/duração da condução incompatíveis')
    grouped_energy = np.bincount(buckets, weights=drive.battery_kwh, minlength=len(frame))
    grouped_hours = np.bincount(buckets, weights=drive.duration_h, minlength=len(frame))
    if not np.allclose(grouped_energy, frame.drive_kwh, atol=1e-7) or not np.allclose(grouped_hours, frame.driving_h, atol=1e-7):
        raise ValueError('Condução não coincide com a integração')
    if (frame.driving_h > dt+1e-7).any() or (frame.loc[(hours >= 6) & (hours < 22), 'driving_h'] > 1e-7).any():
        raise ValueError('Condução conflita com montagem/portátil')
    q = frame.transfer_dc_kw.to_numpy()
    current = frame.charge_current_a.to_numpy()
    ac = current*spec['charge']['voltage_v_assumed']*spec['charge']['power_factor_assumed']/1000
    expected_q = ac/spec['inverter']['efficiency_assumed']
    if (not np.allclose(q, expected_q, atol=1e-7) or not np.isin(current, spec['charge']['current_modes_a_assumed']).all()
            or (frame.loc[frame.driving_h > 1e-8, 'transfer_dc_kw'].abs() > 1e-8).any()
            or (not case['interface_hypothetical'] and (q > 1e-8).any())):
        raise ValueError('Transferência/corrente/intertravamento divergentes')
    shared = ac+frame.house_ac_kw.to_numpy()
    apparent = ac/spec['charge']['power_factor_assumed']+frame.house_ac_kw/spec['inverter']['household_power_factor_assumed']
    if (shared > spec['inverter']['continuous_power_kw_at40c']+1e-8).any() or (apparent > spec['inverter']['apparent_power_kva_at25c']+1e-8).any():
        raise ValueError('Inversor sobrecarregado')
    tc, sc = battery['traction_capacity_kwh'], battery['service_capacity_kwh']
    eta = spec['inverter']['efficiency_assumed']*spec['charge']['onboard_efficiency_assumed']
    et = tc*config['traction_initial_soc']+np.cumsum(q*eta*dt-frame.drive_kwh-frame.curtailed_regen_kwh)
    es = sc*config['service_initial_soc']+np.cumsum((frame.solar_kw-frame.house_dc_kw-q)*dt-frame.curtailed_service_kwh)
    residual = max(float(np.max(abs(et-frame.traction_kwh))), float(np.max(abs(es-frame.service_kwh))))
    if (residual > 1e-5 or (et < tc*config['traction_reserve_soc']-1e-7).any()
            or (et > tc+1e-7).any() or (es < sc*config['service_reserve_soc']-1e-7).any() or (es > sc+1e-7).any()):
        raise ValueError('Balanço ou reserva divergente')
    daily = frame.driving_h.groupby(start.tz_convert(config['timezone']).date).sum()
    if daily.max() > config['driving_hours_per_day_max']+1e-7:
        raise ValueError('Mais de8h por dia de calendário')
    if abs(float(distance.sum())-case['distance_km']) > 1e-5:
        raise ValueError('Distância do resumo divergente')
    return {'distance_km': float(distance.sum()), 'max_balance_residual_kwh': residual,
            'max_driving_hours_per_day': float(daily.max()), 'max_speed_km_h': float(speed.max()),
            'driving_hours': float(drive.duration_h.sum()), 'solar_kwh': float((frame.solar_kw*dt).sum()),
            'house_kwh': float((frame.house_dc_kw*dt).sum()), 'traction_energy_kwh': float(drive.battery_kwh.sum()),
            'weather_source_replayed': True, 'road_speed_bounds_passed': True}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('resultado', type=Path)
    p.add_argument('--fontes', required=True, type=Path)
    p.add_argument('--destino', type=Path)
    args = p.parse_args()
    s = json.loads((args.resultado/'resumo_rota_real.json').read_text())
    root = Path(__file__).resolve().parents[1]
    for name, expected in s['inputs_sha256'].items():
        if hashlib.sha256((root/name).read_bytes()).hexdigest() != expected:
            raise ValueError('Entrada modificada: '+name)
    for name, expected in s['output_csv_sha256'].items():
        if hashlib.sha256(bytes_csv(args.resultado, name)).hexdigest() != expected:
            raise ValueError('CSV modificado: '+name)
    sources = json.loads((args.fontes/'fontes.json').read_text())
    for name, record in sources.items():
        if hashlib.sha256((args.fontes/name).read_bytes()).hexdigest() != record['sha256']:
            raise ValueError('Fonte bruta modificada: '+name)
    def config(name):
        return yaml.safe_load((root/'config'/name).read_text())
    c = s['configuration']
    battery, spec, dynamics = [config(x) for x in ['agenda_portatil_proposta.yaml', 'interface_carga_proposta.yaml', 'energia_sensibilidade.yaml']]
    solar = SolarRota(args.fontes, config('solar_proposta.yaml'), config('solar_portatil_proposta.yaml'), c['timezone'])
    steps = pd.read_csv(args.resultado/'trechos.csv')
    elevation = pd.read_csv(args.resultado/'relevo.csv')
    results = {}
    for name, case in s['cases'].items():
        results[name] = verificar_case(frame_csv(args.resultado, case['agenda_csv']), frame_csv(args.resultado, case['driving_csv']),
                                       case, steps, elevation, solar, c, battery, spec, dynamics)
        print(name+': replayOK', flush=True)
    result = {'passed': True, 'cases': results, 'physical_vehicle_validated': False,
              'verifier_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    if args.destino:
        args.destino.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
