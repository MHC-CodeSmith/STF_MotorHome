"""Geometria rodoviáriaOSRM, limites aproximados e consumo por trecho com relevo."""

import re

import numpy as np
import pandas as pd


def preparar_rota(payload, config):
    if payload.get('code') != 'Ok' or len(payload.get('routes', [])) != 1:
        raise ValueError('Uma rotaOSRM válida obrigatória')
    route = payload['routes'][0]
    coords = np.asarray(route['geometry']['coordinates'], dtype=float)
    distances = np.concatenate([leg['annotation']['distance'] for leg in route['legs']])
    if len(coords) != len(distances)+1 or not np.isfinite(coords).all() or (distances < 0).any():
        raise ValueError('Geometria/anotações incompatíveis')
    distance = np.r_[0., np.cumsum(distances)/1000]
    if abs(distance[-1]-route['distance']/1000) > .01:
        raise ValueError('Distância geométrica e resumo divergentes')
    geometry = pd.DataFrame({'distance_km': distance, 'longitude_deg': coords[:, 0],
                             'latitude_deg': coords[:, 1]})
    steps, offset = [], 0.
    caps = config['approximate_caps_km_h']
    for i, leg in enumerate(route['legs']):
        for step in leg['steps']:
            if step['distance'] <= 0:
                continue
            if step.get('mode') != 'driving' or step['duration'] <= 0:
                raise ValueError('Balsa/modo não rodoviário ou tempo inválido na rota')
            ref, name = step.get('ref', ''), step.get('name', '')
            if re.search(r'BR[- ]?\d', ref):
                category = 'federal'
            elif re.search(r'[A-Z]{2}[- ]?\d', ref):
                category = 'state'
            elif re.search(r'avenida|rua|travessa|praça|alameda', name, re.IGNORECASE):
                category = 'urban'
            else:
                category = 'other'
            estimated = 3.6*step['distance']/step['duration']
            cap = min(caps[category], config['vehicle_limiter_km_h'])
            steps.append({'start_km': offset, 'end_km': offset+step['distance']/1000,
                          'leg': i, 'road': name, 'ref': ref, 'category': category,
                          'approximate_cap_km_h': cap, 'osrm_average_km_h': estimated,
                          'model_max_km_h': min(cap, estimated), 'posted_limit_verified': False})
            offset += step['distance']/1000
    if abs(offset-distance[-1]) > .01:
        raise ValueError('Soma dos passosOSRM divergente')
    # Diferenças de arredondamento entre distâncias dos passos/anotações (<10m).
    steps[-1]['end_km'] = distance[-1]
    return geometry, pd.DataFrame(steps)


def amostrar_geometria(geometry, positions):
    return pd.DataFrame({'distance_km': positions,
                         'latitude_deg': np.interp(positions, geometry.distance_km, geometry.latitude_deg),
                         'longitude_deg': np.interp(positions, geometry.distance_km, geometry.longitude_deg)})


class Rota:
    def __init__(self, steps, elevation, dynamics, proposal, regen=.5):
        self.steps, self.elevation = steps, elevation
        self.end = steps.end_km.to_numpy(float)
        self.total_km = float(self.end[-1])
        self.dynamics, self.proposal = dynamics, proposal
        self.regen = regen
        if (not 0 <= regen <= 1 or not np.isfinite(self.end).all()
                or (np.diff(self.end) <= 0).any()
                or not np.isfinite(elevation[['distance_km', 'elevation_m']]).all().all()
                or (np.diff(elevation.distance_km) <= 0).any()):
            raise ValueError('Perfil de rota inválido')

    def mover(self, position, duration_h, cruise_cap, target_km=None):
        """Cruza tantos trechos quanto caibam no tempo; exporta cada velocidade.

        Energia positiva resiste; recuperação apenas para potência mecânica
        líquida negativa, evitando recuperar toda descida além do arrasto.
        """
        if not 0 <= position <= self.total_km or duration_h <= 0 or cruise_cap <= 0:
            raise ValueError('Posição/duração/velocidade inválidas')
        target = self.total_km if target_km is None else min(target_km, self.total_km)
        if target < position:
            raise ValueError('Alvo anterior à posição')
        remaining, pieces = duration_h, []
        while remaining > 1e-10 and position < target-1e-9:
            j = min(int(np.searchsorted(self.end, position+1e-9, side='right')), len(self.end)-1)
            speed = min(cruise_cap, float(self.steps.iloc[j].model_max_km_h))
            boundary = min(target, self.end[j])
            # Também dividir nas quebras doDEM, mesmo em passosOSRM longos.
            elevations = self.elevation.distance_km.to_numpy()
            ei = np.searchsorted(elevations, position+1e-9, side='right')
            if ei < len(elevations):
                boundary = min(boundary, elevations[ei])
            distance = min(boundary-position, remaining*speed)
            dt = distance/speed
            z0, z1 = np.interp([position, position+distance], elevations, self.elevation.elevation_m)
            grade = (z1-z0)/(distance*1000)
            v = speed/3.6
            d, p = self.dynamics, self.proposal
            force = (.5*d['air_density_kg_m3']*p['drag_coefficient_assumed']*d['frontal_area_m2']*v*v
                     + p['rolling_coefficient_assumed']*d['mass_kg']*9.80665*np.cos(np.arctan(grade))
                     + d['mass_kg']*9.80665*np.sin(np.arctan(grade)))
            wheel_kw = force*v/1000
            battery_kw = (wheel_kw/p['traction_efficiency_assumed'] if wheel_kw >= 0 else wheel_kw*self.regen)+d['driving_auxiliary_power_w']/1000
            pieces.append({'start_km': position, 'end_km': position+distance, 'duration_h': dt,
                           'speed_km_h': speed, 'step_index': j, 'grade_fraction': grade,
                           'approximate_cap_km_h': float(self.steps.iloc[j].approximate_cap_km_h),
                           'wheel_kw': wheel_kw, 'battery_kw': battery_kw, 'battery_kwh': battery_kw*dt})
            position += distance
            remaining -= dt
        return pieces
