"""QA execução02: referências físicas, integração, CAD real e proveniência."""
import argparse
import ast
import hashlib
import json
import platform
import re
from pathlib import Path

import gmsh
import numpy as np
import pandas as pd
import yaml

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'entregas/desenvolvimento_2026-11-09'


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--registrar',action='store_true');args=p.parse_args()
    errors=[];checks=[]
    def check(test,label):
        checks.append({'check':label,'pass':bool(test)})
        if not test:errors.append(label)
    c=yaml.safe_load((ROOT/'config/parametros_globais.yaml').read_text())
    params={k:v['value'] for k,v in c['parameters'].items()}
    check(sha(ROOT/c['decision_record'])==c['sources']['dec']['sha256'],'Registro61 original preservado')
    text=(ROOT/c['decision_record']).read_text()
    check(len(re.findall(r'^## DEC-\d{3}',text,re.MULTILINE))==61,'61 decisões presentes')
    check(params['architecture']=='B' and not params['stored_transfer_allowed'] and not params['dc_interface_demonstrated'],'B e bancos independentes; interface não demonstrada')
    check(params['ac_voltage_v']==220 and params['ac_frequency_hz']==60,'220V60Hz')
    mass=pd.read_csv(OUT/'integracao/inventario_massas.csv')
    layout=json.loads((OUT/'integracao/layouts_massas.json').read_text())
    for name,row in layout['layouts'].items():
        subset=mass[mass.layout==name];nominal=row['nominal']
        total=float(subset.mass_kg.sum())
        cg=sum(float(r.mass_kg)*np.array(ast.literal_eval(r.cg_m)) for r in subset.itertuples())/total
        check(abs(total-nominal['mass_kg'])<1e-7 and np.max(abs(cg-[nominal['cg_x_m'],nominal['cg_y_m'],nominal['cg_z_m']]))<1e-9,f'{name}: massa e momentos independentes')
        check(abs(nominal['front_kg']+nominal['rear_kg']-total)<1e-7,f'{name}: reações conservam massa')
        check(nominal['axle_compliance'] is None,f'{name}: não inventa limite eixo')
    selected=layout['layouts']['A_fixa']
    check(not selected['equipment_collisions'] and not selected['wheel_arch_collisions_assumed_geometry'] and not selected['outside_envelope'],'A: caixas/equipamentos/cotas sem interseção na geometria estimada')
    check(selected['washer_door_service_clearance_m']>=selected['washer_door_required_extension_m'],'A: reserva de abertura lavadora')
    check(abs(params['assembled_typical_mass_kg']-selected['nominal']['mass_kg'])<1e-8,'Massa fonte única = CAD/inventário')
    gmsh.initialize();gmsh.option.setNumber('General.Terminal',0)
    cad=[]
    try:
        for path in sorted([*(OUT/'integracao').glob('*.step'),*(OUT/'rotas_instalacoes').glob('*.step'),*(OUT/'fixacoes_redimensionadas').glob('*.step'),*(OUT/'teto_maxeon').glob('*.step')]):
            gmsh.clear();gmsh.model.add(path.stem);gmsh.model.occ.importShapes(str(path));gmsh.model.occ.synchronize()
            volumes=[gmsh.model.occ.getMass(3,tag) for dim,tag in gmsh.model.getEntities(3)]
            check(len(volumes)>0 and min(volumes)>0,f'{path.name}: STEP reimporta sólidos positivos')
            cad.append({'path':str(path.relative_to(ROOT)),'solid_count':len(volumes),'volume_m3':sum(volumes)})
    finally:gmsh.finalize()
    fem=pd.read_csv(OUT/'integracao/fixacao_bateria_FEM_convergencia.csv')
    check(fem.relative_deflection_error.max()<1e-7 and fem.force_residual_n.abs().max()<1e-5,'FEM versus solução analítica e forças')
    water=pd.read_csv(OUT/'integracao/agua_operacao_14dias.csv')
    check(water.water_balance_residual_l.abs().max()<1e-8 and water.grey_l.max()<=70 and water.black_l.max()<=20,'Água: conservação e capacidades')
    v=pd.read_csv(OUT/'integracao/ventilacao_natural_co2_umidade.csv')
    check((v[v.delta_k==0].flow_m3_h==0).all(),'Sem vento/gradiente não inventa renovação de ar')
    daily=pd.read_csv(OUT/'energia_sistemas/I27_autonomia_otima_modelo_sem_HV.csv')
    check(daily.energy_residual_kwh.abs().max()<1e-8 and (daily.soc_final==.3).all(),'I27 SOC30% e balanço exato')
    check(len(daily[daily.horizon_kind=='optimal_upto24h'])==2,'I27 tempo livre≤24h otimizado em ambas condições iniciais')
    missions=json.loads((OUT/'energia_sistemas/I29_missoes_massas_integradas.json').read_text())
    for row in missions:
        check(abs(row['energy_residual_kwh'])<1e-6 and not row['physical_mission_demonstrated'] and row['external_electric_energy_kwh']==0,f'I29 {row["id"]}: conservação e estado físico')
        # Independent power equation catches accidental omission of fixed
        # traction auxiliaries at the model-to-mission integration boundary.
        speed=row['speed_kmh'];v=speed/3.6
        wheel=(.5*params['rho_range'][1]*params['cd_range'][1]*params['area_m2']*v*v+params['crr_range'][1]*row['mass_kg']*9.80665)*v/1000
        expected=(wheel/params['eta_traction_range'][1]+params['traction_aux_assumed_w']/1000)/speed
        check(abs(row['kwh_km']-expected)<1e-10 and abs(row['totals']['traction_used_kwh']-row['distance_km']*expected)<1e-6,f'I29 {row["id"]}: auxiliares de tração efetivamente consumidos')
    dispatch=json.loads((OUT/'despacho_i25/resumo.json').read_text())
    check(dispatch['cases_milp']==630 and not dispatch['interface_demonstrated'],'I25:630alocações sem inferir interface física')
    check(dispatch['configuration_sha256']==sha(ROOT/'config/parametros_globais.yaml'),'I25: configuração efetivamente executada')
    for path in (OUT/'despacho_i25').glob('perfil_*.csv'):
        f=pd.read_csv(path);dt=float(f.start_h.iloc[1]-f.start_h.iloc[0])
        minimum=float(re.search(r'_min([0-9.]+)kW',path.name)[1])
        on=f.fv_traction_kwh>1e-7
        check((f.loc[on,'parked_for_charge']).all() and (f.loc[on,'driving_h']==0).all(),f'{path.name}: somente DC estacionária')
        check((f.loc[on,'fv_traction_kwh']>=minimum*dt-1e-6).all(),f'{path.name}: mínimoDC respeitado')
        check(f.solar_credit_start_kwh.iloc[0]==0 and f.solar_credit_end_kwh.min()>-1e-6,f'{path.name}: não consome tração inicial')
        check(np.max(np.abs(f.pv_kw*dt-f.fv_traction_kwh-f.fv_services_kwh-f.fv_curtailed_kwh))<1e-6 and f.fv_curtailed_kwh.min()>-1e-6,f'{path.name}: FV sem dupla contagem')
        check(np.max(np.abs(f.solar_credit_end_kwh-f.solar_credit_start_kwh-f.hv_received_kwh+f.traction_used_kwh))<1e-6,f'{path.name}: balanço do crédito solar')
        check(abs(f.service_end_kwh.iloc[-1]-f.service_start_kwh.iloc[0])<1e-6,f'{path.name}: serviços cíclicos')
        load=sum(x['energy_ac_or_dc_kwh_day']['base']/(params['eta_inverter'] if x['side']=='AC' else params['eta_lv']) for x in c['loads'])+params['inverter_idle_w']*24/1000
        if 'servicos0_' in path.name:load=0.
        check(np.max(np.abs(f.service_end_kwh-f.service_start_kwh-params['eta_service_charge']*f.fv_services_kwh+load/len(f)))<1e-6,f'{path.name}: energia de serviços verificada independentemente')
    chronology=pd.read_csv(OUT/'otimizacao_grade/sanitaria_cronologia.csv')
    check(chronology.balance_residual_l.abs().max()<1e-7 and chronology.clean_l.between(0,100).all() and chronology.grey_l.between(0,70).all() and chronology.black_l.between(0,20).all(),'Cronologia hídrica: conservação e capacidades')
    for scenario,events in chronology.groupby('scenario'):
        source=pd.read_csv(OUT/f'otimizacao_grade/melhor_reservas{scenario}.csv.gz')
        ok=True
        for day,group in events.groupby('day'):
            ordered=group.sort_values('start_h')
            ok &= bool((ordered.start_h.to_numpy()[1:]>=ordered.end_h.to_numpy()[:-1]-1e-9).all())
            part=source[source.day==day]
            for row in group.itertuples():
                overlap=part[(part.hour_end>row.start_h+1e-9)&(part.hour_end-.25<row.end_h-1e-9)]
                ok &= len(overlap)>0 and bool((overlap.driving_h_interval==0).all())
        check(ok,f'{scenario}: água sem sobreposição/condução, conferida contra replay')
    grid=json.loads((OUT/'otimizacao_grade/resumo.json').read_text())
    check(abs(grid['mass_kg']-params['assembled_typical_mass_kg'])<1e-8,'Grade1008 usa massa atualCAD/GX')
    check(grid['cases']==1008 and grid['energy_residual_max_kwh']<1e-6 and not grid['global_optimality_proven'],'Grade1008 sem alegar ótimo global')
    for path in (OUT/'otimizacao_grade').glob('melhor_*.csv.gz'):
        profile=pd.read_csv(path)
        check(profile.driving_h_interval.groupby(profile.day).sum().max()<=8+1e-9,f'{path.name}: ≤8h por dia')
        check(profile.soc_traction.between(0,1+1e-9).all() and profile.soc_service.between(0,1+1e-9).all(),f'{path.name}: SOCs físicos')
        check((profile.loc[profile.driving_h_interval>0,'traction_solar_kwh_interval']==0).all(),f'{path.name}: DC estacionária')
    sanitation=pd.read_csv(OUT/'otimizacao_grade/sanitaria_melhores_replays.csv')
    check(sanitation.balance_residual_l.abs().max()<1e-7 and (sanitation.external_electric_kwh==0).all(),'Replays sanitários independentes de recarga elétrica')
    br=pd.read_csv(OUT/'freios_integrados/convergencia.csv')
    check(br.thermal_residual_j.abs().max()<1e-5 and br.mechanical_residual_j.abs().max()<1e-5,'Freios mecânica/térmica conservativos')
    cf=json.loads((OUT/'cabine_transiente/balanco_convergencia.json').read_text())
    check(cf['half_step_mean_delta_k']<.01 and cf['finest_mesh_mean_delta_k']<.2,'CFD: sensibilidade numérica da média dentro do critério de estudo')
    check(max(x['relative_to_absolute_boundary_transfer'] for x in cf['cases'])<.002,'CFD: balanço independente de faces/armazenamento <0.2%')
    check(not cf['acceptable_physical_result'],'CFD: não promover verificação numérica a validação física')
    for path in (OUT/'cabine_transiente').glob('mesh*/campo_3d.npz'):
        field=np.load(path)
        check(np.isfinite(field['temperature_c']).all() and np.isfinite(field['velocity_m_s']).all(),f'{path.parent.name}: campo3D finito')
    thermal=pd.read_csv(OUT/'mecanica_termica/I34_54sensibilidades.csv')
    check(thermal.thermal_residual_j.abs().max()<1e-3 and thermal.electrical_residual_j.abs().max()<1e-3,'Bateria54casos conserva calor/energia')
    bom=json.loads((OUT/'bom_atual/resumo.json').read_text())
    check(bom['known_subtotals_by_currency']=={'EUR':50990,'USD':1486,'BRL':439} and bom['installed_total_brl'] is None,'BOM: separa moedas e não inventa orçamento instalado')
    inv=next(x for x in c['development']['layout_equipment']['A_fixa'] if x['id']=='inversor')
    check('GX' in params['inverter_model'] and inv['mass_kg']==31 and inv['dimensions_m']==[.323,.148,.565],'SeleçãoGX refletida no CAD/massa sem gateway externo')
    protections=json.loads((OUT/'protecoes_fixacoes/resumo.json').read_text())
    check(protections['electrical_cases']==324 and protections['fault_cases']==144 and protections['mounting_cases']==648,'Triagem elétrica/fixações efetivamente executada')
    check(protections['soc_thresholds'] is None and not protections['hardware_control_demonstrated'],'Não inventa limiaresSOC/hardware de controle')
    wires=pd.read_csv(OUT/'protecoes_fixacoes/circuitos_dc.csv')
    check(wires.energy_residual_w.abs().max()<1e-8 and np.max(np.abs(wires.load_voltage_v*wires.current_a-wires.power_ac_w/params['eta_inverter']))<1e-8,'Circuito de potência constante: balanço independente')
    faults=pd.read_csv(OUT/'protecoes_fixacoes/faltas_prospectivas.csv')
    check((~faults.breaking_screen_pass).sum()==56 and faults.actual_fuse_clearing_i2t_a2s.isna().all(),'Faltas: não promove fusível20kA nem inventaI²t real')
    mounts=pd.read_csv(OUT/'protecoes_fixacoes/fixacoes_grupos_parafusos.csv')
    check(mounts.force_residual_n.abs().max()<1e-8 and mounts.moment_residual_nm.abs().max()<1e-8,'Grupos de parafusos conservam força/momento')
    check((mounts.plate_utilization>1).sum()==10 and not mounts.oem_anchorage_verified.any(),'Chapas insuficientes explicitamente identificadas,apoioOEM não comprovado')
    redesign=json.loads((OUT/'fixacoes_redimensionadas/resumo.json').read_text())
    check(redesign['selected']==18 and redesign['candidate_cases']==378 and not redesign['physical_installation_authorized'],'378alternativas e18interfaces locais,sem liberar carroceria')
    check(redesign['configuration_sha256']==sha(ROOT/'config/parametros_globais.yaml'),'Fixações: configuração efetivamente executada')
    dimension=pd.read_csv(OUT/'fixacoes_redimensionadas/selecoes.csv')
    check(dimension.max_utilization.max()<=1 and not dimension.oem_verified.any(),'Interfaces selecionadas satisfazem somente os critérios explícitos do modelo')
    solid=pd.read_csv(OUT/'fixacoes_redimensionadas/elasticidade3d_convergencia.csv')
    check(len(solid)==9 and solid.force_residual_n.max()<1e-6 and solid.moment_residual_nm.max()<1e-7,'Elasticidade3D:9casos e equilíbrio independente')
    check(np.max(np.abs(2*solid.strain_energy_j-solid.external_work_j))<1e-7 and not solid.peak_stress_validated.any(),'Elasticidade3D: energia elástica e sem promover picos de engaste')
    solid_review=json.loads((OUT/'fixacoes_redimensionadas/elasticidade3d_resumo.json').read_text())
    check(all(x['displacement_refinement_criterion_met'] for x in solid_review['convergence']),'Refinamento do deslocamento das duas tiras satisfaz critério de estudo2%')
    check(abs(redesign['step_total_volume_m3']*c['development']['mounting_redesign']['steel_density_kg_m3']-redesign['selected_plates_gross_mass_kg'])<1e-7,'Volume STEP perfurado corresponde à massa de chapa')
    sensitivity=pd.read_csv(OUT/'fixacoes_redimensionadas/massa_consumo_cenario_adicao.csv')
    added=sensitivity[sensitivity.scenario!='base']
    check(np.max(np.abs(added.mass_kg-params['assembled_typical_mass_kg']-redesign['selected_plates_gross_mass_kg']))<1e-7 and np.max(np.abs(added.front_kg+added.rear_kg-added.mass_kg))<1e-7,'Massa adicional conservadora e reações coerentes,sem alterar baseline')
    check(added.axle_compliance.isna().all(),'Adição de chapas não inventa conformidade de eixos')
    ctrl=pd.read_csv(OUT/'protecoes_fixacoes/gerenciamento_falhas.csv')
    check((ctrl.loc[~ctrl.bms_allow | ~ctrl.telemetry_valid | ~ctrl.actuator_ok,'stage']==3).all(),'Falhas BMS/medida/atuador comandamOFF')
    peak=pd.read_csv(OUT/'protecoes_fixacoes/simultaneidade_256.csv')
    check(len(peak)==256 and peak.w.max()<=min(params['inverter_continuous_w']) and peak.va.max()<=5000,'SimultaneidadeW/VA respeitada nos cenários de estudo')
    routes=json.loads((OUT/'rotas_instalacoes/resumo.json').read_text())
    check(routes['vertical_height_565mm'] and not routes['service_envelope_collisions'],'Inversor vertical e envelope de acesso livre')
    check({x['part'] for x in routes['route_equipment_aabb_contacts']}<={'inversor','bomba','boiler'},'Rotas: contatos apenas em terminais conceituais listados')
    aero=json.loads((OUT/'aero_camadas/resumo.json').read_text())
    retry=json.loads((OUT/'aero_camadas/estabilizacao_resumo.json').read_text())
    check(len(aero['cases'])==3 and aero['validated_cd'] is None and not retry['converged'],'TentativasCFD rejeitadas sem promoverCd')
    check(aero['cases'][-1]['added_layer_cells']>0 and not aero['cases'][-1]['solver_converged'],'Malha fina com camadas não confundida com solução física convergida')
    hvac=json.loads((OUT/'hvac_revisao/resumo.json').read_text())
    check(hvac['thermal_cases']==72 and hvac['electrical_cases']==12 and hvac['nominal_va_at220v60hz']==1364,'HVAC: revisão elétrica60Hz e sensibilidades executadas')
    check(hvac['fuse_conflict_open'] and not hvac['actual_purchased_variant_confirmed'] and not hvac['capacity_at_33outside_25inside_demonstrated'],'HVAC: revisão documental não equivale a placa/curva/fusível validado')
    roof=json.loads((OUT/'teto_maxeon/resumo.json').read_text())
    check(roof['nominal_wp']==1540 and roof['fits_assumed_flat_rectangle'] and not roof['installed_geometry_validated'],'1540Wp Maxeon cabe só no retângulo estimado,não instalação validada')
    check(roof['configuration_sha256']==sha(ROOT/'config/parametros_globais.yaml'),'TetoMaxeon:configuração efetivamente executada')
    check(not roof['controller_150v_compatible'] and roof['controller_250v_roof_only_screen_pass'] and not roof['shared_mppt_approved'],'Teto:limitesDC sem aprovar MPPTcompartilhado')
    mismatch=pd.read_csv(OUT/'teto_maxeon/mppt_mismatch_72.csv')
    check(len(mismatch)==72 and (mismatch.shared_w<=mismatch.separate_w+1e-8).all(),'MPPT:72comparações e compartilhamento não cria energia')
    check(roof['source']['sha256']=='d6c76ef9231cb1621d8401a46fbef617724e6bc6ea873bb3f4658261fef75757' and not roof['baseline_updated'],'Ficha2022 rastreada;comparação não altera silenciosamente missões1350Wp')
    review=json.loads((OUT/'revisao_35_itens.json').read_text())
    check(len(review['items'])==35 and sum(r['human_approval_recorded'] for r in review['items'])==0,'35 itens revisados, zero aprovações inferidas')
    if args.registrar:
        inputs=[ROOT/'config/parametros_globais.yaml',ROOT/c['decision_record'],ROOT/'metadata/itens.csv']
        inputs+=list((ROOT/'src/motorhome').glob('*.py'))
        inputs+=list((ROOT/'tests').glob('*.py'))+[ROOT/'pyproject.toml']
        inputs+=list((ROOT/'scripts').glob('*.py'))
        inputs += [ROOT/'scripts/otimizar_grade_missao.py',ROOT/'scripts/integrar_freios_massa.py',ROOT/'scripts/diagnosticar_yplus.py']
        inputs += list((ROOT/'config').glob('*proposta.yaml'))
        inputs += [ROOT/f'entregas/etapa_pos_dec061/{name}' for name in
                   ['matriz_itens_35.json','cabine_31_32_reexecutada.json',
                    'solar_fixo_08_16.csv','solar_alternativo_00_08.csv']]
        outputs=[path for path in OUT.rglob('*') if path.is_file() and path.name not in ['manifesto.json','qa.json']]
        outputs += [ROOT/f'docs/{name}' for name in
                    ['EXECUCAO_TECNICA02.md','REVISAO_TECNICA_EXECUCAO02.md','APROVACOES_FINAIS_PENDENTES.md','PROTECOES_SERVICOS_MODELO.md']]
        manifest={'baseline_parent':'29defc4','inputs_sha256':{str(f.relative_to(ROOT)):sha(f) for f in inputs},
                  'outputs_sha256':{str(f.relative_to(ROOT)):sha(f) for f in outputs},'physical_validation':False,
                  'software':{'python':platform.python_version(),'numpy':np.__version__,
                              'pandas':pd.__version__,'yaml':yaml.__version__,'gmsh':gmsh.__version__,
                              'openfoam':'2412 patch260127; ver logs completos'}}
        (OUT/'manifesto.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    manifest=json.loads((OUT/'manifesto.json').read_text())
    for group in ['inputs_sha256','outputs_sha256']:
        for name,expected in manifest[group].items():
            if not (ROOT/name).is_file() or sha(ROOT/name)!=expected:errors.append(f'Hash divergente: {name}')
    report={'status':'PASSOU' if not errors else 'FALHOU','checks':checks,'errors':errors,'cad_reimport':cad,
            'input_hashes':len(manifest['inputs_sha256']),'output_hashes':len(manifest['outputs_sha256']),
            'stage_complete':False,'final_human_approved':0,'physical_mission_demonstrated':False}
    (OUT/'qa.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['checks','cad_reimport']},ensure_ascii=False))
    raise SystemExit(bool(errors))


if __name__=='__main__':main()
