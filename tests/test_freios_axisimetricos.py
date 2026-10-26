import numpy as np
import pytest

from motorhome.freios_axisimetricos import (
    Pista,
    energia_frenagem,
    placa_analitica,
    resolver,
)


def test_requisito_energia():
    assert energia_frenagem(4250) == 1700000
    assert energia_frenagem(1) == 400


def test_adiabatico_conserva_e_particiona():
    r = resolver(Pista(), nr=12, nz=8, dt_s=.05, h_externo_w_m2k=0, h_canal_w_m2k=0)
    assert r['energia_entrada_disco_j'] == pytest.approx(1700000*.7*.9/2)
    assert abs(r['residuo_disco_j']) < 1e-5
    assert r['energia_saida_disco_j'] == 0


def test_conveccao_e_campo_multidimensional():
    r = resolver(Pista(), nr=24, nz=8, dt_s=.025)
    t = r['temperatura_k']
    assert np.ptp(t[:, -1]) > 10
    assert np.ptp(t[12, :]) > 10
    assert r['energia_saida_disco_j'] > 0
    assert abs(r['residuo_disco_j']) < 1e-5
    assert t.min() >= 298.15


def test_zero_source_e_regeneracao():
    r = resolver(Pista(), fracao_regenerada=1, nr=6, nz=4, dt_s=.1)
    np.testing.assert_allclose(r['temperatura_k'], 298.15, atol=1e-10)
    assert r['energia_entrada_disco_j'] == 0


def test_superposicao_linear():
    a = resolver(Pista(), nr=12, nz=6, dt_s=.05)
    b = resolver(Pista(), fracao_regenerada=.5, nr=12, nz=6, dt_s=.05)
    np.testing.assert_allclose(b['temperatura_k']-298.15, .5*(a['temperatura_k']-298.15), atol=1e-9)


def test_uniforme_analitico_adiabatico():
    # Fonte nas duas faces externas equivalentes, limite de condutividade alta:
    # média volumétrica exata independe de qualquer malha/gradiente.
    p = Pista(contato_interno_m=.09, contato_externo_m=.15)
    r = resolver(p, nr=12, nz=6, dt_s=.05, h_externo_w_m2k=0, h_canal_w_m2k=0)
    rf = np.linspace(.09, .15, 13)
    mean = np.average(r['temperatura_k'].mean(axis=1), weights=np.diff(rf**2))
    exact = 298.15+r['energia_entrada_disco_j']/(r['massa_duas_placas_kg']*500)
    assert mean == pytest.approx(exact, abs=1e-8)


def test_serie_analitica_axial_e_ordem_espacial():
    p = Pista(contato_interno_m=.09, contato_externo_m=.15)
    area = np.pi*(.15**2-.09**2)
    q0 = 4250*4*30*.7*.9/4/area
    errors = []
    for nz in [16, 32, 64]:
        r = resolver(p, nr=3, nz=nz, dt_s=.002, h_externo_w_m2k=0, h_canal_w_m2k=0)
        exact = placa_analitica(.008, nz, 5, q0, 4/30)
        errors.append(np.max(np.abs(r['temperatura_k'][0]-298.15-exact)))
    assert errors[-1] < .01
    assert np.all(np.log2(np.array(errors[:-1])/errors[1:]) > 1.9)


@pytest.mark.parametrize('kwargs', [{'fracao_eixo': 1.1}, {'dt_s': 0}, {'nr': True}, {'h_canal_w_m2k': -1}])
def test_rejeita_entradas(kwargs):
    with pytest.raises(ValueError):
        resolver(Pista(), **kwargs)
