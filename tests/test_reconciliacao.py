"""Conservação, referências analíticas e bloqueios físicos do novo baseline."""

import pytest

from motorhome.freios_axisimetricos import Pista
from motorhome.freios_axisimetricos import resolver as resolver_freio
from motorhome.reconciliacao import (
    consumo_plano,
    dimensionar_modulos,
    indice_lateral,
    passo_solar,
    reacoes_eixos,
    simular_missao,
)


def test_energia_por_distancia_independente_da_conversao_de_tempo():
    # Só rolamento: Wd = m g Crr * 1000m; kWh = J / 3.6e6.
    r = consumo_plano(40, 1000, 1e-20, 1, .01, 1, .8)
    assert r['kwh_km'] == pytest.approx(1000*9.80665*.01*1000/3.6e6/.8)
    assert r['bateria_kw']/r['rodas_kw'] == pytest.approx(1/.8)


@pytest.mark.parametrize('reserve,expected', [(.2, 4), (.3, 5)])
def test_bateria_autonomia_sem_multiplicar_reserva_por_dod(reserve, expected):
    r = dimensionar_modulos(7.5, 2, reserve, 4.8, .95)
    assert r['modulos'] == expected
    assert r['utilizavel_kwh'] >= 15
    assert (expected-1)*4.8*(1-reserve) < 15


def test_ausencia_evidencia_bloqueia_carga_mesmo_com_sobra_solar():
    r = passo_solar(20, 1, True, .9, .5, 1)
    assert r['tracao_kwh'] == 0
    assert r['cortada_kwh'] == 19
    assert r['residuo_kwh'] == pytest.approx(0)


def test_minimo_desconhecido_bloqueia_ate_hipotese_explicita():
    assert passo_solar(20, 0, True, .9, None, 1, hipotetico=True)['tracao_kwh'] == 0


@pytest.mark.parametrize('capacity', [0, 2, 5])
def test_buffer_so_carrega_tracao_parada_e_conserva_em_toda_sequencia(capacity):
    buffer = generated = delivered = loss = cut = services = 0.
    for pv, parked in [(1, False), (3, True), (0, True), (.2, True), (0, False)]:
        r = passo_solar(pv, .1, parked, .8, 1, 1, hipotetico=True,
                       buffer_kwh=buffer, buffer_capacidade_kwh=capacity)
        assert r['residuo_kwh'] == pytest.approx(0, abs=1e-10)
        if not parked:
            assert r['tracao_kwh'] == 0
        generated += pv
        delivered += r['tracao_kwh']
        loss += r['perdas_kwh']
        cut += r['cortada_kwh']
        services += r['servicos_kwh']
        buffer = r['buffer_final_kwh']
    assert generated == pytest.approx(delivered+loss+cut+services+buffer)


def test_buffer_nao_cria_energia_e_precisa_acumular_potencia():
    r = passo_solar(.5, 0, True, .9, 1, 1, hipotetico=True,
                   buffer_capacidade_kwh=2, eficiencia_buffer=.8)
    assert r['tracao_kwh'] == 0
    assert r['buffer_final_kwh'] == pytest.approx(.4)
    assert r['perdas_kwh'] == pytest.approx(.1)


def test_alocacao_fixa_nao_redireciona_sobra_dos_servicos_para_tracao():
    r = passo_solar(10, 0, True, 1, .1, 1, hipotetico=True,
                   alocacao='fixa', fracao_servicos=.8)
    assert r['tracao_kwh'] == pytest.approx(2)
    assert r['cortada_kwh'] == pytest.approx(8)


def test_replay_tem_soc_inicial_cheio_conservacao_e_limite_diario():
    r = simular_missao([1.]*24, [2.]*24, [True]*8+[False]*16,
                      speed_kmh=10, kwh_km=.1, service_kwh_day=1,
                      traction_capacity_kwh=20, service_capacity_kwh=10,
                      reserve_traction=.1, reserve_service=.2, target_km=200,
                      max_days=10, mode='buffer_hipotese', min_dc_kw=1,
                      buffer_capacity_kwh=2)
    assert r['status'] == 'chegada_condicional'
    assert r['distance_km'] == pytest.approx(200)
    assert r['energy_residual_kwh'] == pytest.approx(0, abs=1e-9)
    assert max(x['driving_h'] for x in r['daily']) <= 8
    assert min(x['soc_service'] for x in r['trace']) >= .2-1e-10
    assert max(x['soc_traction'] for x in r['trace']) <= 1+1e-10


def test_controle_sem_interface_interrompe_na_reserva_analitica():
    r = simular_missao([100.]*24, [0.]*24, [True]*8+[False]*16,
                      speed_kmh=10, kwh_km=.1, service_kwh_day=1,
                      traction_capacity_kwh=10, service_capacity_kwh=10,
                      reserve_traction=.2, reserve_service=.2, target_km=200)
    assert r['status'] == 'reserva_tracao_sem_interface'
    assert r['distance_km'] == pytest.approx(80)
    assert r['soc_final_traction'] == pytest.approx(.2)
    assert r['totals']['traction_solar_kwh'] == 0


def test_eixos_conservam_peso_e_momento():
    r = reacoes_eixos([(1000, 0), (600, 4), (200, 2)], 4)
    assert r == {'total_kg': 1800, 'dianteiro_kg': 1100, 'traseiro_kg': 700}
    assert r['traseiro_kg']*4 == 600*4+200*2


def test_indice_lateral_sensivel_ao_deslocamento_de_cg():
    assert indice_lateral(2, 1) == pytest.approx(1)
    assert indice_lateral(2, 1, .2) == pytest.approx(.8)
    assert indice_lateral(2, 2) == pytest.approx(.5)


def test_freio_recebe_so_potencia_atrito_e_conserva_calor():
    r = resolver_freio(Pista(), nr=12, nz=4, dt_s=.1,
                      potencia_total_friccao_w=lambda t: 100000.)
    assert r['energia_entrada_disco_j'] == pytest.approx(100000*5*.7*.9/2)
    assert abs(r['residuo_disco_j']) < 1e-5


def test_freio_rejeita_geracao_artificial_de_calor():
    with pytest.raises(ValueError, match='demanda mecânica'):
        resolver_freio(Pista(), nr=4, nz=2, potencia_total_friccao_w=lambda t: 1e9)


@pytest.mark.parametrize('pv,buffer,capacity', [(-1, 0, 0), (1, -1, 2), (1, 3, 2)])
def test_rejeita_estados_nao_fisicos(pv, buffer, capacity):
    with pytest.raises(ValueError):
        passo_solar(pv, 0, True, .9, 1, 1, buffer_kwh=buffer,
                    buffer_capacidade_kwh=capacity)
