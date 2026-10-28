"""Adquire rotaOSRM, relevoDEM e reanáliseERA5; cache externo comSHA256 eURL."""

import argparse
import hashlib
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from motorhome.rota import amostrar_geometria, preparar_rota


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--destino', type=Path, required=True)
    args = p.parse_args()
    args.destino.mkdir(exist_ok=True, parents=True)
    source = Path('config/rota_belem_chui_proposta.yaml')
    c = yaml.safe_load(source.read_text())
    manifest_path = args.destino/'fontes.json'
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}

    def get(name, url):
        path = args.destino/name
        if path.exists():
            if name not in manifest or manifest[name]['url'] != url:
                raise ValueError('Cache sem proveniência compatível')
            b = path.read_bytes()
            if hashlib.sha256(b).hexdigest() != manifest[name]['sha256']:
                raise ValueError('Hash do cache divergente')
        else:
            req = urllib.request.Request(url, headers={'User-Agent': 'AuroraSolarAcademic/0.1'})
            for attempt in range(5):
                try:
                    with urllib.request.urlopen(req, timeout=60) as response:
                        b = response.read()
                    break
                except urllib.error.HTTPError as exc:
                    if exc.code != 429 or attempt == 4:
                        raise
                    print(f'Limite público temporário: {name}; aguardando {15*(attempt+1)}s', flush=True)
                    time.sleep(15*(attempt+1))
            d = json.loads(b)
            if isinstance(d, dict) and d.get('error'):
                raise ValueError(d)
            path.write_bytes(b)
            manifest[name] = {'url': url, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(),
                              'accessed_utc': datetime.now(timezone.utc).isoformat()}
            manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False)+'\n')
            time.sleep(2)
        return json.loads(b)

    coords = ';'.join(f'{w["lon"]},{w["lat"]}' for w in c['waypoints'])
    url = f'https://router.project-osrm.org/route/v1/driving/{coords}?overview=full&geometries=geojson&steps=true&annotations=distance,duration,speed'
    response = get('osrm.json', url)
    geometry, steps = preparar_rota(response, c)
    geometry.to_csv(args.destino/'geometria.csv', index=False)
    steps.to_csv(args.destino/'trechos.csv', index=False)
    end = float(geometry.distance_km.iloc[-1])
    positions = np.r_[np.arange(0, end, c['grade_sampling_km']), end]
    elevation = amostrar_geometria(geometry, positions)
    heights = []
    for j in range(0, len(elevation), 100):
        batch = elevation.iloc[j:j+100]
        params = urllib.parse.urlencode({'latitude': ','.join(f'{x:.6f}' for x in batch.latitude_deg),
                                        'longitude': ','.join(f'{x:.6f}' for x in batch.longitude_deg)})
        heights.extend(get(f'elevacao-{j//100:02}.json', 'https://api.open-meteo.com/v1/elevation?'+params)['elevation'])
    elevation['elevation_m'] = heights
    if not np.isfinite(elevation.to_numpy()).all():
        raise ValueError('Relevo com lacunas')
    elevation.to_csv(args.destino/'relevo.csv', index=False)
    nodes = amostrar_geometria(geometry, np.linspace(0, end, c['solar_weather_nodes']))
    weather_files = []
    for j, row in nodes.iterrows():
        params = urllib.parse.urlencode({'latitude': round(row.latitude_deg, 5), 'longitude': round(row.longitude_deg, 5),
                                        'start_date': c['start_date'], 'end_date': c['weather_end_date'],
                                        'hourly': 'shortwave_radiation,direct_normal_irradiance,diffuse_radiation,temperature_2m',
                                        'timezone': c['timezone'], 'models': 'era5'})
        filename = f'clima-{j:02}.json'
        weather = get(filename, 'https://archive-api.open-meteo.com/v1/archive?'+params)
        weather_files.append(filename)
        print(json.dumps({'node': int(j), 'route_km': round(row.distance_km), 'hours': len(weather['hourly']['time'])}), flush=True)
    nodes['weather_file'] = weather_files
    nodes.to_csv(args.destino/'nos_clima.csv', index=False)
    result = {'status': c['status'], 'distance_km': end, 'waypoints': c['waypoints'],
              'osrm_duration_h_profile': response['routes'][0]['duration']/3600,
              'road_steps': len(steps), 'geometry_nodes': len(geometry), 'dem_nodes': len(elevation),
              'config_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'source_manifest_sha256': hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
              'attribution': '©OpenStreetMap contributors, ODbL; OSRM; Open-Meteo/ERA5 CC-BY4.0; CopernicusDEM2021GLO90 DOI10.5270/ESA-c5d3d65'}
    (args.destino/'resumo_fontes_rota.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
