"""Preparação experimental com controle de preservação de pneus e área.

Não certifica fidelidade da carroceria nem ausência de auto-interseções. Mantém
arquivo original; gera somente candidato para comissionamento de CFD.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))

import numpy as np
import pymeshfix
import trimesh

from motorhome.geometria_malha import area_frontal


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--entrada', type=Path, required=True)
    p.add_argument('--destino', type=Path, required=True)
    args = p.parse_args()
    scene = trimesh.load(args.entrada, force='scene')
    original = scene.to_mesh()
    parts = {'body': []}
    for node in scene.graph.nodes_geometry:
        mat, key = scene.graph[node]
        g = scene.geometry[key].copy()
        g.apply_transform(mat)
        if node.startswith('Wheel_'):
            # Selecionar pneu exterior, não cubo menor que .3 m (falha anterior).
            if g.extents[0] > .65:
                parts[node] = [g]
        elif node.startswith('Brake_Caliper_'):
            continue
        elif node.startswith('Mirror_'):
            side = 'left' if g.bounds.mean(axis=0)[1] > 0 else 'right'
            parts.setdefault('mirror_'+side, []).append(g)
        else:
            parts['body'].append(g)
    if sum(name.startswith('Wheel_') for name in parts) != 4:
        raise ValueError('Esperados quatro pneus externos da malha de referência')
    args.destino.mkdir(parents=True, exist_ok=False)
    out, repaired, stats = args.destino, [], []
    for name, geoms in parts.items():
        m = trimesh.util.concatenate(geoms)
        m.merge_vertices(digits_vertex=5)
        m.update_faces(m.unique_faces())
        m.update_faces(m.nondegenerate_faces())
        m.remove_unreferenced_vertices()
        v, f = pymeshfix.clean_from_arrays(np.asarray(m.vertices, dtype=np.float64),
                                          np.asarray(m.faces, dtype=np.int32),
                                          verbose=False, joincomp=True, remove_smallest_components=False)
        r = trimesh.Trimesh(v, f, process=False)
        if not r.is_watertight:
            raise ValueError(f'Componente aberto após reparo: {name}')
        if name.startswith('Wheel_') and not np.allclose(m.bounds, r.bounds, atol=.001):
            raise ValueError(f'Reparo destruiu o pneu: {name}')
        stats.append({'part': name, 'before_bounds_m': m.bounds.tolist(), 'after_bounds_m': r.bounds.tolist(),
                      'faces_before': len(m.faces), 'faces_after': len(r.faces), 'closed': bool(r.is_watertight)})
        r.export(out/(name+'.stl'))
        repaired.append(r)
    mesh = trimesh.util.concatenate(repaired)
    a0, a1 = area_frontal(original), area_frontal(mesh)
    relative = abs(a1-a0)/a0
    report = {'status': 'CANDIDATO_PILOTO_NAO_VALIDADO', 'script': 'scripts/reparar_superficie_piloto.py',
              'pymeshfix': pymeshfix.__version__, 'input_sha256': hashlib.sha256(args.entrada.read_bytes()).hexdigest(),
              'area_before_m2': a0, 'area_after_m2': a1, 'relative_area_change': relative,
              'bounds_before_m': original.bounds.tolist(), 'bounds_after_m': mesh.bounds.tolist(),
              'parts': stats, 'all_closed': bool(mesh.is_watertight), 'triangles': len(mesh.faces),
              'cfd_validated': False, 'self_intersections_verified': False,
              'limits': ['Pneus mantidos; detalhes menores substituídos/removidos pelo reparo',
                         'Diferença de silhueta <5% é filtro inicial, não validação de forma',
                         'Interseções entre peças e região de contato pneu/solo precisam de revisão']}
    (out/'manifesto_reparo.json').write_text(json.dumps(report, indent=2, ensure_ascii=False))
    if relative > .05:
        raise ValueError('Mudança de área >5%; candidato rejeitado')
    mesh.export(out/'aurora_cfd_m.stl')
    print(f'Candidato fechado: {len(mesh.faces)} faces; mudança de área {relative:.2%}; sem validação CFD')


if __name__ == '__main__':
    main()
