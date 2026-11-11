"""Tira de chapa do inversor: melhora aproximação de flexão comTet10/4pontosGauss."""
import json
from pathlib import Path

import pandas as pd
import yaml
from verificar_chapas_3d import solve

ROOT=Path(__file__).resolve().parents[1]


def main():
    c=yaml.safe_load((ROOT/'config/parametros_globais.yaml').read_text());g=c['development']['mounting_redesign'];f=g['solid_verification']
    out=ROOT/'entregas/desenvolvimento_2026-11-09/fixacoes_redimensionadas'
    s=pd.read_csv(out/'selecoes.csv');s=s[s.component=='inversor'].iloc[0]
    demand=pd.read_csv(out/f'demandas_inversor_{int(s.span_x_m*1000)}x{int(s.span_y_m*1000)}.csv');force=float(demand.max_tension_n.max())
    rows=[]
    for size in f['mesh_sizes_m'][:3]:
        rows.append(solve(g['local_flange_lever_m'],g['tributary_strip_width_m'],float(s.thickness_m),force,f['young_pa'],f['poisson'],size,out/f'campo_inversor_quadratico_{size:.4f}.npz',order=2))
    pd.DataFrame(rows).to_csv(out/'inversor_quadratico_convergencia.csv',index=False)
    change=abs(rows[-1]['tip_work_average_m']-rows[-2]['tip_work_average_m'])/abs(rows[-1]['tip_work_average_m'])
    result={'cases':len(rows),'element_order':2,'gauss_points':4,'last_relative_displacement_change':change,
        'displacement_refinement_criterion_met':change<=f['displacement_relative_change_criterion'],
        'max_force_residual_n':max(r['force_residual_n'] for r in rows),'max_moment_residual_nm':max(r['moment_residual_nm'] for r in rows),
        'physical_validation':False,'peak_stress_validated':False,'reason':'Tet4 exigia refinamento muito fino para flexão. Tet10 melhora aproximação sem relaxar critério2%;sem validação de contato/ancoragem real.'}
    (out/'inversor_quadratico_resumo.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps(result))


if __name__=='__main__':main()
