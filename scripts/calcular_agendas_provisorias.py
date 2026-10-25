"""Integra cenário energético condicionado ao MILP; não valida o motorhome."""

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
import pandas as pd
import yaml

from motorhome.otimizacao_agenda import maximizar_distancia
from motorhome.otimizacao_viagem import minimizar_tempo


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--solar-csv', type=Path, required=True)
    p.add_argument('--config', type=Path, required=True)
    p.add_argument('--destino', type=Path, required=True)
    args = p.parse_args()
    c = yaml.safe_load(args.config.read_text())
    if c['status'] != 'ESTIMATIVA_CONDICIONADA_NAO_VALIDADA':
        raise ValueError('A rotina exige hipóteses explicitamente condicionadas')
    raw = pd.read_csv(args.solar_csv)
    raw.index = pd.DatetimeIndex(pd.to_datetime(raw.pop('local_time'), utc=True)).tz_convert('America/Sao_Paulo')
    solar = raw['terminal_assumed_2_modules_w'].resample('30min').mean().iloc[:48]
    # Exige um dia completo à resolução de 1 min; médias mantêm energia diária.
    if len(raw) != 1441 or len(solar) != 48 or not np.isfinite(solar).all():
        raise ValueError('Esperado dia solar de 1441 amostras, incluindo a meia-noite final')
    v = np.array([0., 20., 30., 40., 60., 80.])/3.6
    cd, cr, eta = .62487678, .012, .90
    watts = ((.5*c['air_density_kg_m3']*cd*c['frontal_area_m2']*v**2
              + cr*c['mass_kg']*9.80665)*v)/eta+c['driving_auxiliary_power_w']
    watts[0] = 100.  # hipótese explícita, não BOM de habitação validada
    common = {'inicios': solar.index, 'duracao_s': 1800., 'velocidades_m_s': v, 'demandas_w': watts,
                  'solar_w': solar.to_numpy(), 'capacidade_j': 98*3_600_000., 'soc_inicial': 1.,
                  'soc_minimo': .10, 'eficiencia_carga': 1., 'eficiencia_descarga': 1.,
                  'limite_diario_s': 28800., 'solar_durante_conducao': False, 'tempo_limite_s': 30}
    # Eficiências unitárias aqui: potência de tração já referida aos terminais,
    # solar já contém perdas. Não é afirmação de bateria sem perdas internas.
    # O limite de 8 h pertence a I29; I27 só impõe o horizonte de um dia.
    daily_inputs = dict(common)
    daily_inputs['limite_diario_s'] = 86400.
    daily = maximizar_distancia(**daily_inputs, soc_final=.30, tolerancia_soc=0.)
    short_trip = minimizar_tempo(**common, distancia_m=100_000.)
    # I29: limite inferior otimista de energia, não agenda nem tempo mínimo.
    # Ignora arrasto, auxiliares e perdas; usa apenas Cr mínimo assumido.
    rolling_kwh = min(c['rolling_coefficients'])*c['mass_kg']*9.80665*7_000_000/3_600_000
    daily_pv = float(solar.sum()*.5/1000)
    bound_days = max(1, int(np.ceil(max(0, rolling_kwh-98)/daily_pv)))
    summary = {'status': c['status'], 'vehicle_validated': False,
               'inputs_sha256': {str(f): hashlib.sha256(f.read_bytes()).hexdigest() for f in [args.config, args.solar_csv]},
               'scenario': {'cd_pilot': cd, 'cr_assumed': cr, 'traction_efficiency_assumed': eta,
                            'parked_auxiliary_w_assumed': 100., 'battery_usable_kwh_oem': 98.,
                            'soc_definition': 'fração da janela útil de 98 kWh; não SOC OEM confirmado',
                            'solar_while_driving': False, 'solar_interface_verified': False,
                            'grade_s': 1800, 'speed_modes_m_s': v.tolist(), 'terminal_power_modes_w': watts.tolist(),
                            'day_27_driving_cap_s': 86400, 'trip_29_driving_cap_s': 28800,
                            'initial_soc_assumed': 1.},
               'item27_conditioned': daily, 'short_trip_100km_conditioned': short_trip,
               'item29_7000km_lower_bound_only': {
                   'rolling_energy_optimistic_kwh': rolling_kwh,
                   'minimum_calendar_days_at_repeated_june21': bound_days,
                   'assumptions': 'Cr mínimo da grade, sem arrasto/perdas/auxiliares, toda bateria inicial e solar disponíveis; não agenda viável, não previsão meteorológica anual',
                   'optimized_7000km': False},
               'daily_energy_budget': {'solar_2_panels_kwh': daily_pv,
                                       'house_100w_kwh_per_day_assumed': 2.4,
                                       'house_200w_kwh_per_day_assumed': 4.8}}
    args.destino.mkdir(parents=True, exist_ok=False)
    (args.destino/'resumo_agendas.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    if daily['feasible']:
        frame = pd.DataFrame(daily['schedule'])
        frame.to_csv(args.destino/'agenda_i27.csv', index=False)
        hours = np.arange(len(frame))*.5
        fig, axes = plt.subplots(3, 1, figsize=(11, 8), layout='constrained', sharex=True)
        axes[0].step(hours, frame['speed_m_s']*3.6, where='post'); axes[0].set_ylabel('Velocidade [km/h]')
        axes[1].step(hours, frame['terminal_demand_w']/1000, where='post', label='Demanda terminal')
        axes[1].step(hours, frame['available_solar_w']/1000, where='post', label='Solar disponível')
        axes[1].set_ylabel('Potência [kW]'); axes[1].legend()
        axes[2].plot(np.r_[0, hours+.5], np.r_[1., frame['soc_final']]*100)
        axes[2].set(xlabel='Hora local, 21/06 [h]', ylabel='Janela útil [%]', xlim=(0, 24))
        for ax in axes:
            ax.grid(alpha=.3)
        fig.suptitle(f"I27 — cenário condicionado: {daily['distance_m']/1000:.1f} km; SOC final {daily['final_soc']*100:.2f}%\nNão é resultado validado do veículo; ótimo somente se indicado pelo solver")
        fig.savefig(args.destino/'agenda_i27.png', dpi=150); plt.close(fig)
    print(json.dumps({'i27_feasible': daily['feasible'], 'i27_optimal': daily['optimal_in_grid'],
                      'i27_distance_m': daily.get('distance_m'), 'short_trip_elapsed_s': short_trip.get('elapsed_s'),
                      '7000km_optimistic_lower_bound_days': bound_days}))


if __name__ == '__main__':
    main()
