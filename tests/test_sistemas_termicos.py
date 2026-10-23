"""Casos analíticos independentes, todos SYNTHETIC, exceto prescrição I33."""

from math import exp

import pytest

from motorhome.sistemas_termicos import (
    carga_ac,
    carga_ohmica,
    frenagem_especifica,
    geracao_joule,
    perfil_paralelo,
    ponto_bomba,
    resistividade_linear,
    transiente_concentrado,
    trocador,
)


def test_concentrado_limites_adiabatico_e_resfriamento():
    r = transiente_concentrado(1000, 0, 300, 280, 50, 20)
    assert r['temperatura_final_k'] == pytest.approx(301.)
    assert r['energia_para_ambiente_j'] == 0
    r = transiente_concentrado(1000, 10, 350, 300, 0, 100)
    assert r['temperatura_final_k'] == pytest.approx(300+50/exp(1))
    assert r['energia_para_ambiente_j'] == pytest.approx(50000*(1-1/exp(1)))
    r = transiente_concentrado(1000, 10, 310, 300, 100, 1000)
    assert r['temperatura_final_k'] == 310


def test_i32_separa_calor_sensivel_latente_e_eletricidade():
    r = carga_ac(100, 306.15, 298.15, 200, 50, 2, 70, 40, 10, 20, 3)
    assert r['carga_sensivel_w'] == pytest.approx(1200)
    assert r['carga_latente_w'] == pytest.approx(100)
    assert r['capacidade_resfriamento_w'] == pytest.approx(1300)
    assert r['potencia_eletrica_w'] == pytest.approx(1300/3)
    with pytest.raises(ValueError, match='ocupantes'):
        carga_ac(100, 306, 298, 0, 0, 0, 70, 40, 0, 0, 3)


def test_joule_dimensional_e_resistividade():
    # I=10 A, rho_e=2e-8 ohm m, A=1e-6 m²: R/L=.02 ohm/m.
    qv = geracao_joule(10, 2e-8, 1e-6)
    assert qv*1e-6 == pytest.approx(2.)  # W/m
    assert resistividade_linear(2e-8, .004, 350, 300) == pytest.approx(2.4e-8)
    with pytest.raises(ValueError):
        resistividade_linear(2e-8, .004, 1, 500)


def test_frenagem_enunciado_sem_precisar_massa():
    r = frenagem_especifica(30, 10, 5)
    assert r['energia_cinetica_removida_j_kg'] == 400
    assert r['potencia_media_removida_w_kg'] == 80
    assert r['aceleracao_media_m_s2'] == -4
    assert r['distancia_se_desaceleracao_constante_m'] == 100


def test_carga_ohmica_nao_converte_carregador_inteiro_em_calor():
    r = carga_ohmica(20000, 400, .04)
    assert r['corrente_a'] == 50
    assert r['perda_ohmica_w'] == 100
    assert carga_ohmica(80000, 400, .04)['perda_ohmica_w'] == 1600
    with pytest.raises(ValueError, match='Perda'):
        carga_ohmica(100, 1, 1)


@pytest.mark.parametrize('arranjo', ['paralelo', 'contracorrente'])
def test_trocador_conservacao_e_limites(arranjo):
    for ua in [0, 1e-8, 100, 1e8]:
        r = trocador(ua, 100, 200, 380, 300, arranjo)
        assert 0 <= r['efetividade'] <= 1
        qh = 100*(380-r['quente_saida_k'])
        qc = 200*(r['fria_saida_k']-300)
        assert qh == pytest.approx(qc, abs=1e-10)
        assert r['calor_trocado_w'] == pytest.approx(qh, abs=1e-10)
        assert 300 <= r['quente_saida_k'] <= 380
        assert 300 <= r['fria_saida_k'] <= 380


def test_trocador_capacidades_iguais_e_quase_iguais():
    iguais = trocador(100, 100, 100, 380, 300, 'contracorrente')
    quase = trocador(100, 100, 100+1e-10, 380, 300, 'contracorrente')
    assert iguais['efetividade'] == .5
    assert quase['efetividade'] == pytest.approx(.5)
    with pytest.raises(ValueError, match='Arranjo'):
        trocador(100, 100, 100, 380, 300, 'cruzado')


def test_perfil_paralelo_satisfaz_balancos_em_todo_ponto():
    r, perfil = perfil_paralelo(100, 100, 200, 380, 300, [0, .25, .5, 1])
    assert perfil[0] == {'fracao_area': 0., 'quente_k': 380., 'fria_k': 300.}
    assert perfil[-1]['quente_k'] == pytest.approx(r['quente_saida_k'])
    for p in perfil:
        assert 100*(380-p['quente_k']) == pytest.approx(200*(p['fria_k']-300))


def test_bomba_sem_extrapolar_e_com_multiplas_intersecoes():
    assert ponto_bomba([0, 1, 2], [4, 2, 0], [0, 2, 4]) == [
        {'vazao_m3_s': 1., 'pressao_pa': 2.}]
    assert ponto_bomba([0, 1], [10, 10], [1, 1]) == []
    assert len(ponto_bomba([0, 1, 2], [4, 0, 4], [2, 2, 2])) == 2
    with pytest.raises(ValueError, match='coincidente'):
        ponto_bomba([0, 1], [2, 2], [2, 2])
    with pytest.raises(ValueError, match='crescentes'):
        ponto_bomba([0, 0], [2, 1], [0, 1])


@pytest.mark.parametrize('invalido', [True, None, float('nan'), float('inf'), -1, 0])
def test_rejeita_capacidade_termica_invalida(invalido):
    with pytest.raises(ValueError):
        transiente_concentrado(invalido, 1, 300, 300, 1, 1)
