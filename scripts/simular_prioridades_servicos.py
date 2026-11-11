"""ComplementoDEC047: autonomia24/48semSol,consumo médio e cargas por estágio."""
import itertools
import json
import sys
from pathlib import Path

import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from motorhome.cenarios import carregar_configuracao, diretorio_entregas
from motorhome.prioridades import simular_servicos_priorizados


def main():
    c=carregar_configuracao(ROOT);p={k:v['value'] for k,v in c['parameters'].items()};g=c['development']['service_energy_priority_study']
    out=diretorio_entregas(ROOT)/'prioridades_servicos';out.mkdir(exist_ok=True);rows=[];energies=[]
    for horizon,reserve,level,aux,managed in itertools.product(g['horizons_h'],sorted({x[1] for x in p['trip_reserve_pairs']}),['min','base','max'],g['additional_control_w_sweep'],[False,True]):
        load={x['id']:x['energy_ac_or_dc_kwh_day'][level]/(p['eta_inverter'] if x['side']=='AC' else p['eta_lv']) for x in c['loads']}
        idle=(p['inverter_idle_w']+aux)*24/1000
        daily=[sum(load.values())+idle,sum(load[x] for x in g['stage1_ids'])+idle,sum(load[x] for x in g['stage2_ids'])+idle]
        r=simular_servicos_priorizados(p['service_modules_provisional']*p['module_service_kwh'],reserve,horizon,daily,managed=managed)
        trace=r.pop('trace');df=pd.DataFrame(trace)
        hours={f'stage{i}_h':float((df.loc[df.stage==i,'end_h']-df.loc[df.stage==i,'start_h']).sum()) if len(df) else 0 for i in range(3)}
        rows.append({'horizon_h':horizon,'reserve_comparison':reserve,'consumption_level':level,'control_aux_w_hypothetical':aux,'managed':managed,**hours,**r})
        if level=='base' and aux==0:
            df.to_csv(out/f'perfil_{horizon}h_reserva{reserve}_gerenciado{int(managed)}.csv',index=False)
            if horizon==24 and reserve==.2 and managed:energies=[{'stage':i,'battery_kwh_day':x,'included_ids':','.join(load if i==0 else g[f'stage{i}_ids'])} for i,x in enumerate(daily)]
    pd.DataFrame(rows).to_csv(out/'autonomia_72comparacoes.csv',index=False);pd.DataFrame(energies).to_csv(out/'cargas_por_estagio.csv',index=False)
    result={'cases':len(rows),'energy_residual_max_kwh':max(abs(x['energy_residual_kwh']) for x in rows),
        'soc_thresholds_project':None,'hardware_actuators_implemented':False,'mission_full_comfort_model_changed':False,
        'base_cases':[x for x in rows if x['consumption_level']=='base' and x['control_aux_w_hypothetical']==0],
        'consequences':{'stage1':'Retira indução/boiler/lavagem/secagem;mantémA/C,geladeira,DCprioritário.',
            'stage2':'Retira tambémA/C;mantém geladeira eDCprioritário até energia operacional acabar.'},
        'limits':['É recomendação por energia prevista,não ajusteBMS ou patamaresSOC do veículo.',
            'MédiasDEC046 não comprovam horários/ciclos/partidas nem resposta de contatores.',
            'Controleextra0/5/15W é sensibilidade;equipamento e potência reais não selecionados por este modelo.',
            'Sem orçamento para todo o horizonte,essenciais são mantidos apenas até reserva;zeroenergia não garante segurança alimentar.',
            'MissãoI29 mantém perfil moderado completo;este complemento não transforma falha de serviços em chegada viável.']}
    (out/'resumo.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
