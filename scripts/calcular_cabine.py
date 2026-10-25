"""I31/I32: cabine equivalente, hipóteses explícitas, balanço e sensibilidade."""

import argparse
import hashlib
import itertools
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

from motorhome.cabine import integrar_zona, transmitancia, umidade_especifica
from motorhome.solar import simular_dia


def calcular(c, solar, passo_min=1, orientacao=None, alpha=None, g=None, capacidade=None):
    """Uma chamada resolve um cenário completo; parâmetros opcionais são sensibilidade."""
    h, geo, ins = c['assumptions'], c['geometry'], c['insulation']
    heading = geo['front_azimuth_deg'] if orientacao is None else orientacao
    alpha = h['solar_absorptance'] if alpha is None else alpha
    g = h['glass_solar_factor'] if g is None else g
    capacidade = h['effective_heat_capacity_j_k'] if capacidade is None else capacidade
    if not 0 <= alpha <= 1 or not 0 <= g <= 1:
        raise ValueError('Absorptância e fator solar devem estar em [0,1]')
    length = geo['cargo_length_m']+geo['cab_extension_assumed_m']
    width, height = geo['width_m'], geo['height_m']
    areas = {'front': width*height, 'rear': width*height, 'left': length*height,
                 'right': length*height, 'roof': length*width, 'floor': length*width}
    if any(v <= 0 for v in areas.values()):
        raise ValueError('Geometria inválida')
    glass = {key: geo['glass_area_m2'].get(key, 0) for key in areas}
    if any(glass[key] < 0 or glass[key] > areas[key] for key in areas):
        raise ValueError('Área de vidro incompatível com superfície')
    t = ins['evaluation_temperature_c']
    k = (33+0.1*t+0.0008*t*t)/1000
    u = transmitancia([(ins['thickness_m'], k),
                       (h['inner_lining_thickness_m'], h['inner_lining_k_w_mk'])],
                      h['interior_film_w_m2k'], h['exterior_combined_film_w_m2k'])
    ua = sum(u*(areas[key]-glass[key])+h['glass_u_w_m2k']*glass[key]
             for key in areas)+h['thermal_bridge_ua_w_k']
    data = simular_dia(solar, passo_min)
    s = solar['scenario']
    location = pvlib.location.Location(s['latitude_deg'], s['longitude_deg'],
                                      tz=s['timezone'], altitude=s['altitude_m'])
    position = location.get_solarposition(data.index, temperature=s['ambient_temperature_c'])
    az = {'front': heading, 'rear': heading+180, 'right': heading+90, 'left': heading+270,
              'roof': heading, 'floor': heading}
    total = np.zeros(len(data))
    surfaces = []
    noon = int(np.argmin(abs(data.index.hour+data.index.minute/60-12)))
    for key, area in areas.items():
        irradiance = (np.zeros(len(data)) if key == 'floor' else
                      pvlib.irradiance.get_total_irradiance(
                          0 if key == 'roof' else 90, az[key] % 360,
                          position.apparent_zenith, position.azimuth,
                          data.dni_w_m2, data.ghi_w_m2, data.dhi_w_m2,
                          albedo=solar['array']['albedo'], model='isotropic').poa_global.to_numpy())
        opaque_gain = u*(area-glass[key])*alpha*irradiance/h['exterior_combined_film_w_m2k']
        glass_gain = g*glass[key]*irradiance
        total += opaque_gain+glass_gain
        surfaces.append({'surface': key, 'gross_area_m2': area, 'glass_area_m2': glass[key],
                             'noon_poa_w_m2': float(irradiance[noon]),
                             'noon_opaque_solar_gain_w': float(opaque_gain[noon]),
                             'noon_glass_solar_gain_w': float(glass_gain[noon])})
    start = int(h['start_local_hour']*60/passo_min)
    seconds = (data.index[start:]-data.index[start]).total_seconds().to_numpy()
    temps, residual = integrar_zona(seconds, total[start:], ua, capacidade,
                                   s['ambient_temperature_c'], h['initial_temperature_c'])
    data['solar_heat_gain_w'] = total
    data['i31_temperature_c'] = np.nan
    data.loc[data.index[start:], 'i31_temperature_c'] = temps
    p = float(pvlib.atmosphere.alt2pres(s['altitude_m']))
    wo = umidade_especifica(33, s['relative_humidity_percent']/100, p)
    wi = umidade_especifica(25, h['inside_rh_fraction'], p)
    # Vazão de ar exterior convertida em vazão mássica de ar seco a 33°C.
    pv = p*wo/(0.621945+wo)
    mdry = (p-pv)/(287.05*(33+273.15))*h['i32_fresh_air_m3_h']/3600
    ventilation_s = mdry*(h['air_cp_j_kgk']+1860*wo)*8
    ventilation_l = mdry*h['vaporization_j_kg']*max(0, wo-wi)
    loads = []
    for people in (1, 2):
        sensible = ua*8+total[noon]+h['i32_equipment_heat_w']+people*h['occupant_sensible_w']+ventilation_s
        latent = people*h['occupant_latent_w']+ventilation_l
        loads.append({'occupants': people, 'conduction_w': ua*8, 'solar_w': float(total[noon]),
                          'equipment_w': h['i32_equipment_heat_w'], 'sensible_w': float(sensible),
                          'latent_w': float(latent), 'cooling_required_w': float(sensible+latent),
                          'electrical_w_by_assumed_cop': {str(cop): float((sensible+latent)/cop)
                                                       for cop in h['cop_sensitivity']}})
    summary = {'ua_w_k': ua, 'insulation_k_w_mk': k, 'opaque_u_w_m2k': u,
                   'equivalent_volume_m3': length*width*height, 'surfaces': surfaces,
                   'i31_noon_c': float(temps[noon-start]), 'i31_peak_c': float(temps.max()),
                   'i31_peak_local_time': data.index[start+int(np.argmax(temps))].isoformat(),
                   'i31_noon_frozen_equilibrium_c': float(s['ambient_temperature_c']+total[noon]/ua),
                   'time_constant_h': capacidade/ua/3600,
                   'i31_energy_residual_j': residual, 'pressure_pa': p,
                   'humidity_outside_kg_kg': wo, 'humidity_inside_kg_kg': wi,
                   'ventilation_sensible_w': ventilation_s, 'ventilation_latent_w': ventilation_l,
                   'i32': loads, 'heading_deg': heading, 'absorptance': alpha, 'glass_g': g,
                   'capacity_j_k': capacidade}
    return data, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=Path('config/cabine_proposta.yaml'))
    parser.add_argument('--solar', type=Path, default=Path('config/solar_proposta.yaml'))
    parser.add_argument('--destino', type=Path, required=True)
    args = parser.parse_args()
    c, solar = [yaml.safe_load(p.read_text()) for p in (args.config, args.solar)]
    if c['assumptions']['i31_air_changes_h'] != 0:
        raise ValueError('Esta implementação I31 pressupõe zero infiltração')
    data, result = calcular(c, solar)
    _, coarse = calcular(c, solar, 5)
    sensitivity = []
    h = c['assumptions']
    for heading, alpha, g, capacity in itertools.product(
            h['orientation_sensitivity_deg'], h['surface_absorptance_sensitivity'],
            h['glass_solar_factor_sensitivity'], h['effective_capacity_sensitivity_j_k']):
        _, res = calcular(c, solar, 5, heading, alpha, g, capacity)
        sensitivity.append({key: res[key] for key in ('heading_deg', 'absorptance', 'glass_g',
                                                     'capacity_j_k', 'i31_noon_c', 'i31_peak_c', 'i32')})
    output = {'revision': c['revision'], 'status': c['status'], 'script': 'scripts/calcular_cabine.py',
                  'created_utc': datetime.now(timezone.utc).isoformat(), 'approved_vehicle_result': False,
                  'config_sha256': hashlib.sha256(args.config.read_bytes()).hexdigest(),
                  'solar_config_sha256': hashlib.sha256(args.solar.read_bytes()).hexdigest(),
                  'pvlib_version': pvlib.__version__, 'nominal': result,
                  'noon_1min_5min_difference_k': abs(result['i31_noon_c']-coarse['i31_noon_c']),
                  'sensitivity': sensitivity, 'limitations': c['assumptions']['notes'],
                  'geometry_limit': c['geometry']['note']}
    args.destino.mkdir(parents=True, exist_ok=False)
    data.to_csv(args.destino/'cabine_timeseries.csv', index_label='local_time')
    (args.destino/'resumo_cabine.json').write_text(json.dumps(output, ensure_ascii=False, indent=2))
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), layout='constrained')
    hour = (data.index-data.index[0]).total_seconds()/3600
    axes[0].plot(hour, data.i31_temperature_c, label='I31: transiente, fechado, sem ocupantes/AC')
    axes[0].axhline(solar['scenario']['ambient_temperature_c'], color='gray', ls='--', label='Ambiente 25°C')
    axes[0].scatter([12], [result['i31_noon_c']], color='black')
    axes[0].set(xlabel='Hora local [h]', ylabel='Temperatura de zona [°C]',
                title='Cabine equivalente - hipótese geométrica e propriedades não validadas')
    categories = ['Condução', 'Solar', 'Equipamentos', 'Ocupante sensível', 'Ventilação sensível', 'Latente total']
    case = result['i32'][0]
    values = [case['conduction_w'], case['solar_w'], case['equipment_w'], h['occupant_sensible_w'],
              result['ventilation_sensible_w'], case['latent_w']]
    axes[1].bar(categories, values, color='#147a83')
    axes[1].tick_params(axis='x', labelrotation=15)
    axes[1].set(ylabel='Carga de resfriamento [W]', title='I32: meio-dia, exterior 33°C / interior 25°C, um ocupante')
    axes[0].legend(fontsize=8)
    for ax in axes:
        ax.grid(axis='y', alpha=.25)
    fig.savefig(args.destino/'cabine_termica.png', dpi=160)
    plt.close(fig)
    print(json.dumps({k: v for k, v in output.items() if k != 'sensitivity'}, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
