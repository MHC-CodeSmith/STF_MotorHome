"""CAD autoral de alternativa portátil: quatro painéis no solo e bolsas verticais."""

import argparse
import hashlib
import json
from pathlib import Path

import gmsh
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import trimesh
import yaml
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--destino', type=Path, required=True)
    p.add_argument('--resumo', type=Path, required=True)
    args = p.parse_args()
    cfg_path = Path('config/solar_portatil_proposta.yaml')
    c = yaml.safe_load(cfg_path.read_text())
    result = json.loads(args.resumo.read_text())
    args.destino.mkdir(parents=True, exist_ok=False)
    parts = []

    def box(name, lo, size, color, angle=0., origin=(0, 0, 0)):
        parts.append({'name': name, 'lo': lo, 'size': size, 'color': color, 'angle': angle, 'origin': origin})

    for case in result['case_envelopes_interior']:
        x, y, z = case['position_xyz_m']
        x, y, z = x-3.35, y-.935, z+.68
        dx, dy, dz = case['dimensions_xyz_m']
        box(case['id'], [x, y, z], [dx, dy, dz], [37, 45, 53, 255])
        for fraction in [.15, .80]:
            box('cinta_'+case['id'], [x+fraction*dx, y-.001, z], [.025, .002, dz], [112, 121, 127, 255])
        box('alca_'+case['id'], [x+dx*.4, y+.01, z+dz], [dx*.2, .025, .025], [74, 83, 92, 255])
    length, width, thickness = c['module']['open_dimensions_m']
    angle = np.deg2rad(c['assumed']['ground_tilt_deg'])
    for index in range(4):
        x = -3.1+(index % 2)*(length+.15)
        y = -2.3-(index//2)*2.0
        origin = (x, y, .05)
        for fold in range(4):
            lo = [x+fold*length/4, y, .05]
            box(f'painel{index+1}_dobra{fold+1}', lo, [length/4-.008, width, thickness], [29, 43, 58, 255], angle, origin)
            for col in range(3):
                for row in range(6):
                    pos = [lo[0]+.025+col*(length/4-.04)/3, y+.025+row*(width-.04)/6, .05+thickness]
                    box('celulas', pos, [(length/4-.07)/3, (width-.09)/6, .001], [29, 70, 119, 255], angle, origin)
        # Volumes representativos da bolsa/suporte; não desenho OEM ou fixação dimensionada.
        box('apoio_solo', [x+.05, y+.05, .01], [length-.1, .05, .03], [110, 117, 123, 255])
    scenes = {'solo': trimesh.Scene(), 'transporte': trimesh.Scene()}
    gmsh.initialize()
    try:
        gmsh.option.setNumber('General.Terminal', 0)
        gmsh.model.add('solar_portatil')
        for i, part in enumerate(parts):
            size, lo = np.array(part['size']), np.array(part['lo'])
            mesh = trimesh.creation.box(extents=size)
            mesh.apply_translation(lo+size/2)
            tag = gmsh.model.occ.addBox(*lo, *size)
            if part['angle']:
                mesh.apply_transform(trimesh.transformations.rotation_matrix(part['angle'], [1, 0, 0], part['origin']))
                gmsh.model.occ.rotate([(3, tag)], *part['origin'], 1, 0, 0, part['angle'])
            mesh.visual = trimesh.visual.ColorVisuals(mesh=mesh, face_colors=part['color'])
            mesh.metadata.update(authored_integration_model=True, not_oem_cad=True)
            category = 'transporte' if part['name'].startswith(('bolsa', 'cinta', 'alca')) else 'solo'
            scenes[category].add_geometry(mesh, geom_name=f'{i}_{part["name"]}')
        gmsh.model.occ.synchronize()
        gmsh.write(str(args.destino/'solar_portatil.step'))
        gmsh.clear()
        gmsh.model.occ.importShapes(str(args.destino/'solar_portatil.step'))
        gmsh.model.occ.synchronize()
        volumes = [gmsh.model.occ.getMass(3, tag) for _, tag in gmsh.model.getEntities(3)]
        if len(volumes) != len(parts) or min(volumes) <= 0:
            raise ValueError('Falha na reimportação STEP')
    finally:
        gmsh.finalize()
    for category, scene in scenes.items():
        scene.export(args.destino/f'solar_portatil_{category}.glb')
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(projection='3d')
    for mesh in scenes['solo'].geometry.values():
        ax.add_collection3d(Poly3DCollection(mesh.triangles, facecolors=np.asarray(mesh.visual.face_colors)/255, edgecolors='none'))
    # Contexto do veículo é a malha detalhada existente, sem gerar novo bloco.
    body = trimesh.load('entregas/parcial_2026-10-24/aurora_L3H2_proposta_m.glb', force='scene')
    for mesh in body.geometry.values():
        ax.add_collection3d(Poly3DCollection(mesh.triangles, facecolors=[.72, .76, .78, .25], edgecolors='none'))
    ax.set(xlim=(-4, 3), ylim=(-6, 2), zlim=(0, 3), xlabel='X (m)', ylabel='Y (m)', zlabel='Z (m)',
           title='Alternativa estacionada • 4×400 W no solo • arranjo ilustrativo')
    ax.set_box_aspect((7, 8, 3)); ax.view_init(elev=28, azim=-135)
    fig.savefig(args.destino/'solar_portatil.png', dpi=150); plt.close(fig)
    manifest = {'status': c['status'], 'positive_step_volumes': len(parts),
                'storage': 'Bolsas verticais sob cama; envelopes assumidos, sem projeto de ancoragem.',
                'ground': 'Posições ilustrativas; sem cálculo de sombra entre fileiras/vento/ancoragem.',
                'inputs_sha256': {str(f): hashlib.sha256(f.read_bytes()).hexdigest() for f in
                                 [cfg_path, args.resumo, Path(__file__), Path('entregas/parcial_2026-10-24/aurora_L3H2_proposta_m.glb')]}}
    (args.destino/'manifesto_cad_portatil.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False)+'\n')
    print(len(parts), 'sólidos STEP reimportados positivos; GLB solo/transporte separados.')


if __name__ == '__main__':
    main()
