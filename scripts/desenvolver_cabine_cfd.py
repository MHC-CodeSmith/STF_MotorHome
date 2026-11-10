"""I31: CFD RANS 3D complementar, caixa equivalente fechada no instante do meio-dia.

Contornos equivalentes derivados da rede transiente; não é CHT nem CAD OEM.
Requer OpenFOAM local. Mantém campos ASCII, malhas, resíduos e hashes.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from executar_openfoam import ambiente


def header(name, kind='dictionary'):
    return f'FoamFile {{version 2.0; format ascii; class {kind}; object {name};}}\n'


def scalar_field(path):
    text = path.read_text()
    match = re.search(r'internalField\s+nonuniform\s+List<scalar>\s+(\d+)\s*\((.*?)\)\s*;', text, re.DOTALL)
    if not match:
        raise ValueError(f'Campo não escalar não uniforme: {path}')
    result = np.fromstring(match[2], sep=' ')
    if len(result) != int(match[1]) or not np.isfinite(result).all():
        raise ValueError('Campo incompleto/não finito')
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prefixo', type=Path, required=True)
    p.add_argument('--destino', type=Path, default=ROOT/'entregas/desenvolvimento_2026-11-09/cabine_cfd')
    p.add_argument('--iterations', type=int, default=2500)
    args = p.parse_args()
    cfg = yaml.safe_load((ROOT/'config/parametros_globais.yaml').read_text())
    inputs = cfg['development']['cabin_cfd']
    source = ROOT/'entregas/etapa_pos_dec061/cabine_31_32_reexecutada.json'
    network = json.loads(source.read_text())
    length, width, height = inputs['dimensions_m']
    mean_c = network['i31_noon_c']
    surfaces = {}
    glass_gain_total = sum(s['noon_glass_solar_gain_w'] for s in network['surfaces'])
    area_total = sum(s['gross_area_m2'] for s in network['surfaces'])
    for s in network['surfaces']:
        area = s['gross_area_m2']
        ua = (area-s['glass_area_m2'])*network['opaque_u_w_m2k']+s['glass_area_m2']*5.7
        gain = s['noon_opaque_solar_gain_w']+glass_gain_total*area/area_total
        # Equivalent surface of the 1-zone model, h_i=3 W/m2K. Transmitted
        # shortwave is absorbed diffusely over all interior surfaces (assumption).
        surfaces[s['surface']] = mean_c+(gain-ua*(mean_c-25))/(3*area)
    args.destino.mkdir(parents=True, exist_ok=True)
    env = ambiente(args.prefixo)
    results = []
    for nx, ny, nz in inputs['meshes']:
        case = args.destino/f'mesh_{nx}_{ny}_{nz}'
        if case.exists():
            raise FileExistsError(f'Não sobrescrever execução: {case}')
        for folder in ['0', 'constant', 'system']:
            (case/folder).mkdir(parents=True, exist_ok=True)

        def write(name, contents, kind='dictionary', case=case):
            (case/name).write_text(header(Path(name).name, kind)+contents+'\n')

        faces = {'rear': '(0 4 7 3)', 'front': '(1 2 6 5)',
                 'left': '(0 1 5 4)', 'right': '(3 7 6 2)',
                 'floor': '(0 3 2 1)', 'roof': '(4 5 6 7)'}
        patches = ' '.join(f'{k} {{type wall; faces ({v});}}' for k, v in faces.items())
        write('system/blockMeshDict', f'''scale 1;
vertices ((0 0 0)({length} 0 0)({length} {width} 0)(0 {width} 0)
(0 0 {height})({length} 0 {height})({length} {width} {height})(0 {width} {height}));
blocks (hex (0 1 2 3 4 5 6 7) ({nx} {ny} {nz}) simpleGrading (1 1 1));
edges (); boundary ({patches}); mergePatchPairs ();''')
        write('constant/g', 'dimensions [0 1 -2 0 0 0 0]; value (0 0 -9.80665);', 'uniformDimensionedVectorField')
        write('constant/transportProperties', f'''transportModel Newtonian;
nu {inputs['nu_m2_s']}; beta {inputs['beta_1_k']}; TRef {mean_c+273.15}; Pr 0.71; Prt 0.85;''')
        write('constant/turbulenceProperties', 'simulationType RAS; RAS {RASModel kEpsilon; turbulence on; printCoeffs on;}')
        write('system/controlDict', f'''application buoyantBoussinesqSimpleFoam;
startFrom startTime; startTime 0; stopAt endTime; endTime {args.iterations}; deltaT 1;
writeControl timeStep; writeInterval 500; purgeWrite 1; writeFormat ascii;
writePrecision 12; writeCompression off; timeFormat general; timePrecision 8;
runTimeModifiable false;''')
        write('system/fvSchemes', '''ddtSchemes {default steadyState;}
gradSchemes {default Gauss linear;}
divSchemes {default none; div(phi,U) bounded Gauss upwind; div(phi,T) bounded Gauss upwind;
div(phi,k) bounded Gauss upwind; div(phi,epsilon) bounded Gauss upwind;
div((nuEff*dev2(T(grad(U))))) Gauss linear;}
laplacianSchemes {default Gauss linear corrected;}
interpolationSchemes {default linear;} snGradSchemes {default corrected;}
wallDist {method meshWave;}''')
        write('system/fvSolution', '''solvers {
p_rgh {solver GAMG; tolerance 1e-9; relTol 0.01; smoother GaussSeidel;}
"(U|T|k|epsilon)" {solver smoothSolver; smoother symGaussSeidel; tolerance 1e-9; relTol 0.01;}}
SIMPLE {nNonOrthogonalCorrectors 0; pRefCell 0; pRefValue 0;
residualControl {p_rgh 1e-5; U 1e-6; T 1e-7; "(k|epsilon)" 1e-6;}}
relaxationFactors {fields {p_rgh 0.3;} equations {U 0.3; T 0.5; k 0.4; epsilon 0.4;}}''')
        def field(name, dim, initial, conditions, kind='volScalarField'):
            write('0/'+name, f'dimensions {dim}; internalField uniform {initial}; boundaryField {{'+conditions+'}', kind)
        field('U', '[0 1 -1 0 0 0 0]', '(0 0 0)', '".*" {type noSlip;}', 'volVectorField')
        field('p_rgh', '[0 2 -2 0 0 0 0]', '0', '".*" {type fixedFluxPressure; rho rhok; value uniform 0;}')
        field('p', '[0 2 -2 0 0 0 0]', '0', '".*" {type calculated; value uniform 0;}')
        field('T', '[0 0 0 1 0 0 0]', str(mean_c+273.15),
              ' '.join(f'{key} {{type fixedValue; value uniform {value+273.15};}}' for key, value in surfaces.items()))
        for name, dim, value, wall in [('k','[0 2 -2 0 0 0 0]','0.0001','kqRWallFunction'),
                                      ('epsilon','[0 2 -3 0 0 0 0]','0.0001','epsilonWallFunction'),
                                      ('nut','[0 2 -1 0 0 0 0]','0','nutkWallFunction'),
                                      ('alphat','[0 2 -1 0 0 0 0]','0','alphatJayatillekeWallFunction')]:
            extra = 'Prt 0.85;' if name == 'alphat' else ''
            field(name, dim, value, f'".*" {{type {wall}; {extra} value uniform {value};}}')
        for tool in ['blockMesh', 'checkMesh', 'buoyantBoussinesqSimpleFoam']:
            with (case/f'log.{tool}').open('w') as stream:
                run = subprocess.run([tool, '-case', str(case.resolve())], env=env,
                                     stdout=stream, stderr=subprocess.STDOUT, timeout=1800, check=False)
            if run.returncode:
                raise RuntimeError(f'{tool} retornou {run.returncode}: {case}')
        log = (case/'log.buoyantBoussinesqSimpleFoam').read_text()
        times = sorted([x for x in case.iterdir() if x.is_dir() and re.fullmatch(r'\d+(?:\.\d+)?', x.name)], key=lambda x: float(x.name))
        last = times[-1]
        t = scalar_field(last/'T')-273.15
        a = t.reshape(nz, ny, nx)
        np.savez_compressed(case/'campo_3d.npz', temperature_c=a,
                            x_m=(np.arange(nx)+.5)*length/nx,
                            y_m=(np.arange(ny)+.5)*width/ny,
                            z_m=(np.arange(nz)+.5)*height/nz)
        row = {'mesh': [nx, ny, nz], 'cells': nx*ny*nz, 'last_iteration': int(last.name),
               'simple_converged': 'SIMPLE solution converged' in log,
               'mesh_ok': 'Mesh OK.' in (case/'log.checkMesh').read_text(),
               'mean_c': float(t.mean()), 'min_c': float(t.min()), 'max_c': float(t.max()),
               'stratification_top_minus_bottom_k': float(a[-1].mean()-a[0].mean()),
               'final_residuals': dict(re.findall(r'Solving for (\w+), Initial residual = ([\deE.+-]+)', log)[-6:])}
        results.append(row)
        fig, ax = plt.subplots(figsize=(8, 3.5), layout='constrained')
        im = ax.imshow(a[:, ny//2, :], origin='lower', extent=[0,length,0,height], aspect='equal')
        fig.colorbar(im, ax=ax, label='Temperatura [°C]')
        ax.set(xlabel='X traseira → frente [m]', ylabel='Z [m]', title=f'I31 CFD 3D equivalente — {nx*ny*nz} células')
        fig.savefig(case/'temperatura_secao.png', dpi=150)
        plt.close(fig)
        print(json.dumps(row), flush=True)
    summary = {'status': 'CFD_3D_COMPLEMENTAR_CONDICIONADO' if all(r['simple_converged'] for r in results) else 'CFD_3D_EXECUTADO_SEM_CONVERGENCIA_REJEITADO_COMO_FINAL', 'solver': 'OpenFOAM buoyantBoussinesqSimpleFoam kEpsilon',
               'geometry_m': [length,width,height], 'occupants': 0, 'air_conditioning_w': 0,
               'closed': True, 'external_wind_m_s': 0, 'wall_equivalent_c': surfaces,
               'network_noon_c': mean_c, 'cases': results,
               'finest_mean_difference_k': abs(results[-1]['mean_c']-results[-2]['mean_c']),
               'limitations': ['Caixa equivalente com extensão de cabine, sem mobiliário/vidros explícitos.',
                              'Contornos de meio-dia congelados: campo estacionário complementar, não evolução matinal 3D.',
                              'Ganho solar transmitido absorvido difusamente em todas as faces por área; não ray tracing/CHT.',
                              'RANS kEpsilon com funções de parede; y+ e lei térmica não validados.',
                              'Acordo de média/estabilidade numérica não equivale a validação física.'],
               'network_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
               'canonical_parameter_extract': inputs,
               'canonical_parameter_note': 'Somente cabin_cfd lido nesta execução; rede transiente identificada por hash independente.'}
    (args.destino/'resumo.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False)+'\n')


if __name__ == '__main__':
    main()
