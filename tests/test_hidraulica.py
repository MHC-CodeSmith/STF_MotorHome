import numpy as np
import pytest

from motorhome.hidraulica import Circuito, fator_darcy, perda, ponto_operacao


def test_laminar_hagen_poiseuille():
    c = Circuito(2., .01, 0., 0., 1000., .001, .001, 0.)
    q = 1e-6
    expected = 128*.001*2*q/(np.pi*.01**4)
    assert perda(c, q)['total_pa'] == pytest.approx(expected)
    assert fator_darcy(1000, 0) == pytest.approx(.064)


def test_intersecao_quadratica_independente():
    c = Circuito(0., .02, 0., 0., 1000., .001, .001, 100000.)
    q = np.array([0., .0005, .001])
    p = np.array([120000., 60000., 0.])
    r = ponto_operacao(c, q, p, np.array([5., 5., 5.]))
    exact = (-1.2e8+np.sqrt(1.2e8**2+4*1e11*120000))/(2*1e11)
    assert r['flow_m3_s'] == pytest.approx(exact)
    assert abs(r['pressure_residual_pa']) < 1e-4
    assert r['hydraulic_power_w'] <= r['electric_power_w']


def test_sem_extrapolacao():
    c = Circuito(0., .02, 0., 0., 1000., .001, .001, 1.)
    with pytest.raises(ValueError, match='domínio'):
        ponto_operacao(c, [0, .001, .002], [100000, 90000, 80000], [5, 5, 5])


def test_perda_crescente_e_zero():
    c = Circuito(6., .02, 1.5e-6, 8., 1050., .0015, .0005, 43000.)
    losses = [perda(c, q)['total_pa'] for q in np.linspace(0, .0008, 30)]
    assert losses[0] == 0
    assert np.all(np.diff(losses) > 0)


@pytest.mark.parametrize('kwargs', [{'diametro_m': 0}, {'mu_pa_s': -1}])
def test_invalidos(kwargs):
    d = {'comprimento_m': 6., 'diametro_m': .02, 'rugosidade_m': 0., 'soma_k': 8.,
         'rho_kg_m3': 1050., 'mu_pa_s': .0015, 'vazao_referencia_m3_s': .0005,
         'perda_componentes_referencia_pa': 43000.}
    with pytest.raises(ValueError):
        Circuito(**(d | kwargs))
