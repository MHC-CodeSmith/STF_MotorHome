"""Agenda construtiva de 7000 km; limite superior condicionado, não ótimo I29."""

import argparse
import csv
import hashlib
import json
import sys
from datetime import timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

from motorhome.agenda_energia import Intervalo, verificar_agenda


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cenario', type=Path, required=True)
    p.add_argument('--solar-csv', type=Path, required=True)
    p.add_argument('--destino', type=Path, required=True)
    args = p.parse_args()
    scenario = json.loads(args.cenario.read_text())
    if scenario['status'] != 'ESTIMATIVA_CONDICIONADA_NAO_VALIDADA':
        raise ValueError('Esta rotina exige cenário condicionado')
    c = scenario['scenario']
    raw = pd.read_csv(args.solar_csv)
    raw.index = pd.DatetimeIndex(pd.to_datetime(raw.pop('local_time'), utc=True)).tz_convert('America/Sao_Paulo')
    solar = raw['terminal_assumed_2_modules_w'].resample('30min').mean().iloc[:48].to_numpy()
    # Escolha construtiva: apenas velocidade 20 km/h, condução noturna;
    # reserva adicional de um dia de habitação evita comprometer a noite futura.
    v = c['speed_modes_m_s'][1]
    drive_w, idle_w = c['terminal_power_modes_w'][1], c['terminal_power_modes_w'][0]
    if v <= 0 or idle_w < 0 or drive_w <= idle_w or len(solar) != 48:
        raise ValueError('Entradas incompatíveis com a política construtiva')
    capacity = c['battery_usable_kwh_oem']*3_600_000
    energy, distance, reserve = capacity, 0., .1*capacity
    clock = raw.index[0].to_pydatetime()
    intervals, daily_driving, daily_states = [], {}, {}
    target, step = 7_000_000., 1800.
    for index in range(48*3650):
        available = float(solar[index % 48])
        day = clock.date().isoformat()
        driven = daily_driving.get(day, 0.)
        seconds = min(step, (target-distance)/v)
        drive = (available < 1e-9 and driven+seconds <= 28800+1e-8
                 and energy-drive_w*seconds >= reserve+idle_w*86400)
        if drive:
            demand, pv, speed = drive_w, 0., v
            daily_driving[day] = driven+seconds
        else:
            seconds, demand, pv, speed = step, idle_w, available, 0.
        end = clock+timedelta(seconds=seconds)
        energy = min(capacity, energy+(pv-demand)*seconds)
        if energy < reserve-1e-5:
            raise ValueError('Política esgotou a reserva; cenário não gerou agenda viável')
        intervals.append(Intervalo(clock, end, speed, demand, pv,
                                   'CONDICIONADO: repetição de 21/06; potência de sensibilidade; sem carga externa'))
        distance += speed*seconds
        daily_states[day] = {'distance_km': distance/1000, 'soc': energy/capacity}
        clock = end
        if target-distance < 1e-4:
            break
    else:
        raise ValueError('Não chegou dentro de 3650 dias; não é prova de inviabilidade global')
    verification = verificar_agenda(intervals, capacity, 1., 1., 1., .1, 28800., target, .01,
                                    permitir_corte_solar=True)
    if not verification['viavel_no_modelo']:
        raise ValueError(f'Verificação independente rejeitou: {verification["violacoes"][:5]}')
    args.destino.mkdir(parents=True, exist_ok=False)
    with (args.destino/'agenda_7000km.csv').open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['start', 'end', 'speed_m_s', 'demand_w', 'solar_w'])
        writer.writerows([s.inicio.isoformat(), s.fim.isoformat(), s.velocidade_m_s,
                          s.demanda_terminal_w, s.solar_terminal_w] for s in intervals)
    summary = {'status': scenario['status'], 'vehicle_validated': False,
               'script': 'scripts/construir_viagem_condicionada.py', 'optimized': False,
               'scope': 'Agenda construtiva: limite superior de tempo apenas no modelo condicionado',
               'assumptions': ['Repete o mesmo perfil solar de São Carlos em 21/06 em todos os dias/locais/anos',
                               'Não é previsão de geração na rota Belém–Chuí',
                               'Integração solar à tração ainda não verificada',
                               'Condução noturna a 20 km/h; cargas constantes; sem acelerações ou relevo',
                               'Cr, eficiência e auxiliares assumidos; Cd piloto não validado',
                               'Descarga/recarga de energia útil sem modelo de tensão/temperatura/BMS'],
               'elapsed_days': (clock-intervals[0].inicio).total_seconds()/86400,
               'calendar_days': len(daily_states), 'arrival': clock.isoformat(),
               'distance_m': verification['distancia_m'], 'final_soc': verification['soc_final'],
               'max_driving_hours_calendar_day': max(verification['conducao_por_dia_s'].values())/3600,
               'independent_energy_residual_j': verification['residuo_energia_j'],
               'independently_feasible_in_model': verification['viavel_no_modelo'],
               'external_charging': False,
               'initial_energy_kwh': verification['energia_inicial_j']/3_600_000,
               'solar_energy_kwh': verification['solar_terminal_j']/3_600_000,
               'terminal_demand_kwh': verification['demanda_terminal_j']/3_600_000,
               'curtailed_solar_kwh': verification['corte_solar_terminal_j']/3_600_000,
               'inputs_sha256': {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in [args.cenario, args.solar_csv]},
               'schedule_csv_sha256': hashlib.sha256((args.destino/'agenda_7000km.csv').read_bytes()).hexdigest()}
    (args.destino/'resumo_viagem_7000km.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    frame = pd.DataFrame(daily_states).T
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), layout='constrained', sharex=True)
    axes[0].plot(range(1, len(frame)+1), frame['distance_km']); axes[0].set_ylabel('Distância acumulada [km]')
    axes[1].plot(range(1, len(frame)+1), frame['soc']*100)
    axes[1].set(xlabel='Dia do cenário repetido', ylabel='Janela útil [%]')
    for ax in axes:
        ax.grid(alpha=.3)
    fig.suptitle(f"7000 km em {summary['elapsed_days']:.1f} dias — agenda construtiva, não ótimo\nHipóteses condicionadas e mesmo sol de 21/06 repetido; não resultado validado da rota")
    fig.savefig(args.destino/'viagem_7000km.png', dpi=150); plt.close(fig)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    main()
