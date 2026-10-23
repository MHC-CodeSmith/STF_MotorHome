"""Extrai o exterior Ducato GLB existente e gera STL, vistas e área de silhueta.

Nenhum parâmetro global é preenchido. Não fecha furos automaticamente nem gera Cd.
Entrada: release OpenX Assets 20261015, derivado razor24, MPL-2.0 AND CC-BY-4.0.
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from matplotlib.collections import PolyCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from motorhome.geometria_malha import GLTF_PARA_PROJETO, area_frontal, extrair_exterior


def cor(mesh):
    material = getattr(mesh.visual, 'material', None)
    rgba = getattr(material, 'baseColorFactor', None)
    if rgba is None:
        return [.65, .72, .78, 1.]
    c = np.asarray(rgba, dtype=float)/255
    if c[3] < .9:
        return [.24, .48, .64, 1.]
    return c


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--entrada', type=Path, required=True)
    parser.add_argument('--metadados', type=Path, required=True)
    parser.add_argument('--destino', type=Path, required=True)
    args = parser.parse_args()
    metadata = json.loads(args.metadados.read_text())['metadata']
    if metadata['name'] != 'Fiat Ducato':
        raise ValueError('Metadados devem identificar o ativo Fiat Ducato')
    scene = trimesh.load(args.entrada, force='scene')
    exterior, nomes = extrair_exterior(scene)
    mesh = exterior.to_mesh()
    args.destino.mkdir(parents=True, exist_ok=False)
    out = args.destino
    exterior.export(out/'ducato_exterior_m.glb')
    mesh.export(out/'ducato_exterior_m.stl')
    recarregado = trimesh.load(out/'ducato_exterior_m.stl', force='mesh')
    if not np.allclose(mesh.bounds, recarregado.bounds, atol=1e-6, rtol=0):
        raise ValueError('Conversão STL alterou a caixa envolvente')
    area = area_frontal(mesh)
    tamanhos = np.array(mesh.extents, copy=True)
    nomes = sorted(nomes)
    atribuicao = '\n'.join(metadata['copyrights'])
    atribuicao += '\nLicense: '+metadata['license']
    atribuicao += '\nSource: https://github.com/vevalabs/openx-assets/releases/tag/20261015'
    atribuicao += '\nChanges: exterior selection; rigid Y-up to Z-up rotation; GLB/STL export; no scaling.\n'
    (out/'ATTRIBUTION.txt').write_text(atribuicao)
    fig = plt.figure(figsize=(11, 7), layout='constrained')
    ax = fig.add_subplot(111, projection='3d')
    triangles, cores = [], []
    for g in exterior.geometry.values():
        triangles.append(g.triangles)
        cores.append(np.tile(cor(g), (len(g.faces), 1)))
    triangles, cores = np.concatenate(triangles), np.concatenate(cores)
    # Uma única coleção ordena profundidade entre peças, evitando efeito raio X.
    ax.add_collection3d(Poly3DCollection(triangles, facecolors=cores,
                                       edgecolors='none', zsort='average'))
    low, high = mesh.bounds
    ax.set(xlim=(low[0]-.1, high[0]+.1), ylim=(low[1]-.1, high[1]+.1),
           zlim=(0, high[2]+.15), xlabel='X [m] — frente', ylabel='Y [m] — esquerda', zlabel='Z [m]')
    ax.set_box_aspect(tamanhos.copy())
    ax.view_init(elev=19, azim=35)
    ax.set_title('Carroceria de trabalho: Fiat Ducato 2014\nMalha externa existente; rodas, portas, vidros e espelhos preservados')
    fig.text(.5, .01, 'razor24 (2019) / Dogan Ulus (2025) | MPL-2.0 AND CC-BY-4.0 | sem reescala | CFD pendente',
             ha='center', fontsize=9)
    fig.savefig(out/'ducato_exterior.png', dpi=170)
    plt.close(fig)
    fig, axes = plt.subplots(3, 1, figsize=(11, 11), layout='constrained')
    specs = [(0, 2, 'Lateral', 'X [m]', 'Z [m]'),
             (0, 1, 'Superior', 'X [m]', 'Y [m]'),
             (1, 2, 'Frontal — inclui espelhos', 'Y [m]', 'Z [m]')]
    for ax, (i, j, nome, xlabel, ylabel) in zip(axes, specs):
        profundidade = next(k for k in range(3) if k not in (i, j))
        ordem = np.argsort(triangles[:, :, profundidade].mean(axis=1))
        ax.add_collection(PolyCollection(triangles[ordem][:, :, [i, j]],
                                         facecolors=cores[ordem], edgecolors='none'))
        ax.set(xlim=(low[i]-.25, high[i]+.25), ylim=(low[j]-.25, high[j]+.25),
               aspect='equal', xlabel=xlabel, ylabel=ylabel,
               title=f'{nome}: extensão {tamanhos[i]:.3f} × {tamanhos[j]:.3f} m')
        # Cotas principais da malha, separadas das dimensões de fabricante.
        ydim = low[j]-.12
        ax.annotate('', (low[i], ydim), (high[i], ydim),
                    arrowprops={'arrowstyle': '<->', 'color': '#bd4c16'})
        ax.text((low[i]+high[i])/2, ydim+.03, f'{tamanhos[i]:.3f} m', ha='center', color='#bd4c16')
    fig.suptitle('Vistas da malha importada — dimensões a conferir com a variante de projeto\nrazor24 / Dogan Ulus — MPL-2.0 AND CC-BY-4.0')
    fig.savefig(out/'ducato_vistas.png', dpi=170)
    plt.close(fig)
    if not np.allclose(tamanhos, mesh.extents, atol=1e-12, rtol=0):
        raise ValueError('As dimensões medidas foram alteradas durante a renderização')
    resumo = {'revision': 'ducato-exterior-1', 'data_utc': datetime.now(timezone.utc).isoformat(),
              'fonte_release': 'https://github.com/vevalabs/openx-assets/releases/tag/20261015',
              'arquivo_original': str(args.entrada), 'sha256_original': hashlib.sha256(args.entrada.read_bytes()).hexdigest(),
              'metadados_sha256': hashlib.sha256(args.metadados.read_bytes()).hexdigest(),
              'license': metadata['license'], 'copyrights': metadata['copyrights'],
              'script': 'scripts/preparar_carroceria.py', 'unidade_saida': 'm',
              'transformacao_rigida_gltf_para_projeto': GLTF_PARA_PROJETO.tolist(),
              'escala_aplicada': 1., 'nos_externos': nomes, 'triangulos': len(mesh.faces),
              'bounds_m': mesh.bounds.tolist(), 'extensoes_m': tamanhos.tolist(),
              'area_silhueta_frontal_com_apendices_m2': area,
              'malha_fechada': bool(mesh.is_watertight),
              'orientacao_consistente': bool(mesh.is_winding_consistent),
              'volume_cabine_m3': None, 'cd': None, 'cfd_executado': False,
              'parametros_fabricante_aprovados': False,
              'bibliotecas': {'trimesh': trimesh.__version__, 'numpy': np.__version__},
              'limites': ['Malha visual; variante e dimensões a conferir',
                         'Não combinada com interior Delica', 'Não é bateria/motor E-Ducato',
                         'Sem fechamento automático, convex hull ou reescala',
                         'Silhueta da malha não é validação aerodinâmica'],
              'hashes_saidas': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in out.iterdir() if p.is_file()}}
    (out/'manifesto_carroceria.json').write_text(json.dumps(resumo, indent=2, ensure_ascii=False))
    print(json.dumps({k: resumo[k] for k in ['triangulos', 'extensoes_m',
                     'area_silhueta_frontal_com_apendices_m2', 'malha_fechada', 'cfd_executado']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
