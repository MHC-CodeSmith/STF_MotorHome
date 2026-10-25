import pytest

from motorhome.sombra import fracoes_sombreadas


def test_sombra_coincidente_e_sol_vertical():
    rect = [(0, 0, 1, 1)]
    assert fracoes_sombreadas(rect, rect, .1, (0, 0, 1)) == [1]
    assert fracoes_sombreadas(rect, [(1, 0, 2, 1)], .1, (0, 0, 1)) == [0]


def test_translacao_analitica_meio_modulo():
    assert fracoes_sombreadas([(0, 0, 1, 1)], [(1, 0, 2, 1)], .5, (1, 0, 1)) == pytest.approx([.5])


def test_uniao_sem_dupla_contagem():
    assert fracoes_sombreadas([(0, 0, 1, 1)], [(0, 0, 1, 1)]*2, .5, (0, 0, 1)) == [1]
    assert fracoes_sombreadas([(0, 0, 1, 1)], [(0, 0, 1, 1)], .5, (0, 0, -1)) == [0]
