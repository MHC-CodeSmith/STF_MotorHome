"""Compara logs realmente convergidos; não certifica independência de malha."""

import argparse
import hashlib
import json
import re
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt


def read_case(case, field_log, force_log):
    files = {'mesh': case/'log.checkMesh', 'fields': case/field_log, 'forces': case/force_log}
    texts = {key: path.read_text() for key, path in files.items()}
    if 'Mesh OK.' not in texts['mesh']:
        raise ValueError(f'Malha rejeitada: {case}')
    convergence = re.search(r'SIMPLE solution converged in (\d+) iterations', texts['fields'])
    cds = re.findall(r'Cd:\s+([\d.eE+\-]+)\s+([\d.eE+\-]+)\s+([\d.eE+\-]+)', texts['forces'])
    if convergence is None or not cds:
        raise ValueError(f'Campos convergidos/forças ausentes: {case}')
    return {'case': str(case), 'cells': int(re.search(r'cells:\s+(\d+)', texts['mesh'])[1]),
            'iterations': int(convergence[1]), 'cd': float(cds[-1][0]),
            'cd_pressure': float(cds[-1][1]), 'cd_viscous': float(cds[-1][2]),
            'max_nonorthogonality_deg': float(re.search(r'non-orthogonality Max:\s+([\d.]+)', texts['mesh'])[1]),
            'max_skewness': float(re.search(r'Max skewness =\s+([\d.]+)', texts['mesh'])[1]),
            'logs_sha256': {key: {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()} for key, path in files.items()}}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cache', type=Path, required=True)
    p.add_argument('--destino', type=Path, required=True)
    args = p.parse_args()
    # v1912 calculou campos; os mesmos campos foram copiados para pós-processar
    # com 2412 por falha IOstream de forceCoeffs na instalação antiga.
    coarse_case = args.cache/'cfd-aurora-piloto-03'
    force_case = args.cache/'cfd-aurora-2412-01'
    # Leitura individual permite hashes distintos sem copiar/alterar logs antigos.
    text = (force_case/'log.postprocess2412-02').read_text()
    mesh = (coarse_case/'log.checkMesh').read_text()
    fields = (coarse_case/'log.simpleFoam.fields').read_text()
    if 'Mesh OK.' not in mesh or 'SIMPLE solution converged' not in fields:
        raise ValueError('Piloto grosseiro sem evidências válidas')
    cd = re.findall(r'Cd:\s+([\d.eE+\-]+)\s+([\d.eE+\-]+)\s+([\d.eE+\-]+)', text)[-1]
    coarse = {'case': str(coarse_case), 'cells': int(re.search(r'cells:\s+(\d+)', mesh)[1]),
              'iterations': int(re.search(r'SIMPLE solution converged in (\d+) iterations', fields)[1]),
              'cd': float(cd[0]), 'cd_pressure': float(cd[1]), 'cd_viscous': float(cd[2]),
              'logs_sha256': {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in [coarse_case/'log.checkMesh', coarse_case/'log.simpleFoam.fields', force_case/'log.postprocess2412-02']}}
    cases = [coarse,
             read_case(args.cache/'cfd-aurora-refino-semcamadas-01', 'log.simpleFoam', 'log.simpleFoam'),
             read_case(args.cache/'cfd-aurora-refino-semcamadas-02', 'log.simpleFoam', 'log.forcas')]
    comparison = {'status': 'PILOTOS_NAO_VALIDADOS', 'script': 'scripts/comparar_pilotos_cfd.py',
                  'cases': cases, 'mesh_independent': False, 'validated_cd': None,
                  'last_relative_change': abs(cases[-1]['cd']-cases[-2]['cd'])/cases[-2]['cd'],
                  'area_reference_m2': 4.827840375264284, 'speed_m_s': 22.222222,
                  'density_assumed_kg_m3': 1.1,
                  'limitations': ['Sem camadas/y+ verificado', 'Rodas estacionárias',
                                  'Geometria autoral reparada sem validação física',
                                  'Cobertura espacial de refinamento não uniforme; sem extrapolação Richardson/GCI',
                                  'Variação de Cd ainda relevante',
                                  'Refinos com camadas divergiram e foram rejeitados',
                                  'Resíduos baixos não equivalem a validação experimental']}
    args.destino.mkdir(parents=True, exist_ok=False)
    (args.destino/'comparacao_cfd.json').write_text(json.dumps(comparison, indent=2, ensure_ascii=False))
    fig, ax = plt.subplots(figsize=(8, 4.5), layout='constrained')
    ax.plot([c['cells'] for c in cases], [c['cd'] for c in cases], 'o-', color='#255e84')
    for c in cases:
        ax.annotate(f"Cd {c['cd']:.4f}", (c['cells'], c['cd']), xytext=(5, 7), textcoords='offset points')
    ax.set(xlabel='Número de células', ylabel='Cd exploratório',
           title='Aurora Solar — estudo de refinamento incompleto\nSem independência de malha ou validação física')
    ax.set_ylim(.54, .69); ax.grid(alpha=.3)
    fig.savefig(args.destino/'comparacao_cfd.png', dpi=160); plt.close(fig)
    print(json.dumps({'cases': [{k: c[k] for k in ['cells', 'iterations', 'cd']} for c in cases],
                      'last_relative_change': comparison['last_relative_change']}))


if __name__ == '__main__':
    main()
