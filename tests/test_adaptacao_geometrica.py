import numpy as np
import pytest

from motorhome.adaptacao_geometrica import adaptar_vertices, mapa_linear_trechos


def test_marcos_e_extrapolacao_sem_escala():
    np.testing.assert_allclose(mapa_linear_trechos([-1, 0, 1, 2, 3], [0, 2], [0, 4]),
                               [-1, 0, 2, 4, 5])


def test_roda_preserva_distancias_com_translacao():
    v = np.array([[0, 0, 0], [1, 2, 3], [4, 5, 6]])
    r = adaptar_vertices(v, ([0, 6], [0, 9]), ([0, 6], [0, 8]), [-1, .1, 0])
    np.testing.assert_allclose(r[1:]-r[0], v[1:]-v[0])
    np.testing.assert_array_equal(v[0], [0, 0, 0])


@pytest.mark.parametrize('destino', [[0, 0], [1, 0], [0, float('nan')]])
def test_recusa_inversao_e_nan(destino):
    with pytest.raises(ValueError):
        mapa_linear_trechos([0, 1], [0, 1], destino)
