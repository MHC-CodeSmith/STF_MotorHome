"""Caso piloto RANS de malha autoral reparada; sem pretensão de Cd validado.

Primeira execução sem camadas de parede: serve a diagnóstico de domínio/solver.
Exige fonte STL e Aref explícitas; não escreve parâmetros globais.
"""

import argparse
import hashlib
import json
import shutil
from pathlib import Path


def header(name, kind='dictionary'):
    return f'FoamFile {{version 2.0; format ascii; class {kind}; object {name};}}\n'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--superficie', type=Path, required=True)
    p.add_argument('--area-m2', type=float, required=True)
    p.add_argument('--destino', type=Path, required=True)
    p.add_argument('--nivel', type=int, default=2, choices=[2, 3, 4])
    p.add_argument('--camadas', type=int, default=0, choices=[0, 3])
    args = p.parse_args()
    if args.area_m2 <= 0:
        raise ValueError('Aref positiva obrigatória')
    args.destino.mkdir(parents=True, exist_ok=False)
    out = args.destino
    for folder in ['0', 'constant/triSurface', 'system']:
        (out/folder).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(args.superficie, out/'constant/triSurface/aurora.stl')

    def write(name, text, kind='dictionary'):
        (out/name).write_text(header(Path(name).name, kind)+text)

    write('system/blockMeshDict', '''
scale 1;
vertices ((-35 -10 0)(20 -10 0)(20 10 0)(-35 10 0)
          (-35 -10 10)(20 -10 10)(20 10 10)(-35 10 10));
blocks (hex (0 1 2 3 4 5 6 7) (55 20 10) simpleGrading (1 1 1));
edges ();
boundary (
 inlet {type patch; faces ((1 2 6 5));}
 outlet {type patch; faces ((0 4 7 3));}
 ground {type wall; faces ((0 3 2 1));}
 sides {type symmetry; faces ((0 1 5 4)(3 7 6 2));}
 top {type symmetryPlane; faces ((4 5 6 7));}
);
mergePatchPairs ();
''')
    write('system/snappyHexMeshDict', '''
castellatedMesh true; snap true; addLayers false;
geometry {
 aurora.stl {type triSurfaceMesh; name aurora;}
 wake {type searchableBox; min (-15 -2 0); max (4 2 4);}
}
castellatedMeshControls {
 maxLocalCells 400000; maxGlobalCells 400000; minRefinementCells 10;
 maxLoadUnbalance .1; nCellsBetweenLevels 3; features ();
 refinementSurfaces {aurora {level (2 3); patchInfo {type wall;}}}
 resolveFeatureAngle 30;
 refinementRegions {wake {mode inside; levels ((1E15 1));}}
 locationInMesh (15.1 7.1 5.1); allowFreeStandingZoneFaces true;
}
snapControls {
 nSmoothPatch 3; tolerance 2; nSolveIter 30; nRelaxIter 5;
 nFeatureSnapIter 10; implicitFeatureSnap true; explicitFeatureSnap false;
 multiRegionFeatureSnap false;
}
addLayersControls {
 relativeSizes true; layers {}; expansionRatio 1.2; finalLayerThickness .3;
 minThickness .1; nGrow 0; featureAngle 60; nRelaxIter 3;
 nSmoothSurfaceNormals 1; nSmoothNormals 3; nSmoothThickness 10;
 maxFaceThicknessRatio .5; maxThicknessToMedialRatio .3;
 minMedialAxisAngle 90; nBufferCellsNoExtrude 0; nLayerIter 50;
}
meshQualityControls {
 maxNonOrtho 65; maxBoundarySkewness 4; maxInternalSkewness 4;
 maxConcave 80; minVol 1e-13; minTetQuality 1e-15;
 minArea -1; minTwist .02; minDeterminant .001;
 minFaceWeight .02; minVolRatio .01; minTriangleTwist -1;
 nSmoothScale 4; errorReduction .75;
 relaxed {maxNonOrtho 75;}
}
writeFlags (scalarLevels); mergeTolerance 1e-6;
''')
    dictionary = out/'system/snappyHexMeshDict'
    contents = dictionary.read_text().replace('level (2 3)', f'level ({args.nivel} {args.nivel+1})')
    if args.camadas:
        contents = contents.replace('addLayers false;', 'addLayers true;')
        contents = contents.replace('relativeSizes true; layers {};',
                                    'relativeSizes false; layers {"aurora.*" {nSurfaceLayers 3;}}')
        contents = contents.replace('expansionRatio 1.2; finalLayerThickness .3;',
                                    'expansionRatio 1.3; finalLayerThickness .005;')
        contents = contents.replace('minThickness .1;', 'minThickness .001;')
    dictionary.write_text(contents)
    write('system/controlDict', f'''
application simpleFoam; startFrom startTime; startTime 0; stopAt endTime;
endTime 600; deltaT 1; writeControl timeStep; writeInterval 200;
purgeWrite 2; writeFormat binary; writePrecision 8; writeCompression off;
timeFormat general; timePrecision 6; runTimeModifiable true;
functions {{ forces1 {{type forceCoeffs; libs ("libforces.so");
 writeControl timeStep; writeInterval 1; log yes;
 patches ("aurora.*"); rho rhoInf; rhoInf 1.1;
 CofR (0 0 0); liftDir (0 0 1); dragDir (-1 0 0); pitchAxis (0 1 0);
 magUInf 22.222222; lRef 5.998; Aref {args.area_m2};
 }} }}
''')
    write('constant/transportProperties', 'transportModel Newtonian; nu [0 2 -1 0 0 0 0] 1.7e-5;\n')
    write('constant/turbulenceProperties', 'simulationType RAS; RAS {RASModel kOmegaSST; turbulence on; printCoeffs on;}\n')
    write('system/fvSchemes', '''
ddtSchemes {default steadyState;}
gradSchemes {default Gauss linear; grad(U) cellLimited Gauss linear 1;}
divSchemes {default none; div(phi,U) bounded Gauss upwind; div(phi,k) bounded Gauss upwind;
 div(phi,omega) bounded Gauss upwind; div((nuEff*dev2(T(grad(U))))) Gauss linear;}
laplacianSchemes {default Gauss linear limited .5;}
interpolationSchemes {default linear;}
snGradSchemes {default limited .5;}
wallDist {method meshWave;}
''')
    write('system/fvSolution', '''
solvers {
 p {solver GAMG; tolerance 1e-7; relTol .1; smoother GaussSeidel;}
 "(U|k|omega)" {solver smoothSolver; smoother symGaussSeidel; tolerance 1e-7; relTol .1;}
}
SIMPLE {nNonOrthogonalCorrectors 1; consistent no;
 residualControl {p 1e-4; U 1e-5; "(k|omega)" 1e-5;}}
relaxationFactors {fields {p .3;} equations {U .7; k .7; omega .7;}}
''')
    # Piloto: U=-22.22 m/s, solo móvel, rodas estacionárias. I=.01 e L=.1 m assumidos.
    write('0/U', '''dimensions [0 1 -1 0 0 0 0]; internalField uniform (-22.222222 0 0);
boundaryField {
 inlet {type fixedValue; value uniform (-22.222222 0 0);}
 outlet {type zeroGradient;}
 ground {type fixedValue; value uniform (-22.222222 0 0);}
 "aurora.*" {type noSlip;}
 sides {type symmetry;} top {type symmetryPlane;}
}''', 'volVectorField')
    write('0/p', '''dimensions [0 2 -2 0 0 0 0]; internalField uniform 0;
boundaryField {inlet {type zeroGradient;} outlet {type fixedValue; value uniform 0;}
 ground {type zeroGradient;} "aurora.*" {type zeroGradient;}
 sides {type symmetry;} top {type symmetryPlane;}}''', 'volScalarField')
    for name, dim, initial, wall in [('k', '[0 2 -2 0 0 0 0]', '.074074', 'kqRWallFunction'),
                                      ('omega', '[0 0 -1 0 0 0 0]', '4.96904', 'omegaWallFunction'),
                                      ('nut', '[0 2 -1 0 0 0 0]', '0', 'nutkWallFunction')]:
        inlet = 'calculated' if name == 'nut' else 'fixedValue'
        write(f'0/{name}', f'''dimensions {dim}; internalField uniform {initial};
boundaryField {{inlet {{type {inlet}; value uniform {initial};}}
outlet {{type zeroGradient;}} ground {{type {wall}; value uniform {initial};}}
"aurora.*" {{type {wall}; value uniform {initial};}}
sides {{type symmetry;}} top {{type symmetryPlane;}}}}''', 'volScalarField')
    report = {'status': 'PILOTO_NAO_VALIDADO', 'superficie_sha256': hashlib.sha256(args.superficie.read_bytes()).hexdigest(),
              'area_referencia_m2': args.area_m2, 'velocity_m_s': 22.222222,
              'surface_levels': [args.nivel, args.nivel+1], 'requested_layers': args.camadas,
              'hipoteses': ['nu=1.7e-5 e rho=1.1 são valores piloto a revisar',
                           'Camadas solicitadas não garantem cobertura; conferir malha e y+',
                           'Rodas estacionárias; espelhos da malha de referência',
                           'Forma adaptada/reparada não homologada; Cd não é resultado final'],
              'codigo': 'scripts/preparar_cfd_piloto.py'}
    (out/'entrada_piloto.json').write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(out)


if __name__ == '__main__':
    main()
