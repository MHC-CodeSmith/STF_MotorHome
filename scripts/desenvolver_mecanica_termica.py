"""Envelope hipotético0–90, balanço de perdas e sweep térmico OEM não calibrado."""
import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from motorhome.bateria_carga import resolver
from motorhome.reconciliacao import consumo_plano


def main():
    out=ROOT/'entregas/desenvolvimento_2026-11-09/mecanica_termica';out.mkdir(parents=True,exist_ok=True)
    c=yaml.safe_load((ROOT/'config/parametros_globais.yaml').read_text());d=c['development']
    p={k:v['value'] for k,v in c['parameters'].items()}
    geometry=json.loads((ROOT/'entregas/desenvolvimento_2026-11-09/integracao/layouts_massas.json').read_text())
    typ=geometry['layouts']['A_fixa']['nominal']; a=d['performance_envelope']
    cases=[]
    for mass,ratio,gear_eta,mu in itertools.product([typ['mass_kg'],4250],a['gear_ratio'],a['gear_efficiency'],a['tyre_friction_mu']):
        x,h=typ['cg_x_m'],typ['cg_z_m'];L=p['wheelbase_m'];g=9.80665
        # Front wheel drive: front load diminishes during acceleration.
        # Solving a=(mu*(mg*(L-x)/L - m*a*h/L)-R)/m gives adhesion cap.
        def forces(v,mass=mass,ratio=ratio,gear_eta=gear_eta,mu=mu,g=g,L=L,x=x,h=h):
            drag=consumo_plano(max(v*3.6,1e-6),mass,p['cd_range'][1],p['area_m2'],p['crr_range'][1],p['rho_range'][1],p['eta_traction_range'][1])
            resistance=drag['aerodinamica_n']+drag['rolamento_n']
            motor=min(a['peak_torque_nm']*ratio*gear_eta/a['wheel_radius_m'],a['peak_motor_w']*gear_eta/max(v,.001))
            acceleration_limit=(mu*g*(L-x)/L-resistance/mass)/(1+mu*h/L)
            acceleration=min((motor-resistance)/mass,acceleration_limit)
            return max(0.,acceleration),motor,resistance
        def rhs(t,y): return [forces(y[0])[0],y[0]]
        def target(t,y): return y[0]-a['speed_limit_kmh']/3.6
        target.terminal=True;target.direction=1
        r=solve_ivp(rhs,[0,a['max_time_s']],[0,0],events=target,rtol=1e-8,atol=1e-9,max_step=.05,dense_output=True)
        t=float(r.t[-1]);times=np.linspace(0,t,201);ys=r.sol(times)
        case={'mass_kg':mass,'gear_ratio_assumed':ratio,'gear_eta_assumed':gear_eta,'adhesion_mu_assumed':mu,
              'time_to_90_s':t if len(r.t_events[0]) else None,'distance_to_90_m':float(ys[1,-1]),
              'zero_to_100_status':'NAO_ALCANCAVEL_LIMITADOR90','source':'envelope_de_engenharia_nao_curvaOEM'}
        cases.append(case)
        name=f'{mass:.2f}_{ratio}_{gear_eta}_{mu}'
        pd.DataFrame([{'time_s':tt,'speed_kmh':v*3.6,'distance_m':xx,'acceleration_m_s2':forces(v)[0],
                       'motor_torque_envelope_nm':min(a['peak_torque_nm'],a['peak_motor_w']/(max(v,.001)/a['wheel_radius_m']*ratio)),
                       'motor_rpm_assumed_ratio':v/a['wheel_radius_m']*ratio*60/(2*np.pi)}
                      for tt,v,xx in zip(times,ys[0],ys[1])]).to_csv(out/f'aceleracao_{name}.csv',index=False)
    pd.DataFrame(cases).to_csv(out/'I28_envelope_0_90_sensibilidade.csv',index=False)
    losses=[]
    for motor_eta,gear_eta in itertools.product([.85,.90,.95],a['gear_efficiency']):
        wheels=a['peak_motor_w']*gear_eta
        electric=a['peak_motor_w']/motor_eta
        motor_loss=electric-a['peak_motor_w'];gear_loss=a['peak_motor_w']-wheels
        losses.append({'motor_eta_assumed':motor_eta,'gear_eta_assumed':gear_eta,
                       'motor_mechanical_w':a['peak_motor_w'],'wheel_w':wheels,'electrical_w':electric,
                       'motor_inverter_heat_w':motor_loss,'reducer_heat_w':gear_loss,
                       'energy_residual_w':electric-wheels-motor_loss-gear_loss,
                       'oil_grade':None,'oil_volume_l':None,'fluid_flow_l_min':None})
    pd.DataFrame(losses).to_csv(out/'I10_I12_balanco_perdas.csv',index=False)
    thermal=yaml.safe_load((ROOT/'config/bateria_termica_proposta.yaml').read_text())
    base=thermal['assumed']|thermal['official'];s=d['thermal_sweep'];rows=[]
    for power,mass,ua,cooler in itertools.product(s['powers_w'],s['mass_kg'],s['battery_coolant_ua_w_k'],s['cooler_ambient_ua_w_k']):
        r=resolver(base|{'battery_mass_kg':mass,'battery_coolant_ua_w_k':ua,'cooler_ambient_ua_w_k':cooler},power)
        r.pop('history')
        rows.append({'power_w':power,'pack_mass_assumed_kg':mass,'battery_coolant_ua_w_k':ua,
                     'cooler_ambient_ua_w_k':cooler,**r})
    pd.DataFrame(rows).to_csv(out/'I34_54sensibilidades.csv',index=False)
    (out/'resumo.json').write_text(json.dumps({'I28_cases':len(cases),'I34_cases':len(rows),
        'I28_note':a['note'],'thermal_note':s['note'],'nominal_geometry_source':'layoutA integração, CGbase hipotético',
        'motor_maps_oem_available':False,'mechanical_peak_continuous_proven':False,
        'oem_lubrication_identified':False,'physical_validation':False},indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'acceleration_cases':len(cases),'thermal_cases':len(rows)}))


if __name__=='__main__': main()
