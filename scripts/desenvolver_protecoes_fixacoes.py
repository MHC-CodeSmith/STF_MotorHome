"""Serviços48V, falhas, gerenciamento lógico e grupos de fixação parametrizados."""
import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from motorhome.cenarios import carregar_configuracao, diretorio_entregas
from motorhome.protecoes import (
    GerenciadorCargas,
    alocar_picos,
    circuito_dc,
    falta_prospectiva,
    grupo_parafusos,
)


def main():
    out=diretorio_entregas(ROOT)/'protecoes_fixacoes';out.mkdir(parents=True,exist_ok=True)
    c=carregar_configuracao(ROOT);p={k:v['value'] for k,v in c['parameters'].items()}
    e=c['development']['electrical_detail'];m=c['development']['mounting_detail']
    rows=[]
    for voltage,temp,area,length,power in itertools.product(e['battery_voltage_sweep_v'],e['copper_temperature_c'],e['sections_mm2'],e['loop_lengths_m'],e['powers_ac_w']):
        r=circuito_dc(power,voltage,p['eta_inverter'],length,area,temp,p['cable_rho20'],p['cable_alpha'])
        rows.append({'voltage_v':voltage,'temperature_c':temp,'section_mm2':area,'loop_m':length,'power_ac_w':power,**r})
    wires=pd.DataFrame(rows);wires.to_csv(out/'circuitos_dc.csv',index=False)
    faults=[]
    for voltage,resistance,area,length in itertools.product(e['battery_voltage_sweep_v'],e['module_fault_resistance_ohm'],e['sections_mm2'],[0,*e['loop_lengths_m']]):
        rwire=p['cable_rho20']*length/(area*1e-6)
        current=falta_prospectiva(voltage,resistance,p['service_modules_provisional'],rwire)
        # Integrate rho(T) in the copper adiabatic heat equation. This is
        # a physical screening budget, NOT an IEC k-factor or a fuse I²t.
        t0=40;tmax=90;alpha=p['cable_alpha']
        i2t=e['copper_density_kg_m3']*e['copper_cp_j_kgk']*(area*1e-6)**2/(p['cable_rho20']*alpha)*np.log((1+alpha*(tmax-20))/(1+alpha*(t0-20)))
        faults.append({'voltage_v':voltage,'module_r_ohm_assumed':resistance,'section_mm2':area,'loop_m':length,
            'prospective_a':current,'fuse_breaking_a':e['fuse_main']['dc_breaking_a'],
            'breaking_screen_pass':current<=e['fuse_main']['dc_breaking_a'],
            'copper_40_to90_budget_a2s':i2t,'max_unlimited_constant_fault_duration_s':i2t/current**2,
            'actual_fuse_clearing_i2t_a2s':None,'coordination_demonstrated':False})
    pd.DataFrame(faults).to_csv(out/'faltas_prospectivas.csv',index=False)
    powers=[]
    for mask,stage in itertools.product(itertools.product([False,True],repeat=len(e['load_scenarios'])),range(4)):
        loads=[x for x,take in zip(e['load_scenarios'],mask,strict=True) if take]
        r=alocar_picos(loads,stage,min(p['inverter_continuous_w']),5000)
        powers.append({'requested':','.join(x['id'] for x in loads),'stage':stage,'w':r['w'],'va':r['va'],
            'accepted':','.join(r['accepted']),'rejected':json.dumps(r['rejected'],ensure_ascii=False)})
    pd.DataFrame(powers).to_csv(out/'simultaneidade_256.csv',index=False)
    sequences={'normal_recupera':[(0,True,True,True,False)]*8,
        'baixoSOC_recupera':[(0,True,True,True,False)]*3+[(1,True,True,True,False),(2,True,True,True,False)]+[(0,True,True,True,False)]*4,
        'falha_sensor':[(0,True,True,True,False)]*3+[(0,True,False,True,False)]+[(0,True,True,True,False)]*3+[(0,True,True,True,True)]*3,
        'contator_colado':[(0,True,True,True,False)]*3+[(0,True,True,False,False)]+[(0,True,True,True,False)]*4,
        'BMS_inibe':[(0,True,True,True,False)]*3+[(0,False,True,True,False)]+[(0,True,True,True,False)]*4,
        'oscilacao_estagio':[(v,True,True,True,False) for v in [0,1,0,1,0,1,0,1,0,1]]}
    history=[]
    for name,seq in sequences.items():
        ctrl=GerenciadorCargas(e['recovery_hold_s_test'])
        for i,(stage,bms,telemetry,actuator,reset) in enumerate(seq):
            r=ctrl.step(stage,10,bms_allow=bms,telemetry_valid=telemetry,actuator_ok=actuator,reset=reset)
            history.append({'scenario':name,'time_end_s':(i+1)*10,'requested_stage':stage,'bms_allow':bms,'telemetry_valid':telemetry,'actuator_ok':actuator,'reset':reset,**r})
    pd.DataFrame(history).to_csv(out/'gerenciamento_falhas.csv',index=False)
    parts=c['development']['layout_equipment']['A_fixa']
    structural=[]
    for part in parts:
        # Water follows the inventory: clean100L, grey/cassette initially0.
        water_cases={'tanque_limpa':[10,50,100],'tanque_cinza':[0,40,70],'cassete':[0,10,20]}.get(part['id'],[0])
        for water,accel,offset,thick in itertools.product(water_cases,m['accelerations_g'],m['in_plane_eccentricity_m'],m['plate_thickness_m']):
            mass=part['mass_kg']+water
            force=mass*m['gravity_m_s2']*accel
            r=grupo_parafusos([force,0],force*offset,m['bolt_group_xy_m']);maxshear=max(r['bolt_shear_n'])
            shear_stress=maxshear/m['conservative_thread_area_m2'];bearing=maxshear/(m['bolt_diameter_m']*thick)
            structural.append({'component':part['id'],'water_mass_kg':water,'loaded_mass_kg':mass,'acceleration_g_assumed':accel,
                'in_plane_offset_m':offset,'plate_thickness_m':thick,'force_n':force,'moment_nm':force*offset,
                'max_bolt_shear_n':maxshear,'bolt_von_mises_pa':np.sqrt(3)*shear_stress,'plate_bearing_pa':bearing,
                'bolt_utilization':np.sqrt(3)*shear_stress*m['safety_factor']/m['assumed_bolt_yield_pa'],
                'plate_utilization':bearing*m['safety_factor']/m['assumed_plate_yield_pa'],
                'force_residual_n':max(abs(x) for x in r['force_residual_n']),'moment_residual_nm':r['moment_residual_nm'],
                'oem_anchorage_verified':False})
    pd.DataFrame(structural).to_csv(out/'fixacoes_grupos_parafusos.csv',index=False)
    result={'electrical_cases':len(wires),'fault_cases':len(faults),'simultaneity_cases':len(powers),
        'mounting_cases':len(structural),'control_histories':len(sequences),
        'max_circuit_energy_residual_w':float(wires.energy_residual_w.abs().max()),
        'current_range_a':[float(wires.current_a.min()),float(wires.current_a.max())],
        'prospective_fault_range_a':[min(x['prospective_a'] for x in faults),max(x['prospective_a'] for x in faults)],
        'fault_cases_exceeding_20ka':sum(not x['breaking_screen_pass'] for x in faults),
        'main_fuse_provisional':e['fuse_main'],'mppt_fuse_provisional':e['fuse_mppt'],
        'hardware_control_demonstrated':False,'soc_thresholds':e['soc_thresholds'],'coordination_demonstrated':False,
        'integration_new_dependency':'Selecionado provisoriamente MultiPlus-II GX comGX/visor/BMS-CAN integrados;sem central própria ou gateway externo. CANtipoA/DVCC/firmware epartidas devem ser configurados/ensaiados;hardware não implementado.',
        'physical_installation_authorized':False,
        'mounting_limits':'4parafusos iguais por grupo;modelo genérico,sem OEMsuporte/fadiga/prying/tração/arrancamento. Água10/50/100Llimpa,0/40/70Lcinza,0/10/20Lcassete em verificações locais separadas;não soma conteúdos para massa global.',
        'electrical_limits':['Resistência interna varrida é hipótese;BMS não limita a corrente prospectiva por premissa.',
            'Não transferir correntes/PE ou retorno de potência para sistemaHV OEM.',
            'Cobre90°C/manual não comprova ampacidade instalada;I²t real e curvas seletividade faltam.',
            'Cenários de potência não validam partidas desconhecidas;gerenciamento lógico não está instalado.',
            'Fusível200A é recomendação do inversor,não corrente admissível de bateria/terminais.']}
    (out/'resumo.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
