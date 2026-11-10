"""DiaSãoCarlos21junho: séries coerentes com o cenário resolvido, sem arquivos1350Wp."""
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
from motorhome.solar import simular_dia


def main():
    c=carregar_configuracao(ROOT)
    if '_execution' not in c:raise ValueError('Selecionar MOTORHOME_SCENARIO registrado')
    p={k:v['value'] for k,v in c['parameters'].items()};out=diretorio_entregas(ROOT)/'solar';out.mkdir(exist_ok=True)
    base=yaml.safe_load((ROOT/'config/solar_proposta.yaml').read_text())
    base['scenario'].update(date=p['reference_day'],latitude_deg=p['latitude_deg'],longitude_deg=p['longitude_deg'],altitude_m=p['altitude_m'],ambient_temperature_c=p['ambient_c'],wind_speed_m_s=p['wind_m_s'],relative_humidity_percent=p['rh_percent'])
    base['module'].update(p_stc_w=p['roof_power_48v_study_wp'],gamma_pdc_per_k=p['pv_gamma'])
    base['array'].update(module_counts=[1],tilt_deg=0,azimuth_deg=0,albedo=p['pv_albedo'])
    base['assumptions'].update(converter_efficiency=1,other_losses_fraction=p['pv_other_loss'],faiman_u0_w_m2k=p['pv_faiman_u0'],faiman_u1_w_s_m3k=p['pv_faiman_u1'])
    step=p['time_step_minutes'];data=simular_dia(base,step);power=data.terminal_assumed_1_modules_w.to_numpy();roof=(power[:-1]+power[1:])/2000
    times=data.index[:-1]+pd.Timedelta(minutes=step/2);hours=times.hour+times.minute/60
    curves=[]
    for tilt,az in itertools.product(range(0,76,15),[0,90,180,270]):
        cand=copy.deepcopy(base);cand['module'].update(p_stc_w=p['portable_wp'],gamma_pdc_per_k=p['portable_gamma']);cand['array'].update(tilt_deg=tilt,azimuth_deg=az)
        x=simular_dia(cand,step).terminal_assumed_1_modules_w.to_numpy();curves.append((tilt,az,(x[:-1]+x[1:])/2000))
    policies=[]
    for name,start in [('fixo_08_16',8),('alternativo_00_08',0)]:
        drive=(hours-start)%24<8;since=(hours-(start+8))%24
        usable=(~drive)&(since>=p['pv_setup_h'])&(since<16-p['pv_teardown_h'])
        tilt,az,port=max(curves,key=lambda row:float((row[2]*usable).sum()));port=port*usable
        pd.DataFrame({'time':times.astype(str),'roof_kw':roof,'portable_kw':port,'planned_driving':drive}).to_csv(out/f'solar_{name}.csv',index=False)
        policies.append({'policy':name,'tilt_deg':tilt,'azimuth_deg':az,'roof_kwh_day':float(roof.sum()*step/60),'portable_kwh_day':float(port.sum()*step/60),'portable_only_parked':bool(np.all(port[drive]==0))})
    (out/'resumo.json').write_text(json.dumps({'execution':c['_execution'],'policies':policies,'roof_wp':p['roof_power_48v_study_wp'],'gamma_roof_per_k':p['pv_gamma'],'conversion_attribution':'geração independente de rastreadores;recargaDC e alocação são hipóteses,sem saídaMPPT48V ligada aoHV'},indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(policies,ensure_ascii=False))


if __name__=='__main__':main()
