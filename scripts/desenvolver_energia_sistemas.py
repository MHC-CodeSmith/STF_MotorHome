"""MPPT compartilhado, autonomia diária ótima no modelo plano e missão integrada.

I27 tem demonstração de otimalidade SOMENTE no modelo sem reposição HV,
eficiência constante e horizonte de condução dado (Jensen para P(v) convexa).
I29 continua comparação condicional, não certificado de ótimo global.
"""
import argparse
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
from scipy.optimize import brentq

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from motorhome.reconciliacao import consumo_plano, simular_missao


def power_curve(voltage,vmp,voc,imp,isc):
    """I–V interpolada por trechos: hipótese reduzida, NÃO curva fabricante."""
    return voltage*np.interp(voltage,[0,vmp,voc],[isc,imp,0],left=isc,right=0)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destino',type=Path,default=ROOT/'entregas/desenvolvimento_2026-11-09/energia_sistemas')
    args=parser.parse_args();out=args.destino;out.mkdir(parents=True,exist_ok=True)
    c=yaml.safe_load((ROOT/'config/parametros_globais.yaml').read_text())
    p={k:v['value'] for k,v in c['parameters'].items()};d=c['development'];s=d['pv_shared_study']
    integration=json.loads((ROOT/'entregas/desenvolvimento_2026-11-09/integracao/layouts_massas.json').read_text())
    mass=integration['layouts']['A_fixa']['nominal']['mass_kg']
    params=[p['cd_range'][1],p['area_m2'],p['crr_range'][1],p['rho_range'][1],p['eta_traction_range'][1]]
    # IV mismatch under independent temperature and irradiance; independent
    # trackers share no battery output with traction. This compares PV harvest.
    shared=[]
    for tr,tp,gr,gp in itertools.product([25,65,85],[25,65,85],[.4,1],[.4,1]):
        vr=s['roof_series']*s['roof_vmp_v']*(1+s['beta_vmp_per_k']*(tr-25))
        or_=s['roof_series']*s['roof_voc_v']*(1+s['beta_voc_per_k']*(tr-25))
        vp=s['portable_series']*s['portable_vmp_v']*(1+s['beta_vmp_per_k']*(tp-25))
        op=s['portable_series']*s['portable_voc_v']*(1+s['beta_voc_per_k']*(tp-25))
        v=np.linspace(s['battery_charge_v']+1,max(or_,op),10001)
        pr=power_curve(v,vr,or_,s['roof_imp_a']*gr,s['roof_isc_a']*gr)
        pp=power_curve(v,vp,op,s['portable_parallel']*s['portable_imp_a']*gp,s['portable_parallel']*s['portable_isc_a']*gp)
        independent=float(pr.max()+pp.max());combined=pr+pp;best=int(np.argmax(combined))
        shared.append({'roof_c':tr,'portable_c':tp,'roof_sun_fraction':gr,'portable_sun_fraction':gp,
                       'separate_trackers_w':independent,'shared_w':float(combined[best]),
                       'shared_voltage_v':float(v[best]),'mismatch_loss_percent':100*(1-float(combined[best])/independent),
                       'model':'IV_por_trechos_estimado_nao_datasheet'})
    pd.DataFrame(shared).to_csv(out/'mppt_compartilhado_mismatch.csv',index=False)
    isc=s['roof_isc_a']+s['portable_parallel']*s['portable_isc_a']
    cold=max(s['roof_series']*s['roof_voc_v'],s['portable_series']*s['portable_voc_v'])*(1+s['beta_voc_per_k']*(s['cold_c']-25))
    electrical={'controller_reference':s['shared_controller_model'],'isc_total_a':isc,'isc_limit_a':s['controller_isc_max_a'],
                'cold_voc_v':cold,'voc_limit_v':s['controller_voc_max_v'],'coefficient_status':'estimado',
                'voltage_current_screen_pass':isc<=s['controller_isc_max_a'] and cold<s['controller_operating_max_v'],
                'approved_topology':False,'rejected_250_60_document_conflict_a':s['documented_isc_values_a'],'low_voltage_190w_to_48v_demonstrated':False,
                'other_checks':['I–V reais/bypass/proteção contra retorno e conexão portátil não demonstrados.',
                                'Saída únicaMPPT não pode alimentar simultaneamente serviços48V eHV.',
                                'Aprovado estudo compartilhado; rastreadores separados apenas comparador.']}
    (out/'mppt_parecer.json').write_text(json.dumps(electrical,indent=2,ensure_ascii=False)+'\n')
    # I25 numerical curve: solar availability is an explicit upper bound.
    solar=pd.read_csv(ROOT/'entregas/etapa_pos_dec061/solar_alternativo_00_08.csv')
    roof=solar.roof_kw.to_numpy();portable=solar.portable_kw.to_numpy();n=len(roof);dt=24/n
    solar_day=float((roof+portable).sum()*dt)
    # Read canonical energy means rather than treating nominal AC capacity as W.
    ac=sum(x['energy_ac_or_dc_kwh_day']['base'] for x in c['loads'] if x['side']=='AC')
    dc=sum(x['energy_ac_or_dc_kwh_day']['base'] for x in c['loads'] if x['side']=='DC')
    service_day=ac/p['eta_inverter']+dc/p['eta_lv']+p['inverter_idle_w']*24/1000
    speeds=[]
    for speed in range(10,91):
        r=consumo_plano(speed,mass,*params,aux_traction_kw=p['traction_aux_assumed_w']/1000)
        speeds.append({'speed_kmh':speed,**r,'solar_only_traction_control_km':0.,
                       'conditional_upper_bound_without_services_km':solar_day*p['eta_dc']/r['kwh_km'],
                       'conditional_upper_bound_after_services_km':max(0,solar_day-service_day/p['eta_service_charge'])*p['eta_dc']/r['kwh_km']})
    pd.DataFrame(speeds).to_csv(out/'I25_I26_autonomia_solar_consumo.csv',index=False)
    fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
    axes[0].plot([r['speed_kmh'] for r in speeds],[r['conditional_upper_bound_after_services_km'] for r in speeds])
    axes[0].set(xlabel='Velocidade [km/h]',ylabel='Limite energético condicional [km]',title='I25 — sem prova de sessãoDC; não autonomia implementável')
    axes[1].plot([r['speed_kmh'] for r in speeds],[r['km_kwh'] for r in speeds])
    axes[1].set(xlabel='Velocidade [km/h]',ylabel='Tração [km/kWh]',title='I26 — massa integrada estimada, pista plana')
    fig.savefig(out/'I25_I26.png',dpi=160);plt.close(fig)
    # Jensen: P(v)=a*v+b*v³, a,b>0. For fixed integral v dt, constant v
    # minimizes energy. Exhausting budget maximizes distance over given H.
    daily=[]
    for soc0,requested_hours in itertools.product([1,.8],[8,12,24,0]):
        hours=requested_hours or 24
        available=(soc0-.3)*p['traction_usable_kwh']
        fun=lambda v,hours=hours,available=available: consumo_plano(v,mass,*params,aux_traction_kw=p['traction_aux_assumed_w']/1000)['bateria_kw']*hours-available
        v=brentq(fun,.0001,90) if fun(90)>0 else 90.
        if requested_hours==0:
            # e(v)=a+b*v²+Paux/v; derivative zero at (Paux/(2b))^(1/3).
            # Select max(v_at_24h, v_energy_min) to meet both time and energy.
            b=.5*params[0]*params[1]*params[3]/(params[4]*1000*3.6**3)
            optimum_energy_speed=(p['traction_aux_assumed_w']/1000/(2*b))**(1/3)
            v=min(90,max(v,optimum_energy_speed))
            hours=available/consumo_plano(v,mass,*params,aux_traction_kw=p['traction_aux_assumed_w']/1000)['bateria_kw']
        r=consumo_plano(v,mass,*params,aux_traction_kw=p['traction_aux_assumed_w']/1000)
        row={'soc_initial':soc0,'soc_final':.3,'driving_horizon_h':hours,'horizon_kind':'optimal_upto24h' if requested_hours==0 else 'fixed',
             'constant_speed_kmh':v,'auxiliary_traction_w_assumed':p['traction_aux_assumed_w'],
             'distance_km':v*hours,'battery_power_kw':r['bateria_kw'],'wheels_power_kw':r['rodas_kw'],
             'energy_used_kwh':r['bateria_kw']*hours,'energy_residual_kwh':available-r['bateria_kw']*hours,
             'optimality_scope':'modelo plano sem reposicaoHV, rendimento constante, auxiliar fixo só em movimento; Jensen+minimo e(v)',
             'safe_operating_schedule_proven':False}
        daily.append(row)
        profile=[{'time_h':t,'speed_kmh':v,'battery_power_kw':r['bateria_kw'],'wheels_power_kw':r['rodas_kw'],
                  'soc_traction':soc0-r['bateria_kw']*t/p['traction_usable_kwh']} for t in np.linspace(0,hours,97)]
        if hours<24:
            profile.append({'time_h':24,'speed_kmh':0.,'battery_power_kw':0.,'wheels_power_kw':0.,'soc_traction':.3})
        pd.DataFrame(profile).to_csv(out/f'I27_SOC{soc0}_{requested_hours or "otimo_ate24"}h.csv',index=False)
    pd.DataFrame(daily).to_csv(out/'I27_autonomia_otima_modelo_sem_HV.csv',index=False)
    # Full15min replays with integrated typical/PBT mass, same two policies,
    # both reserve pairs. Real DC minimum remains null;1kW only comparison.
    missions=[]
    for name in ['fixo_08_16','alternativo_00_08']:
        source=ROOT/f'entregas/etapa_pos_dec061/solar_{name}.csv'
        sol=pd.read_csv(source)
        driving=sol.planned_driving.astype(str).str.lower().eq('true').tolist()
        for m,speed,reserve,mode in itertools.product([mass,4250],[40,80],[(.1,.2),(.2,.3)],['sem_interface','direta_hipotese']):
            kwh_km=consumo_plano(speed,m,*params)['kwh_km']
            r=simular_missao(sol.roof_kw.tolist(),sol.portable_kw.tolist(),driving,
                speed_kmh=speed,kwh_km=kwh_km,service_kwh_day=service_day,
                traction_capacity_kwh=p['traction_usable_kwh'],service_capacity_kwh=14.4,
                reserve_traction=reserve[0],reserve_service=reserve[1],mode=mode,
                min_dc_kw=None if mode=='sem_interface' else 1.,eta_dc=p['eta_dc'])
            profile=r.pop('trace');r.pop('daily')
            ident=f'{name}_{m:.3f}_{speed}_{reserve[0]}_{mode}'
            pd.DataFrame(profile).to_csv(out/f'missao_{ident}.csv.gz',index=False,compression='gzip')
            missions.append(dict(id=ident,mass_kg=m,speed_kmh=speed,reserve_traction=reserve[0],reserve_service=reserve[1],**r))
    (out/'I29_missoes_massas_integradas.json').write_text(json.dumps(missions,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'service_kwh_day':service_day,'mass_kg':mass,'daily':daily,'mission_count':len(missions)},ensure_ascii=False))


if __name__=='__main__': main()
