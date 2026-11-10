"""Nova tentativa limitada de camadas nas três malhas aero existentes.

Preserva casos antigos; mesma geometria representativa, NÃO equipada/OEM.
Rejeita qualidade/convergência insuficiente e registra falhas de execução.
"""
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml
from executar_openfoam import ambiente

ROOT=Path(__file__).resolve().parents[1]
CACHE=Path('/home/mhc/motorhome_referencias_tarefas')


def main():
    c=yaml.safe_load((ROOT/'config/parametros_globais.yaml').read_text());g=c['development']['aero_layer_retry']
    out=ROOT/'entregas/desenvolvimento_2026-11-09/aero_camadas';out.mkdir(parents=True,exist_ok=False)
    env=ambiente(CACHE/'software/openfoam2412-local/usr/lib/openfoam/openfoam2412');rows=[]
    for number,name in enumerate(g['source_cases']):
        source=CACHE/name;case=out/f'malha{number+1}';case.mkdir()
        for folder in ['0','constant','system']:shutil.copytree(source/folder,case/folder)
        for old in case.rglob('*.gz'):old.unlink() if old.with_suffix('').exists() else None
        path=case/'system/snappyHexMeshDict';s=path.read_text()
        s=s.replace('castellatedMesh true; snap true; addLayers false;','castellatedMesh false; snap false; addLayers true;')
        s=s.replace('relativeSizes true; layers {};','relativeSizes false; layers {"aurora.*" {nSurfaceLayers 3;}}')
        s=s.replace('expansionRatio 1.2; finalLayerThickness .3;',f'expansionRatio {g["expansion_ratio"]}; finalLayerThickness {g["final_layer_m"]};')
        s=s.replace('minThickness .1;',f'minThickness {g["min_layer_m"]};')
        path.write_text(s)
        ctrl=case/'system/controlDict';s=ctrl.read_text()
        s=re.sub(r'endTime\s+\d+;',f'endTime {g["max_iterations"]};',s)
        s=re.sub(r'writeInterval\s+200;', 'writeInterval 100;',s)
        s=s.replace('purgeWrite 2;','purgeWrite 1;');ctrl.write_text(s)
        # Same reference U, nu, rho and A as source pilot; these remain
        # explicitly independent of the mass/consumption central estimate.
        row={'source':str(source),'case':str(case.relative_to(ROOT)),'requested_layers':3,'physical_validation':False,
             'source_surface_sha256':hashlib.sha256((case/'constant/triSurface/aurora.stl').read_bytes()).hexdigest()}
        def run(command,timeout,case=case):
            tool='yPlus' if '-postProcess' in command else command[0]
            try:
                with (case/f'log.{tool}').open('w') as f:
                    r=subprocess.run(command+['-case',str(case)],env=env,stdout=f,stderr=subprocess.STDOUT,timeout=timeout,check=False)
                return r.returncode
            except subprocess.TimeoutExpired:return -999
        status=run(['snappyHexMesh','-overwrite'],g['mesh_timeout_s'])
        row['snappy_exit']=status
        meshlog=(case/'log.snappyHexMesh').read_text()
        added=re.findall(r'Added (\d+) out of (\d+) cells',meshlog)
        row['added_layer_cells']=int(added[-1][0]) if added else None
        row['retained_layers_demonstrated']=bool(row['added_layer_cells'])
        row['accepted_as_cd_result']=False
        if status==0:
            row['check_exit']=run(['checkMesh'],60)
            mesh=(case/'log.checkMesh').read_text();row['mesh_ok']='Mesh OK.' in mesh
            cells=re.search(r'cells:\s+(\d+)',mesh);row['cells']=int(cells[1]) if cells else None
            if row['mesh_ok']:
                row['solver_exit']=run(['simpleFoam'],g['solver_timeout_s'])
                log=(case/'log.simpleFoam').read_text()
                row['solver_converged']='SIMPLE solution converged' in log
                coefficients=re.findall(r'Cd:\s+([\deE.+-]+)\s+([\deE.+-]+)\s+([\deE.+-]+)',log)
                row['last_cd_diagnostic']=float(coefficients[-1][0]) if coefficients else None
                if row['solver_exit']==0:
                    run(['simpleFoam','-postProcess','-func','yPlus','-latestTime'],60)
                    ylog=(case/'log.yPlus').read_text()
                    values=re.findall(r'patch (\w+) y\+ : min = ([\deE.+-]+), max = ([\deE.+-]+), average = ([\deE.+-]+)',ylog)
                    row['yplus']={v[0]:{'min':float(v[1]),'max':float(v[2]),'mean':float(v[3])} for v in values}
        rows.append(row)
        (out/'resumo.json').write_text(json.dumps({'cases':rows,'independence_demonstrated':False,'validated_cd':None,
            'note':'Mesma geometria piloto;solicitar camadas não prova cobertura nem y+. Não substituir Cd do modelo sem convergência/estudo completo.'},indent=2,ensure_ascii=False)+'\n')
        print(json.dumps(row),flush=True)
    return 0


if __name__=='__main__':sys.exit(main())
