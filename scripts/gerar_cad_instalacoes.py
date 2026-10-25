"""CAD autoral de integração em GLB/STEP: interior e cobertura solar deslizante.

Primitivas sólidas parametrizadas; detalhes visuais não são desenhos OEM.
Sem solver estrutural, mecanismo homologado ou comprovação de montagem.
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))

import gmsh
import numpy as np
import trimesh
import yaml

from motorhome.ocupacao import arranjos_em_grade, verificar_caixas


class Modelo:
    def __init__(self):
        self.parts = []

    def box(self, name, group, lo, size, color):
        self.parts.append({'type': 'box', 'name': name, 'group': group,
                           'lo': list(lo), 'size': list(size), 'color': color})

    def cylinder(self, name, group, center, radius, length, color, axis=(0, 0, 1)):
        self.parts.append({'type': 'cylinder', 'name': name, 'group': group,
                           'center': list(center), 'radius': radius, 'length': length,
                           'axis': list(axis), 'color': color})

    def ring(self, name, group, center, major, minor, color, axis=(0, 0, 1)):
        self.parts.append({'type': 'ring', 'name': name, 'group': group,
                           'center': list(center), 'major': major, 'minor': minor,
                           'axis': list(axis), 'color': color})

    def tube(self, name, group, lo, length, side, wall, axis, color):
        # Quatro paredes, sem perfis maciços fictícios; cantos não sobrepostos.
        a, b = [i for i in range(3) if i != axis]
        for j in range(4):
            pos = np.array(lo, dtype=float)
            size = np.full(3, side)
            size[axis] = length
            if j < 2:
                size[a] = wall
                pos[a] += j*(side-wall)
            else:
                size[b] = wall
                size[a] = side-2*wall
                pos[a] += wall
                pos[b] += (j-2)*(side-wall)
            self.box(f'{name}_{j}', group, pos, size, color)

    def export(self, out, stem, alignment):
        scene = trimesh.Scene()
        offset = np.array([alignment['rear_x_m'], -alignment['cargo_width_m']/2, alignment['floor_z_m']])
        gmsh.initialize()
        try:
            gmsh.option.setNumber('General.Terminal', 0)
            gmsh.model.add(stem)
            for index, p in enumerate(self.parts):
                if p['type'] == 'box':
                    size = np.array(p['size'])
                    lo = np.array(p['lo'])+offset
                    mesh = trimesh.creation.box(extents=size)
                    mesh.apply_translation(lo+size/2)
                    tag = gmsh.model.occ.addBox(*lo, *size)
                else:
                    center = np.array(p['center'])+offset
                    axis = np.array(p['axis'], dtype=float)
                    if p['type'] == 'cylinder':
                        mesh = trimesh.creation.cylinder(p['radius'], p['length'], sections=32)
                        start = center-axis*p['length']/2
                        tag = gmsh.model.occ.addCylinder(*start, *(axis*p['length']), p['radius'])
                    else:
                        mesh = trimesh.creation.torus(p['major'], p['minor'], major_sections=32, minor_sections=12)
                        tag = gmsh.model.occ.addTorus(*center, p['major'], p['minor'], zAxis=axis.tolist())
                    mesh.apply_transform(trimesh.geometry.align_vectors([0, 0, 1], axis))
                    mesh.apply_translation(center)
                mesh.visual = trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(
                    baseColorFactor=p['color'], metallicFactor=.15, roughnessFactor=.65,
                    alphaMode='BLEND' if p['color'][3] < 255 else 'OPAQUE', doubleSided=True))
                mesh.metadata.update(component=p['group'], authored_integration_model=True)
                scene.add_geometry(mesh, geom_name=f'{index}_{p["name"]}', node_name=f'{p["group"]}__{index}_{p["name"]}')
                p['cad_volume_tag'] = tag
            gmsh.model.occ.synchronize()
            for p in self.parts:
                gmsh.model.setEntityName(3, p['cad_volume_tag'], p['group']+'__'+p['name'])
            gmsh.write(str(out/f'{stem}.step'))
        finally:
            gmsh.finalize()
        scene.export(out/f'{stem}.glb')


def interior(c):
    m = Modelo()
    wood, pale = [180, 137, 90, 255], [222, 210, 187, 255]
    metal, dark = [174, 187, 195, 255], [32, 43, 51, 255]
    m.box('piso', 'piso', [.015, .035, -.018], [3.67, 1.8, .018], pale)
    # Cama longitudinal elevada: estrado, travessas, colchão, travesseiros e escada.
    m.box('estrado', 'cama', [.02, .04, .90], [1.95, 1.35, .03], wood)
    m.box('colchao', 'cama', [.04, .06, .93], [1.91, 1.31, .12], [102, 154, 142, 255])
    for y in [.13, .79]:
        m.box('travesseiro', 'cama', [.10, y, 1.05], [.37, .5, .08], [240, 237, 221, 255])
    for x in [.02, 1.92]:
        for y in [.04, 1.34]:
            m.box('poste', 'cama', [x, y, 0], [.045, .045, .9], wood)
    for z in [.23, .48, .73]:
        m.box('degrau_retratil', 'cama', [1.75, 1.42, z], [.20, .32, .04], wood)
    # Galley, incluindo aberturas reais no tampo em torno da cuba e da indução.
    for x in [1.97, 2.48, 2.93, 3.35]:
        m.box('divisoria', 'cozinha', [x, .04, .02], [.018, .58, .87], wood)
    for x, length in [(1.97, .54), (2.91, .06), (3.32, .05)]:
        m.box('tampo', 'cozinha', [x, .04, .89], [length, .58, .03], pale)
    for x, length, y0, y1 in [(2.51, .40, .14, .52), (2.97, .35, .16, .51)]:
        m.box('tampo_borda_parede', 'cozinha', [x, .04, .89], [length, y0-.04, .03], pale)
        m.box('tampo_borda_frente', 'cozinha', [x, y1, .89], [length, .62-y1, .03], pale)
    m.box('porta_gabinete', 'cozinha', [2.50, .602, .07], [.40, .018, .65], wood)
    for z in [.10, .36, .61]:
        m.box('gaveta', 'cozinha', [2.96, .602, z], [.36, .018, .22], wood)
        m.cylinder('puxador', 'cozinha', [3.14, .636, z+.12], .008, .18, metal, (1, 0, 0))
    for item in c['items']:
        x, y, z = item['position_xyz_m']
        dx, dy, dz = item['dimensions_xyz_m']
        group, kind = item['id'], item['model']
        if kind == 'sink':
            m.box('fundo_cuba', group, [x, y, z], [dx, dy, .008], metal)
            for px in [x, x+dx-.008]:
                m.box('lateral_cuba', group, [px, y, z], [.008, dy, dz], metal)
            for py in [y, y+dy-.008]:
                m.box('frente_cuba', group, [x+.008, py, z], [dx-.016, .008, dz], metal)
            m.cylinder('torneira', group, [x+.08, y-.03, z+dz+.10], .012, .20, metal)
            m.cylinder('bica', group, [x+.08, y+.03, z+dz+.19], .012, .12, metal, (0, 1, 0))
            continue
        color = ([235, 237, 237, 255] if kind in ['washer', 'toilet'] else
                 [78, 96, 110, 255] if kind == 'fridge' else
                 [28, 74, 105, 150] if kind == 'water' else metal)
        if kind == 'toilet':
            m.box('tanque_inferior', group, [x, y, z], [dx, dy, .22], color)
            m.box('tanque_superior', group, [x+.02, y+.02, z+.22], [dx-.04, dy-.04, .15], color)
            m.ring('assento', group, [x+dx/2, y+dy/2, z+dz-.02], .133, .025, color)
            m.cylinder('tampa', group, [x+dx/2, y+dy/2, z+dz-.004], .13, .008, color)
        else:
            m.box('carcaca', group, [x, y, z], [dx, dy, dz], dark if kind == 'cooktop' else color)
        if kind == 'washer':
            m.cylinder('vidro_porta', group, [x+dx/2, y+dy+.004, z+.40], .195, .012, dark, (0, 1, 0))
            m.ring('aro_porta', group, [x+dx/2, y+dy+.014, z+.40], .197, .025, metal, (0, 1, 0))
            m.box('display', group, [x+.27, y+dy+.003, z+.69], [.26, .006, .09], dark)
            m.cylinder('seletor', group, [x+.17, y+dy+.015, z+.735], .038, .025, metal, (0, 1, 0))
        if kind == 'fridge':
            m.box('porta', group, [x+.01, y+dy, z+.01], [dx-.02, .012, dz-.02], [63, 71, 77, 255])
            m.box('puxador', group, [x+dx-.09, y+dy+.015, z+dz-.08], [.06, .01, .025], metal)
        if kind == 'hvac':
            for i in range(3):
                m.cylinder('saida_duto', group, [x+.13+i*.17, y+dy+.025, z+.17], .03, .05, dark, (0, 1, 0))
            for i in range(9):
                m.box('grelha', group, [x+.04+i*.06, y-.004, z+.04], [.025, .007, .18], dark)
        if kind == 'cooktop':
            m.ring('zona_inducao', group, [x+dx/2, y+dy/2, z+dz+.001], .092, .002, [190, 194, 194, 255])
            for i in range(5):
                m.cylinder('touch', group, [x+.07+i*.045, y+dy-.035, z+dz+.002], .006, .001, metal)
    # Wetbath translúcido, chuveiro, bandeja e porta deslizante transparente.
    bath = [88, 160, 173, 85]
    m.box('bandeja', 'banheiro', [1.985, 1.115, .01], [.87, .67, .03], [238, 236, 224, 255])
    for x in [1.97, 2.855]:
        m.box('parede', 'banheiro', [x, 1.10, .04], [.015, .70, 1.76], bath)
    m.box('parede_externa', 'banheiro', [1.97, 1.785, .04], [.90, .015, 1.76], bath)
    m.box('porta_correr', 'banheiro', [1.98, 1.10, .04], [.87, .008, 1.72], [130, 196, 198, 55])
    m.cylinder('coluna_ducha', 'banheiro', [2.78, 1.75, 1.10], .012, 1.1, metal)
    m.cylinder('chuveiro', 'banheiro', [2.78, 1.68, 1.68], .065, .018, metal)
    # Mesa rebatível e tela, sem assento de viagem extra homologado.
    m.box('mesa_rebativel', 'dinette', [2.96, 1.12, .74], [.60, .64, .025], wood)
    m.cylinder('pedestal', 'dinette', [3.24, 1.46, .38], .022, .72, metal)
    m.box('tela', 'eletronicos', [3.48, 1.76, 1.10], [.012, .05, .30], dark)
    # Dois assentos ilustrativos na cabine, mantidos como parte da massa OEM.
    for y in [.23, 1.12]:
        m.box('base_assento', 'assentos_oem', [4.05, y, .12], [.48, .48, .35], dark)
        m.box('almofada', 'assentos_oem', [4.03, y-.01, .47], [.53, .5, .09], [66, 81, 91, 255])
        m.box('encosto', 'assentos_oem', [4.03, y-.01, .56], [.10, .5, .64], [66, 81, 91, 255])
        m.box('encosto_cabeca', 'assentos_oem', [4.03, y+.10, 1.2], [.10, .28, .16], dark)
    # Apoios telescópicos guardados sob a cama; tubos ocos, não barras maciças.
    for i in range(6):
        for side in [.035, .030, .025]:
            m.tube('apoio_guardado', 'apoios_guardados', [.09, .51+(i%3)*.055, .31+(i//3)*.055],
                   1.02, side, .002, 0, metal)
    return m


def altura_superficie(mesh, x, y):
    triangles = mesh.triangles
    direction = np.array([0., 0., -1.])
    e1, e2 = triangles[:, 1]-triangles[:, 0], triangles[:, 2]-triangles[:, 0]
    h = np.cross(np.broadcast_to(direction, e2.shape), e2)
    a = np.einsum('ij,ij->i', e1, h)
    factor = np.divide(1., a, out=np.zeros_like(a), where=abs(a) > 1e-10)
    off = np.array([x, y, 3.5])-triangles[:, 0]
    u = factor*np.einsum('ij,ij->i', off, h)
    q = np.cross(off, e1)
    v = factor*np.einsum('j,ij->i', direction, q)
    t = factor*np.einsum('ij,ij->i', e2, q)
    ok = (abs(a) > 1e-10) & (u >= 0) & (v >= 0) & (u+v <= 1) & (t > 0)
    if not ok.any():
        raise ValueError(f'Sapata sem superfície abaixo: {x},{y}')
    z = 3.5-float(t[ok].min())
    if z < 2:
        raise ValueError('Apoio não encontrou teto superior')
    return z


def cobertura(layout, aberta, mesh, alignment, extensao=True):
    roof = layout['roof']
    m = Modelo()
    metal = [180, 188, 194, 255]
    length = roof['modules']*roof['module_length_x_m']+(roof['modules']-1)*roof['gap_m']
    sx = roof['start_x_m']
    sy = (layout['cargo_m'][1]-roof['module_width_y_m'])/2
    roof_z = 2.612-.68
    bottom = roof_z+roof['support_height_m']
    # Duas longarinas tubulares30x30x3, três travessas40x40x3.
    for y in [.20, 1.64]:
        m.tube('longarina_30x30x3', 'suportes', [sx, y, roof_z+.03], length, .030, .003, 0, metal)
    for i in range(3):
        x = sx+i*(roof['module_length_x_m']+roof['gap_m'])+.50
        m.tube('travessa_40x40x3', 'suportes', [x, .06, roof_z+.06], 1.75, .040, .003, 1, metal)
        for y in [.20, 1.64]:
            zskin = altura_superficie(mesh, alignment['rear_x_m']+x,
                                     -alignment['cargo_width_m']/2+y)-alignment['floor_z_m']
            m.box('sapata', 'suportes', [x-.04, y-.04, zskin], [.12, .10, .012], metal)
            m.box('pe_suporte', 'suportes', [x, y, zskin+.012], [.025, .025, roof_z+.03-zskin-.012], metal)
    for layer in ((0, 1) if extensao else (0,)):
        shift = (roof['module_width_y_m']+roof['extension_lateral_gap_m']) if layer and aberta else 0
        z = bottom+layer*(roof['module_thickness_m']+roof['extension_vertical_gap_m'])
        for i in range(roof['modules']):
            x = sx+i*(roof['module_length_x_m']+roof['gap_m'])
            y = sy+shift
            group = 'solar_movel' if layer else 'solar_fixo'
            dx, dy, dz = roof['module_length_x_m'], roof['module_width_y_m'], roof['module_thickness_m']
            m.box('modulo450W', group, [x, y, z], [dx, dy, dz], [18, 46, 77, 255])
            for xx in [x, x+dx-.018]:
                m.box('moldura', group, [xx, y, z], [.018, dy, dz+.002], metal)
            for yy in [y, y+dy-.018]:
                m.box('moldura', group, [x+.018, yy, z], [dx-.036, .018, dz+.002], metal)
            for a in range(3):
                for b in range(6):
                    m.box('celulas', group, [x+.035+a*(dx-.07)/3, y+.035+b*(dy-.07)/6, z+dz+.002],
                          [(dx-.09)/3, (dy-.10)/6, .001], [37, 69, 103, 255])
            # Corrediça conceitual independente de cada módulo; sem alegar capacidade.
            rail_length = dy+shift
            if extensao:
                m.tube('guia_corredica', 'suportes', [x+.10, sy, z-.03], rail_length, .025, .003, 1, metal)
            if aberta and layer:
                for xx in [x+.12, x+dx-.12]:
                    total = z+.68
                    for stage, side in enumerate([.035, .030, .025]):
                        height = total/3+(.10 if stage < 2 else 0)
                        m.tube('perna_telescopica', 'apoios_solo',
                               [xx, y+dy-.12, -.68+stage*total/3], height, side, .002, 2, metal)
    cab = roof['cab_module']
    x, dx, dy, dz = cab['start_x_m'], cab['length_x_m'], cab['width_y_m'], cab['thickness_m']
    y = (layout['cargo_m'][1]-dy)/2
    m.box('modulo190W', 'solar_cabine', [x, y, bottom], [dx, dy, dz], [18, 46, 77, 255])
    for xx in [x, x+dx-.018]:
        m.box('moldura190', 'solar_cabine', [xx, y, bottom], [.018, dy, dz+.002], metal)
    for yy in [y, y+dy-.018]:
        m.box('moldura190', 'solar_cabine', [x+.018, yy, bottom], [dx-.036, .018, dz+.002], metal)
    for i in range(4):
        for j in range(6):
            m.box('celula190', 'solar_cabine', [x+.025+i*(dx-.05)/4, y+.025+j*(dy-.05)/6, bottom+dz+.002],
                  [(dx-.07)/4, (dy-.08)/6, .001], [37, 69, 103, 255])
    for xx in [x+.10, x+dx-.10]:
        m.tube('travessa_cabine', 'suportes', [xx, y, bottom-.04], dy, .04, .003, 1, metal)
        for yy in [y+.12, y+dy-.12]:
            zskin = altura_superficie(mesh, alignment['rear_x_m']+xx,
                                     -alignment['cargo_width_m']/2+yy)-alignment['floor_z_m']
            m.box('sapata_cabine', 'suportes', [xx-.04, yy-.04, zskin], [.10, .10, .012], metal)
            m.box('pe_cabine', 'suportes', [xx, yy, zskin+.012], [.025, .025, bottom-.04-zskin-.012], metal)
    return m


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--equipamentos', type=Path, default=Path('config/equipamentos_interior.yaml'))
    p.add_argument('--layout', type=Path, default=Path('config/layout_proposto.yaml'))
    p.add_argument('--destino', type=Path, required=True)
    p.add_argument('--carroceria', type=Path, default=Path('entregas/parcial_2026-10-24/aurora_L3H2_proposta_m.glb'))
    args = p.parse_args()
    c, layout = [yaml.safe_load(path.read_text()) for path in [args.equipamentos, args.layout]]
    check = verificar_caixas(c['items'], layout['cargo_m'])
    if not check['envelope_check_passed']:
        raise ValueError(check)
    args.destino.mkdir(parents=True, exist_ok=False)
    mesh = trimesh.load(args.carroceria, force='scene').to_mesh()
    models = {'interior_equipado': interior(c),
              'cobertura_fixa': cobertura(layout, False, mesh, c['alignment_assumed'], False),
              'cobertura_recolhida': cobertura(layout, False, mesh, c['alignment_assumed']),
              'cobertura_aberta': cobertura(layout, True, mesh, c['alignment_assumed'])}
    for name, model in models.items():
        model.export(args.destino, name, c['alignment_assumed'])
    roof = layout['roof']
    frame = models['cobertura_recolhida']
    aluminum_vol = sum(float(np.prod(p['size'])) for p in frame.parts if p['type'] == 'box' and p['group'] == 'suportes')
    fixed_vol = sum(float(np.prod(p['size'])) for p in models['cobertura_fixa'].parts if p['type'] == 'box' and p['group'] == 'suportes')
    result = {
        'revision': c['revision'], 'created_utc': datetime.now(timezone.utc).isoformat(),
        'status': c['status'], 'script': 'scripts/gerar_cad_instalacoes.py',
        'equipment_envelopes': check, 'equipment': c['items'], 'alignment_assumed': c['alignment_assumed'],
        'part_counts': {name: len(model.parts) for name, model in models.items()},
        'roof_grid': arranjos_em_grade(*layout['cargo_m'][:2], 1.134, 1.762, .03, .05),
        'installed_pv_w': 2890, 'exposed_stowed_pv_w': 1540, 'exposed_deployed_pv_w': 2890,
        'module_mass_kg': 142.5, 'frame_solid_volume_m3': aluminum_vol,
        'frame_mass_estimate_at_2700kg_m3': aluminum_vol*2700,
        'fixed_array_module_mass_kg': 76.5,
        'fixed_frame_mass_estimate_at_2700kg_m3': fixed_vol*2700,
        'fixed_roof_mass_estimate_kg': 76.5+fixed_vol*2700,
        'stacked_roof_mass_estimate_kg': 142.5+aluminum_vol*2700,
        'height_fixed_m': 2.612+roof['support_height_m']+roof['module_thickness_m']+.003,
        'height_stowed_m': 2.612+roof['support_height_m']+2*roof['module_thickness_m']+roof['extension_vertical_gap_m']+.003,
        'array_deployed_width_m': 2*roof['module_width_y_m']+roof['extension_lateral_gap_m'],
        'interference_free_vehicle_verified': False,
        'limitations': ['Envelopes nominais sem sobreposição não verificam portas/mangueiras/manutenção/malha externa.',
                        'Lava-seca total620mm; porta aberta1100mm pode bloquear corredor; fixação/vibração pendentes.',
                        'Longarinas/travessas/corrediças e apoios são conceituais; carga do teto OEM, cálculo estrutural e travas ainda pendentes.',
                        'Recolhida, camada superior sombreia a inferior: só três módulos expostos, não seis.',
                        'Extensão aberta só estacionado; operação com vento e drenagem ainda não dimensionadas.',
                        'Assentos OEM ilustrativos não são assentos adicionais homologados; massa já incluída no veículo-base.',
                        'Detalhes CAD autorais de integração, não geometrias OEM de fabricação.'],
        'inputs_sha256': {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in [args.equipamentos, args.layout, args.carroceria]},
        'outputs_sha256': {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(args.destino.iterdir())},
    }
    (args.destino/'manifesto_instalacoes.json').write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(json.dumps({key: value for key, value in result.items() if key not in ['equipment', 'outputs_sha256']}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
