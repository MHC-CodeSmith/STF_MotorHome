"""Triagem amostral do topo do banheiro contra a malha visual aberta.

Não substitui colisão de sólidos CAD: primeira interseção transversal pode
pertencer a reforço/detalhe. Atesta apenas os raios declarados, não volume todo.
"""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import trimesh
import yaml


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--glb', type=Path, required=True)
    p.add_argument('--layout', type=Path, required=True)
    p.add_argument('--destino', type=Path, required=True)
    args = p.parse_args()
    scene = trimesh.load(args.glb, force='scene')
    triangles = scene.to_mesh().triangles
    layout = yaml.safe_load(args.layout.read_text())
    bath = next(z for z in layout['floor_zones'] if z['id'] == 'banheiro')
    # Mesmo alinhamento explicitamente assumido no visualizador.
    rear, floor = -3.35, .68
    direction = np.array([0., 1., 0.])
    e1, e2 = triangles[:, 1]-triangles[:, 0], triangles[:, 2]-triangles[:, 0]
    h = np.cross(np.broadcast_to(direction, e2.shape), e2)
    a = np.einsum('ij,ij->i', e1, h)
    mask = abs(a) > 1e-10
    factor = np.divide(1., a, out=np.zeros_like(a), where=mask)
    samples = []
    outer_y = -layout['cargo_m'][1]/2+bath['y_m']+bath['width_m']
    for x in np.linspace(rear+bath['x_m']+.02, rear+bath['x_m']+bath['length_m']-.02, 9):
        for z in np.linspace(floor+.05, floor+bath['height_m'], 9):
            offset = np.array([x, 0., z])-triangles[:, 0]
            u = factor*np.einsum('ij,ij->i', offset, h)
            q = np.cross(offset, e1)
            v = factor*np.einsum('j,ij->i', direction, q)
            t = factor*np.einsum('ij,ij->i', e2, q)
            hit = mask & (u >= 0) & (v >= 0) & (u+v <= 1) & (t > 0)
            first = float(t[hit].min()) if hit.any() else None
            samples.append({'x_m': float(x), 'z_m': float(z), 'first_hit_y_m': first,
                            'sample_clearance_m': first-outer_y if first is not None else None})
    rejected = [s for s in samples if s['sample_clearance_m'] is None or s['sample_clearance_m'] < .02]
    report = {'status': 'TRIAGEM_GEOMETRICA_AMOSTRAL_NAO_VALIDACAO_DE_ENCAIXE',
              'script': 'scripts/verificar_topo_banheiro.py', 'sample_count': len(samples),
              'sampled_clearance_at_least_20mm': not rejected, 'rejected_sample_count': len(rejected),
              'minimum_sampled_clearance_m': min((s['sample_clearance_m'] for s in samples if s['sample_clearance_m'] is not None), default=None),
              'alignment_assumed': {'rear_x_m': rear, 'floor_z_m': floor}, 'bathroom': bath,
              'geometry_is_open': True, 'interference_free_vehicle_verified': False,
              'note': 'Folga é contra superfície visual externa; não espessura/isolamento/estrutura reais. Amostragem não prova ausência de colisão entre amostras.',
              'inputs_sha256': {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in [args.glb, args.layout]},
              'samples': samples}
    args.destino.mkdir(parents=True, exist_ok=False)
    (args.destino/'triagem_banheiro.json').write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(json.dumps({k: report[k] for k in ['sample_count', 'rejected_sample_count', 'minimum_sampled_clearance_m']}))


if __name__ == '__main__':
    main()
