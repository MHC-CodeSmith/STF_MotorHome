"""Gera CAD AUTORAL de envelope proposto, com verificação de volume/importação.

Não é modelo do fabricante, CAD aprovado ou resultado CFD. Configuração em m;
kernel/exportação em mm, conversão explícita 1000 mm/m. Sem CAD de terceiros.
"""

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import gmsh
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--destino', type=Path, required=True)
    args = parser.parse_args()
    bruto = args.config.read_bytes()
    c = json.loads(bruto)
    if c['status'] != 'PROPOSTA_NAO_APROVADA':
        raise ValueError('Este gerador exige rotulo PROPOSTA_NAO_APROVADA')
    e, h = c['envelope_m'], c['hipoteses_desenho_m']
    l, w, altura = e['comprimento'], e['largura'], e['altura']
    valores = [l, w, altura, *h.values(), c['malha_superficie_mm']]
    if not all(isinstance(v, (int, float)) and not isinstance(v, bool)
               and np.isfinite(v) and v > 0 for v in valores):
        raise ValueError('Dimensoes positivas e finitas obrigatorias')
    if not (0 < h['comprimento_frente_inclinada'] < l
            and 0 < h['altura_base'] < h['altura_frente'] < altura):
        raise ValueError('Hipoteses de desenho geometricamente inconsistentes')
    perfil = np.array([[0, h['altura_base']], [l, h['altura_base']], [l, altura],
                       [h['comprimento_frente_inclinada'], altura], [0, h['altura_frente']]])
    # Shoelace independente do kernel; corpo = extrusao deste perfil pela largura.
    area = .5*abs(float(np.dot(perfil[:, 0], np.roll(perfil[:, 1], -1))
                       - np.dot(perfil[:, 1], np.roll(perfil[:, 0], -1))))
    volume_m3 = area*w
    args.destino.mkdir(parents=True, exist_ok=False)
    out = args.destino
    gmsh.initialize()
    gmsh.option.setNumber('General.Terminal', 0)
    try:
        gmsh.model.add('ENVELOPE_AUTORAL_PROPOSTA')
        pontos = [gmsh.model.occ.addPoint(x*1000, 0, z*1000) for x, z in perfil]
        linhas = [gmsh.model.occ.addLine(pontos[i], pontos[(i+1) % len(pontos)])
                  for i in range(len(pontos))]
        loop = gmsh.model.occ.addCurveLoop(linhas)
        superficie = gmsh.model.occ.addPlaneSurface([loop])
        gmsh.model.occ.extrude([(2, superficie)], 0, w*1000, 0)
        gmsh.model.occ.synchronize()
        solidos = gmsh.model.getEntities(3)
        if len(solidos) != 1:
            raise ValueError('Esperado um unico solido de envelope')
        volume_kernel_m3 = gmsh.model.occ.getMass(*solidos[0])/1e9
        assert abs(volume_m3-volume_kernel_m3) < 1e-9
        gmsh.write(str(out/'envelope_PROPOSTA_mm.step'))
        gmsh.option.setNumber('Mesh.MeshSizeMin', c['malha_superficie_mm'])
        gmsh.option.setNumber('Mesh.MeshSizeMax', c['malha_superficie_mm'])
        gmsh.model.mesh.generate(2)
        gmsh.write(str(out/'envelope_PROPOSTA_mm.stl'))
        gmsh.write(str(out/'envelope_PROPOSTA_mm.msh'))
        node_tags, _, _ = gmsh.model.mesh.getNodes()
        elem_types, elem_tags, _ = gmsh.model.mesh.getElements(2)
        nfaces = sum(len(v) for v in elem_tags)
        _, triangulos = gmsh.model.mesh.getElementsByType(2)
        if list(elem_types) != [2]:
            raise ValueError('Verificacao topologica exige triangulos lineares')
        incidencias, orientacoes = Counter(), Counter()
        for tri in np.asarray(triangulos).reshape(-1, 3):
            for a, b in [(int(tri[0]), int(tri[1])), (int(tri[1]), int(tri[2])),
                         (int(tri[2]), int(tri[0]))]:
                aresta = (min(a, b), max(a, b))
                incidencias[aresta] += 1
                orientacoes[aresta] += 1 if a < b else -1
        estanque = all(v == 2 for v in incidencias.values())
        orientada = all(v == 0 for v in orientacoes.values())
        assert estanque and orientada
        gmsh.clear()
        gmsh.model.add('reimportacao_STEP')
        gmsh.model.occ.importShapes(str(out/'envelope_PROPOSTA_mm.step'))
        gmsh.model.occ.synchronize()
        reimportados = gmsh.model.getEntities(3)
        assert len(reimportados) == 1
        volume_reimportado = gmsh.model.occ.getMass(*reimportados[0])/1e9
        assert abs(volume_reimportado-volume_m3) < 1e-8
        bbox_mm = gmsh.model.getBoundingBox(-1, -1)
    finally:
        gmsh.finalize()
    # Vistas com cotas do envelope; a linha de solo marca z=0.
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), layout='constrained')
    fechado = np.vstack([perfil, perfil[0]])
    a = axes[0, 0]
    a.fill(fechado[:, 0], fechado[:, 1], color='#ccdce7', edgecolor='#24455c')
    a.set(title=f'Lateral: {l:.3f} m x {altura:.3f} m', xlabel='x [m]', ylabel='z [m]', aspect='equal')
    a.set_ylim(0, altura+.3)
    a = axes[0, 1]
    a.add_patch(plt.Rectangle((0, 0), l, w, facecolor='#ccdce7', edgecolor='#24455c'))
    a.set(xlim=(-.2, l+.2), ylim=(-.2, w+.2), aspect='equal',
          title=f'Superior: {l:.3f} m x {w:.3f} m', xlabel='x [m]', ylabel='y [m]')
    a = axes[1, 0]
    a.add_patch(plt.Rectangle((0, h['altura_base']), w, altura-h['altura_base'],
                              facecolor='#ccdce7', edgecolor='#24455c'))
    a.set(xlim=(-.2, w+.2), ylim=(0, altura+.3), aspect='equal',
          title=f'Projecao frontal: {w:.3f} m x {altura:.3f} m', xlabel='y [m]', ylabel='z [m]')
    a.text(.5, -.28, 'Dimensoes em m; arquivos CAD/STL em mm.\nSem rodas, espelhos, aberturas ou interior.',
           transform=a.transAxes, ha='center', fontsize=9)
    axes[1, 1].axis('off')
    axes[1, 1].text(.02, .85, 'ENVELOPE AUTORAL\nPROPOSTA NAO APROVADA\n\n'
                   'Forma frontal e altura da base sao hipoteses.\n'
                   'Nao reproduz a carroceria de um Fiat.\n'
                   'Nao usar para publicar Cd do veiculo.\n\n'
                   f'Volume geometrico do envelope: {volume_m3:.3f} m³\n'
                   'Este volume nao e volume habitavel nem massa.', fontsize=11, va='top')
    fig.suptitle('Estudo de envelope e verificacao CAD - revisao humana pendente')
    fig.savefig(out/'vistas_envelope_PROPOSTA.png', dpi=160)
    plt.close(fig)
    relatorio = {'status': c['status'], 'revision': c['revision'],
                 'data_utc': datetime.now(timezone.utc).isoformat(),
                 'config_sha256': hashlib.sha256(bruto).hexdigest(),
                 'script': 'scripts/gerar_envelope_cad.py', 'kernel': 'OpenCASCADE via Gmsh '+gmsh.__version__,
                 'solidos': 1, 'volume_analitico_envelope_m3': volume_m3,
                 'volume_kernel_envelope_m3': volume_kernel_m3,
                 'volume_reimportado_envelope_m3': volume_reimportado,
                 'bbox_reimportada_mm': bbox_mm, 'nos_malha_superficie': len(node_tags),
                 'elementos_superficie': nfaces, 'tipos_elemento_gmsh': list(map(int, elem_types)),
                 'malha_superficie_estanque': estanque, 'orientacao_arestas_consistente': orientada,
                 'cfd_executado': False, 'geometria_veiculo_validada': False,
                 'hashes': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in out.iterdir() if p.is_file()}}
    (out/'manifesto_envelope_PROPOSTA.json').write_text(json.dumps(relatorio, indent=2, ensure_ascii=False))
    print(f'Envelope autoral exportado e reimportado: 1 solido, {nfaces} elementos superficiais; CFD nao executado.')


if __name__ == '__main__':
    main()
