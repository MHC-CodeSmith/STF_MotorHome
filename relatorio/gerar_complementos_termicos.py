"""Campos do item30 e verificações complementares do parecer P7, sem alterar o cenário."""
import hashlib
import json
import sys
from dataclasses import replace
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml
from scipy.optimize import brentq

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'scripts')]
from fechar_i30_corrente_maxima import _cabo_de_bitola, _corrente_fase

from motorhome.bateria_carga import resolver as bateria
from motorhome.cabo_hv import CondicoesContorno, resolver_estacionario
from motorhome.hidraulica import Circuito, ponto_operacao
from motorhome.radiador_cruzado import efetividade_integral


def main():
    cfg=yaml.safe_load((ROOT/'config/parametros_globais.yaml').read_text())
    m=yaml.safe_load((ROOT/'config/cabos_tracao_proposta.yaml').read_text())['model']
    spec=cfg['development']['cable_hv']
    corrente=_corrente_fase(205000,.95,.9,400)
    out=ROOT/'relatorio/dados_termicos';out.mkdir(exist_ok=True)
    fig,axes=plt.subplots(1,2,figsize=(9,3.6),layout='constrained')
    campos=[]
    for ax,area in zip(axes,[120,185],strict=True):
        cabo=_cabo_de_bitola(next(x for x in spec['bitolas'] if x['area_mm2']==area),m)
        r=resolver_estacionario(cabo,corrente,CondicoesContorno(**spec['contorno_projeto']))
        f=r['campo'];temp=f['temperatura_k']-273.15
        theta=np.r_[f['theta_rad'],f['theta_rad'][0]+2*np.pi]
        rad=f['r_m']*1000
        x=rad[:,None]*np.cos(theta);y=rad[:,None]*np.sin(theta)
        t=np.c_[temp,temp[:,0]]
        pic=ax.contourf(x,y,t,levels=20,cmap='inferno')
        ax.set(aspect='equal',xlabel='x [mm]',ylabel='y [mm]',title=f'{area} mm²: pico contínuo, {temp.max():.1f} °C')
        fig.colorbar(pic,ax=ax,label='Temperatura [°C]')
        np.savez_compressed(out/f'cabo_{area}mm2_pico.npz',r_m=f['r_m'],theta_rad=f['theta_rad'],temperatura_c=temp)
        campos.append({'area_mm2':area,'current_a':corrente,'temperature_max_c':float(temp.max()),'residual_w_m':r['residuo_w_m'],'angular_boundary_uniform':True})
    fig.savefig(ROOT/'relatorio/figuras/i30_campo.png',dpi=170);plt.close(fig)
    h=yaml.safe_load((ROOT/'config/hidraulica_proposta.yaml').read_text());a=h['assumed'];p=h['pump'];curve=np.array(p['curve_l_h_kpa_a'])
    c=Circuito(a['hose_length_m'],a['hose_internal_diameter_m'],a['roughness_m'],a['minor_loss_k'],a['density_kg_m3'],a['dynamic_viscosity_pa_s'],a['component_reference_flow_m3_s'],sum(a['component_drop_pa_at_reference'].values()))
    hydraulic=[]
    for factor in [1,2,3]:
        r=ponto_operacao(replace(c,perda_componentes_referencia_pa=c.perda_componentes_referencia_pa*factor),curve[:,0]/3.6e6,curve[:,1]*1000,curve[:,2],12)
        hydraulic.append({'component_factor':factor,'flow_l_min':r['flow_l_min'],'pressure_pa':r['pump_pressure_pa'],'component_pressure_pa':r['system']['componentes_pa']})
    base=ponto_operacao(c,curve[:,0]/3.6e6,curve[:,1]*1000,curve[:,2],12)
    ch=base['mass_flow_kg_s']*a['cp_j_kgk'];cc=a['air_mass_flow_kg_s']*a['air_cp_j_kgk'];load=205000*(1/.9-1)+base['electric_power_w']
    def inlet(ua):return 25+load/(efetividade_integral(ua/min(ch,cc),min(ch,cc)/max(ch,cc))*min(ch,cc))
    needed=brentq(lambda ua:inlet(ua)-65,100,5000)
    b=yaml.safe_load((ROOT/'config/bateria_termica_proposta.yaml').read_text());base_b=b['assumed']|b['official'];cases=[]
    for start in [25,35]:
        case=base_b|{'battery_mass_kg':500,'resistance_ref_ohm':.12,'pack_entropy_v_k':.02,'battery_coolant_ua_w_k':125,'cooler_ambient_ua_w_k':250,'initial_battery_k':start+273.15,'initial_coolant_k':start+273.15}
        r=bateria(case,80000);hist=r.pop('history');cases.append({'initial_c':start,**r,'maximum_internal_heat_w':max(x['ohmic_w']+x['reversible_w'] for x in hist)})
    reducer_loss=205000*(1-.97)
    combined_load=load+reducer_loss
    eff=efetividade_integral(a['radiator_ua_w_k']/min(ch,cc),min(ch,cc)/max(ch,cc))
    extra={'reducer_loss_w':reducer_loss,'total_heat_w':combined_load,'inlet_at_ua1000_c':25+combined_load/(eff*min(ch,cc)),'ua_for_65c_w_k':brentq(lambda ua:25+combined_load/(efetividade_integral(ua/min(ch,cc),min(ch,cc)/max(ch,cc))*min(ch,cc))-65,100,10000)}
    sweep_path=ROOT/'entregas/integrado_maxeon1560/mecanica_termica/I34_sensibilidades.csv'
    sweep=pd.read_csv(sweep_path)
    fixed=sweep[(sweep.pack_mass_assumed_kg==500)&(sweep.battery_coolant_ua_w_k==125)&(sweep.cooler_ambient_ua_w_k==250)]
    fig,axes=plt.subplots(1,2,figsize=(8,3.2),layout='constrained')
    for ax,power in zip(axes,[20000,80000],strict=True):
        subset=fixed[fixed.power_w==power]
        pivot=subset.pivot(index='pack_entropy_v_k',columns='resistance_ref_ohm',values='final_battery_k')-273.15
        pic=ax.imshow(pivot.to_numpy(),origin='lower',vmin=22,vmax=45,cmap='YlOrRd',aspect='auto')
        ax.set(xticks=range(3),xticklabels=['0,03','0,06','0,12'],yticks=range(3),yticklabels=['−0,02','0','+0,02'],xlabel='Resistência do pack [Ω]',ylabel='Entropia dU/dT [V/K]',title=f'{power/1000:.0f} kW · 500 kg · UA 125/250 W/K')
        for i,entropy in enumerate(pivot.index):
            for j,resistance in enumerate(pivot.columns):
                row=subset[(subset.pack_entropy_v_k==entropy)&(subset.resistance_ref_ohm==resistance)].iloc[0]
                suffix='*' if row.stop=='temperature_limit' else ''
                ax.text(j,i,f'{pivot.iloc[i,j]:.1f}{suffix}'.replace('.',','),ha='center',va='center',fontsize=10)
    fig.colorbar(pic,ax=axes,label='Temperatura final [°C]')
    fig.savefig(ROOT/'relatorio/figuras/comparacao_bateria.png',dpi=170);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(8,3.2),layout='constrained')
    axes[0].bar([1,2,3],[r['flow_l_min'] for r in hydraulic],color='#1f5fbf')
    axes[0].set(xticks=[1,2,3],xlabel='Fator da perda de pressão dos componentes',ylabel='Vazão de equilíbrio [L/min]',ylim=(0,36))
    ua_grid=np.linspace(700,2200,100)
    for eta,color in [(.95,'#2b8a3e'),(.90,'#1f5fbf'),(.85,'#e8590c')]:
        heat=205000*(1/eta-1)+base['electric_power_w']
        temperature=[25+heat/(efetividade_integral(ua/min(ch,cc),min(ch,cc)/max(ch,cc))*min(ch,cc)) for ua in ua_grid]
        axes[1].plot(ua_grid,temperature,color=color,label=f'η combinado {eta:.0%}')
    axes[1].axhline(65,color='k',ls='--',lw=1,label='meta 65 °C (hipótese)')
    axes[1].set(xlabel='UA do radiador [W/K]',ylabel='Entrada do fluido [°C]');axes[1].legend(fontsize=8)
    fig.savefig(ROOT/'relatorio/figuras/comparacao_arrefecimento.png',dpi=170);plt.close(fig)
    files=['config/parametros_globais.yaml','config/cabos_tracao_proposta.yaml','config/hidraulica_proposta.yaml','config/bateria_termica_proposta.yaml','relatorio/gerar_complementos_termicos.py','entregas/integrado_maxeon1560/mecanica_termica/I34_sensibilidades.csv']
    result={'script':'relatorio/gerar_complementos_termicos.py','cable_fields':campos,'shared_loop_including_reducer_sensitivity':extra,'hydraulic_sensitivity':hydraulic,'ua_for_65c_w_k':needed,'battery_extreme_cases':cases,'npsh_assumptions':{'atmospheric_pa':91500,'vapor_pa':55000,'suction_loss_pa':10000,'density_kg_m3':1050},'npsha_unpressurized_m':(91500-55000-10000)/(1050*9.80665),'npsha_100kpa_gauge_m':(191500-55000-10000)/(1050*9.80665),'ventilation_48v_m3_h':(4000/.9-4000)/(1.10*1006*10)*3600,'physical_validation':False,'inputs_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files}}
    (out/'resumo.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
