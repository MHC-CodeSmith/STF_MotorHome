"""Agendas SYNTHETIC com casos inviáveis que o balanço diário ocultaria."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import pytest

from motorhome.agenda_energia import Intervalo, verificar_agenda


def trecho(hora=0, duracao=1, velocidade=1., carga=10., solar=0.):
    inicio = datetime(2026, 6, 21, tzinfo=ZoneInfo('America/Sao_Paulo')) + timedelta(hours=hora)
    return Intervalo(inicio, inicio+timedelta(hours=duracao), velocidade, carga, solar, 'SYNTHETIC')


def verificar(agenda, **kwargs):
    entradas = {'capacidade_referencia_j': 360000., 'soc_inicial': 1.,
                'eficiencia_carga': 1., 'eficiencia_descarga': 1., 'soc_reserva': 0.,
                'max_conducao_diaria_s': 8*3600., 'distancia_alvo_m': 3600.,
                'tolerancia_distancia_m': 1e-6}
    entradas.update(kwargs)
    return verificar_agenda(agenda, **entradas)


def test_integracao_exata_e_alvo_soc_igualdade():
    r = verificar([trecho(carga=70)], alvo_soc_final=.3, tolerancia_soc=1e-8)
    assert r['viavel_no_modelo']
    assert r['soc_final'] == pytest.approx(.3)
    assert abs(r['residuo_energia_j']) < 1e-8
    assert not verificar([trecho(carga=60)], alvo_soc_final=.3,
                         tolerancia_soc=1e-8)['viavel_no_modelo']


def test_deficit_intermediario_nao_e_escondido_pelo_solar_posterior():
    r = verificar([trecho(carga=150), trecho(hora=1, carga=0, solar=150)],
                  distancia_alvo_m=7200.)
    assert r['soc_final'] == 1
    assert not r['viavel_no_modelo']
    assert any('reserva' in v for v in r['violacoes'])


def test_corte_pv_explicito_e_residuo():
    agenda = [trecho(carga=0, solar=100)]
    assert not verificar(agenda)['viavel_no_modelo']
    r = verificar(agenda, permitir_corte_solar=True, eficiencia_carga=.8)
    assert r['viavel_no_modelo']
    assert r['corte_solar_terminal_j'] == 360000
    assert r['residuo_energia_j'] == 0


def test_eficiencias_de_carga_e_descarga_conservam_energia():
    r = verificar([trecho(carga=10)], eficiencia_descarga=.8)
    assert r['energia_final_j'] == 315000
    assert r['perdas_j'] == 9000
    assert r['residuo_energia_j'] == 0
    r = verificar([trecho(carga=0, solar=10)], soc_inicial=.5, eficiencia_carga=.8)
    assert r['energia_final_j'] == 208800
    assert abs(r['residuo_energia_j']) < 1e-9


def test_limite_conducao_por_calendario_e_nao_por_bloco():
    r = verificar([trecho(hora=20, duracao=8, carga=0), trecho(hora=28, duracao=5, carga=0)],
                  distancia_alvo_m=13*3600.)
    assert r['conducao_por_dia_s'] == {'2026-06-21': 4*3600, '2026-06-22': 9*3600}
    assert not r['viavel_no_modelo']
    assert any('condução' in v for v in r['violacoes'])


def test_paradas_consumem_energia_sem_contar_conducao():
    r = verificar([trecho(), trecho(hora=1, velocidade=0, carga=5)])
    assert r['conducao_por_dia_s'] == {'2026-06-21': 3600}
    assert r['energia_final_j'] == 306000


def test_fuso_com_transicao_usa_segundos_reais():
    # Dia da mudança histórica de verão: 23 h, não 24 h, entre meias-noites.
    zona = ZoneInfo('America/New_York')
    a = Intervalo(datetime(2026, 3, 8, 0, tzinfo=zona),
                  datetime(2026, 3, 9, 0, tzinfo=zona), 0., 1., 0., 'SYNTHETIC')
    r = verificar([a], fuso='America/New_York', capacidade_referencia_j=1e6,
                  distancia_alvo_m=0.)
    assert r['demanda_terminal_j'] == 23*3600


def test_lacunas_sobreposicao_e_datas_sem_fuso_rejeitadas():
    for hora in [0, 2]:
        with pytest.raises(ValueError, match='contínua'):
            verificar([trecho(), trecho(hora=hora)])
    with pytest.raises(ValueError, match='fuso'):
        Intervalo(datetime(2026, 1, 1), datetime(2026, 1, 2), 1, 1, 1, 'SYNTHETIC')  # noqa: DTZ001 - teste de rejeição
    with pytest.raises(ValueError, match='juntos'):
        verificar([trecho()], alvo_soc_final=.3)
