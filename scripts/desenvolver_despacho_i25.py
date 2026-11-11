"""I25: carga estacionária seguida de condução, só energia FV produzida no dia.

Ótimo somente da alocação MILP por janela; melhor partida na grade finita.
Sem prova OEM, sem ótimo global de políticas com múltiplas paradas.
"""
import copy
import hashlib
import itertools
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from motorhome.cenarios import carregar_configuracao, diretorio_entregas
from motorhome.despacho_diario import alocar_dia
from motorhome.reconciliacao import consumo_plano
from motorhome.solar import simular_dia


def main():
    out=diretorio_entregas(ROOT)/'despacho_i25';out.mkdir(parents=True,exist_ok=True)
    config_path=ROOT/'config/parametros_globais.yaml';c=carregar_configuracao(ROOT)
    p={k:v['value'] for k,v in c['parameters'].items()};g=c['development']['daily_dispatch']
    base=yaml.safe_load((ROOT/'config/solar_proposta.yaml').read_text())
    base['scenario'].update(date=p['reference_day'],latitude_deg=p['latitude_deg'],longitude_deg=p['longitude_deg'],
        altitude_m=p['altitude_m'],ambient_temperature_c=p['ambient_c'],wind_speed_m_s=p['wind_m_s'],relative_humidity_percent=p['rh_percent'])
    base['array'].update(module_counts=[1],tilt_deg=0,azimuth_deg=0,albedo=p['pv_albedo'])
    base['assumptions'].update(converter_efficiency=1,other_losses_fraction=p['pv_other_loss'],
        faiman_u0_w_m2k=p['pv_faiman_u0'],faiman_u1_w_s_m3k=p['pv_faiman_u1'])
    ac=sum(x['energy_ac_or_dc_kwh_day']['base'] for x in c['loads'] if x['side']=='AC')
    dc=sum(x['energy_ac_or_dc_kwh_day']['base'] for x in c['loads'] if x['side']=='DC')
    service_day=ac/p['eta_inverter']+dc/p['eta_lv']+p['inverter_idle_w']*24/1000
    departures=np.arange(g['departure_start_h'],g['departure_end_h']+.001,g['departure_step_h'])
    candidates=[];curves=[];best_profiles={};case_count=0
    for step in g['step_minutes']:
        dt=step/60;n=1440//step;hours=(np.arange(n)+.5)*dt
        base['module'].update(p_stc_w=p['roof_power_48v_study_wp'],gamma_pdc_per_k=p['pv_gamma'])
        def power(cfg,step=step):
            x=simular_dia(cfg,step)['terminal_assumed_1_modules_w'].to_numpy()
            return (x[:-1]+x[1:])/2000
        roof=power(base);port_curves=[]
        for tilt,az in itertools.product(g['portable_tilt_deg'],g['portable_azimuth_deg']):
            cfg=copy.deepcopy(base);cfg['array'].update(tilt_deg=tilt,azimuth_deg=az)
            cfg['module'].update(p_stc_w=p['portable_wp'],gamma_pdc_per_k=p['portable_gamma'])
            port_curves.append((tilt,az,power(cfg)))
        best={}
        for departure in departures:
            parked=hours<departure
            deployed=(hours>=p['pv_setup_h'])&(hours<departure-p['pv_teardown_h'])
            tilt,az,port=max(port_curves,key=lambda a:float((a[2]*deployed).sum()))
            solar=roof+port*deployed
            for services,minimum in itertools.product([False,True],g['hypothetical_dc_min_input_kw']):
                r=alocar_dia(solar,parked,dt,minimo_dc_kw=minimum,eta_dc=p['eta_dc'],
                    eta_servicos=p['eta_service_charge'],consumo_servicos_kwh=service_day if services else 0,
                    capacidade_servicos_kwh=g['service_capacity_kwh'],
                    energia_servicos_inicial_kwh=g['service_capacity_kwh']*g['service_initial_fraction'],
                    capacidade_credito_tracao_kwh=(1-g['traction_initial_soc_baseline'])*p['traction_usable_kwh'])
                case_count+=1
                if r['status']!='otimo_para_janela_discreta':continue
                key=(services,minimum)
                for speed in (range(10,91) if step==15 else [40,80]):
                    consumption=consumo_plano(speed,p['assembled_typical_mass_kg'],p['cd_range'][1],p['area_m2'],
                        p['crr_range'][1],p['rho_range'][1],p['eta_traction_range'][1],aux_traction_kw=p['traction_aux_assumed_w']/1000)
                    energy=r['credito_solar_tracao_kwh'];duration=min(24-departure,energy/consumption['bateria_kw'])
                    used=duration*consumption['bateria_kw'];distance=duration*speed
                    row={'step_min':step,'services_cyclic':services,'hypothetical_dc_min_input_kw':minimum,
                         'speed_kmh':speed,'departure_h':float(departure),'distance_km':distance,'driving_h':duration,
                         'solar_credit_initial_kwh':0.,'solar_hv_received_kwh':energy,'traction_used_kwh':used,
                         'solar_credit_final_kwh':energy-used,'portable_tilt_deg':tilt,'portable_azimuth_deg':az,
                         'service_day_kwh':service_day if services else 0,'service_balance_max_kwh':r['residuo_servicos_kwh'],
                         'pv_generated_kwh':float(solar.sum()*dt),'milp_gap':r['gap_milp'],
                         'physical_interface_demonstrated':False}
                    if step==15 and speed in [40,80]:candidates.append(row)
                    fullkey=(*key,speed)
                    if fullkey not in best or distance>best[fullkey]['distance_km']+1e-9:
                        best[fullkey]=row
                        if speed in [40,80]:
                            moving_h=np.clip(np.minimum((np.arange(n)+1)*dt,departure+duration)-np.maximum(np.arange(n)*dt,departure),0,dt)
                            use=moving_h*consumption['bateria_kw'];hv=r['fv_tracao_kwh']*p['eta_dc']
                            credit=np.r_[0,np.cumsum(hv-use)]
                            profile=pd.DataFrame({'start_h':np.arange(n)*dt,'parked_for_charge':parked,
                                'portable_deployed':deployed,'pv_kw':solar,'fv_traction_kwh':r['fv_tracao_kwh'],
                                'fv_services_kwh':r['fv_servicos_kwh'],'fv_curtailed_kwh':r['fv_cortada_kwh'],
                                'hv_received_kwh':hv,'driving_h':moving_h,'traction_used_kwh':use,
                                'solar_credit_start_kwh':credit[:-1],'solar_credit_end_kwh':credit[1:],
                                'service_start_kwh':r['energia_servicos_kwh'][:-1],'service_end_kwh':r['energia_servicos_kwh'][1:]})
                            best_profiles[(step,*fullkey)]=profile
        curves.extend(best.values())
        print(json.dumps({'step_min':step,'milp_cases_accumulated':case_count,'best_40_80':[v for k,v in best.items() if k[-1] in [40,80]]}),flush=True)
    for key,profile in best_profiles.items():
        step,services,minimum,speed=key
        profile.to_csv(out/f'perfil_{step}min_servicos{int(services)}_min{minimum}kW_{speed}kmh.csv',index=False)
    pd.DataFrame(curves).to_csv(out/'melhores_por_velocidade.csv',index=False)
    pd.DataFrame(candidates).to_csv(out/'partidas_comparadas_40_80.csv',index=False)
    finest=[r for r in curves if r['step_min']==min(g['step_minutes'])]
    convergence=[]
    for r in finest:
        key=['services_cyclic','hypothetical_dc_min_input_kw','speed_kmh']
        comparisons=[x for x in curves if all(x[k]==r[k] for k in key)]
        convergence.append({**{k:r[k] for k in key},'fine_distance_km':r['distance_km'],
            **{f'delta_{x["step_min"]}min_km':x['distance_km']-r['distance_km'] for x in comparisons}})
    pd.DataFrame(convergence).to_csv(out/'sensibilidade_passo.csv',index=False)
    fig,ax=plt.subplots(figsize=(8,5),layout='constrained')
    for services in [False,True]:
        rows=[r for r in curves if r['step_min']==15 and r['services_cyclic']==services and r['hypothetical_dc_min_input_kw']==1]
        ax.plot([r['speed_kmh'] for r in rows],[r['distance_km'] for r in rows],label='Com serviços cíclicos' if services else 'Só tração')
    ax.set(xlabel='Velocidade constante [km/h]',ylabel='Distância solar do próprio dia [km]',title='I25 — despacho condicional; mínimo de entrada DC hipotético 1 kW')
    ax.legend();ax.grid(alpha=.25);fig.savefig(out/'autonomia_temporal.png',dpi=160);plt.close(fig)
    summary={'cases_milp':case_count,'configuration_sha256':hashlib.sha256(config_path.read_bytes()).hexdigest(),
        'best_40_80_finest':finest,'conditional':True,'interface_demonstrated':False,'global_policy_optimum':False,
        'scope':'Melhor partida na grade de30min; uma parada00h-partida e condução posterior até24h. Ângulo fixo escolhido por energia FV da parada. MILP aloca a geração entre circuitos independentes.',
        'service_boundary':'Comparador com Eserviços inicial=final7.2kWh; energia inicial não financia tração. Sem serviços, autonomia refere-se só à propulsão.',
        'charge_boundary':'SOCbase30% não gasto; crédito solar inicia0. Armazenamento é packOEM, não buffer novo. Mínimos0/1/3kW de entrada são hipóteses, não dadosOEM.',
        'limits':['Sem dinâmica de handshake/rampas/reinício; aceitação intraintervalo constante média.',
                  'Alocação FV flexível conceitual, perdas constantes; chaveamento físico não demonstrado.',
                  f'{p["roof_power_48v_study_wp"]}Wp fixos de estudo; meta1540Wp preservada. Portáteis somente parados com montagem/desmontagem.',
                  'Sem limite8h doI29 imposto aoI25. Velocidade constante idealiza urbano/estrada; não ciclo real.',
                  'Controle sem interface tem distância solar de tração0km.']}
    (out/'resumo.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')


if __name__=='__main__':main()
