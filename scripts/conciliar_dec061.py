"""Reexecuta o baseline pós-DEC061 sem promover hipóteses a validação física.

Uso: PYTHONPATH=src .venv/bin/python scripts/conciliar_dec061.py
Saídas numéricas e matrizes derivadas; não altera o registro original.
"""
import argparse
import copy
import csv
import gzip
import hashlib
import itertools
import json
import platform
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pvlib
import scipy
import yaml
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
sys.path.insert(0, str(ROOT/'scripts'))
from calcular_cabine import calcular as calcular_cabine

from motorhome.cabos_polares import Cabo
from motorhome.cabos_polares import resolver as resolver_cabo
from motorhome.freios_axisimetricos import Pista
from motorhome.freios_axisimetricos import resolver as resolver_freio
from motorhome.reconciliacao import (
    consumo_plano,
    dimensionar_modulos,
    indice_lateral,
    passo_solar,
    simular_missao,
)
from motorhome.solar import simular_dia


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False)+'\n')


def save_csv(path, rows):
    if not rows:
        raise ValueError('Tabela vazia')
    opener = gzip.open if path.suffix == '.gz' else open
    with opener(path, 'wt', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destino', type=Path, default=ROOT/'entregas/etapa_pos_dec061')
    args = parser.parse_args()
    out = args.destino.resolve()
    out.mkdir(parents=True, exist_ok=True)
    master = ROOT/'config/parametros_globais.yaml'
    cfg = yaml.safe_load(master.read_text())
    if cfg['revision'] != '1.0.0-pos-DEC061':
        raise ValueError('Executor do baseline29defc4; revisão atual: scripts/desenvolver_*.py e scripts/verificar_desenvolvimento.py. Reproduzir o baseline no commit29defc4.')
    params = cfg['parameters']
    p = {k: v['value'] for k, v in params.items()}
    decision_path = ROOT/cfg['decision_record']
    if sha(decision_path) != cfg['sources']['dec']['sha256']:
        raise ValueError('Registro original foi alterado')
    for k, v in params.items():
        if v['source'] not in cfg['sources'] or v['version'] != cfg['revision']:
            raise ValueError(f'Proveniência inválida:{k}')
    assert p['architecture'] == 'B' and not p['stored_transfer_allowed']
    assert not p['dc_interface_demonstrated'] and p['dc_min_power_kw'] is None
    assert p['ac_voltage_v'] == 220 and p['ac_frequency_hz'] == 60
    assert p['trip_initial_soc'] == [1, 1] and p['trip_flat']
    # Mean service energy and distinct peak inventory: missing peaks stay unknown.
    energy, sizing = [], []
    for level in ['min', 'base', 'max']:
        ac = sum(x['energy_ac_or_dc_kwh_day'][level] for x in cfg['loads'] if x['side'] == 'AC')
        dc = sum(x['energy_ac_or_dc_kwh_day'][level] for x in cfg['loads'] if x['side'] == 'DC')
        idle = p['inverter_idle_w']*24/1000
        # .90 is a conversion-stage study assumption; idle is separately added.
        total = ac/p['eta_inverter']+dc/p['eta_lv']+idle
        energy.append({'level': level, 'ac_kwh_day': ac, 'dc_load_kwh_day': dc,
                       'battery_kwh_day': total, 'idle_kwh_day': idle})
        for days, reserve in itertools.product([1, 2], [.2, .3]):
            row = dimensionar_modulos(total, days, reserve, p['module_service_kwh'], p['module_service_dod'])
            sizing.append({'level': level, 'hours_requested': days*24, 'service_reserve': reserve,
                           **row, 'module_mass_kg': row['modulos']*p['module_service_mass_kg'],
                           'module_volume_m3': row['modulos']*np.prod(p['module_service_dimensions_m']),
                           'price_brl': None})
    save_csv(out/'servicos_24_48h.csv', sizing)
    save_json(out/'cargas_media_e_picos.json', {'loads': cfg['loads'], 'energy': energy,
              'peaks_verified': False, 'shedding_implemented': False,
              'note': 'Somar energia média não demonstra partidas ou capacidade de operação simultânea. Faltam potência/partidaAC/lava-seca/boiler. Não usar todos ligados.'})
    base_energy = next(x['battery_kwh_day'] for x in energy if x['level'] == 'base')
    # Full factorial sensitivity of six uncertain quantities at40/80.
    tractions = []
    for speed, mass, cd, cr, rho, eta, af in itertools.product(
            p['consumption_speeds_kmh'], p['mass_study_kg'], p['cd_range'],
            p['crr_range'], p['rho_range'], p['eta_traction_range'], p['area_multiplier_range']):
        result = consumo_plano(speed, mass, cd, p['area_m2']*af, cr, rho, eta)
        tractions.append({'speed_kmh': speed, 'mass_kg': mass, 'cd': cd, 'crr': cr,
                          'rho_kg_m3': rho, 'eta': eta, 'area_m2': p['area_m2']*af, **result})
    save_csv(out/'tracao_40_80_sensibilidade.csv', tractions)
    central = [dict(speed_kmh=s, mass_kg=m, **consumo_plano(
        s, m, p['cd_range'][1], p['area_m2'], p['crr_range'][1],
        p['rho_range'][1], p['eta_traction_range'][1]))
        for s, m in itertools.product(p['consumption_speeds_kmh'], p['mass_study_kg'])]
    # Reuse the actual solar library, not a fabricated daily kWh constant.
    solar = yaml.safe_load((ROOT/'config/solar_proposta.yaml').read_text())
    solar['scenario'].update(date=p['reference_day'], latitude_deg=p['latitude_deg'],
        longitude_deg=p['longitude_deg'], altitude_m=p['altitude_m'],
        ambient_temperature_c=p['ambient_c'], wind_speed_m_s=p['wind_m_s'],
        relative_humidity_percent=p['rh_percent'])
    solar['module'].update(p_stc_w=p['roof_power_48v_study_wp'], gamma_pdc_per_k=p['pv_gamma'])
    solar['array'].update(module_counts=[1], tilt_deg=0, azimuth_deg=0, albedo=p['pv_albedo'])
    solar['assumptions'].update(converter_efficiency=1., other_losses_fraction=p['pv_other_loss'],
        faiman_u0_w_m2k=p['pv_faiman_u0'], faiman_u1_w_s_m3k=p['pv_faiman_u1'])
    step = p['time_step_minutes']
    s = simular_dia(solar, step)
    # Trapezoid endpoints produce average powers per interval, maintaining units.
    roof = (s['terminal_assumed_1_modules_w'].to_numpy()[:-1]+s['terminal_assumed_1_modules_w'].to_numpy()[1:])/2000
    times = s.index[:-1]+pd.Timedelta(minutes=step/2)
    h = times.hour+times.minute/60
    # For each planned parking window: discrete angle search, then HOLD angle.
    profiles, angles = {}, []
    for name, drive_start in [('fixo_08_16', 8), ('alternativo_00_08', 0)]:
        drive = (h >= drive_start) & (h < drive_start+8)
        # Stop crosses midnight08–16policy: start16, next end08.
        park_start = (drive_start+8) % 24
        since_start = (h-park_start) % 24
        usable = (~drive) & (since_start >= p['pv_setup_h']) & (since_start < 16-p['pv_teardown_h'])
        best = None
        for tilt, azimuth in itertools.product(range(0, 76, 15), [0, 90, 180, 270]):
            candidate = copy.deepcopy(solar)
            candidate['array'].update(tilt_deg=tilt, azimuth_deg=azimuth)
            candidate['module']['p_stc_w'] = p['portable_wp']
            candidate['module']['gamma_pdc_per_k'] = p['portable_gamma']
            power = simular_dia(candidate, step)['terminal_assumed_1_modules_w'].to_numpy()
            port = (power[:-1]+power[1:])/2000*usable
            energy_kwh = float(port.sum()*step/60)
            if best is None or energy_kwh > best[0]:
                best = (energy_kwh, tilt, azimuth, port)
        profiles[name] = (roof, best[3], drive)
        angles.append({'policy': name, 'tilt_deg': best[1], 'azimuth_deg': best[2],
                       'roof_dc_after_losses_kwh_day': float(roof.sum()*step/60),
                       'portable_dc_after_losses_kwh_day': best[0],
                       'setup_h_per_stop': p['pv_setup_h'], 'teardown_h_per_stop': p['pv_teardown_h'],
                       'hold_angles_during_stop': True})
        save_csv(out/f'solar_{name}.csv', [{'time':t.isoformat(), 'roof_kw':float(a),
                 'portable_kw':float(b), 'planned_driving':bool(d)}
                 for t, a, b, d in zip(times, roof, best[3], drive, strict=True)])
    # DCdirect vs buffer: minimum power is ONLY a study parameter, never OEM.
    dc_comparison = []
    for policy, (rf, pt, drive) in profiles.items():
        for minimum, capacity in itertools.product(p['dc_min_sweep_kw'], p['buffer_study_kwh']):
            buf = 0.
            sums = dict.fromkeys(['pv_kwh', 'service_kwh', 'traction_kwh', 'loss_kwh', 'cut_kwh'], 0.)
            for a, b, moving in zip(rf, pt, drive, strict=True):
                generated = float(a+b)*step/60
                result = passo_solar(generated, base_energy/len(rf)/p['eta_service_charge'], not moving,
                    p['eta_dc'], minimum, step/60, hipotetico=True, buffer_kwh=buf,
                    buffer_capacidade_kwh=capacity, eficiencia_buffer=p['eta_buffer'])
                buf = result['buffer_final_kwh']
                sums['pv_kwh'] += generated
                sums['service_kwh'] += result['servicos_kwh']
                sums['traction_kwh'] += result['tracao_kwh']
                sums['loss_kwh'] += result['perdas_kwh']
                sums['cut_kwh'] += result['cortada_kwh']
            residual = sums['pv_kwh']-sums['service_kwh']-sums['traction_kwh']-sums['loss_kwh']-sums['cut_kwh']-buf
            dc_comparison.append({'policy': policy, 'hypothetical_min_dc_kw': minimum,
                'buffer_capacity_kwh': capacity, 'buffer_initial_kwh': 0., 'buffer_final_kwh': buf,
                **sums, 'residual_kwh': residual, 'physical_status': 'nao_demonstrado'})
    save_csv(out/'dc_direta_vs_buffer_hipoteses.csv', dc_comparison)
    # Reconciled flat7000km replay: controls + selected conditional cases.
    missions, full_examples = [], []
    for policy, (rf, pt, drive) in profiles.items():
        for speed, reserves, mode, allocation in itertools.product(p['consumption_speeds_kmh'],
                p['trip_reserve_pairs'], ['sem_interface', 'direta_hipotese', 'buffer_hipotese'],
                ['A', 'B', 'flexivel']):
            if mode == 'sem_interface' and allocation != 'flexivel':
                continue
            rate = next(x['kwh_km'] for x in central if x['speed_kmh'] == speed and x['mass_kg'] == p['oem_pbt_kg'])
            result = simular_missao(rf, pt, drive, speed_kmh=speed, kwh_km=rate,
                service_kwh_day=base_energy, traction_capacity_kwh=p['traction_usable_kwh'],
                service_capacity_kwh=p['service_modules_provisional']*p['module_service_kwh'],
                reserve_traction=reserves[0], reserve_service=reserves[1], target_km=p['trip_km'],
                mode=mode, allocation=allocation,
                min_dc_kw=None if mode=='sem_interface' else p['mission_hypothetical_min_kw'],
                eta_dc=p['eta_dc'], eta_service=p['eta_service_charge'], eta_buffer=p['eta_buffer'],
                buffer_capacity_kwh=p['mission_hypothetical_buffer_kwh'] if mode=='buffer_hipotese' else 0.)
            case=f'{policy}_{speed}kmh_{reserves[0]}_{reserves[1]}_{mode}_{allocation}'
            trace = result.pop('trace'); daily=result.pop('daily')
            result.update(case=case, policy=policy, speed_kmh=speed, mass_study_kg=p['oem_pbt_kg'],
                          reserve_traction=reserves[0], reserve_service=reserves[1],
                          minimum_power_source='hipotese1kW, NÃO dadoOEM',
                          max_driving_h_day=max(x['driving_h'] for x in daily))
            missions.append(result)
            # Preserve all daily states and compressed full series; no hand-drawn curves.
            save_csv(out/f'missao_{case}.csv.gz', trace)
            save_csv(out/f'diario_{case}.csv', daily)
            full_examples.append(case)
    save_json(out/'missoes_7000km.json', missions)
    # I25 no physically demonstrated solar injection; no claim of solar range.
    save_json(out/'itens25_26_27.json', {
        'i25': {'status':'nao_demonstrado', 'solar_traction_demonstrated_kwh':0,
                'note':'Zero é crédito permitido no modelo sem interface; não prova física de impossibilidade universal.'},
        'i26':central,
        'i27_no_solar_conditional_storage_only':[
            {'speed_kmh':x['speed_kmh'], 'mass_study_kg':x['mass_kg'], 'initial_soc':soc,
             'final_soc':p['item27_final_soc'], 'available_traction_kwh':(soc-p['item27_final_soc'])*p['traction_usable_kwh'],
             'distance_km':(soc-p['item27_final_soc'])*p['traction_usable_kwh']/x['kwh_km'],
             'optimization_demonstrated':False}
            for x in central for soc in p['item27_initial_soc']]})
    # Actual2D steady cable fields for48V services; no modification of OEMHV.
    cable_rows=[]
    for section, nr, nt in itertools.product([70,95], [12,24,48], [64]):
        nt=nt*(nr//12)
        rad=np.sqrt(section*1e-6/np.pi)
        cable=Cabo(rad,rad+p['cable_insulation_m'],p['cable_k_copper'],
                   p['cable_k_insulation'],p['cable_rho20']/(section*1e-6),p['cable_alpha'])
        current=p['inverter_continuous_w'][0]/(p['cable_min_voltage_v']*p['cable_eta'])
        theta=(np.arange(nt)+.5)*2*np.pi/nt
        result=resolver_cabo(cable,current,nr,nt,10*(1+.5*np.cos(theta)),p['ambient_c']+273.15)
        cable_rows.append({'section_mm2':section,'nr_each_material':nr,'ntheta':nt,
            'current_a':current,'tmax_c':result['temperatura_max_k']-273.15,
            'joule_w_m':result['joule_w_m'],'residual_w_m':result['residuo_w_m'],
            'loop_voltage_drop_v':result['joule_w_m']*p['cable_loop_m']/current,
            'commercial_ampacity_verified':False})
        if nr==48:
            np.savez_compressed(out/f'campo_cabo_servicos_{section}mm2.npz',
                                temperatura_k=result['temperatura_k'],r_m=result['r_m'],theta_rad=result['theta_rad'])
    save_csv(out/'cabos_servicos_convergencia.csv', cable_rows)
    # Brake model reused: friction profile after aero/rolling + regeneration power cap.
    brake_cfg=yaml.safe_load((ROOT/'config/freios_proposta.yaml').read_text())
    b=brake_cfg['assumed'];mat=brake_cfg['material_reference']
    track=Pista(b['inner_ring_radius_m'],brake_cfg['reference_component']['diameter_m']/2,
        b['plate_thickness_m'],b['pad_track_inner_radius_m'],b['pad_track_outer_radius_m'],
        mat['density_kg_m3'],mat['cp_j_kgk'],mat['conductivity_w_mk'])
    brake_rows=[]
    for mass, regen in itertools.product(p['mass_study_kg'],p['regen_power_study_kw']):
        def components(t, mass=mass, regen=regen):
            v=30-4*t
            demand=mass*4*v
            aero=.5*p['rho_range'][1]*p['cd_range'][1]*p['area_m2']*v**3
            rolling=p['crr_range'][1]*mass*9.80665*v
            recovered=min(regen*1000,max(0,demand-aero-rolling))
            return demand,aero,rolling,recovered,max(0,demand-aero-rolling-recovered)
        for nr,nz,dt in [(24,8,.02),(48,16,.02),(96,32,.02),(96,32,.01)]:
            result=resolver_freio(track,massa_kg=mass,fracao_eixo=b['front_axle_energy_fraction'],
                fracao_disco=b['disc_heat_fraction'],nr=nr,nz=nz,dt_s=dt,
                potencia_total_friccao_w=lambda t: components(t)[4])
            points=(np.arange(round(5/dt))+.5)*dt
            es=np.sum(np.array([components(t) for t in points]),axis=0)*dt
            brake_rows.append({'mass_kg':mass,'regen_cap_hypothetical_kw':regen,'nr':nr,'nz':nz,
                'dt_s':dt,'kinetic_j':400*mass,'aero_j':float(es[1]),'rolling_j':float(es[2]),
                'regen_mechanical_j':float(es[3]),'friction_total_j':float(es[4]),
                'mechanical_residual_j':float(es[0]-sum(es[1:])),
                'front_disc_heat_j':result['energia_entrada_disco_j'],
                'thermal_residual_j':result['residuo_disco_j'],
                'peak_surface_c':result['pico_superficie_k']-273.15})
            if nr==96 and dt==.01:
                np.savez_compressed(out/f'campo_freio_{mass}kg_regen{regen}kw.npz',
                     temperatura_k=result['temperatura_k'],r_m=result['r_m'],z_m=result['z_m'])
    save_csv(out/'freios_2d_atrito_regeneracao.csv',brake_rows)
    # Existing thermal network kept as a network, NEVER relabelled as3DCFD.
    cabin_cfg=yaml.safe_load((ROOT/'config/cabine_proposta.yaml').read_text())
    cabin_cfg['insulation']['thickness_m']=p['insulation_provisional_m']
    cabin_data,cabin_summary=calcular_cabine(cabin_cfg,solar,passo_min=5)
    cabin_data.dropna(subset=['i31_temperature_c']).to_csv(out/'cabine_rede_transiente.csv',index_label='time')
    cabin_summary.update(cfd_3d_executed=False,model='rede_termica_equivalente',
                         physical_envelope_validated=False, ventilation_30m3h_is_assumed=True)
    save_json(out/'cabine_31_32_reexecutada.json',cabin_summary)
    #12/24V: same load/loop/section; converter efficiencies remain unknown.
    lv=[]
    for v in [12,24]:
        current=p['lv_power_study_w']/v
        resistance=p['cable_rho20']*p['lv_cable_loop_study_m']/(p['lv_cable_section_study_mm2']*1e-6)
        lv.append({'bus_v':v,'load_w':p['lv_power_study_w'],'current_a':current,
                   'loop_m':p['lv_cable_loop_study_m'],'section_mm2':p['lv_cable_section_study_mm2'],
                   'drop_v':current*resistance,'joule_w':current**2*resistance,
                   'converter_efficiency':None,'status':'comparacao_nao_homologacao'})
    save_csv(out/'comparacao_12_24v.csv',lv)
    lateral=[{'h_cg_hypothetical_m':height,'y_cg_hypothetical_m':offset,
              'track_m':p['rear_track_m'],'geometric_index_g':indice_lateral(p['rear_track_m'],height,offset),
              'actual_cg_known':False} for height,offset in itertools.product(
                  p['lateral_cg_height_sweep_m'],p['lateral_cg_offset_sweep_m'])]
    save_csv(out/'estabilidade_quase_estatica_sensibilidade.csv',lateral)
    save_json(out/'agua_e_massa.json',{
        'occupants_baggage_initial_water_kg':sum(p['occupants_kg'])+p['baggage_kg']+p['water_clean_l'],
        'nominal_clean_days_without_laundry':p['water_clean_l']/p['water_daily_study_l'],
        'laundry_cycle_l':68.8,'nominal_clean_days_including_one_laundry':(p['water_clean_l']-68.8)/p['water_daily_study_l'],
        'extra_black_tank':False,'assembled_mass_kg':None,'axle_loads_verified':False,
        'note':'100L incluem água do boiler e descarga. Ciclo68.8L usa98% do tanque cinza70L antes de banho/cozinha; exige esvaziamento adequado. Níveis exatos de transferência e fixações continuam pendentes.'})
    # Potable water is a NEW circuit, distinct from legacy glycol cooling.
    curve=np.asarray(p['potable_pump_curve'],dtype=float)
    q_values=curve[::-1,1]
    pressure_values=curve[::-1,0]*6894.757293
    amp_values=curve[::-1,2]
    potable=[]
    for diameter in p['potable_pipe_diameters_m']:
        def circuit(q_lpm, diameter=diameter):
            q=q_lpm/60000
            velocity=q/(np.pi*diameter**2/4)
            reynolds=p['potable_density_kg_m3']*velocity*diameter/p['potable_viscosity_pa_s']
            # Smooth-pipe Blasius in turbulent range; no claim of material-specific roughness.
            friction=64/reynolds if reynolds < 2300 else .3164/reynolds**.25
            pipe=(friction*p['potable_pipe_lengths_m']/diameter+p['potable_minor_k'])*p['potable_density_kg_m3']*velocity**2/2
            static=p['potable_density_kg_m3']*9.80665*p['potable_height_m']
            fixture=p['potable_fixture_pressure_pa']*(q_lpm/p['potable_fixture_design_lpm'])**2
            return pipe+static+fixture,pipe,static,fixture,reynolds
        root=brentq(lambda q:np.interp(q,q_values,pressure_values)-circuit(q)[0],q_values[0],q_values[-1])
        pressure,pipe,static,fixture,reynolds=circuit(root)
        amps=float(np.interp(root,q_values,amp_values))
        potable.append({'diameter_m':diameter,'flow_lpm':root,'total_pressure_pa':pressure,
            'pipe_minor_loss_pa':pipe,'static_pa':static,'fixture_pa':fixture,'reynolds':reynolds,
            'pump_current_a_12v':amps,'pump_power_w':12*amps,
            'pressure_residual_pa':float(np.interp(root,q_values,pressure_values)-pressure),
            'above_design_flow':root>=p['potable_fixture_design_lpm'],
            'commercial_pipe_pressure_rating_verified':False})
    save_csv(out/'hidraulica_potavel_trecho_critico.csv',potable)
    # Traceable audit, including all original61 sections, all35owner folders.
    mapping=yaml.safe_load((ROOT/'metadata/conciliacao_dec061.yaml').read_text())['rows']
    original=decision_path.read_text()
    matches=list(re.finditer(r'^## DEC-(\d{3})[^\n]*',original,re.MULTILINE))
    if [int(x[1]) for x in matches] != list(range(1,62)):
        raise ValueError('O registro deve conter exatamente DEC001–061')
    item_source=json.loads((ROOT/'entregas/etapa_2026-10-28_rota_real/revisao_35_itens.json').read_text())['items']
    with (ROOT/'metadata/itens.csv').open() as f:
        roster={int(x['numero']):x for x in csv.DictReader(f)}
    decisions=[]
    for i,m in enumerate(matches):
        segment=original[m.start():matches[i+1].start() if i+1<len(matches) else len(original)]
        row=next(x for x in mapping if x['decision']==f'DEC-{i+1:03}')
        keys=[k for k,v in params.items() if row['decision'] in v['decisions']]
        assert keys and (ROOT/row['evidence']).is_file()
        decisions.append({**row,'title':m[0].split(' — ',1)[1], 'section_sha256':hashlib.sha256(segment.encode()).hexdigest(),
                          'parameter_keys':keys,'owners':sorted({roster[n]['pessoa'] for n in row['items']}),
                          'status':'em_integracao_sem_aprovacao_final'})
    items=[]
    for old in item_source:
        n=old['item'];folder=ROOT/roster[n]['pasta']
        notes=[x for x in decisions if n in x['items']]
        paths=[f.relative_to(ROOT).as_posix() for f in folder.rglob('*') if f.is_file() and '__pycache__' not in f.parts]
        items.append({**old,'status':'parcial_requer_validacao_humana','historical_evidence':old['evidence'],
            'folder':roster[n]['pasta'],'existing_item_files':paths,'decisions':[x['decision'] for x in notes],
            'pending_after_dec061':list(dict.fromkeys(x['pending'] for x in notes if x['decision'] not in ['DEC-035','DEC-061'])),
            'human_approval_recorded':False})
    save_json(out/'matriz_decisoes_61.json',decisions)
    save_json(out/'matriz_itens_35.json',{'reviewed':35,'final_human_approved':0,'items':items})
    header='# Matriz DEC-001–DEC-061 → parâmetros → itens → responsáveis\n\nGerada por `scripts/conciliar_dec061.py`; parâmetros em `config/parametros_globais.yaml`. Estado de engenharia: parcial; decisões de método aprovadas não aprovam resultados.\n\n'
    table='|Decisão|Chaves da fonte única|Itens|Líder / interfaces|Evidência existente|Pendência|\n|---|---|---|---|---|---|\n'
    for x in decisions:
        table+=f"|{x['decision']} — {x['title']}|{', '.join(x['parameter_keys'])}|{', '.join(map(str,x['items']))}|{x['lead']} / {', '.join(x['owners'])}|`{x['evidence']}`|{x['pending']}|\n"
    (ROOT/'docs/MATRIZ_DECISOES_61.md').write_text(header+table)
    table='# Revisão dos35itens — baseline pósDEC061\n\n35 trabalhos iniciados; **0 aprovações humanas finais**. CAD/CFD e resultados anteriores são evidência histórica, não configuração reconciliada automaticamente. Os arquivos por item foram inventariados no JSON desta etapa.\n\n|Item / dono|Requisito|Evidência anterior, sujeita à conciliação|Pendências após decisões|\n|---|---|---|---|\n'
    for x in items:
        # Each row shows specific issues plus linked full decision map for completeness.
        own=[d for d in decisions if d['lead']==x['owner'] and x['item'] in d['items'] and d['decision'] not in ['DEC-035','DEC-061']]
        gaps='; '.join(f"{d['decision']}: {d['pending']}" for d in own) or x['missing']
        table+=f"|{x['item']:02} / {x['owner']}|{x['requirement']}|{x['historical_evidence']}|{gaps}|\n"
    (ROOT/'docs/REVISAO_35_ITENS.md').write_text(table)
    # A run manifest captures exact code + input versions; historical outputs unchanged.
    inputs=['config/parametros_globais.yaml','metadata/conciliacao_dec061.yaml','metadata/itens.csv',
            cfg['decision_record'],'config/solar_proposta.yaml','config/cabine_proposta.yaml',
            'config/freios_proposta.yaml','scripts/calcular_cabine.py','scripts/conciliar_dec061.py',
            'src/motorhome/reconciliacao.py','src/motorhome/freios_axisimetricos.py',
            'src/motorhome/cabos_polares.py','src/motorhome/cabine.py','src/motorhome/solar.py',
            'entregas/etapa_2026-10-28_rota_real/revisao_35_itens.json']
    manifest={'generated_utc':datetime.now(timezone.utc).isoformat(),'revision':cfg['revision'],
              'command':'PYTHONPATH=src .venv/bin/python scripts/conciliar_dec061.py',
              'software':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
                          'pandas':pd.__version__,'pvlib':pvlib.__version__},
              'inputs_sha256':{name:sha(ROOT/name) for name in inputs},
              'outputs_sha256':{f.name:sha(f) for f in sorted(out.iterdir()) if f.is_file()
                  and f.name not in ['manifesto.json', 'manifesto_pacote.json',
                                     'bom_rastreavel.csv', 'bom_massas_custos_resumo.json']},
              'owner_counts':dict(sorted(Counter(x['owner'] for x in items).items())),
              'technical_conclusion':'INTERFACE_DC_NAO_DEMONSTRADA_MISSAO_CONDICIONAL',
              'human_final_approvals':0,'historical_outputs_rewritten':False}
    save_json(out/'manifesto.json',manifest)
    print(json.dumps({'revision':cfg['revision'],'parameters':len(params),'decisions':len(decisions),'items':len(items),
          'traction_sensitivity_cases':len(tractions),'mission_cases':len(missions),'dc_cases':len(dc_comparison),
          'service_base_kwh_day':base_energy,'mission_states':dict(Counter(x['status'] for x in missions)),
          'maximum_mission_energy_residual_kwh':max(abs(x['energy_residual_kwh']) for x in missions),
          'output':str(out)},ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
