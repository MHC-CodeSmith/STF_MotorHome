"""Reexecuta comparações controladas da revisão P5 sem alterar o cenário nominal.

Um parâmetro por vez no consumo; dois novos pisos CC no despacho; dias parados
entre viagens em janela diurna, mantendo ambos os bancos e conservação de energia.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'src'), str(ROOT/'scripts')]
from fechar_i29_velocidade import preparar

from motorhome.despacho_diario import alocar_dia
from motorhome.reconciliacao import consumo_plano, simular_missao

OUT = ROOT/'relatorio/dados_comparacoes'
FIG = ROOT/'relatorio/figuras'


def consumption(p, speed, **overrides):
    values = {'mass':p['assembled_typical_mass_kg'], 'cd':p['cd_range'][1],
              'area':p['area_m2'], 'cr':p['crr_range'][1], 'rho':p['rho_range'][1],
              'eta':p['eta_traction_range'][1], 'aux':p['traction_aux_assumed_w']/1000}
    values.update(overrides)
    return consumo_plano(speed, values['mass'], values['cd'], values['area'],
                         values['cr'], values['rho'], values['eta'], aux_traction_kw=values['aux'])


def main():
    os.environ['MOTORHOME_SCENARIO'] = 'maxeon1560_independente'
    OUT.mkdir(exist_ok=True)
    context = preparar(5)
    p, cfg = context['params'], context['config']
    plt.rcParams.update({'font.size':9, 'axes.grid':True, 'grid.alpha':.2})
    rows = []
    variants = [('Referência', {}), ('Massa: 4250 kg', {'mass':4250}),
                ('Cd: 0,581', {'cd':p['cd_range'][0]}), ('Cd: 0,720', {'cd':p['cd_range'][2]}),
                ('Cr: 0,008', {'cr':.008}), ('Cr: 0,016', {'cr':.016}),
                ('Rendimento: 85%', {'eta':.85}), ('Rendimento: 95%', {'eta':.95}),
                ('Auxiliares: 0 W', {'aux':0}), ('Auxiliares: 1400 W', {'aux':1.4})]
    for speed, (name, overrides) in itertools.product([40,80], variants):
        rows.append({'variant':name, 'speed_kmh':speed, 'changed':json.dumps(overrides),
                     **consumption(p,speed,**overrides)})
    pd.DataFrame(rows).to_csv(OUT/'consumo_um_parametro.csv',index=False)
    fig, ax = plt.subplots(figsize=(8,3.8),layout='constrained')
    for speed, color, delta in [(40,'#1f5fbf',-.16),(80,'#e8590c',.16)]:
        subset=[r for r in rows if r['speed_kmh']==speed]
        ax.barh(np.arange(len(variants))+delta,[r['kwh_km'] for r in subset],height=.30,label=f'{speed} km/h',color=color)
    ax.set(yticks=range(len(variants)),yticklabels=[n for n,_ in variants],xlabel='Consumo no lado da bateria [kWh/km]')
    ax.invert_yaxis();ax.legend();fig.savefig(FIG/'comparacao_consumo.png',dpi=170);plt.close(fig)
    print('Consumo: 20 casos concluídos.',flush=True)

    # Same original 5-minute grid and half-hour departures; only the floor varies.
    g=cfg['development']['daily_dispatch'];hours=context['slot_hours'];dt=5/60
    old=pd.read_csv(ROOT/'entregas/integrado_maxeon1560/despacho_i25/melhores_por_velocidade.csv')
    best=[r for r in old.to_dict('records') if r['step_min']==5 and r['speed_kmh'] in [40,80]]
    milp_cases=0
    for minimum, services in itertools.product([.5,1.0],[False,True]):
        leaders={}
        for departure in np.arange(g['departure_start_h'],g['departure_end_h']+.001,g['departure_step_h']):
            parked=hours<departure
            deployed=(hours>=p['pv_setup_h'])&(hours<departure-p['pv_teardown_h'])
            tilt,az,curve=max(context['portables'],key=lambda x:float((x[2]*deployed).sum()))
            solar=context['roof']+curve*deployed
            r=alocar_dia(solar,parked,dt,minimo_dc_kw=minimum,eta_dc=p['eta_dc'],
                        eta_servicos=p['eta_service_charge'],consumo_servicos_kwh=context['service_day'] if services else 0,
                        capacidade_servicos_kwh=g['service_capacity_kwh'],
                        energia_servicos_inicial_kwh=g['service_capacity_kwh']*g['service_initial_fraction'],
                        capacidade_credito_tracao_kwh=(1-g['traction_initial_soc_baseline'])*p['traction_usable_kwh'])
            milp_cases+=1
            if r['status']!='otimo_para_janela_discreta':continue
            assert r['residuo_servicos_kwh']<1e-7
            for speed in [40,80]:
                c=consumption(p,speed);energy=r['credito_solar_tracao_kwh']
                duration=min(24-departure,energy/c['bateria_kw'])
                row={'step_min':5,'services_cyclic':services,'hypothetical_dc_min_input_kw':minimum,
                     'speed_kmh':speed,'departure_h':float(departure),'distance_km':duration*speed,
                     'solar_hv_received_kwh':energy,'pv_generated_kwh':float(solar.sum()*dt),
                     'service_day_kwh':context['service_day'] if services else 0,
                     'service_balance_max_kwh':r['residuo_servicos_kwh'],'milp_gap':r['gap_milp']}
                if speed not in leaders or row['distance_km']>leaders[speed]['distance_km']+1e-9:leaders[speed]=row
        best.extend(leaders.values())
        print(f'Despacho: piso {minimum} kW, serviços {services}, {milp_cases} janelas.',flush=True)
    pd.DataFrame(best).to_csv(OUT/'limiar_dc_40_80.csv',index=False)
    fig, ax=plt.subplots(figsize=(7.6,3.3),layout='constrained')
    for speed,services in itertools.product([40,80],[False,True]):
        subset=sorted((r for r in best if r['speed_kmh']==speed and r['services_cyclic']==services),key=lambda r:r['hypothetical_dc_min_input_kw'])
        ax.plot([r['hypothetical_dc_min_input_kw'] for r in subset],[r['distance_km'] for r in subset],marker='o',ls='--' if services else '-',label=f'{speed} km/h; '+('com habitação' if services else 'só tração'))
    ax.set(xlabel='Potência mínima na saída CC [kW]',ylabel='Distância com o sol do dia [km]',xticks=[0,.38,.5,1,3]);ax.legend(fontsize=8)
    fig.savefig(FIG/'comparacao_limiar_dc.png',dpi=170);plt.close(fig)

    mission=[]
    for speed, period in itertools.product([40,80],[1,2,3]):
        start=8.;slot=context['slot_hours'];drive=(slot>=start)&(slot<start+8)
        deployed=(~drive)&((slot<start-p['pv_teardown_h'])|(slot>=start+8+p['pv_setup_h']))
        tilt,az,curve=max(context['portables'],key=lambda x:float(x[2].sum()))
        r=simular_missao(context['roof'].tolist(),(curve*deployed).tolist(),drive.tolist(),
                         speed_kmh=speed,kwh_km=consumption(p,speed)['kwh_km'],service_kwh_day=context['service_day'],
                         traction_capacity_kwh=p['traction_usable_kwh'],service_capacity_kwh=14.4,
                         reserve_traction=.1,reserve_service=.2,mode='direta_hipotese',min_dc_kw=.38,
                         eta_dc=p['eta_dc'],eta_service=p['eta_service_charge'],primeira_partida_h=start,
                         driving_day_period=period,portable_parked_kw=curve.tolist())
        trace=r.pop('trace');daily=r.pop('daily')
        assert abs(r['energy_residual_kwh'])<1e-6
        assert max(x['driving_h'] for x in daily)<=8+1e-8
        assert min(x['soc_traction'] for x in trace)>=.1-1e-8
        assert min(x['soc_service'] for x in trace)>=.2-1e-8
        pd.DataFrame(daily).to_csv(OUT/f'viagem_{speed}kmh_ciclo{period}dias.csv',index=False)
        first=next((x for x in trace if x['soc_traction']<=.1+1e-9),None)
        after=None if first is None else (r['distance_km']-first['distance_km'])/(r['elapsed_days']-(first['day']-1+first['hour_end']/24))
        mission.append({'speed_kmh':speed,'start_hour':start,'driving_day_period':period,
                        'portable_tilt_deg':tilt,'portable_azimuth_deg':az,'km_per_day_after_reserve':after,**r})
        print(f'Viagem: {speed} km/h, ciclo {period} dias: {r["status"]}, {r["elapsed_days"]:.2f} dias.',flush=True)
    (OUT/'acumular_energia.json').write_text(json.dumps(mission,ensure_ascii=False,indent=2)+'\n')
    lines=[r'\begin{table}[H]\centering\small',r'\caption{Viagem com janela de 08 a 16h: efeito de intercalar dias parados para acumular energia solar.}\label{tab:acumulacao}',r'\begin{tabular}{rrlrrr}',r'\toprule $v$ [km/h] & Pausa [dias] & Resultado & Tempo [dias] & Distância [km] & Ao volante [h] \\\midrule']
    for r in mission:
        status='chegada' if r['status']=='chegada_condicional' else 'serviços na reserva'
        vals=[str(r['speed_kmh']),str(r['driving_day_period']-1),status,f"{r['elapsed_days']:.1f}",f"{r['distance_km']:.0f}",f"{r['totals']['driving_h']:.1f}"]
        lines.append(' & '.join(x.replace('.',',') for x in vals)+r' \\')
    lines.extend([r'\bottomrule\end{tabular}\end{table}'])
    (ROOT/'relatorio/tabela_acumulacao.tex').write_text('\n'.join(lines)+'\n')
    # Plot the already executed roof comparison next to its discussion in the report.
    incl=pd.read_csv(ROOT/'entregas/integrado_maxeon1560/p5_geracao_portateis/inclinacao_teto.csv')
    fig,ax=plt.subplots(figsize=(7,2.8),layout='constrained')
    for az,label in [(0,'norte'),(90,'leste'),(180,'sul'),(270,'oeste')]:
        x=incl[incl.azimute_face_deg==az];ax.plot(x.inclinacao_deg,x.teto_kwh_dia,marker='o',label=label)
    ax.set(xlabel='Inclinação do teto [graus]',ylabel='Geração do teto [kWh/dia]');ax.legend(ncol=4)
    fig.savefig(FIG/'comparacao_inclinacao.png',dpi=170);plt.close(fig)
    files=['config/parametros_globais.yaml','src/motorhome/reconciliacao.py','src/motorhome/despacho_diario.py',
           'scripts/fechar_i29_velocidade.py','relatorio/comparar_parametros.py',
           'entregas/integrado_maxeon1560/despacho_i25/melhores_por_velocidade.csv',
           'entregas/integrado_maxeon1560/p5_geracao_portateis/inclinacao_teto.csv']
    summary={'scenario':'maxeon1560_independente','time_step_minutes':5,'executed_utc':datetime.now(timezone.utc).isoformat(),
             'oat_cases':len(rows),'new_milp_cases':milp_cases,'new_dc_floors_kw':[.5,1.0],
             'accumulation_missions':len(mission),'maximum_energy_residual_kwh':max(abs(r['energy_residual_kwh']) for r in mission),
             'hypothetical_dc_interface':True,'physical_validation':False,
             'limits':['Clima claro repetido, pista plana, sem energia externa.',
                       'Um dia de condução seguido de zero, um ou dois dias parados; janela08–16, até8h/dia.',
                       'Portáteis disponíveis o dia todo nos dias parados; início/fim do ciclo ocorrem sem sol, depois da montagem/antes do recolhimento.',
                       'Comparação de política fixa; não é otimização global nem deve ser comparada como se usasse horário18–02.'],
             'inputs_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files}}
    (OUT/'execucao.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':main()
