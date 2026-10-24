"""Executa ferramenta OpenFOAM da instalação local, sem alterar o sistema."""

import argparse
import os
import subprocess
from pathlib import Path


def ambiente(prefixo):
    p = Path(prefixo).resolve()
    if not (p/'bin/simpleFoam').is_file() or not (p/'share/openfoam/etc').is_dir():
        raise FileNotFoundError('Prefixo deve conter bin/simpleFoam e share/openfoam/etc')
    env = os.environ.copy()
    env.update(WM_PROJECT_DIR=str(p/'share/openfoam'), FOAM_ETC=str(p/'share/openfoam/etc'),
               FOAM_LIBBIN=str(p/'lib'), OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1')
    env['PATH'] = str(p/'bin')+os.pathsep+env.get('PATH', '')
    env['LD_LIBRARY_PATH'] = os.pathsep.join([str(p/'lib'), str(p/'lib/x86_64-linux-gnu'), env.get('LD_LIBRARY_PATH', '')])
    return env


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prefixo', type=Path, required=True)
    p.add_argument('--caso', type=Path, required=True)
    p.add_argument('--ferramenta', choices=['blockMesh', 'snappyHexMesh', 'checkMesh', 'simpleFoam', 'surfaceCheck'], required=True)
    p.add_argument('--timeout', type=float, default=300)
    p.add_argument('--somente-campos', action='store_true', help='Desativa functionObjects; não gera forças/Cd')
    args = p.parse_args()
    caso = args.caso.resolve()
    command = [args.ferramenta, '-case', str(caso)]
    if args.ferramenta == 'snappyHexMesh':
        command += ['-overwrite']
    if args.ferramenta == 'surfaceCheck':
        command = ['surfaceCheck', str(caso/'constant/triSurface/aurora.stl')]
    if args.somente_campos:
        if args.ferramenta != 'simpleFoam':
            raise ValueError('--somente-campos é exclusivo de simpleFoam')
        command += ['-noFunctionObjects']
    log = caso/f'log.{args.ferramenta}'
    if args.somente_campos:
        log = caso/'log.simpleFoam.fields'
    if log.exists():
        raise FileExistsError(f'Log existente: {log}; preservar execução anterior')
    with log.open('w') as stream:
        result = subprocess.run(command, env=ambiente(args.prefixo), cwd=caso, check=False,
                                stdout=stream, stderr=subprocess.STDOUT, timeout=args.timeout)
    print(f'{args.ferramenta}: saída {result.returncode}; log {log}')
    if args.ferramenta == 'checkMesh' and 'Mesh OK.' not in log.read_text():
        raise SystemExit('Malha recusada: checkMesh não confirmou Mesh OK, mesmo com saída 0')
    raise SystemExit(result.returncode)


if __name__ == '__main__':
    main()
