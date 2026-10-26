"""Verificações analíticas/conservativas; parâmetros destes testes são sintéticos."""
from dataclasses import replace

import numpy as np
import pytest

from motorhome.cabos_polares import Cabo, perfil_analitico_sem_feedback, resolver

C = Cabo(.005, .008, 3., .2, .0002, alpha_por_k=0)


def test_convergencia_radial_analitica_dois_materiais():
    errors = []
    for n in [8, 16, 32]:
        r = resolver(C, 100, n, 12)
        exact = perfil_analitico_sem_feedback(C, 100, 10, 298.15, r['r_m'])
        errors.append(float(np.max(abs(r['temperatura_k']-exact[:, None]))))
        assert abs(r['residuo_w_m']) < 1e-8
    assert errors[0]/errors[1] > 3
    assert errors[1]/errors[2] > 3


def test_harmonico_angular_verifica_realmente_duas_dimensoes():
    # T=300+A(r/R)^2 cos(2theta) é harmônico, k igual nos dois domínios.
    c = replace(C, k_isolamento_w_mk=C.k_feixe_w_mk)
    errors = []
    for n in [8, 16, 32]:
        nt = 4*n
        theta = (np.arange(nt)+.5)*2*np.pi/nt
        a, h, radius = 2., 1000., c.raio_externo_m
        ambient = 300+a*(1+2*c.k_feixe_w_mk/(h*radius))*np.cos(2*theta)
        r = resolver(c, 0, n, nt, h, ambient)
        exact = 300+a*(r['r_m'][:, None]/radius)**2*np.cos(2*theta)
        errors.append(float(np.sqrt(np.mean((r['temperatura_k']-exact)**2))))
        assert r['variacao_angular_superficie_k'] > 3
        assert abs(r['residuo_w_m']) < 1e-8
    assert errors[0]/errors[1] > 3
    assert errors[1]/errors[2] > 3


def test_joule_acoplado_conserva_e_aumenta_temperatura():
    base = resolver(C, 200, 12, 32)
    r = resolver(replace(C, alpha_por_k=.00393), 200, 12, 32,
                 h_w_m2k=np.r_[np.full(16, 10), np.full(16, 5)])
    assert r['temperatura_max_k'] > base['temperatura_max_k']
    assert r['variacao_angular_superficie_k'] > .1
    assert r['joule_w_m'] > base['joule_w_m']
    assert abs(r['residuo_w_m'])/r['joule_w_m'] < 1e-8


def test_zero_corrente_e_instabilidade():
    assert np.allclose(resolver(C, 0)['temperatura_k'], 298.15)
    with pytest.raises(ValueError, match='estacionária'):
        resolver(replace(C, alpha_por_k=.00393), 2000)


@pytest.mark.parametrize('kwargs', [{'nr': 1}, {'ntheta': 2}, {'h_w_m2k': 0},
                                    {'ambiente_k': -1}, {'corrente_a': -1}])
def test_entradas_invalidas(kwargs):
    params = {'corrente_a': 100, **kwargs}
    with pytest.raises(ValueError):
        resolver(C, **params)
