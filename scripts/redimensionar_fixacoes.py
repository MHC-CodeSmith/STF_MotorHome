"""Dimensionamento condicional de interfaces locais; nenhuma ancoragemOEM liberada."""
import ast
import hashlib
import itertools
import json
import sys
from pathlib import Path

import gmsh
import numpy as np
import pandas as pd
import yaml

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from motorhome.protecoes import grupo_parafusos_espacial
from motorhome.reconciliacao import consumo_plano


def main():
    config=ROOT/'config/parametros_globais.yaml';c=yaml.safe_load(config.read_text())
    m=c['development']['mounting_detail'];g=c['development']['mounting_redesign']
    params={k:v['value'] for k,v in c['parameters'].items()}
    out=ROOT/'entregas/desenvolvimento_2026-11-09/fixacoes_redimensionadas';out.mkdir(parents=True,exist_ok=True)
    records=[];selections=[];sf=m['safety_factor'];fy=m['assumed_plate_yield_pa']
    for part in c['development']['layout_equipment']['A_fixa']:
        water={'tanque_limpa':100,'tanque_cinza':70,'cassete':20,'boiler':params['boiler_candidate_l']}.get(part['id'],0)
        mass=part['mass_kg']+water
        for sx,sy in g['group_spans_xy_m']:
            coords=[[x,y,0] for x,y in itertools.product([-sx/2,sx/2],[-sy/2,sy/2])]
            cases=[]
            for accel,height,offset,vertical,axis,sign in itertools.product(m['accelerations_g'],g['cg_height_above_mount_m'],g['in_plane_offset_m'],g['vertical_accelerations_g'],range(2),[-1,1]):
                force=np.array([0.,0.,mass*m['gravity_m_s2']*vertical]);force[axis]=sign*mass*m['gravity_m_s2']*accel
                arm=np.array([offset if axis==1 else 0,offset if axis==0 else 0,height])
                moment=np.cross(arm,force)
                r=grupo_parafusos_espacial(force,moment,coords)
                shear=np.array(r['bolt_shear_n']);tension=np.array(r['bolt_tension_n'])
                cases.append({'acceleration_g':accel,'cg_height_m':height,'offset_m':offset,'vertical_g':vertical,'axis':axis,'sign':sign,
                    'force_residual_n':max(abs(x) for x in r['force_residual_n']),
                    'moment_residual_nm':max(abs(x) for x in r['moment_residual_nm']),
                    'max_shear_n':float(shear.max()),'max_tension_n':float(tension.max()),
                    'max_support_compression_n':max(r['support_compression_n']),
                    'bolt_utilization':float(np.sqrt(tension**2+3*shear**2).max()/m['conservative_thread_area_m2']*sf/m['assumed_bolt_yield_pa'])})
            for thick in g['thickness_candidates_m']:
                edge_clear=g['edge_distance_m']-g['hole_diameter_m']/2
                # Each hole's local strip, conservative pure-force stress screens.
                bearing=max(x['max_shear_n'] for x in cases)/(m['bolt_diameter_m']*thick)*sf/fy
                shearout=max(x['max_shear_n'] for x in cases)/(2*edge_clear*thick)*np.sqrt(3)*sf/fy
                net=max(x['max_shear_n'] for x in cases)/((g['tributary_strip_width_m']-g['hole_diameter_m'])*thick)*sf/fy
                bending=max(x['max_tension_n'] for x in cases)*6*g['local_flange_lever_m']/(g['tributary_strip_width_m']*thick**2)*sf/fy
                transverse_shear=1.5*max(x['max_tension_n'] for x in cases)/(g['tributary_strip_width_m']*thick)*sf/fy
                strip_combined=float(np.hypot(bending,np.sqrt(3)*transverse_shear))
                bolt=max(x['bolt_utilization'] for x in cases)
                plate_mass=((sx+2*g['edge_distance_m'])*(sy+2*g['edge_distance_m'])-4*np.pi*g['hole_diameter_m']**2/4)*thick*g['steel_density_kg_m3']
                records.append({'component':part['id'],'loaded_mass_kg':mass,'water_local_only_kg':water,'span_x_m':sx,'span_y_m':sy,'thickness_m':thick,
                    'plate_mass_kg':plate_mass,'bolt_utilization':bolt,'bearing_utilization':bearing,'shearout_utilization':shearout,
                    'net_section_utilization':net,'strip_bending_utilization':bending,'strip_combined_conservative_utilization':strip_combined,'max_utilization':max(bolt,bearing,shearout,net,strip_combined),
                    'load_cases':len(cases),'max_force_residual_n':max(x['force_residual_n'] for x in cases),
                    'max_moment_residual_nm':max(x['moment_residual_nm'] for x in cases),'oem_verified':False})
            # Keep demands to permit auditing the case behind each envelope.
            pd.DataFrame(cases).to_csv(out/f"demandas_{part['id']}_{int(sx*1000)}x{int(sy*1000)}.csv",index=False)
        candidates=[x for x in records if x['component']==part['id'] and x['max_utilization']<=1]
        if candidates:
            choice=dict(min(candidates,key=lambda x:x['plate_mass_kg']));choice['status']='selecionado_provisoriamente_no_modelo'
        else:
            choice={'component':part['id'],'status':'nenhum_candidato_atende_envelope'}
        selections.append(choice)
    pd.DataFrame(records).to_csv(out/'comparacao.csv',index=False)
    pd.DataFrame(selections).to_csv(out/'selecoes.csv',index=False)
    # Tiled, perforated local interface coupons; no implied attachment to OEM body.
    gmsh.initialize()
    try:
        gmsh.option.setNumber('General.Terminal',0);gmsh.model.add('chapas_locais_condicionais')
        for i,row in enumerate(x for x in selections if 'thickness_m' in x):
            x0=(i%5)*.5;y0=(i//5)*.4;e=g['edge_distance_m'];sx=row['span_x_m'];sy=row['span_y_m'];t=row['thickness_m']
            plate=gmsh.model.occ.addBox(x0,y0,0,sx+2*e,sy+2*e,t)
            holes=[(3,gmsh.model.occ.addCylinder(x0+e+x,y0+e+y,-t,0,0,3*t,g['hole_diameter_m']/2)) for x,y in itertools.product([0,sx],[0,sy])]
            shapes,_=gmsh.model.occ.cut([(3,plate)],holes)
            gmsh.model.occ.synchronize()
            for dim,tag in shapes:gmsh.model.setEntityName(dim,tag,row['component'])
        gmsh.write(str(out/'chapas_locais_condicionais.step'))
        volumes=[gmsh.model.occ.getMass(3,t) for d,t in gmsh.model.getEntities(3)]
    finally:gmsh.finalize()
    selected=[x for x in selections if 'plate_mass_kg' in x]
    inventory=pd.read_csv(ROOT/'entregas/desenvolvimento_2026-11-09/integracao/inventario_massas.csv')
    inventory=inventory[inventory.layout=='A_fixa']
    base_mass=float(inventory.mass_kg.sum())
    base_moment=sum(float(row.mass_kg)*np.array(ast.literal_eval(row.cg_m)) for row in inventory.itertuples())
    added_moment=np.zeros(3)
    for row in selected:
        equip=next(x for x in c['development']['layout_equipment']['A_fixa'] if x['id']==row['component'])
        center=np.array(ast.literal_eval(inventory[inventory.id==row['component']].iloc[0].cg_m))
        center[2]-=equip['dimensions_m'][2]/2+row['thickness_m']/2
        added_moment+=row['plate_mass_kg']*center
    added_mass=sum(x['plate_mass_kg'] for x in selected);sensitivity=[]
    for factor in [0,1]:
        mass=base_mass+factor*added_mass;cg=(base_moment+factor*added_moment)/mass
        rear=mass*cg[0]/params['wheelbase_m'];front=mass-rear
        for speed in [40,80]:
            energy=consumo_plano(speed,mass,params['cd_range'][1],params['area_m2'],params['crr_range'][1],params['rho_range'][1],params['eta_traction_range'][1],aux_traction_kw=params['traction_aux_assumed_w']/1000)
            sensitivity.append({'scenario':'base' if factor==0 else 'adicao_integral_conservadora_sem_substituicao',
                'mass_kg':mass,'pbt_margin_kg':params['oem_pbt_kg']-mass,'cg_x_m':cg[0],'cg_y_m':cg[1],'cg_z_m':cg[2],
                'front_kg':front,'rear_kg':rear,'speed_kmh':speed,'kwh_km':energy['kwh_km'],
                'energy_7000km_traction_kwh':7000*energy['kwh_km'],'axle_compliance':None,'physical_installation_authorized':False})
    pd.DataFrame(sensitivity).to_csv(out/'massa_consumo_cenario_adicao.csv',index=False)
    result={'configuration_sha256' :hashlib.sha256(config.read_bytes()).hexdigest(),'candidate_cases':len(records),
        'components':len(selections),'selected':len(selected),'unresolved':[x['component'] for x in selections if 'plate_mass_kg' not in x],
        'local_load_cases_per_geometry':records[0]['load_cases'],'max_selected_utilization':max(x['max_utilization'] for x in selected),
        'selected_plates_gross_mass_kg':sum(x['plate_mass_kg'] for x in selected),'step_solid_count':len(volumes),
        'step_total_volume_m3':sum(volumes),'max_force_residual_n':max(x['max_force_residual_n'] for x in records),
        'max_moment_residual_nm':max(x['max_moment_residual_nm'] for x in records),
        'mass_added_to_vehicle_kg':0,'net_mass_change_unknown':True,'physical_installation_authorized':False,
        'limits':['Reações compressivas são apoios idealizados;sem contato unilateral/prying/pré-carga/fadiga.',
            'Flexão local é tira de chapa em balanço, não soluçãoFEM da base inteira.',
            'Volumes perfurados STEP são corpos de prova locais em mosaico, não pontos OEM ou CAD de instalação.',
            'Massas de chapa são comparação bruta;reserva agregada de suportes não permite substituição líquida.',
            'Reservatórios e boiler15L cheios são casos locais independentes;água do boiler provém dos100L existentes,nenhuma água adicionada ao inventário global.',
            'Não dimensiona soldas/esmagamento de espaçadores/arrancamento da carroceria ou retenção interna do equipamento.',
            'Cama_colchao modela apenas retenção do colchão12kg em movimento;estrutura da cama ocupada precisa caminho de carga próprio.',
            'Combinação de máximos de flexão/cisalhamento da tira é envelope conservador,não tensão pontualFEM;espessura pode ser comparável ao balanço e exige verificação3D.']}
    (out/'resumo.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
