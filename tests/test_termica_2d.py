"""Verificação matemática; valores SYNTHETIC, sem dados de componentes."""

import numpy as np
import pytest

from motorhome.termica_2d import Contorno, Malha, Material, resolver


def isolados():
    return {l: Contorno('isolado') for l in ['esquerda', 'direita', 'inferior', 'superior']}


def test_adiabatico_com_fonte_bate_solucao_analitica():
    m = Malha(.3, .2, .01, 9, 7)
    r = resolver(m, Material(5, 800, 200), 300., 32000., isolados(), .3)
    assert np.allclose(r['temperatura_k'], 300.06, rtol=0, atol=1e-11)
    assert abs(r['historico'][-1]['residuo_j']) < 1e-7


def test_fluxo_prescrito_conserva_energia():
    b = isolados()
    b['superior'] = Contorno('fluxo', fluxo_entrada_w_m2=17.)
    m = Malha(1., .7, .2, 12, 8)
    r = resolver(m, Material(1, 1, 1), 300., 0., b, .01)
    estado = r['historico'][-1]
    assert estado['contorno_entrada_j'] == pytest.approx(17*1*.2*.01)
    assert estado['armazenada_j'] == pytest.approx(estado['contorno_entrada_j'])
    assert np.ptp(r['temperatura_k']) > 0


def test_perfil_linear_dirichlet_e_estacionario():
    m = Malha(2., .7, .1, 17, 11)
    x, _ = m.centros()
    ti = 400.-100*x/m.lx_m
    b = isolados()
    b.update(esquerda=Contorno('temperatura', 400.), direita=Contorno('temperatura', 300.))
    r = resolver(m, Material(1, 1, 1), ti, 0., b, .1)
    assert np.max(abs(r['temperatura_k']-ti)) < 1e-10
    assert abs(r['historico'][-1]['residuo_j']) < 1e-10


def test_resistencia_meia_celula_e_filme_robin():
    m = Malha(2., .7, .1, 15, 9)
    x, _ = m.centros()
    k, hl, hr = 3., 7., 11.
    fluxo = (400.-300.)/(1/hl+m.lx_m/k+1/hr)
    ti = 400.-fluxo/hl-fluxo*x/k
    b = isolados()
    b.update(esquerda=Contorno('conveccao', 400., hl),
             direita=Contorno('conveccao', 300., hr))
    r = resolver(m, Material(k, 1, 1), ti, 0., b, .1)
    assert np.max(abs(r['temperatura_k']-ti)) < 1e-10


def test_convergencia_espacial_com_solucao_2d_analitica():
    erros = []
    for n in [8, 16, 32]:
        m = Malha(1., .7, .1, n, n)
        x, y = m.centros()
        modo = np.cos(np.pi*x)*np.cos(np.pi*y/.7)
        ti = 300.+10*modo
        r = resolver(m, Material(1, 1, 1), ti, 0., isolados(), .02, seguranca=.1)
        exato = 300.+10*modo*np.exp(-np.pi**2*(1+1/.7**2)*.02)
        erros.append(float(np.sqrt(np.mean((r['temperatura_k']-exato)**2))))
        assert abs(r['historico'][-1]['residuo_j']) < 1e-10
    assert erros[0]/erros[1] > 3.5
    assert erros[1]/erros[2] > 3.5


def test_convergencia_temporal_contra_autovalor_discreto():
    m = Malha(1., 1., .1, 12, 12)
    x, y = m.centros()
    modo = np.cos(np.pi*x)*np.cos(np.pi*y)
    autovalor = 8/m.dx**2*np.sin(np.pi/(2*m.nx))**2
    exato_semi_discreto = 300.+10*modo*np.exp(-autovalor*.03)
    erros = []
    for passos in [30, 60, 120]:
        r = resolver(m, Material(1, 1, 1), 300.+10*modo, 0.,
                     isolados(), .03, passo_s=.03/passos)
        erros.append(float(np.sqrt(np.mean((r['temperatura_k']-exato_semi_discreto)**2))))
    assert 1.9 < erros[0]/erros[1] < 2.1
    assert 1.9 < erros[1]/erros[2] < 2.1


@pytest.mark.parametrize('invalido', [None, True, float('nan'), float('inf'), -1., 0.])
def test_material_invalido(invalido):
    with pytest.raises(ValueError):
        Material(invalido, 1., 1.)


def test_rejeita_instabilidade_e_formato_incorreto():
    m, mat = Malha(1., 1., .1, 8, 8), Material(1, 1, 1)
    with pytest.raises(ValueError, match='instável'):
        resolver(m, mat, 300., 0., isolados(), 1., passo_s=1.)
    with pytest.raises(ValueError, match='formato'):
        resolver(m, mat, [[300, 300]], 0., isolados(), .1)
    with pytest.raises(ValueError, match='quatro'):
        resolver(m, mat, 300., 0., {}, .1)
    with pytest.raises(ValueError, match='excedem'):
        resolver(m, mat, 300., 0., isolados(), 1., max_passos=1)


def test_extremos_preservados_sem_fonte():
    m = Malha(1., 1., .1, 12, 12)
    x, y = m.centros()
    inicial = 300.+50*np.exp(-30*((x-.5)**2+(y-.5)**2))
    r = resolver(m, Material(1, 1, 1), inicial, 0., isolados(), .02)
    assert r['temperatura_k'].min() >= inicial.min()
    assert r['temperatura_k'].max() <= inicial.max()
    assert r['temperatura_k'].mean() == pytest.approx(inicial.mean())
