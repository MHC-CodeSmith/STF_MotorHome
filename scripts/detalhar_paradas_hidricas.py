"""Reproduz água em horários estacionários reais dos oito melhores replays.

Não refaz missão energética: DEC046 mantém energia média; localização e
existência de instalações sanitárias seguem hipotéticas. Eventos são tomadas
de água, não duração certificada de banho ou de ciclo da lavadora.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from motorhome.desenvolvimento import consumir_agua


def agendar_eventos(livre, eventos, state, dt_h=.25, desired_slots=None):
    """Insere abastecimento/descarte ANTES de uso; intervalos não sobrepostos."""
    available=np.array(livre,dtype=bool).copy();state=state.copy();result=[];cursor=0
    for index,(event,amount,black) in enumerate(eventos):
        if desired_slots is not None:cursor=max(cursor,desired_slots[index])
        needs=False
        try: consumir_agua(state,amount,black)
        except ValueError:needs=True
        count=2 if needs else 1
        slot=next((i for i in range(cursor,len(available)-count+1) if available[i:i+count].all()),None)
        if slot is None:raise ValueError('Janela estacionária insuficiente para demanda hídrica')
        if needs:
            result.append({'event':'reabastecer_descartar','start_h':slot*dt_h,'end_h':(slot+1)*dt_h,
                'refill_l':100-state['clean_l'],'disposal_l':state['grey_l']+state['black_l'],
                'draw_l':0.,'clean_l':100.,'grey_l':0.,'black_l':0.})
            state={'clean_l':100.,'grey_l':0.,'black_l':0.};slot+=1
        new=consumir_agua(state,amount,black);state={k:new[k] for k in state}
        result.append({'event':event,'start_h':slot*dt_h,'end_h':(slot+1)*dt_h,'refill_l':0.,'disposal_l':0.,
                       'draw_l':amount,**state})
        # Both logistics and draw occupy distinct slots; no repeated timestamps.
        available[round(result[-count]['start_h']/dt_h):slot+1]=False
        cursor=slot+1
    return result,state


def main():
    out=ROOT/'entregas/desenvolvimento_2026-11-09/otimizacao_grade'
    summary=json.loads((out/'resumo.json').read_text())
    canonical=yaml.safe_load((ROOT/'config/parametros_globais.yaml').read_text())
    p={k:v['value'] for k,v in canonical['parameters'].items()};g=canonical['development']['water_chronology']
    rows=[]
    for key,best in summary['best_by_reserve'].items():
        profile=pd.read_csv(out/f'melhor_reservas{key}.csv.gz')
        state={'clean_l':100.,'grey_l':0.,'black_l':0.};refilled=disposed=0.
        for day,part in profile.groupby('day',sort=True):
            # Actual stopped intervals; exclude solar assembly/disassembly
            # according to selected planned stop, without adding driving time.
            end=part.hour_end.to_numpy();hours=end-.125
            elapsed=float(end[-1]);size=round(elapsed/.25)
            free=np.zeros(size,dtype=bool)
            since=(hours-(best['start_h']+best['window_h']))%24
            allowed=(part.driving_h_interval.to_numpy()==0)&(since>=p['pv_setup_h'])&(since<24-best['window_h']-p['pv_teardown_h'])
            free[np.rint(end/.25).astype(int)-1]=allowed
            demand=g['daily_base_l']*elapsed/24
            events=[('uso_base',demand/g['base_batches'],g['black_fraction'])]*g['base_batches']
            if day%g['laundry_every_days']==0:events.append(('admissao_lavadora',g['laundry_water_l'],0.))
            slots=np.flatnonzero(free)
            desired=[int(slots[min(len(slots)-1,round((i+1)*len(slots)/(len(events)+1)))]) for i in range(len(events))] if len(slots) else [0]*len(events)
            events,state=agendar_eventos(free,events,state,desired_slots=desired)
            for event in events:
                refilled+=event['refill_l'];disposed+=event['disposal_l']
                rows.append({'scenario':key,'day':int(day),**event,
                    'balance_residual_l':100+refilled-disposed-event['clean_l']-event['grey_l']-event['black_l'],
                    'external_electric_kwh':0.,'station_availability_proven':False})
    frame=pd.DataFrame(rows);frame.to_csv(out/'sanitaria_cronologia.csv',index=False)
    result={'events':len(frame),'scenarios':frame.scenario.nunique(),
        'max_water_residual_l':float(frame.balance_residual_l.abs().max()),
        'refuelling_events':int((frame.event=='reabastecer_descartar').sum()),
        'all_events_in_stationary_windows':True,'geographical_availability_proven':False,
        'energy_recomputed':False,'note':'Tomadas de água/logística15min, sequenciais, somente estacionado e fora montagem/recolhimento FV. Base do último dia proporcional à duração. Ciclo/horários de eletrodomésticos não substituem energia média DEC046; postos reais e tempos não comprovados.'}
    (out/'sanitaria_cronologia_resumo.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
