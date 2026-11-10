"""Três CFD com coberturaFV equivalente; wall functions sem repetir camadas falhas.

Painel equivalente contínuo simplifica os20mm entre módulos e suportes.
Resultados permanecem condicionados à geometria piloto e resolução de parede.
"""
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

import numpy as np
import trimesh
import yaml
from executar_openfoam import ambiente

ROOT=Path(__file__).resolve().parents[1]
CACHE=Path('/home/mhc/motorhome_referencias_tarefas')


def main():
    c=yaml.safe_load((ROOT/'config/parametros_globais.yaml').read_text())
    g=c['development']['equipped_aero_verification'];roof=c['development']['roof_maxeon_comparison']
    out=ROOT/'entregas/aero_equipado1540';out.mkdir(exist_ok=False)
    env=ambiente(CACHE/'software/openfoam2412-local/usr/lib/openfoam/openfoam2412');results=[]
    for i,name in enumerate(g['source_cases']):
        source=CACHE/name;case=out/f'malha{i+1}';case.mkdir()
        for folder in ['0','constant','system']:shutil.copytree(source/folder,case/folder)
        shutil.rmtree(case/'constant/polyMesh')
        for old in ['cellLevel','pointLevel']:
            for path in (case/'0').glob(old+'*'):path.unlink()
        body=trimesh.load(case/'constant/triSurface/aurora.stl')
        dims=[4*roof['module_dimensions_m'][0]+3*roof['gap_m'],roof['module_dimensions_m'][1],roof['module_dimensions_m'][2]]
        lo=[body.bounds[0,0]+roof['end_margin_m'],-dims[1]/2,body.bounds[1,2]+g['panel_gap_above_body_m']]
        panel=trimesh.creation.box(extents=dims);panel.apply_translation(np.array(lo)+np.array(dims)/2)
        panel.export(case/'constant/triSurface/pvdeck.stl')
        p=case/'system/snappyHexMeshDict';s=p.read_text();s=s.replace('geometry {','geometry {\n pvdeck.stl {type triSurfaceMesh; name pvdeck;}')
        s=s.replace('refinementSurfaces {','refinementSurfaces {pvdeck {level (4 5); patchInfo {type wall;}}')
        p.write_text(s)
        # All fields receive the additional no-slip/turbulence wall patch.
        for p in (case/'0').iterdir():
            if p.is_file():p.write_text(p.read_text().replace('"aurora.*"','"(aurora|pvdeck).*"'))
        p=case/'system/controlDict';s=p.read_text();s=re.sub(r'endTime\s+\d+;',f'endTime {g["max_iterations"]};',s)
        s=s.replace('patches ("aurora.*")','patches ("(aurora|pvdeck).*")').replace('purgeWrite 2','purgeWrite 1')
        p.write_text(s)
        row={'source':name,'case':str(case.relative_to(ROOT)),'body_stl_sha256':hashlib.sha256((case/'constant/triSurface/aurora.stl').read_bytes()).hexdigest(),
            'pvdeck_stl_sha256':hashlib.sha256((case/'constant/triSurface/pvdeck.stl').read_bytes()).hexdigest(),
            'panel_bbox_lo_m':lo,'panel_bbox_size_m':dims,'validated_cd':None}
        def run(command,timeout,logname,case=case):
            try:
                with (case/logname).open('w') as f:
                    return subprocess.run(command+['-case',str(case)],env=env,stdout=f,stderr=subprocess.STDOUT,timeout=timeout,check=False).returncode
            except subprocess.TimeoutExpired:return -999
        row['block_exit']=run(['blockMesh'],60,'log.blockMesh')
        row['snappy_exit']=run(['snappyHexMesh','-overwrite'],g['mesh_timeout_s'],'log.snappyHexMesh') if row['block_exit']==0 else None
        if row['snappy_exit']==0:
            row['check_exit']=run(['checkMesh'],60,'log.checkMesh');mesh=(case/'log.checkMesh').read_text()
            row['mesh_ok']='Mesh OK.' in mesh
            match=re.search(r'cells:\s+(\d+)',mesh);row['cells']=int(match[1]) if match else None
            if row['mesh_ok']:
                row['solver_exit']=run(['simpleFoam'],g['solver_timeout_s'],'log.simpleFoam')
                log=(case/'log.simpleFoam').read_text();row['solver_converged']='SIMPLE solution converged' in log
                cd=[float(x) for x in re.findall(r'Cd:\s+([\deE.+-]+)',log)]
                row['last_cd_diagnostic']=cd[-1] if cd else None
                row['last50_cd_relative_span']=None if len(cd)<50 else (max(cd[-50:])-min(cd[-50:]))/max(abs(np.mean(cd[-50:])),1e-12)
                row['finite_cd']=bool(cd and np.isfinite(cd).all())
                if row['solver_exit']==0:
                    run(['simpleFoam','-postProcess','-func','yPlus','-latestTime'],60,'log.yPlus')
                    ylog=(case/'log.yPlus').read_text();y=re.findall(r'patch (\w+) y\+ : min = ([\deE.+-]+), max = ([\deE.+-]+), average = ([\deE.+-]+)',ylog)
                    row['yplus']={x[0]:[float(v) for v in x[1:]] for x in y}
        results.append(row)
        summary={'configuration_source_sha256':hashlib.sha256((ROOT/'config/parametros_globais.yaml').read_bytes()).hexdigest(),
            'cases':results,'validated_cd':None,'physical_validation':False,'global_grid_independence':False,
            'method':'Mesma geometria piloto;novo deckFV contínuo,parede sem camadas com kOmegaSST/wallfunctions. Não repete malha fina extrudida divergente.',
            'limits':['Geometria piloto não é CAD certificadoL3H2;suportes e gaps20mm entre módulos omitidos.',
                'Gap constante ao topo máximo da carroceria é hipótese;não posição real de ancoragem.',
                'Parede/y+ e folga painel precisam resolução e incerteza;convergência residual não equivale aCd validado.']}
        (out/'resumo.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
        print(json.dumps(row),flush=True)


if __name__=='__main__':main()
