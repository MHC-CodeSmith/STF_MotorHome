"""Execução02: CAD comparativo, massas/CG/eixos, FEM, ventilação e dinâmica.

Todos os novos parâmetros físicos são lidos da fonte canônica. CAD é autoral
de envelopes; dados OEM não publicados permanecem hipóteses sensibilizadas.
"""
import argparse
import csv
import hashlib
import itertools
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'src'), str(ROOT/'scripts')]
from gerar_cad_instalacoes import Modelo

from motorhome.desenvolvimento import (
    caixa_intersecao,
    centro_massa,
    consumir_agua,
    vazao_chamine,
    viga_fem,
)
from motorhome.reconciliacao import consumo_plano, indice_lateral, reacoes_eixos


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False)+'\n')


def table(path, rows):
    keys = list(dict.fromkeys(k for row in rows for k in row))
    with path.open('w') as f:
        w = csv.DictWriter(f,keys,lineterminator='\n'); w.writeheader(); w.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destino', type=Path, default=ROOT/'entregas/desenvolvimento_2026-11-09/integracao')
    args = parser.parse_args(); out=args.destino
    out.mkdir(parents=True,exist_ok=True)
    canonical = ROOT/'config/parametros_globais.yaml'
    c=yaml.safe_load(canonical.read_text()); d=c['development']
    p={k:v['value'] for k,v in c['parameters'].items()}
    geo=d['geometry']; mat=d['materials']; mass=d['mass_assumptions']
    length,width,height=np.array(geo['cargo_outer_m'])-2*geo['lining_each_side_m']
    cases=c['development']['layout_equipment']
    summaries={}; mass_rows=[]; sensitivity=[]; traction=[]
    for label,parts in cases.items():
        model=Modelo()
        for part in parts:
            model.box(part['id'],part['kind'],part['position_m'],part['dimensions_m'],[105,155,180,180])
        # CAD shares coordinates and mass-producing panel geometry. No solid
        # furniture block masquerades as a solid wood mass.
        panel_specs=[('piso',[0,0,-.018],[length,width,.018]),
                     ('tampo',[2.53,0,.91],[1.08,.62,.018]),
                     ('parede_banho',[1.99,width-.72,0],[.012,.72,1.78]),
                     ('parede_banho2',[2.89,width-.72,0],[.012,.72,1.78]),
                     ('base_banho',[2.,width-.72,0],[.89,.72,.012])]
        for x in [2.54,3.02,3.57]:
            panel_specs.append((f'divisoria_{x}',[x,0,0],[.012,.62,.91]))
        if label=='A_fixa':
            panel_specs.append(('estrado',[.02,.02,.98],[1.95,1.35,.018]))
        else:
            for y in [.02,width-.52]:
                panel_specs.append((f'assento_{y}',[.02,y,.58],[1.95,.50,.018]))
            panel_specs.append(('ponte_cama',[.02,.52,.58],[1.95,width-1.04,.018]))
        inventory=[]
        def add(name, m, local, estimated, source, inventory=inventory):
            # Front axle origin, transverse centerline, global ground height.
            inventory.append({'id':name,'mass_kg':m,
                              'cg_m':[geo['rear_plane_from_front_axle_m']-local[0],
                                      local[1]-width/2,geo['floor_z_global_m']+local[2]],
                              'estimated':estimated,'source':source})
        for part in parts:
            add(part['id'],part['mass_kg'],
                (np.array(part['position_m'])+np.array(part['dimensions_m'])/2).tolist(),
                part['estimated'],'hyp' if part['estimated'] else 'canonical_bom')
        for name,pos,size in panel_specs:
            m=float(np.prod(size)*mat['plywood_density_kg_m3'])
            model.box(name,'madeira',pos,size,[187,151,108,230])
            add(name,m,(np.array(pos)+np.array(size)/2).tolist(),True,'volumeCAD*density_hyp')
        opaque_area=2*(length*height+width*height)+2*length*width
        foam_mass=opaque_area*.032*mat['foam_density_kg_m3']
        add('isolamento',foam_mass,[length/2,width/2,height/2],True,'area_equivalente*density_hyp')
        # Thin wall/roof lining mass; floor already included separately.
        lining_area=2*(length*height+width*height)+length*width
        add('revestimentos',lining_area*.006*mat['plywood_density_kg_m3'],
            [length/2,width/2,height/2],True,'area_equivalente*density_hyp')
        add('PV_JA3',66,[1.85,width/2,2.0],False,'history_JA450')
        add('PV190',10.5,[3.926,width/2,2.0],False,'history_Victron190')
        for allowance in d['mass_allowances']:
            add(allowance['id'],allowance['mass_kg'],allowance['cg_local_m'],True,'hyp_allowance')
        # Basin/sink, mattress support/fasteners, seats/travel remain OEM except
        # stationary furniture. The remaining fitting allowance is explicit.
        add('cuba_torneira',4,[2.8,.3,.83],True,'hyp_allowance')
        add('ferragens_estrutura_cama',12 if label=='A_fixa' else 20,[1.,.8,.5],True,'hyp_allowance')
        add('bagagens',mass['baggage_kg'],[1.,.8,.5],False,'DEC008')
        for i,m in enumerate(mass['occupants_kg']):
            inventory.append({'id':f'ocupante{i+1}','mass_kg':m,'cg_m':[.2,(-.45 if i==0 else .45),1.15],
                              'estimated':False,'source':'DEC008_massa_posicao_estimada'})
        # Water is not new mass for each tank: states always sum to100L.
        water_positions=[(np.array(next(part for part in parts if part['id']==name)['position_m'])+
                          np.array(next(part for part in parts if part['id']==name)['dimensions_m'])/2).tolist()
                         for name in ['tanque_limpa','tanque_cinza','cassete']]
        for factor,rearfrac,baseheight,water in itertools.product(
                mass['estimated_mass_factor'],mass['base_rear_fraction'],
                mass['base_cg_height_m'],mass['water_states_l']):
            work=[dict(part,mass_kg=part['mass_kg']*(factor if part['estimated'] else 1)) for part in inventory]
            for j,(volume,local) in enumerate(zip(water,water_positions)):
                work.append({'id':f'agua{j}','mass_kg':volume,
                             'cg_m':[geo['rear_plane_from_front_axle_m']-local[0],local[1]-width/2,geo['floor_z_global_m']+local[2]]})
            work.append({'id':'base_oem','mass_kg':p['oem_tare_kg'],
                         'cg_m':[p['wheelbase_m']*rearfrac,0,baseheight]})
            total,cg=centro_massa(work)
            axles=reacoes_eixos([(part['mass_kg'],part['cg_m'][0]) for part in work],p['wheelbase_m'])
            row={'layout':label,'estimated_mass_factor':factor,'oem_rear_fraction_assumed':rearfrac,
                 'oem_cg_height_assumed_m':baseheight,'water_clean_grey_black_l':str(water),
                 'mass_kg':total,'cg_x_m':cg[0],'cg_y_m':cg[1],'cg_z_m':cg[2],
                 'front_kg':axles['dianteiro_kg'],'rear_kg':axles['traseiro_kg'],
                 'pbt_margin_kg':4250-total,'axle_compliance':None,
                 'geometric_ay_g':indice_lateral(p['rear_track_m'],cg[2],cg[1])}
            sensitivity.append(row)
            if factor==1 and rearfrac==.42 and baseheight==.78 and water==[100,0,0]:
                mass_rows.extend([dict(layout=label,**part) for part in work])
                nominal=row
        collisions=[]
        for a,b in itertools.combinations(parts,2):
            volume=caixa_intersecao(a,b)
            if volume: collisions.append({'a':a['id'],'b':b['id'],'volume_m3':volume})
        arch_collisions=[]
        for part,arch in itertools.product(parts,geo['wheel_arch_boxes']):
            volume=caixa_intersecao(part,arch)
            if volume: arch_collisions.append({'part':part['id'],'arch':arch['id'],'volume_m3':volume})
        # AABB tests include external grey tank intentionally; not claimed to
        # prove underbody clearances. Door service spaces are separate tests.
        outside=[part['id'] for part in parts if part['id']!='tanque_cinza' and (
            any(x < 0 for x in part['position_m']) or
            any(x+y > z+1e-9 for x,y,z in zip(part['position_m'],part['dimensions_m'],[length,width,height])))]
        door_clearance=(2.53-(1.32+.62)) if label=='A_fixa' else width-.72-.60
        model.export(out,label,{'rear_x_m':0,'cargo_width_m':width,'floor_z_m':0})
        for speed in np.arange(10,91,2):
            for mname,m in [('tipica_estimada',nominal['mass_kg']),('teto_PBT_nao_homologado_eixos',4250)]:
                result=consumo_plano(float(speed),m,p['cd_range'][1],p['area_m2'],p['crr_range'][1],p['rho_range'][1],p['eta_traction_range'][1],aux_traction_kw=p['traction_aux_assumed_w']/1000)
                traction.append({'layout':label,'mass_case':mname,'mass_kg':m,'speed_kmh':speed,**result})
        summaries[label]={'nominal':nominal,'equipment_collisions':collisions,
                          'wheel_arch_collisions_assumed_geometry':arch_collisions,'outside_envelope':outside,
                          'washer_door_service_clearance_m':door_clearance,
                          'washer_door_required_extension_m':1.10-.62,
                          'aisle_front_m':width-.62-.72,'geometry_status':'ESTUDO_DE_ENVELOPES_NAO_VALIDADO',
                          'selection':'A_provisorio_espaco_manutencao_verificar' if label=='A_fixa' else 'comparador_conversivel',
                          'axle_limits_documented':False}
        fig,axes=plt.subplots(1,3,figsize=(14,4),layout='constrained')
        for ax,(i,j),title in zip(axes,[(0,1),(0,2),(1,2)],['Planta','Lateral','Traseira']):
            for part in parts:
                pos=part['position_m']; sz=part['dimensions_m']
                ax.add_patch(plt.Rectangle((pos[i],pos[j]),sz[i],sz[j],alpha=.35))
                ax.text(pos[i]+sz[i]/2,pos[j]+sz[j]/2,part['id'],fontsize=5,ha='center')
            extents=[length,width,height]
            ax.annotate('',xy=(0,-.22),xytext=(extents[i],-.22),arrowprops={'arrowstyle':'<->'})
            ax.text(extents[i]/2,-.31,f'{extents[i]:.3f} m',ha='center',fontsize=8)
            ax.annotate('',xy=(extents[i]+.05,0),xytext=(extents[i]+.05,extents[j]),arrowprops={'arrowstyle':'<->'})
            ax.text(extents[i]+.08,extents[j]/2,f'{extents[j]:.3f} m',rotation=90,fontsize=8)
            ax.set(xlim=(-.1,extents[i]+.22),ylim=(-.4,extents[j]+.1),aspect='equal',title=title,xlabel='m',ylabel='m')
        fig.suptitle(label+' — envelopes cotados em metros, hipóteses de integração')
        fig.savefig(out/f'{label}_vistas.png',dpi=160); plt.close(fig)
    table(out/'inventario_massas.csv',mass_rows);table(out/'massa_cg_eixos_sensibilidade.csv',sensitivity)
    table(out/'dinamica_massa_integrada.csv',traction)
    save(out/'layouts_massas.json',{'layouts':summaries,'inner_envelope_m':[length,width,height],
        'base_cg_and_axles':'OEM não publicados; hipóteses .35/.42/.50 traseiro, z .65/.78/.90m',
        'pbt_case':'4250kg é teto condicional; não massa máxima admissível sem limites por eixo',
        'unknown_mass':'InterfaceDC/buffer não instalados; massas adicionais requeridas reduzem margem.'})
    # Structural sizing: real Euler-Bernoulli stiffness matrix, convergence and
    # comparison with an independent closed-form solution.
    s=d['structure']; inertia=(s['beam_outer_side_m']**4-(s['beam_outer_side_m']-2*s['beam_wall_m'])**4)/12
    fea=[]
    for factor,n in itertools.product(s['vertical_load_factors'],s['elements']):
        q=s['battery_payload_kg']*9.80665*factor/s['number_rails']/s['beam_length_m']
        result=viga_fem(s['beam_length_m'],mat['steel_E_pa'],inertia,q,n)
        stress=q*s['beam_length_m']**2/8*(s['beam_outer_side_m']/2)/inertia
        fea.append({'load_factor':factor,'elements':n,'max_displacement_m':result['max_displacement_m'],
                    'analytic_m':result['analytic_max_m'],'stress_pa':stress,
                    'yield_margin_ratio':mat['steel_yield_pa']/stress,'force_residual_n':result['force_residual_n'],
                    'relative_deflection_error':abs(result['max_displacement_m']/result['analytic_max_m']-1)})
        table(out/f'FEM_bateria_{factor}g_{n}elementos.csv',
              [{'x_m':x,'deflection_m':v,'rotation_rad':r} for x,v,r in zip(result['x_m'],result['displacement_m'],result['rotation_rad'])])
    table(out/'fixacao_bateria_FEM_convergencia.csv',fea)
    # Roof: retain target1540Wp; two orientations quantitatively rejected or
    # conditioned by independent envelope and string-compatibility checks.
    roof_results=[]
    for roof in d['roof_candidates']:
        boxes=[]
        for i in range(roof['main_count']):
            pos=list(roof['main_start_m']); pos[0]+=i*(roof['main_dimensions_m'][0]+roof['gap_m'])
            boxes.append({'id':f'JA_{i}','position_m':pos,'dimensions_m':roof['main_dimensions_m']})
        boxes.append({'id':'190W','position_m':roof['extra_position_m'],'dimensions_m':roof['extra_dimensions_m']})
        outside=[b['id'] for b in boxes if b['position_m'][0]+b['dimensions_m'][0]>d['roof_assumed_envelope_m'][0]
                 or b['position_m'][1]+b['dimensions_m'][1]>d['roof_assumed_envelope_m'][1]]
        model=Modelo()
        for b in boxes: model.box(b['id'],'PV',b['position_m'],b['dimensions_m'],[40,65,120,255])
        model.export(out,roof['id'],{'rear_x_m':0,'cargo_width_m':width,'floor_z_m':0})
        roof_results.append({'id':roof['id'],'target_wp':1540,'outside_assumed_envelope':outside,
                             'area_modules_m2':sum(b['dimensions_m'][0]*b['dimensions_m'][1] for b in boxes),
                             'power_with_demonstrated_48v_string_wp':1350,
                             'installation_verified':False,'note':d['roof_note']})
    save(out/'teto_duas_configuracoes.json',roof_results)
    # Natural ventilation: zero buoyancy at equal temperatures, even when the
    # openings are large; CO2 and humidity are separately checked.
    v=d['ventilation_study']; ventilation=[]
    for area,delta,vapour in itertools.product(v['opening_free_area_m2'],v['delta_temperature_k'],v['vapour_kg_h']):
        q=vazao_chamine(area,area,v['vertical_separation_m'],25+delta,25,v['discharge_coefficient'])*3600
        co2=None if q==0 else v['outside_co2_ppm']+2*v['co2_generation_l_h_person']/1000/q*1e6
        ventilation.append({'area_each_m2':area,'delta_k':delta,'flow_m3_h':q,'vapour_source_kg_h':vapour,
                            'co2_equilibrium_ppm':co2,'vapour_excess_kg_m3':None if q==0 else vapour/q,
                            'co2_target_met':co2 is not None and co2<=v['target_co2_ppm']})
    table(out/'ventilacao_natural_co2_umidade.csv',ventilation)
    water=[];state={'clean_l':100.,'grey_l':0.,'black_l':0.}
    # Refill/disposal performed before capacity violation, explicit no grid.
    incoming=outgoing=0.
    for day in range(1,15):
        refill=dispose=0.
        demands=[('uso_moderado',60.,.10)]
        if day%7==0: demands.append(('lavagem',68.8,0.))
        for name,volume,frac in demands:
            try: next_state=consumir_agua(state,volume,frac)
            except ValueError:
                dispose=state['grey_l']+state['black_l'];refill=100-state['clean_l']
                outgoing+=dispose;incoming+=refill
                state={'clean_l':100.,'grey_l':0.,'black_l':0.}
                next_state=consumir_agua(state,volume,frac)
            state={k:next_state[k] for k in ['clean_l','grey_l','black_l']}
            residual=100+incoming-outgoing-sum(state.values())
            water.append({'day':day,'event':name,'refill_l':refill,'disposed_l':dispose,**state,
                          'water_balance_residual_l':residual,'external_electric_kwh':0.})
            refill=dispose=0.
    table(out/'agua_operacao_14dias.csv',water)
    save(out/'resumo_execucao.json',{'canonical_sha256':hashlib.sha256(canonical.read_bytes()).hexdigest(),
        'items_covered_by_integration_review':list(range(1,36)),
        'calculated_here':[8,11,13,14,15,16,17,18,20,21,22,26],
        'mass_scenarios':len(sensitivity),'traction_points':len(traction),'FEA_cases':len(fea),
        'physical_validation':False,'final_human_approval':False,
        'limits':['Massa estimada completa de trabalho, não pesagem.',
                  'Eixos OEM, apoio carroceria e CGbase não documentados; reações condicionadas.',
                  'FEM1D de trilho não valida parafusos, soldas ou fixação na van.',
                  'Geometrias estimadas conservadas com colisões registradas, sem ocultar não conformidades.']})
    print(json.dumps({'layouts':summaries,'mass_scenarios':len(sensitivity),'FEA_cases':len(fea)},ensure_ascii=False))


if __name__=='__main__':
    main()
