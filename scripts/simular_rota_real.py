"""Belém–Chuí: geografia real, limites aproximados, relevo e sol no calendário."""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import yaml

from motorhome.rota import Rota
from motorhome.viagem_rota import SolarRota, simular_viagem


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--fontes', required=True, type=Path)
    p.add_argument('--destino', required=True, type=Path)
    p.add_argument('--historico', action='store_true', help='Método anterior às DEC001/020/043; não representa o baseline atual')
    args = p.parse_args()
    if not args.historico:
        p.error('Execução histórica bloqueada por padrão após DEC061. Use scripts/conciliar_dec061.py; --historico permite apenas reproduzir o método antigo, sem validade para a arquitetura B.')
    paths = [Path('config')/name for name in ['rota_belem_chui_proposta.yaml', 'agenda_portatil_proposta.yaml',
             'interface_carga_proposta.yaml', 'energia_sensibilidade.yaml', 'solar_proposta.yaml', 'solar_portatil_proposta.yaml']]
    c, battery, spec, dynamics, solar_config, portable = [yaml.safe_load(path.read_text()) for path in paths]
    manifest = json.loads((args.fontes/'fontes.json').read_text())
    for name, record in manifest.items():
        if sha(args.fontes/name) != record['sha256']:
            raise ValueError('Fonte alterada: '+name)
    if json.loads((args.fontes/'resumo_fontes_rota.json').read_text())['config_sha256'] != sha(paths[0]):
        raise ValueError('Configuração mudou desde a aquisição das fontes')
    geometry, steps, elevation = [pd.read_csv(args.fontes/name) for name in ['geometria.csv', 'trechos.csv', 'relevo.csv']]
    route = Rota(steps, elevation, dynamics, battery, c['regeneration_efficiency_assumed'])
    print('Preparando geração solar geográfica/histórica...', flush=True)
    solar = SolarRota(args.fontes, solar_config, portable, c['timezone'])
    args.destino.mkdir(exist_ok=False, parents=True)
    source_budget = Path('entregas/parcial_2026-10-24/resumo_expansao_solar.json')
    budget = json.loads(source_budget.read_text())['household_assumptions_excluding_dryer_kwh_day']
    cases, curves = {}, {}
    configurations = [(weather, speed, True) for weather in ['clear', 'era5'] for speed in c['cruise_caps_km_h']]
    configurations.append(('clear', 80, False))
    for scenario, speed, interface in configurations:
        name = f'{scenario}_{speed}'+('' if interface else '_sem_interface')
        print('Simulando '+name, flush=True)
        summary, frame, drive = simular_viagem(route, solar, geometry, c, battery, spec, budget, speed, scenario, interface)
        frame.to_csv(args.destino/f'{name}_agenda.csv', index=False)
        drive.to_csv(args.destino/f'{name}_conducao.csv', index=False)
        if len(frame):
            frame.index = pd.DatetimeIndex(pd.to_datetime(frame.start, utc=True)).tz_convert(c['timezone'])
            daily = frame.groupby(frame.index.date).agg(distance_km=('position_end_km', 'last'), driving_h=('driving_h', 'sum'),
                                                       traction_soc=('traction_kwh', 'last'), service_soc=('service_kwh', 'last'))
            daily['traction_soc'] /= battery['traction_capacity_kwh']
            daily['service_soc'] /= battery['service_capacity_kwh']
            daily['solar_kwh'] = frame.solar_kw.groupby(frame.index.date).sum()*c['integration_minutes']/60
            daily['house_kwh'] = frame.house_dc_kw.groupby(frame.index.date).sum()*c['integration_minutes']/60
            daily.to_csv(args.destino/f'{name}_dias.csv', index_label='date')
            curves[name] = daily
        summary['agenda_csv'] = f'{name}_agenda.csv'
        summary['driving_csv'] = f'{name}_conducao.csv'
        cases[name] = summary
        print(json.dumps(summary, ensure_ascii=False), flush=True)
    route_summary = {'status': c['status'], 'generated_utc': datetime.now(timezone.utc).isoformat(), 'configuration': c,
                     'actual_route_km': route.total_km, 'prescribed_distance_km': 7000,
                     'extra_distance_km': route.total_km-7000, 'cases': cases,
                     'physical_vehicle_validated': False, 'sources_attribution': '©OpenStreetMap contributors/OSRM; Open-Meteo/ERA5; CopernicusDEM2021GLO90 DOI10.5270/ESA-c5d3d65',
                     'solar_method': 'pvlibIneichen céu limpo variável por data/local OU ERA5horário; interpolação linear entre14nós na distância da rota; PV12V sem crédito',
                     'time_resolution_minutes': c['integration_minutes'], 'weather_resolution_h': 1,
                     'unavailable_trailing_weather_hours_discarded': solar.trailing_unavailable_hours,
                     'last_available_weather_hour': solar.index[-1].isoformat(),
                     'limitations': c['limits']+['Mapas motor/eficiência/Cd/Cr e demandaHVAC são os cenários condicionados anteriores.',
                                                'Não inclui acelerações, filas, pedágios, vento relativo, partidas dos aparelhos ou secagem.',
                                                'Relevo em5km não resolve rampas curtas; céu limpo usa25°C e vento0, histórico usa temperaturaERA5 e vento0.',
                                                'A política pode falhar onde outra gestão de energia seria viável; falha de política não prova inviabilidade global.']}
    input_paths = [*paths, source_budget, Path(__file__), Path('src/motorhome/rota.py'), Path('src/motorhome/viagem_rota.py'),
                   Path('src/motorhome/interface_carga.py'), args.fontes/'fontes.json', args.fontes/'resumo_fontes_rota.json',
                   *[args.fontes/name for name in ['geometria.csv', 'trechos.csv', 'relevo.csv', 'nos_clima.csv']]]
    route_summary['inputs_sha256'] = {str(path): sha(path) for path in input_paths}
    for name in ['trechos.csv', 'relevo.csv', 'nos_clima.csv']:
        (args.destino/name).write_bytes((args.fontes/name).read_bytes())
    route_summary['output_csv_sha256'] = {path.name: sha(path) for path in args.destino.glob('*.csv')}
    (args.destino/'resumo_rota_real.json').write_text(json.dumps(route_summary, indent=2, ensure_ascii=False)+'\n')
    fig, axes = plt.subplots(1, 2, figsize=(12, 8), layout='constrained')
    axes[0].plot(geometry.longitude_deg, geometry.latitude_deg, color='#2266aa', lw=1)
    for w in c['waypoints'][::2]:
        axes[0].scatter(w['lon'], w['lat'], s=9, color='black')
        axes[0].annotate(w['name'], (w['lon'], w['lat']), fontsize=7, xytext=(3, 3), textcoords='offset points')
    axes[0].set(xlabel='Longitude [graus]', ylabel='Latitude [graus]', title=f'Corredor costeiro roteado: {route.total_km:.1f}km')
    axes[0].set_aspect(1.05)
    for name, data in curves.items():
        axes[1].plot(range(1, len(data)+1), data.distance_km, label=name, lw=1.2)
    axes[1].axhline(7000, color='black', lw=.8, ls='--', label='7000km do enunciado')
    axes[1].set(xlabel='Dias desde21/06/2025', ylabel='Progresso [km]', title='Política com solar local, reservas e até8h/dia')
    axes[1].legend(fontsize=7)
    for ax in axes:
        ax.grid(alpha=.25)
    fig.suptitle('AuroraSolar • rotaOSRM e cenários condicionados de energia\nLimites aproximados; interfaceOEM ainda hipotética; sem certificado de mínimo global')
    fig.savefig(args.destino/'rota_e_progresso.png', dpi=170)
    plt.close(fig)


if __name__ == '__main__':
    main()
