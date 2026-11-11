"""Fecha comparação24/48h com CAD de2/3/4/5módulos,massa/CG e suporte local."""
import ast
import copy
import itertools
import json
import sys
from pathlib import Path

import gmsh
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from motorhome.cenarios import carregar_configuracao, diretorio_entregas
from motorhome.desenvolvimento import centro_massa, viga_fem
from motorhome.protecoes import grupo_parafusos_espacial
from motorhome.reconciliacao import dimensionar_modulos


def main():
    c=carregar_configuracao(ROOT);p={k:v['value'] for k,v in c['parameters'].items()};d=c['development'];geo=d['geometry'];beam=d['structure'];mat=d['materials'];mount=d['mounting_detail']
    root=diretorio_entregas(ROOT);out=root/'bancos_24_48_cad';out.mkdir(exist_ok=True)
    service=sum(x['energy_ac_or_dc_kwh_day']['base']/(p['eta_inverter'] if x['side']=='AC' else p['eta_lv']) for x in c['loads'])+p['inverter_idle_w']*24/1000
    sizing=[]
    for hours,reserve in itertools.product([24,48],sorted({x[1] for x in p['trip_reserve_pairs']})):
        sizing.append({'hours':hours,'reserve':reserve,**dimensionar_modulos(service,hours/24,reserve,p['module_service_kwh'],p['module_service_dod'])})
    parts=d['layout_equipment']['A_fixa'];original=sorted([x for x in parts if x['id'].startswith('US5000_')],key=lambda x:x['position_m'][2]);first=original[0]
    pitch=original[1]['position_m'][2]-first['position_m'][2]
    if any(abs(x['position_m'][2]-(first['position_m'][2]+i*pitch))>1e-9 for i,x in enumerate(original)):raise ValueError('Pilha original não uniforme')
    inventory=pd.read_csv(root/'integracao/inventario_massas.csv');inventory=inventory[(inventory.layout=='A_fixa')&~inventory.id.str.startswith('US5000_')]
    base=[{'mass_kg':float(x.mass_kg),'cg_m':ast.literal_eval(x.cg_m)} for x in inventory.itertuples()]
    counts=sorted({x['modulos'] for x in sizing}|{len(original)});rows=[];supports=[]
    gmsh.initialize();gmsh.option.setNumber('General.Terminal',0)
    try:
        for count in counts:
            gmsh.clear();gmsh.model.add(f'banco_{count}modulos');gmsh.model.occ.importShapes(str(root/'integracao/A_fixa.step'));gmsh.model.occ.synchronize()
            width=geo['cargo_outer_m'][1]-2*geo['lining_each_side_m'];shift=np.array([0,-width/2,0]);old_tags=[]
            for dim,tag in gmsh.model.getEntities(3):
                bbox=np.array(gmsh.model.getBoundingBox(dim,tag));lo=bbox[:3];size=bbox[3:]-lo
                if any(np.max(abs(lo-(np.array(x['position_m'])+shift)))<1e-6 and np.max(abs(size-x['dimensions_m']))<1e-6 for x in original):old_tags.append((dim,tag))
            if len(old_tags)!=len(original):raise ValueError('CAD não identifica os módulos originais por geometria')
            gmsh.model.occ.remove(old_tags,recursive=True);gmsh.model.occ.synchronize()
            obstacles=[(tag,np.array(gmsh.model.getBoundingBox(3,tag))) for _,tag in gmsh.model.getEntities(3)]
            work=copy.deepcopy(base);collisions=[];modules=[]
            for i in range(count):
                pos=np.array(first['position_m']);pos[2]+=i*pitch;size=np.array(first['dimensions_m']);lo=pos+shift;hi=lo+size
                for tag,b in obstacles:
                    overlap=np.minimum(hi,b[3:])-np.maximum(lo,b[:3])
                    if (overlap>1e-6).all():collisions.append({'module':i+1,'obstacle_entity':tag,'bbox_overlap_m3':float(np.prod(overlap))})
                gmsh.model.occ.addBox(*lo,*size)
                local=pos+size/2;cg=[geo['rear_plane_from_front_axle_m']-local[0],local[1]-width/2,geo['floor_z_global_m']+local[2]]
                work.append({'mass_kg':p['module_service_mass_kg'],'cg_m':cg});modules.append({'id':f'US5000_{i+1}','position_m':pos.tolist(),'dimensions_m':size.tolist()})
            gmsh.model.occ.synchronize();gmsh.write(str(out/f'A_banco_{count}modulos.step'))
            total,cg=centro_massa(work);rear=total*cg[0]/p['wheelbase_m'];front=total-rear
            payload=count*p['module_service_mass_kg'];height=first['position_m'][2]+first['dimensions_m'][2]/2+(count-1)*pitch/2
            row={'modules':count,'bank_nominal_kwh':count*p['module_service_kwh'],'bank_mass_kg':payload,
                'module_envelope_m3':count*float(np.prod(first['dimensions_m'])),'stack_top_m':float(modules[-1]['position_m'][2]+first['dimensions_m'][2]),
                'cad_aabb_collisions':collisions,'vehicle_mass_modules_only_kg':total,'cg_x_m':cg[0],'cg_y_m':cg[1],'cg_z_m':cg[2],
                'front_kg':front,'rear_kg':rear,'pbt_margin_kg':p['oem_pbt_kg']-total,'axle_compliance':None,'rack_mass_change_unknown':True,'installed_price_brl':None}
            rows.append(row)
            side=beam['beam_outer_side_m'];wall=beam['beam_wall_m'];inertia=(side**4-(side-2*wall)**4)/12
            # Existing beam geometry reused;each variant changes payload,not an
            # invented OEMbeam or certified anchorage.Whole-rack CG now used.
            rail_mass=beam['number_rails']*beam['beam_length_m']*(side**2-(side-2*wall)**2)*mat['steel_density_kg_m3']
            support_payload=payload+rail_mass
            combined_height=(payload*height+rail_mass*side/2)/support_payload
            for factor in beam['vertical_load_factors']:
                q=support_payload*mount['gravity_m_s2']*factor/(beam['number_rails']*beam['beam_length_m'])
                fem=viga_fem(beam['beam_length_m'],mat['steel_E_pa'],inertia,q,elements=32)
                stress=q*beam['beam_length_m']**2/8*(side/2)/inertia
                span=np.array(first['dimensions_m'][:2])-2*d['mounting_redesign']['edge_distance_m']
                coords=[[x,y,0] for x,y in itertools.product([-span[0]/2,span[0]/2],[-span[1]/2,span[1]/2])]
                maxutil=0.;force_residual=moment_residual=0.
                for axis,sign,vertical in itertools.product([0,1],[-1,1],[-1,1]):
                    force=np.array([0.,0.,support_payload*mount['gravity_m_s2']*vertical]);force[axis]=sign*support_payload*mount['gravity_m_s2']*factor
                    r=grupo_parafusos_espacial(force,np.cross([0,0,combined_height],force),coords)
                    shear=np.array(r['bolt_shear_n']);tension=np.array(r['bolt_tension_n'])
                    maxutil=max(maxutil,float(np.sqrt(tension**2+3*shear**2).max()/mount['conservative_thread_area_m2']*mount['safety_factor']/mount['assumed_bolt_yield_pa']))
                    force_residual=max(force_residual,max(abs(x) for x in r['force_residual_n']));moment_residual=max(moment_residual,max(abs(x) for x in r['moment_residual_nm']))
                supports.append({'modules':count,'factor_g_hypothetical':factor,'rail_self_mass_kg':rail_mass,'support_payload_kg':support_payload,'beam_stress_pa':stress,
                    'beam_yield_utilization':stress*mount['safety_factor']/mat['steel_yield_pa'],
                    'beam_max_deflection_m':fem['max_displacement_m'],'beam_analytic_relative_error':abs(fem['max_displacement_m']/fem['analytic_max_m']-1),
                    'rack_bolt_span_x_m':float(span[0]),'rack_bolt_span_y_m':float(span[1]),'rack_bolt_combined_utilization':maxutil,
                    'force_residual_n':force_residual,'moment_residual_nm':moment_residual,'oem_anchorage_verified':False})
    finally:gmsh.finalize()
    pd.DataFrame(sizing).to_csv(out/'dimensionamento_24_48.csv',index=False);pd.DataFrame(supports).to_csv(out/'suporte_banco_completo.csv',index=False)
    (out/'layouts_massas.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
    result={'module_counts':counts,'sizing':sizing,'layouts':len(rows),'all_equipment_aabb_clear':all(not x['cad_aabb_collisions'] for x in rows),
        'support_cases':len(supports),'module_pitch_inferred_m':pitch,'gap_from_existing_estimated_cad_m':pitch-first['dimensions_m'][2],
        'physical_installation_validated':False,'capacity_final_approved':False,
        'limits':['CAD remove3módulos e insere cada quantidade,sem somar água/ocupantes novamente.',
            'Passo/folga10mm é da geometria estimada existente,não requisito de fabricante verificado.',
            'Cargas por eixo/cursoOEM,acesso/ventilação/rack real e material/fadiga/placas/ancoragem permanecem pendentes.',
            'Massa veicular varia só módulos;trilhos próprios4.53kg já cabem na reserva de suporte,não somados outra vez. Cálculo de esforço inclui seu peso;demaisdiferenças de rack/cabos/proteções desconhecidas.',
            'Parafusos usam grupo no contorno geométrico disponível,não furaçãoOEM. Aprovação de beam/bolt local não prova carroceria.']}
    (out/'resumo.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
