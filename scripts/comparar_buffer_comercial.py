"""Buffer dedicado comercial como comparação, sem instalá-lo ou criar energia inicial."""
import itertools
import json
import sys
from pathlib import Path

import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from motorhome.cenarios import carregar_configuracao, diretorio_entregas
from motorhome.reconciliacao import consumo_plano, simular_missao


def main():
    c=carregar_configuracao(ROOT);p={k:v['value'] for k,v in c['parameters'].items()};out=diretorio_entregas(ROOT)/'buffer_comercial';out.mkdir(exist_ok=True)
    service=sum(x['energy_ac_or_dc_kwh_day']['base']/(p['eta_inverter'] if x['side']=='AC' else p['eta_lv']) for x in c['loads'])+p['inverter_idle_w']*24/1000
    rows=[]
    for policy,speed,reserve,minimum,use_buffer in itertools.product(['fixo_08_16','alternativo_00_08'],[40,80],p['trip_reserve_pairs'],[1,3],[False,True]):
        solar=pd.read_csv(diretorio_entregas(ROOT)/f'solar/solar_{policy}.csv')
        mass=p['assembled_typical_mass_kg']+(p['module_service_mass_kg'] if use_buffer else 0)
        credit=p['module_service_kwh']*p['module_service_dod'] if use_buffer else 0
        rate=consumo_plano(speed,mass,p['cd_range'][1],p['area_m2'],p['crr_range'][1],p['rho_range'][1],p['eta_traction_range'][1],aux_traction_kw=p['traction_aux_assumed_w']/1000)['kwh_km']
        r=simular_missao(solar.roof_kw.to_list(),solar.portable_kw.to_list(),solar.planned_driving.to_list(),speed_kmh=speed,kwh_km=rate,service_kwh_day=service,traction_capacity_kwh=p['traction_usable_kwh'],service_capacity_kwh=p['service_modules_provisional']*p['module_service_kwh'],reserve_traction=reserve[0],reserve_service=reserve[1],mode='buffer_hipotese' if use_buffer else 'direta_hipotese',min_dc_kw=minimum,eta_dc=p['eta_dc'],eta_service=p['eta_service_charge'],eta_buffer=p['eta_buffer'],buffer_capacity_kwh=credit)
        r.pop('trace');daily=r.pop('daily')
        rows.append({'policy':policy,'speed_kmh':speed,'reserve_traction':reserve[0],'reserve_service':reserve[1],
            'minimum_dc_kw_hypothetical':minimum,'buffer_module':p['service_module_model'] if use_buffer else None,
            'buffer_module_count':int(use_buffer),'mass_lower_bound_kg':mass,'supports_cabling_mass_unknown':use_buffer,
            'buffer_pv_credit_capacity_kwh':credit,'buffer_initial_pv_credit_kwh':0,'buffer_constant_unavailable_reserve_kwh':p['module_service_kwh']-credit if use_buffer else 0,
            'buffer_price_unknown':use_buffer,'max_daily_driving_h':max(x['driving_h'] for x in daily),**r})
    (out/'comparacao.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
    result={'cases':len(rows),'buffer_installed':False,'buffer_candidate_source':'parameters.service_module_model/module_service_kwh/module_service_dod/module_service_mass_kg',
        'dedicated_buffer_does_not_use_service_bank':True,'physical_interface_demonstrated':False,
        'max_energy_residual_kwh':max(abs(x['energy_residual_kwh']) for x in rows),
        'limits':['Módulo comercial usado como candidato dedicado de estudo;aplicação móvel/BMS/cargaDC e potência não comprovados.',
            'Estado buffer representa créditoFV acima da reserva mínima constante,não pack comzeroV. Crédito inicia0;reserva constante não alimenta tração.',
            'Massa adicional inclui módulo39.7kg;suportes,conversores,proteções,cabos e custos extras são desconhecidos. Massa é limite inferior.',
            'Nenhum armazenamento extra integra CAD/BOMbase ou aquisição;min1/3kW são hipóteses,sem compatibilidadeOEM inferida.']}
    (out/'resumo.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
