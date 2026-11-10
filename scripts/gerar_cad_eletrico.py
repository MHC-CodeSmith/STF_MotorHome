"""Conjuntos autorais de integração elétrica; envelopes de tração são estimativas."""

import argparse
import hashlib
import itertools
import json
from datetime import datetime, timezone
from pathlib import Path

import gmsh
import numpy as np
import yaml
from gerar_cad_instalacoes import Modelo

BLUE = [31, 115, 174, 255]
METAL = [150, 165, 176, 255]
DARK = [38, 48, 57, 255]
ORANGE = [245, 113, 24, 255]


def linha(m, name, group, points, radius, color):
    """Trechos retilíneos com cotovelos esféricos não incluídos; rota conceitual."""
    for a, b in itertools.pairwise(points):
        a, b = np.array(a), np.array(b)
        delta = b-a
        length = float(np.linalg.norm(delta))
        if length == 0:
            raise ValueError('Trecho nulo')
        m.cylinder(name, group, (a+b)/2, radius, length, color, delta/length)


def construir(c):
    m = Modelo()
    for item in c['items']:
        x, y, z = item['position_xyz_m']
        dx, dy, dz = item['dimensions_xyz_m']
        group, kind = item['id'], item['model']
        if kind == 'motor':
            m.cylinder('carcaca_motor', group, [x+dx/2, y+dy/2, z+dz/2], dx/2, dy, METAL, (0, 1, 0))
            for py in [y+.03, y+dy-.03]:
                m.ring('flange', group, [x+dx/2, py, z+dz/2], dx/2, .012, DARK, (0, 1, 0))
            continue
        if kind == 'traction_pack':
            # Bandeja, tampa e15módulos são ilustração, não componentes OEM reconstituídos.
            m.box('bandeja', group, [x, y, z], [dx, dy, .025], METAL)
            for py in [y, y+dy-.02]:
                m.box('parede', group, [x, py, z+.025], [dx, .02, dz-.025], METAL)
            for px in [x, x+dx-.02]:
                m.box('parede', group, [px, y+.02, z+.025], [.02, dy-.04, dz-.025], METAL)
            for i in range(5):
                for j in range(3):
                    m.box(f'modulo_ilustrativo_{i}_{j}', group,
                          [x+.06+i*.56, y+.05+j*.45, z+.04], [.52, .41, .23], BLUE)
            m.box('tampa_translucida', group, [x+.02, y+.02, z+dz-.015],
                  [dx-.04, dy-.04, .015], [125, 158, 171, 90])
            m.box('caixa_contatores_estimada', group, [x+dx-.30, y+.10, z+.08], [.23, .23, .16], ORANGE)
            continue
        color = BLUE if kind in ['battery', 'controller', 'inverter'] else METAL
        m.box('envelope', group, [x, y, z], [dx, dy, dz], color)
        if kind == 'battery':
            for px, col in [(x+.035, [203, 51, 40, 255]), (x+dx-.035, DARK)]:
                m.cylinder('terminal', group, [px, y+dy/2, z+dz+.008], .010, .016, col)
            for px in [x+.06, x+dx-.07]:
                m.box('cinta_fixacao', group, [px, y-.005, z+dz], [.012, dy+.01, .004], DARK)
        if kind in ['controller', 'inverter', 'electronics']:
            for i in range(7):
                m.box('aleta', group, [x+.02+i*(dx-.045)/7, y-.012, z+.02],
                      [.005, .012, dz-.04], DARK)
            m.box('etiqueta', group, [x+.02, y+dy+.001, z+dz*.55], [dx-.04, .002, dz*.20], [216, 230, 236, 255])
        if kind == 'radiator':
            for i in range(20):
                m.box('canal', group, [x+dx+.001, y+.02+i*.033, z+.02], [.006, .008, dz-.04], DARK)
            for py in [y+.19, y+.53]:
                m.ring('ventoinha', group, [x-.015, py, z+dz/2], .145, .012, DARK, (1, 0, 0))
                m.cylinder('cubo', group, [x-.015, py, z+dz/2], .04, .02, DARK, (1, 0, 0))
        if kind == 'distribution':
            for i in range(5):
                m.box('modulo_din_ilustrativo', group, [x+.015+i*.043, y+dy, z+.08], [.035, .025, .11], [227, 226, 217, 255])
    # Semieixos e juntas; posição longitudinal do eixo coincide com a adaptação existente.
    for py in [-.65, .65]:
        m.cylinder('semieixo_ilustrativo', 'redutor', [1.5417, py, .44], .018, .50, METAL, (0, 1, 0))
        m.cylinder('junta', 'redutor', [1.5417, py, .44], .045, .08, DARK, (0, 1, 0))
    # Cofre técnico seco lateral, protegido da roupa/colchão e separado da água.
    m.box('anteparo_lateral', 'armario_tecnico', [-3.30, .455, .70], [1.96, .008, .82], METAL)
    m.box('teto_termico', 'armario_tecnico', [-3.30, .455, 1.52], [1.96, .38, .008], METAL)
    m.box('bandeja', 'armario_tecnico', [-3.30, .455, .70], [1.96, .38, .008], METAL)
    for z in [.74, 1.45]:
        for i in range(14):
            m.box('lamela_porta_removivel', 'armario_tecnico', [-3.29+i*.136, .82, z], [.10, .008, .025], METAL)
    # Dois trilhos e gaveta removível no pequeno volume livre sobre tanque de água.
    m.box('gaveta_bagagem', 'garagem', [-3.22, -.82, 1.04], [.85, .35, .025], [174, 137, 93, 255])
    for py in [-.82, -.49]:
        m.box('trilho_gaveta', 'garagem', [-3.22, py, 1.03], [.85, .015, .015], METAL)
        m.box('borda_gaveta', 'garagem', [-3.22, py, 1.065], [.85, .015, .10], [174, 137, 93, 255])
    # Rotas ilustrativas: alta tensão no chassi, serviços em canaleta independente.
    linha(m, 'hv_pack_inversor', 'rotas_hv', [[.75, -.50, .45], [1.02, -.50, .45], [1.02, -.50, .90], [1.32, -.30, .90]], .012, ORANGE)
    linha(m, 'hv_motor', 'rotas_hv', [[1.53, -.32, .85], [1.53, -.55, .85], [1.53, -.55, .57]], .014, ORANGE)
    linha(m, 'alimentacao_48v', 'rotas_servicos', [[-2.12, -.12, 1.0], [-2.12, .36, 1.0], [-2.84, .36, 1.0], [-2.84, .565, 1.0]], .008, [195, 53, 43, 255])
    linha(m, 'calha_12v', 'rotas_servicos', [[-1.50, .70, .95], [-1.40, .70, .95], [-1.40, -.915, .95], [0.0, -.915, .95]], .006, [236, 201, 60, 255])
    # Dutos conceituais60mm saindo dos três bocais FreshWell existentes.
    for i in range(3):
        x = -2.20+.13+i*.17
        endz = 1.08+i*.12
        linha(m, 'ramal_ar', 'dutos_hvac', [[x, -.385, .88], [x, -.355, .88], [x, -.355, endz]], .030, [107, 164, 177, 255])
        m.ring('difusor', 'dutos_hvac', [x, -.355, endz], .032, .005, DARK)
    # Circuito de arrefecimento representado como reserva, não circuito hidráulico calculado.
    linha(m, 'ida_retorno_conceitual', 'arrefecimento', [[1.50, .34, .68], [1.85, .34, .68], [1.85, .34, .55], [2.04, .34, .55]], .014, [54, 164, 154, 255])
    m.cylinder('bomba_envelope', 'arrefecimento', [1.89, .34, .55], .06, .12, DARK, (1, 0, 0))
    return m


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--historico', action='store_true', help='Reproduz somente configuração elétrica antiga, não baseline DEC061')
    p.add_argument('--config', type=Path, default=Path('config/instalacoes_eletricas_proposta.yaml'))
    p.add_argument('--destino', type=Path, required=True)
    args = p.parse_args()
    if not args.historico:
        p.error('Configuração elétrica histórica; use --historico para reprodução. Baseline atual: parametros_globais.yaml e detalhar_rotas_cad.py.')
    c = yaml.safe_load(args.config.read_text())
    args.destino.mkdir(parents=True, exist_ok=False)
    m = construir(c)
    m.export(args.destino, 'tracao_e_servicos', c['alignment_assumed'])
    gmsh.initialize()
    try:
        gmsh.option.setNumber('General.Terminal', 0)
        entities = gmsh.model.occ.importShapes(str(args.destino/'tracao_e_servicos.step'))
        gmsh.model.occ.synchronize()
        volumes = [gmsh.model.occ.getMass(d, t) for d, t in entities if d == 3]
    finally:
        gmsh.finalize()
    if len(volumes) != len(m.parts) or min(volumes) <= 0:
        raise ValueError('STEP não preservou sólidos positivos')
    fixed = sum(i['mass_kg'] or 0 for i in c['items'] if not i['mass_in_oem_curb'] and not i.get('optional_extension'))
    result = {'revision': c['revision'], 'created_utc': datetime.now(timezone.utc).isoformat(),
              'script': 'scripts/gerar_cad_eletrico.py', 'policy': c['policy'],
              'parts': len(m.parts), 'step_positive_volumes': len(volumes),
              'service_known_mass_fixed_kg': fixed, 'service_optional_mass_kg': 1.25,
              'service_nominal_energy_kwh': 10.24, 'service_energy_at_assumed_80pct_dod_kwh': 8.192,
              'traction_pack_assumed_ground_clearance_m': .23,
              'traction_pack_assumed_outer_volume_m3': 2.9*1.44*.32,
              'traction_pack_mass_hypotheses_kg': [110000/e for e in c['traction_mass_sensitivity']['assumed_pack_specific_energy_wh_kg']],
              'oem_traction_added_mass_kg': 0,
              'thermal_or_structural_validation': False,
              'config_sha256': hashlib.sha256(args.config.read_bytes()).hexdigest(),
              'generator_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'outputs_sha256': {q.name: hashlib.sha256(q.read_bytes()).hexdigest() for q in args.destino.iterdir()},
              'limitations': ['Rotas e difusores são conceituais; sem perda de carga/vazão dimensionada.',
                              'Envelope do pack/motor/redutor e seus arranjos não são cotas OEM.',
                              'Massas desconhecidas não foram substituídas por zero em orçamento completo.',
                              'STEP reimportado verifica sólidos, não ausência de interferência entre todos os sistemas.']}
    (args.destino/'manifesto_cad_eletrico.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
