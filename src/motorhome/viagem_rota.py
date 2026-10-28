"""Viagem em geografiaOSRM e calendário real, com duas baterias e geração local.

Política construtiva determinística: portátil aberto06:30–21:30, instalação e
recolhimento30min. Dirige22–06 (até8h/calendário), limitado por energia e via.
DespachaEVSE em blocos30min, verifica energia em passos5min. Não prova ótimo.
"""

import json

import numpy as np
import pandas as pd
import pvlib

from motorhome.interface_carga import potencias_interface


class SolarRota:
    def __init__(self, source, solar, portable, timezone):
        self.nodes = pd.read_csv(source/'nos_clima.csv')
        self.distance = self.nodes.distance_km.to_numpy()
        self.tables = {'clear': [], 'era5': []}
        self.elevations = []
        self.trailing_unavailable_hours = {}
        self.index = None
        for _, node in self.nodes.iterrows():
            weather = json.loads((source/node.weather_file).read_text())
            raw = weather['hourly']
            names = ['shortwave_radiation', 'direct_normal_irradiance', 'diffuse_radiation', 'temperature_2m']
            values = np.column_stack([np.asarray(raw[k], dtype=float) for k in names])
            valid = np.isfinite(values).all(axis=1)
            missing = np.flatnonzero(~valid)
            if len(missing):
                first = int(missing[0])
                if valid[first:].any():
                    raise ValueError('Lacuna meteorológica interna: não interpolar silenciosamente')
                self.trailing_unavailable_hours[node.weather_file] = len(valid)-first
                weather['hourly'] = {k: v[:first] for k, v in raw.items()}
            index = pd.DatetimeIndex(pd.to_datetime(weather['hourly']['time'])).tz_localize(timezone)
            if self.index is not None and not index.equals(self.index):
                raise ValueError('Datas da reanálise incompatíveis entre nós')
            self.index = index
            self.elevations.append(weather['elevation'])
            # Open-Meteo: irradiância média da hora precedente; posição no meio dessa hora.
            midpoint = index-pd.Timedelta(minutes=30)
            location = pvlib.location.Location(node.latitude_deg, node.longitude_deg, tz=timezone,
                                               altitude=weather['elevation'])
            pos = location.get_solarposition(midpoint)
            clear = location.get_clearsky(midpoint, model='ineichen', solar_position=pos)
            raw = weather['hourly']
            for scenario in self.tables:
                if scenario == 'clear':
                    ghi, dni, dhi, temp = clear.ghi.to_numpy(), clear.dni.to_numpy(), clear.dhi.to_numpy(), np.full(len(index), 25.)
                else:
                    ghi, dni, dhi, temp = [np.asarray(raw[k], dtype=float) for k in ['shortwave_radiation', 'direct_normal_irradiance', 'diffuse_radiation', 'temperature_2m']]
                if not all(np.isfinite(x).all() for x in [ghi, dni, dhi, temp]):
                    raise ValueError('Clima com lacunas; não substituir por céu limpo')
                output = []
                for power, gamma, tilt in [(1350., solar['module']['gamma_pdc_per_k'], 0.),
                                            (portable['module']['quantity']*portable['module']['p_stc_w'], portable['module']['gamma_pdc_per_k'], 45.)]:
                    poa = pvlib.irradiance.get_total_irradiance(tilt, 0., pos.apparent_zenith.to_numpy(),
                                                              pos.azimuth.to_numpy(), dni, ghi, dhi,
                                                              albedo=.2, model='isotropic')['poa_global']
                    tm = pvlib.temperature.faiman(poa, temp, 0., u0=25., u1=6.84)
                    dc = pvlib.pvsystem.pvwatts_dc(poa, tm, power, gamma)
                    output.append(np.maximum(0., dc)*.9*.95/1000)
                self.tables[scenario].append(np.column_stack(output))
        self.tables = {key: np.array(value) for key, value in self.tables.items()}

    def at(self, timestamp, position, scenario):
        # O valor emhh:00 representa[hh-1,hh]; usar o fim da hora de timestamp.
        hour = int((timestamp.ceil('h')-self.index[0]).total_seconds()/3600)
        if not 0 <= hour < len(self.index):
            raise ValueError('Horário fora do arquivo meteorológico')
        j = int(np.clip(np.searchsorted(self.distance, position, side='right')-1, 0, len(self.distance)-2))
        weight = (position-self.distance[j])/(self.distance[j+1]-self.distance[j])
        return self.tables[scenario][j, hour]*(1-weight)+self.tables[scenario][j+1, hour]*weight


def cargas(timestamp, budget, spec):
    h = timestamp.hour+timestamp.minute/60
    house = spec['household']
    ac = budget['cold_wash_once_week_daily_average_kwh']/24+spec['charge']['evse_standby_kw_assumed']
    if house['hvac_start_hour_assumed'] <= h < house['hvac_start_hour_assumed']+house['hvac_duration_h_assumed']:
        ac += budget['hvac_two_people_3h_assumed_cop2_5_kwh']/house['hvac_duration_h_assumed']
    if house['cooktop_start_hour_assumed'] <= h < house['cooktop_start_hour_assumed']+house['cooktop_duration_h_assumed']:
        ac += budget['cooktop_half_hour_kwh']/house['cooktop_duration_h_assumed']
    dc12 = (budget['fridge_55w_assumed_50percent_duty_kwh']+budget['lights_pump_electronics_assumed_kwh'])/24
    demand = ac/spec['inverter']['efficiency_assumed']+dc12/house['dc_dc_efficiency_assumed']+spec['inverter']['idle_power_kw_published']
    return demand, ac, dc12


def simular_viagem(route, solar, geometry, config, battery, spec, budget, cruise, scenario,
                   interface=True):
    dt = config['integration_minutes']/60
    if config['integration_minutes'] != 5 or config['portable_setup_minutes'] != 30 or config['portable_teardown_minutes'] != 30:
        raise ValueError('Política implementada exige5min, montagem/recolhimento30min')
    ac_modes, dc_modes = potencias_interface(spec)
    eta = spec['inverter']['efficiency_assumed']*spec['charge']['onboard_efficiency_assumed']
    tc, sc = battery['traction_capacity_kwh'], battery['service_capacity_kwh']
    et, es = tc*config['traction_initial_soc'], sc*config['service_initial_soc']
    rt, rs = tc*config['traction_reserve_soc'], sc*config['service_reserve_soc']
    position, rows, drive_rows, milestones = 0., [], [], {}
    start = pd.Timestamp(config['start_date'], tz=config['timezone'])
    daily_drive, q, mode = {}, 0., 0
    status, failure = 'horizon_exhausted', None
    horizon = int(config['max_days']*24/dt)
    if hasattr(solar, 'index'):
        horizon = min(horizon, int((solar.index[-1]-start).total_seconds()/3600/dt))
    for t in range(horizon):
        clock = start+pd.Timedelta(minutes=t*config['integration_minutes'])
        middle = clock+pd.Timedelta(minutes=config['integration_minutes']/2)
        h = middle.hour+middle.minute/60
        day = clock.date().isoformat()
        daily_drive.setdefault(day, 0.)
        demand, house_ac, dc12 = cargas(middle, budget, spec)
        fixed, portable_possible = solar.at(middle, position, scenario)
        drive_time = h < config['night_driving_end_hour'] or h >= config['night_driving_start_hour']
        state = 'stowed'
        if 6 <= h < 6.5:
            state = 'setup'
        elif 6.5 <= h < 21.5:
            state = 'deployed'
        elif 21.5 <= h < 22:
            state = 'teardown'
        pv = float(fixed+(portable_possible if state == 'deployed' else 0.))
        if clock.minute % 30 == 0:
            q, mode = 0., 0
            if interface and not drive_time and et < tc-1e-6:
                for j in range(len(dc_modes)-1, 0, -1):
                    test_es, feasible = es, True
                    for ahead in range(6):
                        when = middle+pd.Timedelta(minutes=ahead*5)
                        hh = when.hour+when.minute/60
                        f, po = solar.at(when, position, scenario)
                        solar_kw = float(f+(po if 6.5 <= hh < 21.5 else 0.))
                        house, house_ahead, _ = cargas(when, budget, spec)
                        apparent = ac_modes[j]/spec['charge']['power_factor_assumed']+house_ahead/spec['inverter']['household_power_factor_assumed']
                        test_es = min(sc, test_es+(solar_kw-house-dc_modes[j])*dt)
                        feasible &= (house_ahead+ac_modes[j] <= spec['inverter']['continuous_power_kw_at40c']+1e-9
                                     and apparent <= spec['inverter']['apparent_power_kva_at25c']+1e-9
                                     and test_es >= rs-1e-9)
                    if feasible and test_es >= config['service_target_before_trip_soc']*sc and et+dc_modes[j]*eta*.5 <= tc+1e-9:
                        q, mode = float(dc_modes[j]), j
                        break
        if drive_time:
            q, mode = 0., 0
        chunks = []
        if drive_time and et > rt+config['traction_keep_next_day_kwh'] and daily_drive[day] < config['driving_hours_per_day_max']-1e-9:
            planned = route.mover(position, min(dt, config['driving_hours_per_day_max']-daily_drive[day]), cruise)
            remaining_energy = et-rt-config['traction_keep_next_day_kwh']
            for piece in planned:
                piece = dict(piece)
                fraction = min(1., remaining_energy/piece['battery_kwh']) if piece['battery_kwh'] > 0 else 1.
                if fraction <= 1e-9:
                    break
                if fraction < 1:
                    piece['end_km'] = piece['start_km']+(piece['end_km']-piece['start_km'])*fraction
                    piece['duration_h'] *= fraction
                    piece['battery_kwh'] *= fraction
                chunks.append(piece)
                remaining_energy -= piece['battery_kwh']
                if fraction < 1:
                    break
        driving_h = sum(x['duration_h'] for x in chunks)
        drive_energy = sum(x['battery_kwh'] for x in chunks)
        if chunks:
            state = 'driving'
        qpack = q*eta*dt
        service_before_cut = es+(pv-demand-q)*dt
        cut = max(0., service_before_cut-sc)
        next_es = service_before_cut-cut
        # Não ocultar déficit para manter a política; registrar primeira falha.
        if next_es < rs-1e-8:
            status = 'service_reserve_violation_predicted'
            failure = {'time': clock.isoformat(), 'projected_service_soc': next_es/sc,
                       'last_feasible_km': position, 'policy_infeasible': True}
            break
        regen_cut = 0.
        next_et = et+qpack
        for piece in chunks:
            next_et -= piece['battery_kwh']
            regen_cut += max(0., next_et-tc)
            next_et = min(next_et, tc)
        if not rt-1e-7 <= next_et <= tc+1e-7:
            raise ValueError('Energia de tração fora de limites')
        old_position = position
        offset_h = 0.
        for piece in chunks:
            timestamp = clock+pd.Timedelta(hours=offset_h)
            drive_rows.append(dict(piece, start=timestamp.isoformat(), end=(timestamp+pd.Timedelta(hours=piece['duration_h'])).isoformat()))
            for milestone in [7000., route.total_km]:
                key = '7000km' if milestone == 7000 else 'route_finish'
                if key not in milestones and piece['start_km'] < milestone <= piece['end_km']+1e-8:
                    fraction = (milestone-piece['start_km'])/(piece['end_km']-piece['start_km'])
                    when = timestamp+pd.Timedelta(hours=piece['duration_h']*fraction)
                    milestones[key] = {'time': when.isoformat(), 'elapsed_days': (when-start).total_seconds()/86400,
                                       'latitude_deg': float(np.interp(milestone, geometry.distance_km, geometry.latitude_deg)),
                                       'longitude_deg': float(np.interp(milestone, geometry.distance_km, geometry.longitude_deg))}
            offset_h += piece['duration_h']
        if chunks:
            position = chunks[-1]['end_km']
        daily_drive[day] += driving_h
        rows.append({'start': clock.isoformat(), 'end': (clock+pd.Timedelta(hours=dt)).isoformat(),
                     'position_start_km': old_position, 'position_end_km': position,
                     'latitude_deg': float(np.interp(old_position, geometry.distance_km, geometry.latitude_deg)),
                     'longitude_deg': float(np.interp(old_position, geometry.distance_km, geometry.longitude_deg)),
                     'state': state, 'driving_h': driving_h, 'drive_kwh': drive_energy,
                     'roof48_kw': float(fixed), 'portable_available_kw': float(portable_possible),
                     'solar_kw': pv, 'house_dc_kw': demand, 'house_ac_kw': house_ac, 'dc12_kw': dc12,
                     'transfer_dc_kw': q, 'charge_current_a': spec['charge']['current_modes_a_assumed'][mode],
                     'curtailed_service_kwh': cut, 'curtailed_regen_kwh': regen_cut,
                     'traction_kwh': next_et, 'service_kwh': next_es})
        et, es = next_et, next_es
        if position >= route.total_km-1e-7:
            status = 'arrived'
            break
        if not interface and t >= 2*24/dt and et <= rt+config['traction_keep_next_day_kwh']+1e-6:
            status = 'traction_stranded_without_interface'
            break
    return {'status': status, 'arrived': status == 'arrived', 'scenario': scenario, 'cruise_cap_km_h': cruise,
            'interface_hypothetical': interface, 'failure': failure, 'distance_km': position,
            'route_target_km': route.total_km, 'milestones': milestones,
            'traction_final_soc': et/tc, 'service_final_soc': es/sc,
            'max_driving_h_day': max(daily_drive.values(), default=0.),
            'globally_optimized': False}, pd.DataFrame(rows), pd.DataFrame(drive_rows)
