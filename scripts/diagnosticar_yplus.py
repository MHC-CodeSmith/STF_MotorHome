"""Calcula y+ nos campos aerodinâmicos finos existentes, preservando o original."""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

from executar_openfoam import ambiente


def main():
    root=Path(__file__).resolve().parents[1]
    cache=Path('/home/mhc/motorhome_referencias_tarefas')
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--origem',type=Path,default=cache/'cfd-aurora-refino-semcamadas-02')
    p.add_argument('--caso-cache',type=Path,required=True)
    p.add_argument('--prefixo',type=Path,default=cache/'software/openfoam2412-local/usr/lib/openfoam/openfoam2412')
    p.add_argument('--destino',type=Path,default=root/'entregas/desenvolvimento_2026-11-09/aerodinamica')
    args=p.parse_args();out=args.destino;out.mkdir(parents=True,exist_ok=True)
    case=args.caso_cache;case.mkdir(parents=True,exist_ok=False);src=args.origem
    for folder in ['constant','system']:shutil.copytree(src/folder,case/folder)
    times=sorted([x for x in src.iterdir() if x.is_dir() and x.name.isdigit()],key=lambda x:int(x.name));last=times[-1]
    shutil.copytree(last,case/last.name)
    with (out/'log.yPlus').open('w') as f:
        result=subprocess.run(['simpleFoam','-case',str(case.resolve()),'-postProcess','-func','yPlus','-latestTime'],
                              env=ambiente(args.prefixo),stdout=f,stderr=subprocess.STDOUT,check=False,timeout=300)
    text=(out/'log.yPlus').read_text()
    rows=re.findall(r'patch (\w+) y\+ : min = ([\deE.+-]+), max = ([\deE.+-]+), average = ([\deE.+-]+)',text)
    inputs=[f for folder in [src/'constant',src/'system',last] for f in folder.rglob('*') if f.is_file()]
    report={'returncode':result.returncode,'time':last.name,'source_case':str(src),
            'patches':{r[0]:{'min':float(r[1]),'max':float(r[2]),'average':float(r[3])} for r in rows},
            'inputs_sha256':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in inputs},
            'independent_mesh':False,'physical_validation':False,
            'note':'Pós-processamento de campos existentes, não nova simulação de geometria equipada.'}
    (out/'yplus_resultado.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    if result.returncode or not rows:raise RuntimeError('yPlus não calculado')
    print(json.dumps(report['patches']))


if __name__=='__main__':main()
