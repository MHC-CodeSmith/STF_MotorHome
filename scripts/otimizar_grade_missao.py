"""I29: busca exaustiva FINITA de políticas, com replay conservativo completo.

Painel portátil tem ângulo constante por parada. Mínimo1kW é hipotético.
Melhor política na grade não equivale a ótimo global ou missão física.
"""
import copy
import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from motorhome.cenarios import carregar_configuracao, diretorio_entregas
from motorhome.desenvolvimento import consumir_agua
from motorhome.reconciliacao import consumo_plano, simular_missao
from motorhome.solar import simular_dia


def main():
    out=diretorio_entregas(ROOT)/'otimizacao_grade';out.mkdir(parents=True,exist_ok=True)
    c=carregar_configuracao(ROOT)
    p={k:v['value'] for k,v in c['parameters'].items()};g=c['development']['mission_grid']
    mass=p['assembled_typical_mass_kg'];base=yaml.safe_load((ROOT/'config/solar_proposta.yaml').read_text())
    base['scenario'].update(date=p['reference_day'],latitude_deg=p['latitude_deg'],longitude_deg=p['longitude_deg'],
         altitude_m=p['altitude_m'],ambient_temperature_c=p['ambient_c'],wind_speed_m_s=p['wind_m_s'],relative_humidity_percent=p['rh_percent'])
    base['module'].update(p_stc_w=p['roof_power_48v_study_wp'],gamma_pdc_per_k=p['pv_gamma'])
    base['array'].update(module_counts=[1],tilt_deg=0,azimuth_deg=0,albedo=p['pv_albedo'])
    base['assumptions'].update(converter_efficiency=1,other_losses_fraction=p['pv_other_loss'],
                             faiman_u0_w_m2k=p['pv_faiman_u0'],faiman_u1_w_s_m3k=p['pv_faiman_u1'])
    data=simular_dia(base,15);power=data['terminal_assumed_1_modules_w'].to_numpy()
    roof=(power[:-1]+power[1:])/2000
    hours=np.arange(96)*.25+.125;port_curves=[]
    for tilt,az in itertools.product(range(0,76,15),[0,90,180,270]):
        candidate=copy.deepcopy(base);candidate['array'].update(tilt_deg=tilt,azimuth_deg=az)
        candidate['module'].update(p_stc_w=p['portable_wp'],gamma_pdc_per_k=p['portable_gamma'])
        power=simular_dia(candidate,15)['terminal_assumed_1_modules_w'].to_numpy()
        port_curves.append((tilt,az,(power[:-1]+power[1:])/2000))
    ac=sum(x['energy_ac_or_dc_kwh_day']['base'] for x in c['loads'] if x['side']=='AC')
    dc=sum(x['energy_ac_or_dc_kwh_day']['base'] for x in c['loads'] if x['side']=='DC')
    service_day=ac/p['eta_inverter']+dc/p['eta_lv']+p['inverter_idle_w']*24/1000
    results=[];best={}; profiles={}
    for start,duration in itertools.product(g['start_hours'],g['driving_window_hours']):
        drive=(hours-start)%24<duration
        since_park=(hours-(start+duration))%24
        usable=(~drive)&(since_park>=p['pv_setup_h'])&(since_park<24-duration-p['pv_teardown_h'])
        tilt,az,curve=max(port_curves,key=lambda item:float((item[2]*usable).sum()))
        port=curve*usable
        for speed,reserve,aux_w in itertools.product(g['speed_kmh'],g['reserves'],g['auxiliary_sweep_w']):
            consumption=consumo_plano(speed,mass,p['cd_range'][1],p['area_m2'],p['crr_range'][1],p['rho_range'][1],p['eta_traction_range'][1],aux_traction_kw=aux_w/1000)
            r=simular_missao(roof.tolist(),port.tolist(),drive.tolist(),speed_kmh=speed,kwh_km=consumption['kwh_km'],
                service_kwh_day=service_day,traction_capacity_kwh=p['traction_usable_kwh'],service_capacity_kwh=14.4,
                reserve_traction=reserve[0],reserve_service=reserve[1],mode=g['mode'],min_dc_kw=g['hypothetical_min_dc_kw'],
                max_days=g['max_days'],eta_dc=p['eta_dc'])
            profile=r.pop('trace');r.pop('daily')
            row={'auxiliary_traction_w_assumed':aux_w,'start_h':start,'window_h':duration,'speed_kmh':speed,'reserve_traction':reserve[0],'reserve_service':reserve[1],
                 'portable_tilt_deg':tilt,'portable_azimuth_deg':az,'solar_kwh_planned_day':float((roof+port).sum()*.25),**r}
            results.append(row);key=f'{reserve}_aux{aux_w}W'
            if r['status']=='chegada_condicional' and (key not in best or r['elapsed_days']<best[key]['elapsed_days']):
                best[key]=row;profiles[key]=profile
        print(json.dumps({'start':start,'duration':duration,'cases_done':len(results),'best_days':{k:r['elapsed_days'] for k,r in best.items()}}),flush=True)
    pd.DataFrame([{k:v for k,v in row.items() if k!='totals'} for row in results]).to_csv(out/'grade_1008_cenarios.csv',index=False)
    # Sanitária integrada ao melhor replay: fonte de água/descarte adequado
    # disponível a cada parada escolhida é hipótese explícita, não mapa real.
    sanitation=[]
    for key,profile in profiles.items():
        pd.DataFrame(profile).to_csv(out/f'melhor_reservas{key}.csv.gz',index=False,compression='gzip')
        days=int(np.ceil(best[key]['elapsed_days']));state={'clean_l':100.,'grey_l':0.,'black_l':0.}
        supplied=disposed=0.
        for day in range(1,days+1):
            for event,amount,black in [('base',60.,.1)]+([('lavagem',68.8,0.)] if day%7==0 else []):
                need_stop=False;refill=drain=0.
                try: new=consumir_agua(state,amount,black)
                except ValueError:
                    need_stop=True;drain=state['grey_l']+state['black_l'];refill=100-state['clean_l']
                    supplied+=refill;disposed+=drain;state={'clean_l':100.,'grey_l':0.,'black_l':0.}
                    new=consumir_agua(state,amount,black)
                state={k:new[k] for k in ['clean_l','grey_l','black_l']}
                sanitation.append({'reserves':key,'day':day,'event':event,'scheduled_stop_h':(best[key]['start_h']+best[key]['window_h'])%24,
                    'stop_needed':need_stop,'duration_h_assumed':.25 if need_stop else 0,'refill_l':refill,'disposal_l':drain,
                    **state,'balance_residual_l':100+supplied-disposed-sum(state.values()),'external_electric_kwh':0.,
                    'stop_availability':'hipotese_sem_fontes_geograficas','changes_driving_hours':False})
    pd.DataFrame(sanitation).to_csv(out/'sanitaria_melhores_replays.csv',index=False)
    summary={'scope':g['note'],'cases':len(results),'mass_kg':mass,'service_kwh_day':service_day,
             'best_by_reserve':best,'min_power_kw_is_hypothesis':True,'global_optimality_proven':False,
             'portable_angle_held_per_stop':True,'water_stop_availability_proven':False,
             'water_stop_note':'15min/evento hipotético dentro da janela estacionária; montagem solar não deslocada nesta idealização.',
             'physical_mission_demonstrated':False,'energy_residual_max_kwh':max(abs(r['energy_residual_kwh']) for r in results)}
    (out/'resumo.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')


if __name__=='__main__':main()
