"""Refina CFD fechado via PIMPLE transiente quando o SIMPLE não estaciona.

Continuação dos campos iniciais do estudo congelado de meio-dia. Tempo não
representa a manhã: serve à estabilidade temporal do complemento CFD.
"""
import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

import numpy as np
from desenvolver_cabine_cfd import ROOT, header, scalar_field
from executar_openfoam import ambiente


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prefixo',type=Path,required=True)
    p.add_argument('--origem',type=Path,default=ROOT/'entregas/desenvolvimento_2026-11-09/cabine_cfd')
    p.add_argument('--destino',type=Path,default=ROOT/'entregas/desenvolvimento_2026-11-09/cabine_transiente')
    p.add_argument('--tempo-s',type=float,default=300)
    args=p.parse_args(); args.destino.mkdir(parents=True,exist_ok=True)
    base=json.loads((args.origem/'resumo.json').read_text()); summary=[]
    env=ambiente(args.prefixo)
    grids=[(r,.1) for r in base['cases']]+[(base['cases'][1],.05)]
    for row,dt in grids:
        nx,ny,nz=row['mesh']; name=f'mesh_{nx}_{ny}_{nz}'
        src=args.origem/name; case=args.destino/f'{name}_dt{dt}'
        if case.exists(): raise FileExistsError(case)
        for folder in ['constant','system']: shutil.copytree(src/folder,case/folder)
        shutil.copytree(src/str(row['last_iteration']),case/'0')
        (case/'system/controlDict').write_text(header('controlDict')+f'''
application buoyantBoussinesqPimpleFoam; startFrom startTime; startTime 0;
stopAt endTime; endTime {args.tempo_s}; deltaT {dt}; adjustTimeStep yes;
maxCo 0.7; maxDeltaT {dt}; writeControl adjustableRunTime; writeInterval 50;
purgeWrite 0; writeFormat ascii; writePrecision 12; writeCompression off;
timeFormat general; timePrecision 10; runTimeModifiable false;
''')
        path=case/'system/fvSchemes'
        path.write_text(path.read_text().replace('steadyState','Euler').replace('bounded Gauss','Gauss'))
        path=case/'system/fvSolution'
        path.write_text(header('fvSolution')+'''
solvers {
p_rgh {solver GAMG; tolerance 1e-8; relTol 0.01; smoother GaussSeidel;}
p_rghFinal {$p_rgh; relTol 0;}
"(U|T|k|epsilon).*" {solver smoothSolver; smoother symGaussSeidel; tolerance 1e-8; relTol 0;}}
PIMPLE {nOuterCorrectors 2; nCorrectors 2; nNonOrthogonalCorrectors 0; pRefCell 0; pRefValue 0;}
relaxationFactors {equations {".*" 1;}}
''')
        with (case/'log.buoyantBoussinesqPimpleFoam').open('w') as stream:
            run=subprocess.run(['buoyantBoussinesqPimpleFoam','-case',str(case.resolve())],env=env,
                               stdout=stream,stderr=subprocess.STDOUT,timeout=2400,check=False)
        if run.returncode: raise RuntimeError(f'PIMPLE {run.returncode}: {case}')
        times=sorted([x for x in case.iterdir() if x.is_dir() and re.fullmatch(r'\d+(?:\.\d+)?',x.name)],key=lambda x:float(x.name))
        samples=[]
        for folder in times[1:]:
            t=scalar_field(folder/'T')-273.15
            a=t.reshape(nz,ny,nx)
            samples.append({'time_s':float(folder.name),'mean_c':float(t.mean()),'max_c':float(t.max()),
                            'stratification_k':float(a[-1].mean()-a[0].mean())})
        last=times[-1];t=scalar_field(last/'T')-273.15
        text=(last/'U').read_text()
        m=re.search(r'internalField\s+nonuniform\s+List<vector>\s+\d+\s*\((.*?)\)\s*;',text,re.DOTALL)
        velocity=np.fromstring(m[1].replace('(',' ').replace(')',' '),sep=' ').reshape(nz,ny,nx,3)
        length,width,height=base['geometry_m']
        np.savez_compressed(case/'campo_3d.npz',temperature_c=t.reshape(nz,ny,nx),velocity_m_s=velocity,
                            x_m=(np.arange(nx)+.5)*length/nx,y_m=(np.arange(ny)+.5)*width/ny,z_m=(np.arange(nz)+.5)*height/nz)
        result={'mesh':[nx,ny,nz],'max_dt_s':dt,'snapshots':samples,
                'max_velocity_m_s':float(np.linalg.norm(velocity,axis=-1).max()),
                'last100s_mean_spread_k':float(np.ptp([s['mean_c'] for s in samples[-3:]])),
                'last100s_max_spread_k':float(np.ptp([s['max_c'] for s in samples[-3:]])),
                'physical_validation':False}
        summary.append(result); print(json.dumps(result),flush=True)
    (args.destino/'resumo.json').write_text(json.dumps({'cases':summary,'base':str(args.origem.relative_to(ROOT)),
       'status':'CFD_TRANSIENTE_CONDICIONADO','limitations':base['limitations']+
       ['Tempo após reinicialização não é horário civil; estabilidade temporal avaliada sem alegar solução estacionária.',
        'Fechamento de energia e y+ devem ser verificados antes de adotar campo final.']},indent=2,ensure_ascii=False)+'\n')


if __name__=='__main__': main()
