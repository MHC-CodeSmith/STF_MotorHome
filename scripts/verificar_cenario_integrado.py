"""Verificações independentes do cenário1540,com resultados condicionais separados."""
import argparse
import ast
import hashlib
import json
import math
import sys
from pathlib import Path

import gmsh
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from motorhome.cenarios import carregar_configuracao, diretorio_entregas


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--registrar',action='store_true');args=parser.parse_args()
    c=carregar_configuracao(ROOT)
    if '_execution' not in c:raise ValueError('Selecionar cenário')
    p={k:v['value'] for k,v in c['parameters'].items()};out=diretorio_entregas(ROOT);checks=[];errors=[]
    def check(ok,label):
        checks.append({'label':label,'pass':bool(ok)})
        if not ok:errors.append(label)
    mass=pd.read_csv(out/'integracao/inventario_massas.csv');summary=json.loads((out/'integracao/layouts_massas.json').read_text())
    for layout,parts in mass.groupby('layout'):
        total=float(parts.mass_kg.sum());cg=sum(x.mass_kg*np.array(ast.literal_eval(x.cg_m)) for x in parts.itertuples())/total
        nominal=summary['layouts'][layout]['nominal']
        check(abs(total-nominal['mass_kg'])<1e-7 and np.max(abs(cg-[nominal['cg_x_m'],nominal['cg_y_m'],nominal['cg_z_m']]))<1e-9,f'{layout}:massa/momentos independentes')
        water=parts[parts.id.astype(str).str.startswith('agua')]
        check(abs(water.mass_kg.sum()-100)<1e-8 and water[water.id=='agua_boiler'].mass_kg.iloc[0]==15 and water[water.id=='agua0'].mass_kg.iloc[0]==85,f'{layout}:100L totais localizados85+15sem duplicar')
        check(parts[parts.id.str.startswith('MAXEON')].mass_kg.sum()==76 and not parts.id.isin(['PV190','PV_JA3']).any(),f'{layout}:inventário4Maxeon sem painéis antigos')
    nominal=summary['layouts']['A_fixa']['nominal'];check(abs(nominal['mass_kg']-p['assembled_typical_mass_kg'])<1e-8,'Massafonteúnica=CAD')
    check(p['roof_power_48v_study_wp']==1540 and p['pv_gamma']==-.0027,'PV1540/coeftérmico próprio')
    check(p['architecture']=='B' and not p['stored_transfer_allowed'] and not p['dc_interface_demonstrated'],'B/independência sem provaDC')
    check(p['ac_voltage_v']==220 and p['ac_frequency_hz']==60,'220V60Hz')
    for path in (out/'solar').glob('solar_*.csv'):
        solar=pd.read_csv(path);check((solar.loc[solar.planned_driving,'portable_kw']==0).all(),f'{path.name}:portátil somente parado')
    missions=json.loads((out/'energia_sistemas/I29_missoes_massas_integradas.json').read_text())
    for r in missions:
        speed=r['speed_kmh'];v=speed/3.6
        expected=((.5*p['rho_range'][1]*p['cd_range'][1]*p['area_m2']*v*v+p['crr_range'][1]*r['mass_kg']*9.80665)*v/1000/p['eta_traction_range'][1]+p['traction_aux_assumed_w']/1000)/speed
        check(abs(expected-r['kwh_km'])<1e-10 and abs(expected*r['distance_km']-r['totals']['traction_used_kwh'])<1e-6,f'{r["id"]}:consumo físico independente')
        if r['mode']=='sem_interface':check(r['totals']['traction_solar_kwh']==0 and r['status']!='chegada_condicional',f'{r["id"]}:controle sem interface não ganha energiaHV')
        check(abs(r['energy_residual_kwh'])<1e-6 and not r['physical_mission_demonstrated'] and r['external_electric_energy_kwh']==0,f'{r["id"]}:energia/semrecargaexterna')
    daily=pd.read_csv(out/'energia_sistemas/I27_autonomia_otima_modelo_sem_HV.csv');check((daily.soc_final==.3).all() and daily.energy_residual_kwh.abs().max()<1e-8,'I27 condição final30%')
    dispatch=json.loads((out/'despacho_i25/resumo.json').read_text());check(dispatch['cases_milp']==630 and not dispatch['interface_demonstrated'],'I25 MILP630condicional')
    for path in (out/'despacho_i25').glob('perfil_*.csv'):
        f=pd.read_csv(path);dt=float(f.start_h.iloc[1]-f.start_h.iloc[0]);on=f.fv_traction_kwh>1e-7
        check((f.loc[on,'driving_h']==0).all() and np.max(abs(f.pv_kw*dt-f.fv_traction_kwh-f.fv_services_kwh-f.fv_curtailed_kwh))<1e-6 and f.fv_curtailed_kwh.min()>-1e-6,f'{path.name}:sem recarga emmovimento/sem dupla contagem')
        check(f.solar_credit_start_kwh.iloc[0]==0 and f.solar_credit_end_kwh.min()>-1e-6 and abs(f.service_end_kwh.iloc[-1]-f.service_start_kwh.iloc[0])<1e-6,f'{path.name}:solar inicial0/serviços cíclicos')
    grid=json.loads((out/'otimizacao_grade/resumo.json').read_text());check(grid['cases']==1008 and abs(grid['mass_kg']-p['assembled_typical_mass_kg'])<1e-8 and not grid['global_optimality_proven'],'Grade1008 massa correta,sem ótimo global')
    extra=json.loads((out/'otimizacao_janela_missao_refino_extra/resumo.json').read_text())
    extra_best=sorted(extra['best_by_reserve_and_auxiliary'],key=lambda row:row['reserve_traction'])
    check(extra['rows_total']==292 and extra['coarse_cases']==0 and extra['refined_cases']==286 and len(extra['auxiliary_sensitivities_at_selected_policy'])==6 and extra['time_step_h']==0.25,'I29 refinamento extra:286 pontos locais+6sensibilidades auxiliares,sem alterar passo temporal')
    check([round(row['elapsed_days'],6) for row in extra_best]==[242.802083,244.802083] and max(abs(row['energy_residual_kwh']) for row in extra_best)<1e-8,'I29 refinamento extra preserva duração e conserva energia;sem ótimo global')
    check(extra['hypothetical_dc_interface'] and not extra['physical_mission_demonstrated'] and not extra['global_optimum_claimed'],'I29 refinamento permanece condicionado e hipotético')
    temporal=json.loads((out/'otimizacao_resolucao_temporal/resumo.json').read_text())
    temporal_cases=json.loads((out/'otimizacao_resolucao_temporal/candidatos.json').read_text())
    counts={step:sum(row['time_step_min']==step for row in temporal_cases) for step in (15,5,1)}
    check(temporal['candidate_count']==294 and counts=={15:98,5:98,1:98},
          'I29 resolução temporal: 98 políticas locais em cada passo de15/5/1min')
    check(temporal['max_abs_energy_residual_kwh']<1e-8 and
          max(abs(row['energy_residual_kwh']) for row in temporal_cases)<1e-8 and
          all(row['mode']=='direta_hipotese' and not row['physical_mission_demonstrated']
              for row in temporal_cases),
          'I29 resolução temporal: balanço fechado e interface física não inferida')
    temporal_leaders=temporal['best_local_by_resolution_and_reserve']
    check(len(temporal_leaders)==6 and
          [round(row['elapsed_days'],6) for row in temporal_leaders]==
          [242.802083,244.802083,248.763889,250.760417,248.784028,250.779861] and
          temporal['hypothetical_dc_interface'] and not temporal['physical_mission_demonstrated'] and
          not temporal['global_optimum_claimed'],
          'I29 comparação15/5/1min reproduz sensibilidade temporal local sem ótimo global')
    road=json.loads((out/'dinamica_resistiva_sensibilidade/resumo.json').read_text())
    road_frame=pd.read_csv(out/'dinamica_resistiva_sensibilidade/envelope_grade_vento.csv')
    check(road['cases']==8100 and len(road_frame)==8100 and not road['oem_motor_map_used'] and
          not road['road_grade_or_wind_is_approved_mission_input'] and not road['physical_validation'],
          'I21/I22 envelope grade/vento:8100 sensibilidades sem mapa OEM ou missão aprovada')
    flat_reference=road_frame[(road_frame.mass_kg==p['assembled_typical_mass_kg']) &
        (road_frame.speed_kmh==40) & (road_frame.grade_percent==0) &
        (road_frame.headwind_m_s==0) & (road_frame.crr_assumed==p['crr_range'][1]) &
        (road_frame.cd_assumed==p['cd_range'][1]) &
        (road_frame.air_density_kg_m3==p['rho_range'][1])].iloc[0]
    speed=40/3.6
    force=(p['crr_range'][1]*p['assembled_typical_mass_kg']*9.80665+
           .5*p['rho_range'][1]*p['cd_range'][1]*p['area_m2']*speed**2)
    wheel_kw=force*speed/1000
    expected_kwh_km=(wheel_kw/p['eta_traction_range'][1]+
                     p['traction_aux_assumed_w']/1000)/40
    check(abs(flat_reference.total_road_load_n-force)<1e-8 and
          abs(flat_reference.wheel_power_signed_kw-wheel_kw)<1e-8 and
          abs(flat_reference.estimated_battery_kwh_per_km_no_regen_credit-expected_kwh_km)<1e-10,
          'I21/I22 ponto plano reproduzido independentemente')
    grade_reference=road_frame[(road_frame.mass_kg==p['assembled_typical_mass_kg']) &
        (road_frame.speed_kmh==40) & (road_frame.grade_percent==6) &
        (road_frame.headwind_m_s==5) & (road_frame.crr_assumed==p['crr_range'][1]) &
        (road_frame.cd_assumed==p['cd_range'][1]) &
        (road_frame.air_density_kg_m3==p['rho_range'][1])].iloc[0]
    angle=math.atan(.06)
    relative_speed=40/3.6+5
    grade_force=(p['crr_range'][1]*p['assembled_typical_mass_kg']*9.80665*math.cos(angle)+
        p['assembled_typical_mass_kg']*9.80665*math.sin(angle)+
        .5*p['rho_range'][1]*p['cd_range'][1]*p['area_m2']*relative_speed**2)
    check(abs(grade_reference.total_road_load_n-grade_force)<1e-8 and
          abs(grade_reference.wheel_power_signed_kw-grade_force*40/3.6/1000)<1e-8,
          'I21/I22 aclive/vento reproduzido com rolagem projetada e vento relativo')
    ventilation=json.loads((out/'ventilacao_mecanica_sensibilidade/resumo.json').read_text())
    vent_frame=pd.read_csv(out/'ventilacao_mecanica_sensibilidade/envelope_ventilacao.csv')
    check(ventilation['cases']==648 and len(vent_frame)==648 and
          ventilation['natural_ventilation_remains_priority'] and
          not ventilation['mechanical_fallback_selected_or_installed'] and
          not ventilation['regulatory_minimum_claimed'] and not ventilation['physical_validation'],
          'I11 fallback mecânico:648 sensibilidades sem seleção ou conformidade normativa')
    vent_nominal=vent_frame[(vent_frame.occupants==2) &
        (vent_frame.co2_target_study_ppm==1000) &
        (vent_frame.co2_generation_l_h_person_assumed==18) &
        (vent_frame.pressure_drop_assumed_pa==50) &
        (vent_frame.fan_total_efficiency_assumed==.2) &
        (vent_frame.indoor_outdoor_delta_k_assumed==8) &
        (vent_frame.operation_h_day_assumed==24)].iloc[0]
    required_flow=2*18/1000/((1000-420)*1e-6)
    expected_fan_power=required_flow/3600*50/.2
    expected_ventilation_load=1.2*(required_flow/3600)*1005*8
    check(abs(vent_nominal.required_outdoor_air_m3_h_for_co2_balance-required_flow)<1e-10 and
          abs(vent_nominal.baseline_flow_30_m3_h_equilibrium_co2_ppm-1620)<1e-10 and
          abs(vent_nominal.fan_electrical_power_estimate_w-expected_fan_power)<1e-10 and
          abs(vent_nominal.ventilation_sensible_load_estimate_w-expected_ventilation_load)<1e-10 and
          (vent_frame.fan_energy_estimate_kwh_day>=0).all(),
          'I11 balanço estacionário de CO2, potência estimada e carga sensível reproduzidos')
    priority_vent=pd.read_csv(out/'ventilacao_mecanica_sensibilidade/integracao_autonomia_servicos.csv')
    pvent=ventilation['service_priority_integration']
    reference_priority=priority_vent[(priority_vent.occupants==2) &
        (priority_vent.fan_operation_h_day_assumed==24) &
        (priority_vent.horizon_h==48) &
        (priority_vent.service_reserve_fraction_sensitivity==.3)].iloc[0]
    check(len(priority_vent)==16 and pvent['cases']==16 and
          pvent['maximum_energy_balance_residual_kwh']<1e-8 and
          pvent['hardware_actuators_implemented'] is False and
          reference_priority.with_fan_horizon_completed and
          abs(reference_priority.with_fan_final_service_soc-
              pvent['two_occupants_48h_reserve30_fan24h_final_soc'])<1e-12 and
          (priority_vent.with_fan_energy_residual_kwh.abs()<1e-8).all(),
          'I11 ventilação essencial integrada às prioridades de energia:16 casos e balanço fechado')
    hvac_vent=ventilation['hvac_ventilation_coupling']
    two_people_hvac=hvac_vent['design_flow_occupant_cases'][1]
    check(hvac_vent['capacity_at_33c_25c_demonstrated'] is False and
          abs(two_people_hvac['co2_balance_flow_m3_h']-required_flow)<1e-10 and
          abs(two_people_hvac['updated_hvac_demand_w']-
              (two_people_hvac['baseline_hvac_demand_w_at_30m3h']+
               two_people_hvac['ventilation_sensible_increment_w']+
               two_people_hvac['ventilation_latent_increment_w']))<1e-8 and
          abs(two_people_hvac['margin_w_at_2700w_capacity_claim']-
              (2700-two_people_hvac['updated_hvac_demand_w']))<1e-8 and
          abs(two_people_hvac['margin_w_at_1758w_capacity_claim']-
              (1758-two_people_hvac['updated_hvac_demand_w']))<1e-8,
          'I11/I32 margem HVAC recalculada com carga psicrométrica incremental sem alegar capacidade real')
    check(abs(two_people_hvac['updated_hvac_demand_w']-2867.3401980189237)<1e-6 and
          two_people_hvac['margin_w_at_2700w_capacity_claim']<0 and
          hvac_vent['design_flow_occupant_cases'][0]['margin_w_at_2700w_capacity_claim']>0,
          'I32 ventilação altera a margem do caso de dois ocupantes; conflito de capacidade permanece explícito')
    negative=road_frame[road_frame.wheel_power_signed_kw<0]
    check(len(negative)>0 and (negative.positive_wheel_demand_kw==0).all() and
          (negative.mechanical_braking_demand_kw_no_regen_credit>0).all(),
          'I21/I22 descida contabilizada como demanda mecânica de frenagem,sem crédito regenerativo')
    for path in (out/'otimizacao_grade').glob('melhor_*.csv.gz'):
        f=pd.read_csv(path);check(f.driving_h_interval.groupby(f.day).sum().max()<=8+1e-9 and f.soc_service.between(0,1+1e-9).all() and f.soc_traction.between(0,1+1e-9).all(),f'{path.name}:8h/SOCs físicos')
        check((f.loc[f.driving_h_interval>0,'traction_solar_kwh_interval']==0).all(),f'{path.name}:DCsóparado')
    water=pd.read_csv(out/'otimizacao_grade/sanitaria_cronologia.csv');check(water.balance_residual_l.abs().max()<1e-7 and water.clean_l.between(0,100).all() and water.grey_l.between(0,70).all() and water.black_l.between(0,20).all(),'Água cronológica conserva massa/capacidades')
    for scenario,events in water.groupby('scenario'):
        profile=pd.read_csv(out/f'otimizacao_grade/melhor_reservas{scenario}.csv.gz');ok=True
        best=grid['best_by_reserve'][scenario]
        for day,group in events.groupby('day'):
            ordered=group.sort_values('start_h');ok &= bool((ordered.start_h.to_numpy()[1:]>=ordered.end_h.to_numpy()[:-1]-1e-9).all())
            part=profile[profile.day==day]
            for event in group.itertuples():
                overlap=part[(part.hour_end>event.start_h+1e-9)&(part.hour_end-.25<event.end_h-1e-9)]
                mid=overlap.hour_end.to_numpy()-.125;since=(mid-(best['start_h']+best['window_h']))%24
                ok &= len(overlap)>0 and bool((overlap.driving_h_interval==0).all())
                ok &= bool(((since>=p['pv_setup_h']-1e-9)&(since<24-best['window_h']-p['pv_teardown_h']+1e-9)).all())
        check(ok,f'{scenario}:água sem sobreposição,parada e fora montagemFV porreplay')
    brakes=pd.read_csv(out/'freios_integrados/convergencia.csv');check(brakes.thermal_residual_j.abs().max()<1e-5 and brakes.mechanical_residual_j.abs().max()<1e-5,'Freios conserva calor/mecânica')
    axle_braking=pd.read_csv(out/'integracao/envelope_frenagem_eixos/casos.csv')
    axle_summary=json.loads((out/'integracao/envelope_frenagem_eixos/resumo.json').read_text())
    check(len(axle_braking)==972 and axle_summary['source_cases']==162 and
          axle_braking.axle_sum_error_kg.abs().max()<1e-9 and
          not axle_summary['physical_validation'] and axle_summary['oem_compliance'].startswith('indeterminate') and
          (out/'integracao/envelope_frenagem_eixos/envelope_frenagem.png').is_file(),
          'Envelope frenagem de eixos:972 casos/conservação/figura,sem conformidade OEM')
    traction=pd.read_csv(out/'integracao/limite_aderencia_tracao_dianteira/casos.csv')
    traction_summary=json.loads((out/'integracao/limite_aderencia_tracao_dianteira/resumo.json').read_text())
    check(len(traction)==2430 and traction_summary['source_cases']==162 and
          traction.force_balance_residual_n.abs().max()<1e-8 and
          not traction_summary['physical_validation'] and not traction_summary['oem_acceleration_prediction'] and
          (out/'integracao/limite_aderencia_tracao_dianteira/envelope_aderencia.png').is_file(),
          'Aderência dianteira:2430 casos/equilíbrio/figura,sem prever aceleração OEM')
    climb_path=out/'integracao/envelope_subida_condicional'
    climb=pd.read_csv(climb_path/'casos.csv')
    climb_summary=json.loads((climb_path/'resumo.json').read_text())
    check(len(climb)==65610 and climb_summary['source_mass_cg_cases']==162 and
          climb.force_balance_residual_n_at_limit.abs().max()<1e-6 and
          not climb_summary['maximum_grade_represents_continuous_oem_performance'] and
          not climb_summary['global_optimum_claimed'] and not climb_summary['physical_validation'] and
          (climb_path/'envelope_subida.png').is_file(),
          'Subida condicional:65610 casos/equilíbrio/figura sem alegar desempenho contínuo OEM')
    climb_reference=climb[(climb.speed_kmh==60) & (climb.mu_assumed==.5) &
        (climb.headwind_m_s==0) & (climb.crr_assumed==.012) &
        (climb.drivetrain_efficiency_assumed==.9)].iloc[0]
    climb_ratio=climb_reference.maximum_grade_percent_in_model/100
    climb_angle=math.atan(climb_ratio)
    climb_speed=60/3.6
    climb_normal=climb_reference.mass_kg*9.80665*(
        math.cos(climb_angle)*(p['wheelbase_m']-climb_reference.cg_x_m)/p['wheelbase_m']-
        climb_reference.cg_z_m*math.sin(climb_angle)/p['wheelbase_m'])
    climb_tire=.5*max(0,climb_normal)
    climb_power=.9*p['motor_peak_kw']*1000/climb_speed
    climb_demand=(.012*climb_reference.mass_kg*9.80665*math.cos(climb_angle)+
        climb_reference.mass_kg*9.80665*math.sin(climb_angle)+
        .5*p['rho_range'][1]*p['cd_range'][1]*p['area_m2']*climb_speed**2)
    check(abs(min(climb_tire,climb_power)-climb_demand)<1e-5,
          'Subida condicional: ponto selecionado reproduz força de pneu/potência versus resistência')
    alias_path=out/'otimizacao_resolucao_temporal/aliasing_limiar_dc'
    alias_summary=json.loads((alias_path/'resumo.json').read_text())
    alias_daily=pd.read_csv(alias_path/'resumo_por_data_passo.csv')
    alias_intervals=pd.read_csv(alias_path/'intervalos.csv')
    alias_one_min=alias_daily[alias_daily.step_min==1]
    alias_coarse=alias_daily[alias_daily.step_min>1]
    check(len(alias_daily)==20 and len(alias_intervals)==5056 and
          alias_summary['intervals_non_driving']==5056 and
          alias_summary['dates']==['2026-03-20','2026-06-21','2026-09-22','2026-12-21'] and
          alias_summary['steps_min']==[1,5,15,30,60] and
          not alias_summary['linear_1min_curve_is_physical_truth'] and
          not alias_summary['physical_charger_behavior_demonstrated'] and
          not alias_summary['physical_mission_demonstrated'] and
          (alias_path/'aliasing_limiar_dc.png').is_file(),
          'I29 limiar DC:5056 intervalos/20 comparações,hipóteses e limites físicos explícitos')
    check(alias_one_min.relative_difference_current_percent.abs().max()<.1 and
          alias_coarse.relative_difference_current_percent.abs().max()<5.3 and
          abs(alias_daily.difference_current_minus_reference_kwh.abs().max()-0.4309193346602749)<1e-8,
          'I29 limiar DC:regra média aproxima referência linear em1min e erro sazonal coarsestep quantificado')
    battery=pd.read_csv(out/'mecanica_termica/I34_54sensibilidades.csv');check(len(battery)==54 and battery.thermal_residual_j.abs().max()<1e-3,'Bateria54sensibilidades térmicas')
    sensitivity=json.loads((out/'sensibilidades/resumo.json').read_text());check(sensitivity['traction_cases']==972 and sensitivity['mission_cases']==120 and sensitivity['dc_daily_cases']==36 and sensitivity['max_energy_residual_kwh']<1e-6,'972incertezas/120missões/36DC com conservação')
    for r in json.loads((out/'sensibilidades/missoes_120_comparacoes.json').read_text()):check(r['max_daily_driving_h']<=8+1e-9 and not r['physical_mission_demonstrated'],'Extremos/buffer:8h/sem afirmarviabilidade')
    buffer=json.loads((out/'buffer_comercial/resumo.json').read_text());check(buffer['cases']==32 and buffer['max_energy_residual_kwh']<1e-6 and not buffer['buffer_installed'],'Buffer comercial32casos,sem instalação')
    priorities=json.loads((out/'prioridades_servicos/resumo.json').read_text())
    check(priorities['cases']==72 and priorities['energy_residual_max_kwh']<1e-8 and priorities['soc_thresholds_project'] is None and not priorities['hardware_actuators_implemented'],'Prioridades72casos:conservação sem patamaresSOC/hardware inventados')
    priority_cases=pd.read_csv(out/'prioridades_servicos/autonomia_72comparacoes.csv')
    check((priority_cases.soc_final>=priority_cases.reserve_comparison-1e-9).all(),'Gerenciamento não atravessa reserva de comparação')
    banks=json.loads((out/'bancos_24_48_cad/resumo.json').read_text())
    check(banks['module_counts']==[2,3,4,5] and banks['all_equipment_aabb_clear'] and not banks['physical_installation_validated'],'Bancos2/3/4/5:CAD comparativo sem colisãoAABB,não homologado')
    bank_support=pd.read_csv(out/'bancos_24_48_cad/suporte_banco_completo.csv')
    check(len(bank_support)==12 and bank_support.beam_analytic_relative_error.max()<1e-7 and bank_support.force_residual_n.abs().max()<1e-7 and (bank_support.support_payload_kg>bank_support.modules*39.7).all(),'Suporte do banco inteiro inclui peso dos trilhos,verificaFEM/estática')
    pylon=json.loads((out/'protecao_pylon_documentada/resumo.json').read_text())
    check(pylon['cases']==5 and not pylon['fuse_coordination_demonstrated'] and not pylon['prospective_fault_model_replaced'],'DadoPylon2000A/1ms não substitui curto prospectivo/I²t real')
    bom=json.loads((out/'bom_atual/resumo.json').read_text())
    check(bom['known_subtotals_by_currency']=={'EUR':50990,'USD':1951,'BRL':439} and bom['installed_total_brl'] is None,'BOM1540 inclui250/60USD465,moedas separadas e sem orçamento instalado')
    # Reimport CAD independently of export; no visual estimate of solid validity.
    gmsh.initialize();gmsh.option.setNumber('General.Terminal',0)
    try:
        for path in [*(out/'integracao').glob('*.step'),*(out/'rotas_instalacoes').glob('*.step'),*(out/'bancos_24_48_cad').glob('*.step')]:
            gmsh.clear();gmsh.model.add(path.stem);gmsh.model.occ.importShapes(str(path));gmsh.model.occ.synchronize()
            vols=[gmsh.model.occ.getMass(3,t) for d,t in gmsh.model.getEntities(3)];check(bool(vols) and min(vols)>0,f'{path.name}:sólidos válidos reimportados')
    finally:gmsh.finalize()
    if args.registrar:
        inputs=[ROOT/'config/parametros_globais.yaml',ROOT/c['decision_record'],
                ROOT/'config/cabine_proposta.yaml',ROOT/'config/solar_proposta.yaml',
                ROOT/'entregas/desenvolvimento_2026-11-09/hvac_revisao/resumo.json',
                ROOT/'metadata/interfaces_contextuais.csv',
                *list((ROOT/'src/motorhome').glob('*.py')),*list((ROOT/'scripts').glob('*.py')),*list((ROOT/'tests').glob('*.py'))]
        outputs=[f for f in out.rglob('*') if f.is_file() and f.name not in ['manifesto.json','qa.json','execucao_pipeline.json','verificar_cenario_integrado.log']]
        manifest={'inputs':{str(f.relative_to(ROOT)):sha(f) for f in inputs},'outputs':{str(f.relative_to(ROOT)):sha(f) for f in outputs},'physical_validation':False}
        (out/'manifesto.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    manifest=json.loads((out/'manifesto.json').read_text())
    for group in ['inputs','outputs']:
        for path,expected in manifest[group].items():
            if sha(ROOT/path)!=expected:errors.append(f'Hash divergente:{path}')
    report={'status':'PASSOU' if not errors else 'FALHOU','checks':checks,'errors':errors,'scenario':c['_execution']['scenario'],
        'physical_mission_demonstrated':False,'human_approved':0,'scope':'Verificação numérica do cenário condicional;sem homologação ou completude físicaOEM.'}
    (out/'qa.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='checks'},ensure_ascii=False))
    raise SystemExit(bool(errors))


if __name__=='__main__':main()
