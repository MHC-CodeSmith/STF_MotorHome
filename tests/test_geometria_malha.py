"""Casos geométricos analíticos; nenhum é dimensão de fabricante."""

import numpy as np
import pytest
import trimesh

from motorhome.geometria_malha import area_frontal, extrair_exterior


def test_area_uniao_nao_soma_triangulos_ocultos():
    caixa = trimesh.creation.box(extents=[4., 2., 3.])
    outra = caixa.copy()
    outra.apply_translation([10, 0, 0])
    assert area_frontal(trimesh.util.concatenate([caixa, outra])) == pytest.approx(6.)


def test_preserva_transformacao_descarta_interior_e_nao_reescala():
    scene = trimesh.Scene()
    scene.graph.update(frame_to='Grp_Exterior', matrix=trimesh.transformations.translation_matrix([4, 0, 0]))
    scene.add_geometry(trimesh.creation.box(extents=[4, 3, 2]), geom_name='body',
                       node_name='body', parent_node_name='Grp_Exterior')
    scene.add_geometry(trimesh.creation.box(extents=[99, 99, 99]), geom_name='interior', node_name='interior')
    exterior, nomes = extrair_exterior(scene)
    assert nomes == ['body']
    mesh = exterior.to_mesh()
    np.testing.assert_allclose(mesh.extents, [4, 2, 3])
    np.testing.assert_allclose(mesh.bounds.mean(axis=0), [4, 0, 0])
    assert area_frontal(mesh) == pytest.approx(6.)


def test_grupo_ausente_nao_escolhe_geometria_errada():
    with pytest.raises(ValueError, match='não encontrado'):
        extrair_exterior(trimesh.Scene(trimesh.creation.box()))
