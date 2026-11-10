"""Propaga caixa de incertezas e comparaDCdireta/buffer sem transferência entre bancos."""
import itertools
import json
import sys
from pathlib import Path

import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from motorhome.cenarios import carregar_configuracao, diretorio_entregas
from motorhome.reconciliacao import consumo_plano, passo_solar, simular_missao


def main():
    c=carregar_configuracao(ROOT);p={k:v['value'] for k,v in c['parameters'].items()}
    out=diretorio_entregas(ROOT)/'sensibilidades';out.mkdir(exist_ok=True)
    rows=[]
    for mass,speed,cd,crr,eta,rho,area in itertools.product([p['assembled_typical_mass_kg'],p['oem_pbt_kg']],[40,80],p['cd_range'],p['crr_range'],p['eta_traction_range'],p['rho_range'],p['area_multiplier_range']):
        r=consumo_plano(speed,mass,cd,p['area_m2']*area,crr,rho,eta,aux_traction_kw=p['traction_aux_assumed_w']/1000)
        rows.append({'mass_kg':mass,'speed_kmh':speed,'cd_assumed':cd,'crr_assumed':crr,'eta_assumed':eta,'rho_kg_m3':rho,'area_factor':area,**r})
    table=pd.DataFrame(rows);table.to_csv(out/'tracao_972_caixa_parametros.csv',index=False)
    envelope=table.groupby(['mass_kg','speed_kmh']).kwh_km.agg(['min','max']).reset_index();envelope.to_csv(out/'envelope_40_80.csv',index=False)
    ac=sum(x['energy_ac_or_dc_kwh_day']['base'] for x in c['loads'] if x['side']=='AC');dc=sum(x['energy_ac_or_dc_kwh_day']['base'] for x in c['loads'] if x['side']=='DC')
    service=ac/p['eta_inverter']+dc/p['eta_lv']+p['inverter_idle_w']*24/1000
    capacity=p['service_modules_provisional']*p['module_service_kwh'];missions=[];comparison=[]
    for policy in ['fixo_08_16','alternativo_00_08']:
        solar=pd.read_csv(diretorio_entregas(ROOT)/f'solar/solar_{policy}.csv');rf=solar.roof_kw.to_list();port=solar.portable_kw.to_list();drive=solar.planned_driving.to_list();dt=24/len(rf)
        # Pure traction-input experiment, not an assertion that services
        # receive their daily energy for free. Full missions below track both.
        for minimum,bufcap in itertools.product(p['dc_min_sweep_kw'],p['buffer_study_kwh']):
            buffer=0.;totals=dict.fromkeys(['pv_kwh','traction_kwh','loss_kwh','cut_kwh'],0.)
            for a,b,moving in zip(rf,port,drive,strict=True):
                energy=(a+(0 if moving else b))*dt
                step=passo_solar(energy,0,not moving,p['eta_dc'],minimum,dt,hipotetico=True,buffer_kwh=buffer,buffer_capacidade_kwh=bufcap,eficiencia_buffer=p['eta_buffer'])
                buffer=step['buffer_final_kwh'];totals['pv_kwh']+=energy;totals['traction_kwh']+=step['tracao_kwh'];totals['loss_kwh']+=step['perdas_kwh'];totals['cut_kwh']+=step['cortada_kwh']
            residual=totals['pv_kwh']-totals['traction_kwh']-totals['loss_kwh']-totals['cut_kwh']-buffer
            comparison.append({'policy':policy,'minimum_dc_kw_hypothetical':minimum,'buffer_capacity_kwh':bufcap,'buffer_initial_kwh':0,'buffer_final_kwh':buffer,'services_included':False,'energy_residual_kwh':residual,**totals})
        for mass,speed,reserve,corner in itertools.product([p['assembled_typical_mass_kg'],p['oem_pbt_kg']],[40,80],p['trip_reserve_pairs'],['favoravel','central','desfavoravel']):
            i={'favoravel':0,'central':1,'desfavoravel':2}[corner];j=2-i
            rate=consumo_plano(speed,mass,p['cd_range'][i],p['area_m2']*p['area_multiplier_range'][i],p['crr_range'][i],p['rho_range'][i],p['eta_traction_range'][j],aux_traction_kw=p['traction_aux_assumed_w']/1000)['kwh_km']
            r=simular_missao(rf,port,drive,speed_kmh=speed,kwh_km=rate,service_kwh_day=service,traction_capacity_kwh=p['traction_usable_kwh'],service_capacity_kwh=capacity,reserve_traction=reserve[0],reserve_service=reserve[1],mode='direta_hipotese',min_dc_kw=1,eta_dc=p['eta_dc'],eta_service=p['eta_service_charge'])
            trace=r.pop('trace');daily=r.pop('daily');maxdrive=max(x['driving_h'] for x in daily)
            if maxdrive>8+1e-8 or abs(r['energy_residual_kwh'])>1e-6:raise ValueError('Missão viola conservação/8h')
            missions.append({'policy':policy,'mass_kg':mass,'speed_kmh':speed,'reserve_traction':reserve[0],'reserve_service':reserve[1],'corner':corner,'kwh_km':rate,'max_daily_driving_h':maxdrive,**r})
            if mass==p['assembled_typical_mass_kg'] and speed==40 and reserve==p['trip_reserve_pairs'][0] and policy=='alternativo_00_08':
                pd.DataFrame(trace).to_csv(out/f'perfil_extremo_{corner}.csv.gz',index=False,compression='gzip')
        # One coherent fair comparison: same initial states, mass, weather,
        # schedule, services, reserves and allPV accounting in each alternative.
        for speed,reserve,allocation,bufcap in itertools.product([40,80],p['trip_reserve_pairs'],['A','B','flexivel'],p['buffer_study_kwh']):
            rate=consumo_plano(speed,p['assembled_typical_mass_kg'],p['cd_range'][1],p['area_m2'],p['crr_range'][1],p['rho_range'][1],p['eta_traction_range'][1],aux_traction_kw=p['traction_aux_assumed_w']/1000)['kwh_km']
            r=simular_missao(rf,port,drive,speed_kmh=speed,kwh_km=rate,service_kwh_day=service,traction_capacity_kwh=p['traction_usable_kwh'],service_capacity_kwh=capacity,reserve_traction=reserve[0],reserve_service=reserve[1],mode='buffer_hipotese' if bufcap else 'direta_hipotese',allocation=allocation,min_dc_kw=1,eta_dc=p['eta_dc'],eta_service=p['eta_service_charge'],eta_buffer=p['eta_buffer'],buffer_capacity_kwh=bufcap)
            trace=r.pop('trace');daily=r.pop('daily')
            if abs(r['energy_residual_kwh'])>1e-6:raise ValueError('Buffer viola conservação')
            missions.append({'policy':policy,'mass_kg':p['assembled_typical_mass_kg'],'speed_kmh':speed,'reserve_traction':reserve[0],'reserve_service':reserve[1],'corner':'comparacao_buffer_alocacao','kwh_km':rate,'buffer_capacity_kwh':bufcap,'buffer_initial_kwh':0,'max_daily_driving_h':max(x['driving_h'] for x in daily),**r})
    pd.DataFrame(comparison).to_csv(out/'dc_direta_buffer_36_ensaios.csv',index=False)
    (out/'missoes_120_comparacoes.json').write_text(json.dumps(missions,indent=2,ensure_ascii=False)+'\n')
    result={'execution':c.get('_execution'),'traction_cases':len(rows),'mission_cases':len(missions),'dc_daily_cases':len(comparison),
        'max_energy_residual_kwh':max(abs(x['energy_residual_kwh']) for x in missions+comparison),
        'physical_dc_interface_demonstrated':False,'buffer_installed':False,'envelope_40_80':envelope.to_dict('records'),
        'limits':['Extremos conjuntos de caixa de parâmetros,não intervalo estatístico ou correlações medidas.',
            'Cd0.72 é sensibilidade para CFD equipado não independente,nãoCdOEM.',
            'EnsaiosDCdiários excluem serviços explicitamente;missões completas contabilizam ambos os bancos.',
            'Buffer começa vazio e é dedicado;pesos/custos próprios não incluídos nesta comparação energética isolada.',
            'Qualquer chegada requer interfaceDC/autorização/alocaçãoFV ainda não demonstradas.']}
    (out/'resumo.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
