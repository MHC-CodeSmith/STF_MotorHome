"""Retry limitado da malha fina com camadas: relaxação/pressão robustas."""
import json
import re
import shutil
import subprocess
from pathlib import Path

from executar_openfoam import ambiente

ROOT=Path(__file__).resolve().parents[1]


def main():
    out=ROOT/'entregas/desenvolvimento_2026-11-09/aero_camadas'
    source=out/'malha3';case=out/'estabilizacao_fina';case.mkdir(exist_ok=False)
    for folder in ['0','constant','system']:shutil.copytree(source/folder,case/folder)
    path=case/'system/fvSolution';s=path.read_text()
    s=s.replace('solver GAMG; tolerance 1e-7; relTol .1; smoother GaussSeidel;',
        'solver PCG; preconditioner DIC; tolerance 1e-7; relTol .05; maxIter 500;')
    s=s.replace('nNonOrthogonalCorrectors 1','nNonOrthogonalCorrectors 2')
    s=s.replace('p .3;','p .1;').replace('U .7; k .7; omega .7;','U .25; k .25; omega .25;')
    path.write_text(s)
    path=case/'system/controlDict';s=path.read_text().replace('endTime 600;','endTime 500;');path.write_text(s)
    env=ambiente(Path('/home/mhc/motorhome_referencias_tarefas/software/openfoam2412-local/usr/lib/openfoam/openfoam2412'))
    try:
        with (case/'log.simpleFoam').open('w') as f:
            r=subprocess.run(['simpleFoam','-case',str(case)],env=env,stdout=f,stderr=subprocess.STDOUT,timeout=240,check=False)
        code=r.returncode
    except subprocess.TimeoutExpired:code=-999
    log=(case/'log.simpleFoam').read_text();cd=re.findall(r'Cd:\s+([\deE.+-]+)',log)
    result={'returncode':code,'converged':'SIMPLE solution converged' in log,
            'last_cd_diagnostic':float(cd[-1]) if cd else None,'validated_cd':None,'physical_validation':False,
            'method':'PCG/DIC pressão,2correções nãoortogonais,p.1/U,k,omega.25;mesma malha fina178298células.'}
    if code==0:
        with (case/'log.yPlus').open('w') as f:
            subprocess.run(['simpleFoam','-case',str(case),'-postProcess','-func','yPlus','-latestTime'],env=env,stdout=f,stderr=subprocess.STDOUT,timeout=60,check=False)
        y=(case/'log.yPlus').read_text();vals=re.findall(r'patch (\w+) y\+ : min = ([\deE.+-]+), max = ([\deE.+-]+), average = ([\deE.+-]+)',y)
        result['yplus']={x[0]:[float(v) for v in x[1:]] for x in vals}
    (out/'estabilizacao_resumo.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps(result))


if __name__=='__main__':main()
