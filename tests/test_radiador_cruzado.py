"""Verificação sintética independente de peças/curvas reais."""
import numpy as np
import pytest

from motorhome.radiador_cruzado import efetividade_integral, resolver


def test_campo_convergente_contra_integral_independente():
    exact = efetividade_integral(1., .5)
    errors = []
    for n in [8, 16, 32]:
        r = resolver(1000, 2000, 1000, 350, 300, n, n)
        errors.append(abs(r['efetividade']-exact))
        assert abs(r['residuo_w']) < 1e-8
        assert r['quente_k'].min() >= 300
        assert r['fria_k'].max() <= 350
        assert np.ptp(r['quente_k'][:, -1]) > 0
    assert errors[0]/errors[1] > 3.8
    assert errors[1]/errors[2] > 3.8


def test_reciprocidade_e_limite_sem_troca():
    a = resolver(1000, 2000, 1000, 350, 300)
    b = resolver(1000, 1000, 2000, 350, 300)
    assert a['calor_w'] == pytest.approx(b['calor_w'])
    r = resolver(0, 2000, 1000, 350, 300)
    assert r['calor_w'] == 0
    assert efetividade_integral(0, .5) == 0
    assert efetividade_integral(1, 0) == pytest.approx(1-np.exp(-1))


@pytest.mark.parametrize('ua,ch,cc,thi,tci,n', [(-1, 1, 1, 350, 300, 8),
    (1, 0, 1, 350, 300, 8), (1, 1, 1, 300, 350, 8), (1000, 1, 1, 350, 300, 2)])
def test_invalidos(ua, ch, cc, thi, tci, n):
    with pytest.raises(ValueError):
        resolver(ua, ch, cc, thi, tci, n, n)
