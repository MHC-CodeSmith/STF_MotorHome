"""I27 atual e agenda construtiva I29 com portátil; hipótese HV explícita."""

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

from motorhome.agenda_portatil import otimizar_dia, verificar_agenda


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_solar(path, column, step_minutes):
    raw = pd.read_csv(path, index_col=0)
    index = pd.DatetimeIndex(pd.to_datetime(raw.index, utc=True)).tz_convert('America/Sao_Paulo')
    if (len(index) != 1441 or index[0].hour != 0 or index[0].minute != 0
            or not np.allclose((index[1:]-index[:-1]).total_seconds(), 60)
            or not np.isfinite(raw[column]).all() or (raw[column] < 0).any()):
        raise ValueError('Esperado dia completo de 1441 amostras solares a cada minuto')
    # Trapézios por intervalo preservam a integral do perfil original, sem usar
    # sol de outro horário no estado aberto. A meia-noite final não vira novo dia.
    values = raw[column].to_numpy()/1000
    return pd.Series([float(np.trapz(values[i:i+step_minutes+1], dx=1)/step_minutes)
                      for i in range(0, 1440, step_minutes)], index=index[:-1:step_minutes])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--destino', required=True, type=Path)
    p.add_argument('--config', default=Path('config/agenda_portatil_proposta.yaml'), type=Path)
    p.add_argument('--step-minutes', type=int, help='Sobrescreve só a grade deste cenário')
    p.add_argument('--daily-only', action='store_true', help='Calcula somente I27 para comparar grades')
    p.add_argument('--historico', action='store_true', help='Método anterior às DEC001/020/043; não representa o baseline atual')
    args = p.parse_args()
    if not args.historico:
        p.error('Execução histórica bloqueada por padrão após DEC061. Use scripts/conciliar_dec061.py; --historico permite apenas reproduzir o método antigo, sem validade para a arquitetura B.')
    delivery = Path('entregas/parcial_2026-10-24')
    names = ['expansao_solar.csv', 'solar_portatil_solar_portatil.csv',
             'resumo_expansao_solar.json', 'resumo_solar_portatil.json']
    manifest_path = delivery/'manifesto_entrega.json'
    manifest = json.loads(manifest_path.read_text())['artefatos']
    for name in names:
        if sha(delivery/name) != manifest[name]:
            raise ValueError(f'Fonte da entrega com hash divergente: {name}')
    config_paths = [args.config, Path('config/energia_sensibilidade.yaml'),
                    Path('config/limites_operacionais_proposta.yaml'),
                    Path('config/instalacoes_eletricas_proposta.yaml')]
    c, e, limit, electrical = [yaml.safe_load(path.read_text()) for path in config_paths]
    if args.step_minutes is not None:
        c['step_minutes'] = args.step_minutes
    if (c['status'] != 'ESTIMATIVA_CONDICIONADA_NAO_VALIDADA' or c['transfer_interface_verified']
            or max(c['speed_modes_km_h']) > limit['speed_limiter_km_h']):
        raise ValueError('Hipóteses/limite de velocidade incompatíveis com este estudo')
    step = c['step_minutes']
    if not isinstance(step, int) or step <= 0 or 1440 % step:
        raise ValueError('Passo em minutos inteiros deve dividir o dia')
    if not 0 < c['household_aggregate_efficiency_assumed'] <= 1:
        raise ValueError('Eficiência residencial inválida')
    bank = electrical['service_bank']
    if (c['service_capacity_kwh'] != bank['energy_kwh']
            or c['service_min_soc'] < 1-bank['assumed_max_dod']-1e-9):
        raise ValueError('Capacidade/reserva de serviços incompatível com a proposta elétrica')
    fixed = load_solar(delivery/names[0], 'mixed_stowed_w', step)
    portable = load_solar(delivery/names[1], 'terminal_assumed_4_modules_w', step)
    if not fixed.index.equals(portable.index):
        raise ValueError('Datas solares incompatíveis')
    expansion, solar = [json.loads((delivery/name).read_text()) for name in names[2:]]
    if (abs(fixed.sum()*step/60-expansion['energy_kwh']['mixed_stowed_w']) > 1e-8
            or abs(portable.sum()*step/60-solar['portable_generation_kwh_day']) > 1e-8):
        raise ValueError('Integral solar divergente dos resumos atuais')
    data = pd.DataFrame({'fixed_kw': fixed, 'portable_kw': portable,
                         'house_kw': expansion['household_total_excluding_dryer_kwh_day']/24/
                         c['household_aggregate_efficiency_assumed']})
    v = np.array(c['speed_modes_km_h'])/3.6
    force = (.5*e['air_density_kg_m3']*c['drag_coefficient_assumed']*e['frontal_area_m2']*v**2
             + c['rolling_coefficient_assumed']*e['mass_kg']*9.80665)
    drive_kw = (force*v/c['traction_efficiency_assumed']+e['driving_auxiliary_power_w'])/1000
    wheel_kw = force*v/1000
    args.destino.mkdir(parents=True, exist_ok=False)
    data.to_csv(args.destino/'entradas_grade.csv', index_label='local_time')
    cases = {}

    def solve(name, initial, final, cap, transfer, target=None):
        print(f'Calculando {name}...', flush=True)
        r = otimizar_dia(data, c, drive_kw, initial, final, cap, transfer, target)
        if r['feasible']:
            for row in r['schedule']:
                mode = c['speed_modes_km_h'].index(row['speed_km_h']) if row['speed_km_h'] else None
                row['wheel_mechanical_kw'] = float(wheel_kw[mode]) if mode is not None else 0.
                row['motor_shaft_kw'] = None  # Não inventar perdas/relação da transmissão.
            pd.DataFrame(r['schedule']).to_csv(args.destino/f'{name}.csv', index=False)
        cases[name] = {k: value for k, value in r.items() if k != 'schedule'}
        print(json.dumps(cases[name], ensure_ascii=False), flush=True)
        return r

    initial, final, transfer = c['traction_initial_soc'], c['traction_final_soc_i27'], c['transfer_power_kw_assumed']
    solve('i27_sem_interface', initial, final, 24., 0.)
    daily = solve('i27_com_interface_hipotetica', initial, final, 24., transfer)
    first = solve('i29_primeiro_dia', initial, final, 8., transfer) if not args.daily_only else {'feasible': False}
    cycle = solve('i29_dia_ciclico', final, final, 8., transfer) if not args.daily_only else {'feasible': False}
    trip = {'constructed': False, 'globally_optimized': False, 'distance_target_km': 7000.}
    if first['feasible'] and cycle['feasible'] and cycle['distance_km'] > 1e-6:
        if first['distance_km'] >= 7000:
            raise ValueError('Caso inesperado: primeiro dia já excede a missão; revisar cenário')
        repeats = math.floor((7000-first['distance_km'])/cycle['distance_km'])
        remaining = 7000-first['distance_km']-repeats*cycle['distance_km']
        last = solve('i29_ultimo_dia', final, final, 8., transfer, remaining) if remaining > 1e-6 else None
        if last is None or last['feasible']:
            templates = [first, *([cycle]*repeats), *([last] if last is not None else [])]
            rows, frames = [], []
            for day, template in enumerate(templates):
                offset = pd.Timedelta(days=day)
                frame = data.copy()
                frame.index = frame.index+offset
                frames.append(frame)
                for item in template['schedule']:
                    row = copy.deepcopy(item)
                    row['start'] = (pd.Timestamp(row['start'])+offset).isoformat()
                    rows.append(row)
            verification = verificar_agenda(rows, pd.concat(frames), c, drive_kw,
                                              initial, final, 8., transfer)
            if abs(verification['distance_km']-7000) > 1e-4:
                raise ValueError('Verificação rejeitou distância da viagem')
            pd.DataFrame(rows).to_csv(args.destino/'i29_viagem_7000km.csv', index=False)
            trip.update(constructed=True, full_days=len(templates), repeated_cycle_days=repeats,
                        elapsed_days_upper_bound=len(templates),
                        arrival_upper_bound=(data.index[0]+pd.Timedelta(days=len(templates))).isoformat(),
                        verification=verification,
                        scope='Inclui esperas e serviços até meia-noite final; política diária repetida, não menor tempo I29')
    speed_per_kwh = np.array(c['speed_modes_km_h'])/drive_kw
    no_hv_bound = c['traction_capacity_kwh']*(initial-c['traction_min_soc'])*float(speed_per_kwh.max())
    sources = [*config_paths, manifest_path, *[delivery/name for name in names],
               Path(__file__), Path('src/motorhome/agenda_portatil.py')]
    result = {'status': c['status'], 'generated_utc': datetime.now(timezone.utc).isoformat(),
              'vehicle_validated': False, 'transfer_interface_verified': False,
              'inputs_sha256': {str(path): sha(path) for path in sources},
              'configuration': c, 'traction_modes_kw': drive_kw.tolist(),
              'wheel_mechanical_modes_kw': wheel_kw.tolist(), 'motor_shaft_modes_kw': None,
              'daily_only': args.daily_only,
              'full_day_fixed_kwh': float(fixed.sum()*step/60),
              'full_day_portable_kwh_if_always_deployed': float(portable.sum()*step/60),
              'house_battery_demand_kwh_day': float(data['house_kw'].sum()*step/60),
              'cases': cases, 'trip_7000km': trip,
              'without_hv_interface': {'traction_distance_upper_bound_km_in_this_model': no_hv_bound,
                                       '7000km_infeasible_in_this_model': no_hv_bound < 7000,
                                       'basis': 'Reserva10%, só98kWh de tração; melhor km/kWh dos modos, sem contribuição solar HV'},
              'notes': c['limits']+['Certificado MILP é restrito a esta grade/modos e duração variável, não controle contínuo.',
                                     'Optimal_in_grid false preserva incumbente e limite superior; viagem só é limite superior condicionado.']}
    outputs = sorted(args.destino.glob('*.csv'))
    result['output_csv_sha256'] = {path.name: sha(path) for path in outputs}
    (args.destino/'resumo_agenda_portatil.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    if daily['feasible']:
        frame = pd.DataFrame(daily['schedule'])
        hours = np.arange(len(frame))*step/60
        fig, axes = plt.subplots(3, 1, figsize=(11, 8), layout='constrained', sharex=True)
        axes[0].bar(hours, frame['speed_km_h'], width=frame['driving_h'], align='edge')
        axes[0].set_ylabel('Velocidade [km/h]')
        axes[1].step(hours, frame['fixed_kw']+frame['portable_kw'], where='post', label='Solar disponível')
        axes[1].step(hours, frame['transfer_kw'], where='post', label='Transferência hipotética HV')
        axes[1].bar(hours, frame['drive_kw'], width=frame['driving_h'], align='edge', alpha=.3, label='Demanda na tração')
        axes[1].set_ylabel('Potência [kW]'); axes[1].legend()
        axes[2].plot(np.r_[0, hours+step/60], np.r_[initial, frame['traction_kwh']/c['traction_capacity_kwh']]*100, label='Tração')
        axes[2].plot(np.r_[0, hours+step/60], np.r_[c['service_initial_soc'], frame['service_kwh']/c['service_capacity_kwh']]*100, label='Serviços')
        axes[2].set(xlabel='Hora local 21/06 [h]', ylabel='Janela útil [%]', xlim=(0, 24)); axes[2].legend()
        for ax in axes:
            ax.grid(alpha=.25)
        fig.suptitle(f"I27 condicionado: {daily['distance_km']:.2f}km; SOC tração final30%\nBancos separados; conexão HV hipotética; não validação do veículo")
        fig.savefig(args.destino/'agenda_i27.png', dpi=150); plt.close(fig)
    print(json.dumps({'trip': {k: v for k, v in trip.items() if k != 'verification'},
                      'without_hv_interface_upper_bound_km': no_hv_bound}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
