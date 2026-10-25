import pytest

from motorhome.ocupacao import arranjos_em_grade, verificar_caixas


def test_tres_modulos_cabem_quarto_nao():
    rows = arranjos_em_grade(3.705, 1.870, 1.134, 1.762, .03, .05)
    assert max(r['count'] for r in rows) == 3
    assert max(r['count'] for r in arranjos_em_grade(3.705, 1.870, 1.134, 1.762, .03, .10)) == 1


def test_grade_rotacionada():
    result = arranjos_em_grade(4, 2, 2, 1, 0, 0)
    assert [r['count'] for r in result] == [4, 4]


def test_intersecao_apenas_volumetrica():
    a = {'id': 'a', 'position_xyz_m': [0, 0, 0], 'dimensions_xyz_m': [1, 1, 1]}
    b = {'id': 'b', 'position_xyz_m': [1, 0, 0], 'dimensions_xyz_m': [1, 1, 1]}
    assert verificar_caixas([a, b], [2, 1, 1])['envelope_check_passed']
    b['position_xyz_m'] = [.99, 0, 0]
    assert verificar_caixas([a, b], [2, 1, 1])['overlaps'] == [['a', 'b']]
    b['position_xyz_m'] = [1.01, 0, 0]
    assert verificar_caixas([a, b], [2, 1, 1])['outside'] == ['b']


def test_dados_nao_finitos():
    with pytest.raises(ValueError):
        arranjos_em_grade(float('nan'), 2, 1, 1, 0, 0)
