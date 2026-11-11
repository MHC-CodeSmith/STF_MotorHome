"""Extrai convergência/variação observadas, sem inventarGCI em refinamentos locais."""
import json
import re
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]


def main():
    out=ROOT/'entregas/aero_equipado1540';r=json.loads((out/'resumo.json').read_text());rows=[]
    fig,axes=plt.subplots(1,2,figsize=(10,4),layout='constrained')
    for i,case in enumerate(r['cases']):
        path=ROOT/case['case'];time=0.;history=[]
        for line in (path/'log.simpleFoam').read_text().splitlines():
            m=re.match(r'Time = ([0-9.eE+-]+)',line)
            if m:time=float(m[1])
            cd=re.match(r'\s*Cd:\s+([0-9.eE+-]+)',line)
            if cd:history.append({'iteration':time,'cd':float(cd[1])})
        pd.DataFrame(history).to_csv(out/f'historico_malha{i+1}.csv',index=False)
        axes[0].plot([x['iteration'] for x in history],[x['cd'] for x in history],label=f'{case["cells"]:,}células')
        rows.append({'cells':case['cells'],'cd_diagnostic':case['last_cd_diagnostic'],'last50_relative_span':case['last50_cd_relative_span'],
            'body_mean_yplus':case['yplus']['aurora'][2],'deck_mean_yplus':case['yplus']['pvdeck'][2],'solver_converged':case['solver_converged']})
    df=pd.DataFrame(rows);df.to_csv(out/'convergencia_observada.csv',index=False)
    cd=df.cd_diagnostic.to_numpy();counts=df.cells.to_numpy();delta=abs(cd[-1]-cd[-2])/abs(cd[-1])
    axes[0].set(xlabel='Iteração SIMPLE',ylabel='Cd de diagnóstico',ylim=(.5,.85));axes[0].legend(fontsize=7)
    axes[1].plot(counts**(-1/3),cd,'o-');axes[1].set(xlabel='N⁻¹/³ [1]',ylabel='Cd de diagnóstico',title='Refinamento local;GCI não estabelecido')
    fig.savefig(out/'convergencia_observada.png',dpi=150);plt.close(fig)
    result={'cases':len(rows),'all_residual_converged':bool(df.solver_converged.all()),'last_relative_cd_change':float(delta),
        'observed_cd_range':[float(cd.min()),float(cd.max())],'effective_refinement_ratios':(counts[1:]/counts[:-1])**(1/3),
        'gci':None,'gci_reason':'Refinamento local diferente na carroceria com resolução de deckfixada;sem família geometricamente similar/assintótica demonstrada.',
        'wall_model_validation':False,'validated_cd':None,'physical_validation':False,
        'propagated_sensitivity_range':[.5806668,.72],'reference_area_note':'Aref4.827840375m² permanece a referência comum de normalização;Cd×A inclui força do deck,não confundir com nova área geométrica frontal medida.'}
    result['effective_refinement_ratios']=result['effective_refinement_ratios'].tolist()
    (out/'incerteza_observada.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
