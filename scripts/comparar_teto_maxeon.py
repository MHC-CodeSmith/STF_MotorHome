"""Alternativa1540Wp documentada: CAD plano, limitesDC e MPPT por I–V estimada."""
import hashlib
import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'scripts')]
from desenvolver_energia_sistemas import power_curve
from gerar_cad_instalacoes import Modelo


def series_iv(voltage,models,temp,sun,g):
    """Inversão das I–V lineares por trechos; sem bypass/reverse-breakdown."""
    currents=[m['isc_a']*(1+g['alpha_isc_per_k']*(temp-25))*sun for m in models]
    # Include every MPP kink explicitly: a uniform current grid alone smears
    # the piecewise-linear corner and fails even identical modules in series.
    kinks=[m['imp_a']*(1+g['alpha_isc_per_k']*(temp-25))*sun for m in models]
    current=np.unique(np.r_[np.linspace(0,min(currents),4001),[i for i in kinks if i<=min(currents)]])
    string_voltage=np.zeros_like(current)
    for model,isc in zip(models,currents,strict=True):
        imp=model['imp_a']*(1+g['alpha_isc_per_k']*(temp-25))*sun
        vmp=model['vmp_v']*(1+g['beta_vmp_assumed_per_k']*(temp-25))
        voc=model['voc_v']*(1+g['beta_voc_per_k']*(temp-25))
        string_voltage+=np.interp(current,[0,imp,isc],[voc,vmp,0])
    return np.interp(voltage,string_voltage[::-1],current[::-1],left=min(currents),right=0)


def main():
    config=ROOT/'config/parametros_globais.yaml';c=yaml.safe_load(config.read_text());d=c['development'];g=d['roof_maxeon_comparison'];s=d['pv_shared_study']
    out=ROOT/'entregas/desenvolvimento_2026-11-09/teto_maxeon';out.mkdir(parents=True,exist_ok=True)
    model=Modelo();positions=[]
    for i,index in enumerate(g['module_order']):
        position=[g['end_margin_m']+i*(g['module_dimensions_m'][0]+g['gap_m']),(d['roof_assumed_envelope_m'][1]-g['module_dimensions_m'][1])/2,2]
        positions.append({'model':g['models'][index]['id'],'position_m':position,'dimensions_m':g['module_dimensions_m']})
        model.box(f'modulo{i+1}_{index}','FVfixo',position,g['module_dimensions_m'],[30,45,90,255])
    model.export(out,'alternativa1540_plana',{'rear_x_m':0,'cargo_width_m':0,'floor_z_m':0})
    total_length=2*g['end_margin_m']+4*g['module_dimensions_m'][0]+3*g['gap_m']
    pvpair=[g['models'][i] for i in g['module_order'][:2]]
    pair_voc=sum(m['voc_v'] for m in pvpair)
    cold=pair_voc*(1+g['beta_voc_per_k']*(s['cold_c']-25))*(1+g['voc_isc_positive_tolerance'])
    roof_isc=2*max(m['isc_a'] for m in pvpair)*(1+g['alpha_isc_per_k']*(s['hot_c']-25))*(1+g['voc_isc_positive_tolerance'])
    rows=[];v=np.linspace(0,250,20001)
    for series,tr,tp,gr,gp in itertools.product([2,4],[25,65,85],[25,65,85],[.4,1],[.4,1]):
        parallel=4//series
        pr=v*2*series_iv(v,pvpair,tr,gr,g)
        vp=series*s['portable_vmp_v']*(1+s['beta_vmp_per_k']*(tp-25))
        op=series*s['portable_voc_v']*(1+s['beta_voc_per_k']*(tp-25))
        pp=power_curve(v,vp,op,parallel*s['portable_imp_a']*gp,parallel*s['portable_isc_a']*gp)
        independent=float(pr.max()+pp.max());shared=pr+pp;best=int(np.argmax(shared))
        rows.append({'portable_series':series,'portable_parallel':parallel,'roof_temp_c':tr,'portable_temp_c':tp,'roof_sun_fraction':gr,'portable_sun_fraction':gp,
            'separate_w':independent,'shared_w':float(shared[best]),'voltage_shared_v':float(v[best]),
            'mismatch_loss_percent':100*(1-float(shared[best])/independent),'iv_curves_measured':False})
    pd.DataFrame(rows).to_csv(out/'mppt_mismatch_72.csv',index=False)
    limitations=[]
    for series in [2,4]:
        parallel=4//series
        portable_cold=series*s['portable_voc_v']*(1+s['beta_voc_per_k']*(s['cold_c']-25))
        # Portable coefficient is an inherited assumption; no undocumented Isc
        # temperature law is silently imported as an EcoFlow specification.
        limitations.append({'portable_series':series,'portable_parallel':parallel,
            'roof_hot_isc_plus_portable_stc_a':roof_isc+parallel*s['portable_isc_a'],
            'isc_portable_hot_unknown':True,'max_cold_voc_v':max(cold,portable_cold),
            'conservative_35a_screen_pass':roof_isc+parallel*s['portable_isc_a']<=35,
            'shared_topology_demonstrated':False})
    result={'configuration_sha256':hashlib.sha256(config.read_bytes()).hexdigest(),'nominal_wp':sum(g['models'][i]['power_wp'] for i in g['module_order']),
        'module_mass_kg':4*g['module_mass_kg'],'required_length_including_margins_m':total_length,
        'length_remaining_m':d['roof_assumed_envelope_m'][0]-total_length,'width_remaining_m':d['roof_assumed_envelope_m'][1]-g['module_dimensions_m'][1],
        'fits_assumed_flat_rectangle':total_length<=d['roof_assumed_envelope_m'][0] and g['module_dimensions_m'][1]<=d['roof_assumed_envelope_m'][1],
        'positions':positions,'pair_cold_voc_tolerance_v':cold,'roof_hot_isc_tolerance_a':roof_isc,
        'controller_150v_compatible':cold<150,'controller_250v_roof_only_screen_pass':cold<250 and roof_isc<35,
        'shared_screen':limitations,'mismatch_cases':len(rows),'mismatch_range_percent':[min(x['mismatch_loss_percent'] for x in rows),max(x['mismatch_loss_percent'] for x in rows)],
        'source':c['sources']['maxeon3_2022'],'baseline_updated':False,'installed_geometry_validated':False,
        'dc_traction_demonstrated':False,'shared_mppt_approved':False,
        'limits':['Folga longitudinal final6mm é adicional às duas margens25mm,sem tolerâncias OEM/suportes/aberturas.',
            '2S2P misto380+390 evita inferir modelo385W não documentado;curvasIV ainda estimadas.',
            'CoeficienteVmp e potência portátil por temperatura são hipóteses,não curvasOEM.',
            '76kg são apenas módulos;suportes e custos/estoque/compatibilidade veicular não demonstrados.',
            '250/60 limita35A por conflito documental;2S2P portátil falha triagem conservadora.4S reduz corrente mas amplia mismatch e requer proteções reais.',
            'Apenas estudo comparativo;missões ainda usam1350Wp e massa anterior;nenhumaenergia creditada aHV por esta comparação.']}
    (out/'resumo.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
