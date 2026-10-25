"""Cobertura mista e sombra direta da extensão, sem supor conexão ao pack OEM."""

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pvlib
import yaml

from motorhome.solar import integrar_kwh, simular_dia
from motorhome.sombra import fracoes_sombreadas


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--destino', type=Path, required=True)
    args = p.parse_args()
    config_path, layout_path = Path('config/solar_proposta.yaml'), Path('config/layout_proposto.yaml')
    c, layout = [yaml.safe_load(path.read_text()) for path in [config_path, layout_path]]
    d = simular_dia(c)
    s, roof = c['scenario'], layout['roof']
    loc = pvlib.location.Location(s['latitude_deg'], s['longitude_deg'],
                                  tz=s['timezone'], altitude=s['altitude_m'])
    pos = loc.get_solarposition(d.index, temperature=s['ambient_temperature_c'])
    # Hipótese de orientação: +X norte e +Y leste. Outras orientações a refazer.
    elevation, azimuth = np.radians(pos.apparent_elevation), np.radians(pos.azimuth)
    vectors = np.column_stack((np.cos(elevation)*np.cos(azimuth),
                               np.cos(elevation)*np.sin(azimuth), np.sin(elevation)))
    sx, dx, dy = roof['start_x_m'], roof['module_length_x_m'], roof['module_width_y_m']
    sy = (layout['cargo_m'][1]-dy)/2
    rectangles = [(sx+i*(dx+roof['gap_m']), sy, sx+i*(dx+roof['gap_m'])+dx, sy+dy) for i in range(3)]
    shift = dy+roof['extension_lateral_gap_m']
    upper = [(x0, y0+shift, x1, y1+shift) for x0, y0, x1, y1 in rectangles]
    delta_z = roof['module_thickness_m']+roof['extension_vertical_gap_m']
    shaded = np.array([fracoes_sombreadas(rectangles, upper, delta_z, vector) for vector in vectors])
    # Irradiação difusa inalterada: é limite de modelo, não fator de vista calculado.
    direct = (d.dni_w_m2*np.maximum(0, np.sin(elevation))).to_numpy()
    lower_dc = np.zeros(len(d))
    for i in range(3):
        poa = np.maximum(0, d.poa_w_m2.to_numpy()-direct*shaded[:, i])
        temperature = pvlib.temperature.faiman(poa, s['ambient_temperature_c'], s['wind_speed_m_s'],
                                               u0=c['assumptions']['faiman_u0_w_m2k'],
                                               u1=c['assumptions']['faiman_u1_w_s_m3k'])
        lower_dc += pvlib.pvsystem.pvwatts_dc(poa, temperature, c['module']['p_stc_w'], c['module']['gamma_pdc_per_k'])
    losses = (1-c['assumptions']['other_losses_fraction'])*c['assumptions']['converter_efficiency']
    small_dc = pvlib.pvsystem.pvwatts_dc(d.poa_w_m2, d.temperature_module_c,
                                         roof['cab_module']['power_w'], -.0045).clip(lower=0)
    d['cab_190w_after_assumed_losses_w'] = small_dc*losses
    d['mixed_stowed_w'] = d['terminal_assumed_3_modules_w']+d.cab_190w_after_assumed_losses_w
    d['mixed_open_no_shading_upper_w'] = d['terminal_assumed_6_modules_w']+d.cab_190w_after_assumed_losses_w
    d['mixed_open_geometric_beam_shading_w'] = (3*d.module_dc_w+lower_dc)*losses+d.cab_190w_after_assumed_losses_w
    # Limite conservador de despacho: desliga a string inferior quando há sombra em qualquer módulo.
    no_shade = (shaded.max(axis=1) < 1e-9).astype(float)
    d['mixed_open_lower_string_off_if_shaded_w'] = (3*d.module_dc_w+3*d.module_dc_w*no_shade)*losses+d.cab_190w_after_assumed_losses_w
    d['lower_geometric_direct_shade_fraction_max'] = shaded.max(axis=1)
    cols = ['mixed_stowed_w', 'mixed_open_no_shading_upper_w',
            'mixed_open_geometric_beam_shading_w', 'mixed_open_lower_string_off_if_shaded_w']
    energies = {name: integrar_kwh(d[name]) for name in cols}
    # Orçamento de habitação assumido, sem secagem: não mascara a lacuna do ciclo.
    cabin_path = Path('entregas/parcial_2026-10-24/resumo_cabine.json')
    cabin = json.loads(cabin_path.read_text())
    cooling_two = cabin['nominal']['i32'][1]['cooling_required_w']/1000
    household = {'fridge_55w_assumed_50percent_duty_kwh': .055*12,
                 'cooktop_2300w_half_hour_kwh': 2.3*.5,
                 'hvac_two_people_3h_assumed_cop2_5_kwh': cooling_two/2.5*3,
                 'cold_wash_once_week_daily_average_kwh': .29/7,
                 'lights_pump_electronics_assumed_kwh': .4}
    result = {'status': 'ESTIMATIVA_CONDICIONADA_NAO_VALIDADA', 'script': 'scripts/calcular_expansao_solar.py',
              'exposed_stowed_stc_w': 1540, 'exposed_open_stc_w': 2890,
              'exposed_stowed_module_area_m2': 3*dx*dy+roof['cab_module']['length_x_m']*roof['cab_module']['width_y_m'],
              'exposed_open_module_area_m2': 6*dx*dy+roof['cab_module']['length_x_m']*roof['cab_module']['width_y_m'],
              'small_module': roof['cab_module'], 'energy_kwh': energies,
              'household_assumptions_excluding_dryer_kwh_day': household,
              'household_total_excluding_dryer_kwh_day': sum(household.values()),
              'remaining_after_household_before_storage_losses_kwh_day': {name: energy-sum(household.values()) for name, energy in energies.items()},
              'approved_vehicle_result': False, 'hv_interface_verified': False,
              'limitations': ['MPPT/conversão95% e perdas10% assumidos; barramentos12/48V ainda propostos, não energia confirmada na tração400V.',
                              'Sombra só geométrica direta; difusa sem bloqueio e área sombreada não prediz diodos/mismatch da string.',
                              'Sem sombras de árvores/aberturas/antenas; extensão aberta idealmente durante todo o sol, ventozero do enunciado.',
                              'Faiman não calibrado para painéis empilhados; temperatura da pequena placa usa aproximação comum de módulo.',
                              'Perfil de habitação é hipótese; energia de secagem desconhecida e não incluída. Não viabilidade da missão.'],
              'inputs_sha256': {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in [config_path, layout_path, cabin_path]}}
    args.destino.mkdir(parents=True, exist_ok=False)
    d.to_csv(args.destino/'expansao_solar.csv', index_label='local_time')
    (args.destino/'resumo_expansao_solar.json').write_text(json.dumps(result, indent=2, ensure_ascii=False))
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), layout='constrained')
    hour = (d.index-d.index[0]).total_seconds()/3600
    for name, label in [('mixed_stowed_w', 'Recolhida:1540W STC'),
                        ('mixed_open_geometric_beam_shading_w', 'Aberta:2890W STC / sombra direta geométrica'),
                        ('mixed_open_lower_string_off_if_shaded_w', 'Aberta / desliga string inferior sombreada')]:
        axes[0].plot(hour, d[name], label=f'{label}: {energies[name]:.2f}kWh/dia')
    axes[0].set(xlabel='Hora local [h]', ylabel='Potência após perdas assumidas [W]',
                title='São Carlos21/06 - estimativa de cobertura mista, sem validação elétrica')
    axes[1].plot(hour, d.lower_geometric_direct_shade_fraction_max)
    axes[1].set(xlabel='Hora local [h]', ylabel='Maior fração de área sob sombra direta', ylim=(0, 1),
                title='Três placas móveis elevadas60mm - orientaçãoX=norte/Y=leste assumida')
    for ax in axes:
        ax.grid(alpha=.25)
        ax.set_xlim(0, 24)
    axes[0].legend(fontsize=8)
    fig.savefig(args.destino/'expansao_solar.png', dpi=160)
    plt.close(fig)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
