"""Adapta malha existente às cotas-alvo L3H2, com hipóteses explícitas.

Conserva rodas por translação rígida; forma intermediária é projeto autoral.
Não é CAD homologado Fiat e não fecha a superfície para CFD automaticamente.
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import trimesh
import yaml
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from motorhome.adaptacao_geometrica import adaptar_vertices
from motorhome.geometria_malha import area_frontal


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--entrada', type=Path, required=True)
    p.add_argument('--config', type=Path, required=True)
    p.add_argument('--destino', type=Path, required=True)
    args = p.parse_args()
    c = yaml.safe_load(args.config.read_text())
    chassis = c['chassis']
    s = trimesh.load(args.entrada, force='scene')
    before = s.to_mesh()
    rear, front = -1.4608, 1.5417  # marcos do ativo .xoma; não dados OEM
    wb = chassis['wheelbase_m']
    delta = wb-(front-rear)
    # Cabine/frente fixas. Alongamento no trecho de carga e ajuste do balanço traseiro.
    xmin, xmax = before.bounds[:, 0]
    xtarget = xmax-chassis['length_m']
    mx = ([xmin, rear+.38, front-.65, xmax],
          [xtarget, rear+.38-delta, front-.65, xmax])
    zmax = float(before.bounds[1, 2])
    # Extremo alto da faixa OEM é hipótese explícita de variante, não cota exclusiva.
    h = max(chassis['height_range_m'])
    mz = ([0., 1.35, zmax], [0., 1.35, h])
    adapted = trimesh.Scene()
    wheel_checks, triangles, colors = [], [], []
    for node in s.graph.nodes_geometry:
        matrix, key = s.graph[node]
        g = s.geometry[key].copy()
        g.apply_transform(matrix)
        original = g.vertices.copy()
        rigid = None
        if node.startswith(('Wheel_', 'Brake_Caliper_')):
            rigid = [-delta if g.bounds.mean(axis=0)[0] < 0 else 0., 0., 0.]
        g.vertices = adaptar_vertices(original, mx, mz, rigid)
        if rigid is not None:
            assert np.allclose(np.ptp(original, axis=0), g.extents, atol=1e-12)
            wheel_checks.append({'node': node, 'preserva_dimensoes': True, 'translacao_m': rigid})
        adapted.add_geometry(g, node_name=node, geom_name=node)
        triangles.append(g.triangles)
        mat = getattr(g.visual, 'material', None)
        color = getattr(mat, 'baseColorFactor', None)
        color = np.array(color if color is not None else [170, 185, 200, 255])/255
        if color[3] < .9:
            color = [.23, .45, .6, 1.]
        colors.append(np.tile(color, (len(g.faces), 1)))
    m = adapted.to_mesh()
    assert abs(m.extents[0]-chassis['length_m']) < 1e-6
    assert abs(m.bounds[1, 2]-h) < 1e-6
    args.destino.mkdir(parents=True, exist_ok=False)
    out = args.destino
    adapted.export(out/'aurora_L3H2_proposta_m.glb')
    m.export(out/'aurora_L3H2_proposta_m.stl')
    loaded = trimesh.load(out/'aurora_L3H2_proposta_m.stl', force='mesh')
    assert np.allclose(loaded.bounds, m.bounds, atol=1e-6)
    t, col = np.concatenate(triangles), np.concatenate(colors)
    fig = plt.figure(figsize=(11, 7), layout='constrained')
    ax = fig.add_subplot(111, projection='3d')
    ax.add_collection3d(Poly3DCollection(t, facecolors=col, edgecolors='none'))
    lo, hi = m.bounds
    ax.set(xlim=(lo[0]-.1, hi[0]+.1), ylim=(lo[1]-.1, hi[1]+.1), zlim=(0, hi[2]+.1),
           xlabel='X [m]', ylabel='Y [m]', zlabel='Z [m]')
    ax.set_box_aspect(m.extents.copy())
    ax.view_init(elev=20, azim=35)
    ax.set_title('Aurora Solar: adaptação autoral para L3H2 elétrica\n5,998 m; entre-eixos 4,035 m; teto-alvo 2,612 m')
    fig.text(.5, .01, 'Proposta geométrica — não CAD OEM. Derivado razor24 / Dogan Ulus; MPL-2.0 AND CC-BY-4.0.', ha='center', fontsize=9)
    fig.savefig(out/'aurora_L3H2_proposta.png', dpi=160)
    plt.close(fig)
    report = {'revision': 'adaptacao-0.1', 'status': 'PROPOSTA_AUTORAL_NAO_HOMOLOGADA',
              'data_utc': datetime.now(timezone.utc).isoformat(), 'script': 'scripts/adaptar_educato.py',
              'sha256_fonte': hashlib.sha256(args.entrada.read_bytes()).hexdigest(),
              'sha256_config': hashlib.sha256(args.config.read_bytes()).hexdigest(),
              'marcos_x_origem_destino_m': mx, 'marcos_z_origem_destino_m': mz,
              'rodas_componentes_preservados': wheel_checks,
              'wheelbase_alvo_m': wb, 'extensoes_m': m.extents.tolist(),
              'area_frontal_m2': area_frontal(m), 'triangulos': len(m.faces),
              'fechada': bool(m.is_watertight), 'cfd_executado': False,
              'limites': ['Largura da fonte preservada; espelhos dobrados, não posição de rodagem OEM',
                         'Altura 2,612 m é hipótese no extremo da faixa publicada',
                         'Região de carga alongada, teto elevado: forma aproximada autoral',
                         'Nenhuma aprovação física ou cálculo de volume habitável'],
              'hashes': {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in out.iterdir()}}
    (out/'manifesto.json').write_text(json.dumps(report, indent=2, ensure_ascii=False))
    (out/'ATTRIBUTION.txt').write_text('Derived from Fiat Ducato 2014, razor24 (2019), Dogan Ulus (2025), OpenX Assets 20261015.\nMPL-2.0 AND CC-BY-4.0.\nChanges: cargo-body lengthening, roof raising, rigid wheel translations; original dimensions not claimed.\nhttps://github.com/vevalabs/openx-assets/releases/tag/20261015\n')
    print(json.dumps({k: report[k] for k in ['extensoes_m', 'area_frontal_m2', 'fechada']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
