"""Recalcula I27/I29: PV48V separado, perfis AC/DC e cargaOEM discreta hipotética."""

import argparse
import copy
import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml
from calcular_agenda_portatil import load_solar

from motorhome.interface_carga import (
    otimizar_interface,
    potencias_interface,
    verificar_interface,
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--destino', required=True, type=Path)
    p.add_argument('--sem-interface', action='store_true', help='SóI27 com todos modos de carga desligados')
    args = p.parse_args()
    config_paths = [Path('config')/name for name in ['agenda_portatil_proposta.yaml',
                    'interface_carga_proposta.yaml', 'energia_sensibilidade.yaml',
                    'instalacoes_eletricas_proposta.yaml']]
    c, spec, energy, electrical = [yaml.safe_load(path.read_text()) for path in config_paths]
    c = copy.deepcopy(c)
    c['transfer_efficiency_assumed'] = spec['inverter']['efficiency_assumed']*spec['charge']['onboard_efficiency_assumed']
    if args.sem_interface:
        spec['charge']['current_modes_a_assumed'] = [0]
    _, transfer_modes_dc = potencias_interface(spec)
    c['transfer_power_kw_assumed'] = float(transfer_modes_dc.max())
    c.pop('household_aggregate_efficiency_assumed')  # Perdas calculadas por ramo nesta etapa.
    c['limits'] = spec['limits']+['Perfis horários de AC/DC substituem habitação uniforme da etapa anterior.']
    # Esta implementação exige30min para representar as janelas sem médias de pico.
    if c['step_minutes'] != 30:
        raise ValueError('Perfis de carga desta etapa exigem grade30min')
    delivery = Path('entregas/parcial_2026-10-24')
    names = ['expansao_solar.csv', 'solar_portatil_solar_portatil.csv', 'resumo_expansao_solar.json']
    manifest_path = delivery/'manifesto_entrega.json'
    manifest = json.loads(manifest_path.read_text())['artefatos']
    for name in names:
        if sha(delivery/name) != manifest[name]:
            raise ValueError(f'Entrada divergente: {name}')
    fixed48 = load_solar(delivery/names[0], 'terminal_assumed_3_modules_w', 30)
    fixed12 = load_solar(delivery/names[0], 'cab_190w_after_assumed_losses_w', 30)
    portable = load_solar(delivery/names[1], 'terminal_assumed_4_modules_w', 30)
    if not fixed48.index.equals(portable.index) or not fixed48.index.equals(fixed12.index):
        raise ValueError('Perfis solares incompatíveis')
    budget = json.loads((delivery/names[2]).read_text())['household_assumptions_excluding_dryer_kwh_day']
    index = fixed48.index
    local_h = index.hour+index.minute/60
    h = spec['household']
    ac = np.full(len(index), budget['cold_wash_once_week_daily_average_kwh']/24+spec['charge']['evse_standby_kw_assumed'])
    for start, duration, demand in [(h['hvac_start_hour_assumed'], h['hvac_duration_h_assumed'], budget['hvac_two_people_3h_assumed_cop2_5_kwh']),
                                    (h['cooktop_start_hour_assumed'], h['cooktop_duration_h_assumed'], budget['cooktop_half_hour_kwh'])]:
        if duration <= 0 or start < 0 or start+duration > 24 or start*2 % 1 or duration*2 % 1:
            raise ValueError('Janelas devem alinhar à grade e caber no dia')
        ac[(local_h >= start) & (local_h < start+duration)] += demand/duration
    dc = (budget['fridge_55w_assumed_50percent_duty_kwh']+budget['lights_pump_electronics_assumed_kwh'])/24
    house = ac/spec['inverter']['efficiency_assumed']+dc/h['dc_dc_efficiency_assumed']+spec['inverter']['idle_power_kw_published']
    data = pd.DataFrame({'fixed_kw': fixed48, 'portable_kw': portable, 'house_kw': house,
                         'house_ac_kw': ac, 'dc12_kw': dc, 'excluded_12v_solar_kw': fixed12})
    speeds = np.array(c['speed_modes_km_h'])
    v = speeds/3.6
    force = (.5*energy['air_density_kg_m3']*c['drag_coefficient_assumed']*energy['frontal_area_m2']*v*v
             + c['rolling_coefficient_assumed']*energy['mass_kg']*9.80665)
    powers = (force*v/c['traction_efficiency_assumed']+energy['driving_auxiliary_power_w'])/1000
    args.destino.mkdir(exist_ok=False, parents=True)
    data.to_csv(args.destino/'entradas_interface.csv', index_label='local_time')
    cases = {}

    def solve(name, initial, final, cap, target=None):
        print(f'Calculando {name}...', flush=True)
        r = otimizar_interface(data, c, powers, spec, initial, final, cap, target)
        if r['feasible']:
            for row in r['schedule']:
                mode = c['speed_modes_km_h'].index(row['speed_km_h']) if row['speed_km_h'] else None
                row['wheel_mechanical_kw'] = float(force[mode]*v[mode]/1000) if mode is not None else 0.
                row['motor_shaft_kw'] = None
            pd.DataFrame(r['schedule']).to_csv(args.destino/f'{name}.csv', index=False)
        cases[name] = {k: x for k, x in r.items() if k != 'schedule'}
        print(json.dumps(cases[name], ensure_ascii=False), flush=True)
        return r

    initial, final = c['traction_initial_soc'], c['traction_final_soc_i27']
    daily = solve('i27', initial, final, 24.)
    trip = {'constructed': False, 'globally_optimized': False, 'target_km': 7000.}
    if not args.sem_interface:
        first = solve('i29_primeiro', initial, final, 8.)
        cycle = solve('i29_ciclo', final, final, 8.)
        if first['feasible'] and cycle['feasible'] and cycle['distance_km'] > 1e-6:
            repeats = math.floor((7000-first['distance_km'])/cycle['distance_km'])
            remaining = 7000-first['distance_km']-repeats*cycle['distance_km']
            last = solve('i29_ultimo', final, final, 8., remaining)
            if last['feasible']:
                templates = [first, *([cycle]*repeats), last]
                rows, frames = [], []
                for day, template in enumerate(templates):
                    delta = pd.Timedelta(days=day)
                    frame = data.copy(); frame.index = frame.index+delta
                    frames.append(frame)
                    for row in template['schedule']:
                        row = row.copy(); row['start'] = (pd.Timestamp(row['start'])+delta).isoformat()
                        rows.append(row)
                verification = verificar_interface(rows, pd.concat(frames), c, powers, spec, initial, final, 8.)
                if abs(verification['distance_km']-7000) > 1e-4:
                    raise ValueError('Distância da viagem divergente')
                pd.DataFrame(rows).to_csv(args.destino/'viagem_7000km.csv', index=False)
                trip.update(constructed=True, full_days_upper_bound=len(templates), repeated_cycles=repeats,
                            verification=verification, same_june21_repeated=True)
    # Conferência da potência média/RMS é somente triagem de cargas contínuas.
    ac_modes, dc_modes = potencias_interface(spec)
    simultaneous = []
    for phase, house_power in [('base', float(ac.min())), ('hvac', float(ac[local_h == 12][0])), ('cooktop', float(ac[local_h == 19][0]))]:
        for a, p_ac, p_dc in zip(spec['charge']['current_modes_a_assumed'], ac_modes, dc_modes):
            simultaneous.append({'house_case': phase, 'charge_current_a': a, 'house_ac_kw': house_power,
                                 'shared_ac_kw': float(house_power+p_ac), 'charge_dc_input_kw': float(p_dc),
                                 'active_limit_passed': bool(house_power+p_ac <= spec['inverter']['continuous_power_kw_at40c'])})
    known_bank = electrical['service_bank']
    summary = {'status': spec['status'], 'generated_utc': datetime.now(timezone.utc).isoformat(),
               'configuration': c, 'interface_specification': spec, 'cases': cases, 'trip': trip,
               'traction_powers_kw': powers.tolist(), 'interface_oem_verified': False,
               'daily_fixed_48v_kwh': float(fixed48.sum()*.5),
               'daily_12v_solar_excluded_kwh': float(fixed12.sum()*.5),
               'house_dc_demand_kwh_day': float(data['house_kw'].sum()*.5),
               'house_ac_demand_kwh_day_including_evse_standby': float(ac.sum()*.5),
               'dc12_demand_kwh_day': float(dc*24), 'simultaneity': simultaneous,
               'conservative_max_dc_current_at44_8v_a': float((house.max()+dc_modes.max())*1000/44.8),
               'service_bank_max_continuous_a': known_bank['max_continuous_discharge_a'],
               'limitations': spec['limits']+['Solar12V não alimenta48V/HV e não é creditado às cargas desta missão; reserva conservadora, não otimização do barramento12V.',
                                              'Perfis horários de uso assumidos, sem secagem, lavagem como média semanal e sem potência de partida.',
                                              'Contabiliza18W contínuos de standby além de perdas proporcionais assumidas; não curva medida do inversor.',
                                              'A corrente anunciada pelo EVSE é limite superior; OBC pode aceitar menos ou interromper.',
                                              'Dias21junSãoCarlos repetidos, sem clima/rota real; viagem construtiva não mínimo global.']}
    paths = [*config_paths, manifest_path, *[delivery/name for name in names], Path(__file__),
             Path('scripts/calcular_agenda_portatil.py'), Path('src/motorhome/agenda_portatil.py'),
             Path('src/motorhome/interface_carga.py'),
             Path('/home/mhc/motorhome_referencias_tarefas/interface-fontes-01/nrgkick-2602-04-1.pdf')]
    summary['inputs_sha256'] = {str(path): sha(path) for path in paths}
    summary['output_csv_sha256'] = {path.name: sha(path) for path in args.destino.glob('*.csv')}
    (args.destino/'resumo_interface_carga.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False)+'\n')
    if daily['feasible']:
        frame = pd.DataFrame(daily['schedule']); hours = np.arange(len(frame))*.5
        fig, axes = plt.subplots(3, 1, figsize=(11, 8), layout='constrained', sharex=True)
        axes[0].bar(hours, frame['speed_km_h'], width=frame['driving_h'], align='edge'); axes[0].set_ylabel('Velocidade [km/h]')
        axes[1].step(hours, frame['charge_current_a'], where='post'); axes[1].set_ylabel('Corrente EVSE [A]')
        axes[2].plot(np.r_[0, hours+.5], np.r_[initial, frame['traction_kwh']/c['traction_capacity_kwh']]*100, label='Tração')
        axes[2].plot(np.r_[0, hours+.5], np.r_[c['service_initial_soc'], frame['service_kwh']/c['service_capacity_kwh']]*100, label='Serviços')
        axes[2].set(xlabel='Hora local21/06 [h]', ylabel='Janela útil [%]', xlim=(0, 24)); axes[2].legend()
        for ax in axes:
            ax.grid(alpha=.25)
        fig.suptitle(f"I27 condicionado {daily['distance_km']:.2f}km • PV48V e EVSE discreto\nAceitação OEM monofásica60Hz e proteção ainda não verificadas")
        fig.savefig(args.destino/'interface_i27.png', dpi=150); plt.close(fig)
    print(json.dumps({'trip_days_upper_bound': trip.get('full_days_upper_bound'),
                      'solar12_excluded_kwh': summary['daily_12v_solar_excluded_kwh']}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
