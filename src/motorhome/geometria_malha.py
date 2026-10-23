"""Extração de carroceria existente, sem reconstruir ou reescalar o veículo."""

import numpy as np
import trimesh
from shapely import Polygon, union_all

# glTF: Y para cima. Projeto: X frente, Y esquerda, Z para cima. Rotação rígida.
GLTF_PARA_PROJETO = np.array([[1., 0., 0., 0.], [0., 0., -1., 0.],
                             [0., 1., 0., 0.], [0., 0., 0., 1.]])


def extrair_exterior(scene, grupo='Grp_Exterior'):
    """Preserva todos os descendentes externos e as transformações da montagem.

    Exige o grupo explícito; nunca faz fallback silencioso para interior/convex hull.
    A seleção mantém rodas, espelhos, portas e vidros que pertencem ao grupo.
    A saída usa metros e Z para cima, sem escala ou ajuste à configuração global.
    """
    if grupo not in scene.graph.nodes:
        raise ValueError(f'Grupo externo não encontrado: {grupo}')
    parents = scene.graph.transforms.parents
    saida, nomes = trimesh.Scene(), []
    for node in scene.graph.nodes_geometry:
        atual, visitados = node, set()
        while atual != grupo and atual in parents:
            if atual in visitados:
                raise ValueError('Hierarquia com ciclo')
            visitados.add(atual)
            atual = parents[atual]
        if atual != grupo:
            continue
        matriz, geometria = scene.graph[node]
        mesh = scene.geometry[geometria].copy()
        if not isinstance(mesh, trimesh.Trimesh):
            raise TypeError(f'Objeto não triangular: {node}')
        mesh.apply_transform(GLTF_PARA_PROJETO @ matriz)
        if not np.isfinite(mesh.vertices).all():
            raise ValueError('Vértices não finitos')
        saida.add_geometry(mesh, node_name=node, geom_name=node)
        nomes.append(node)
    if not nomes:
        raise ValueError('Grupo externo sem geometria')
    return saida, nomes


def area_frontal(mesh):
    """União das projeções triangulares no plano YZ [m²], observação ao longo de X.

    Inclui todos os apêndices da malha de entrada. A área do retângulo envolvente
    não substitui a silhueta. Não infere área de teto útil, volume de cabine ou Cd.
    """
    if not isinstance(mesh, trimesh.Trimesh) or len(mesh.faces) == 0:
        raise ValueError('Malha triangular não vazia obrigatória')
    if not np.isfinite(mesh.vertices).all():
        raise ValueError('Vértices não finitos')
    poligonos = []
    for tri in mesh.triangles[:, :, 1:3]:
        p = Polygon(tri)
        if p.area > 1e-14:
            poligonos.append(p)
    if not poligonos:
        raise ValueError('Projeção frontal sem área')
    silhueta = union_all(poligonos)
    return float(silhueta.area)
