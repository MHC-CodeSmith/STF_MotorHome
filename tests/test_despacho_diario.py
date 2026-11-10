import numpy as np
import pytest

from motorhome.despacho_diario import alocar_dia


def solve(pv,park,minimum=0,services=0,initial=1,capacity=2):
    return alocar_dia(pv,park,1,minimo_dc_kw=minimum,eta_dc=.9,
        eta_servicos=.8,consumo_servicos_kwh=services,capacidade_servicos_kwh=capacity,
        energia_servicos_inicial_kwh=initial,capacidade_credito_tracao_kwh=10)


def test_solar_zero_nao_usa_energia_inicial_servicos_para_tracao():
    assert solve([0,0],[True,True])['credito_solar_tracao_kwh']==0


def test_carga_so_estacionado_e_perdas_sem_dupla_contagem():
    r=solve([2,2],[True,False])
    assert r['credito_solar_tracao_kwh']==pytest.approx(1.8)
    assert r['fv_tracao_kwh'][1]==0
    assert r['residuo_servicos_kwh']<1e-9


def test_minimo_nao_e_maximo_nem_buffer_de_servicos():
    r=solve([.5,2],[True,True],minimum=1)
    assert r['fv_tracao_kwh']==pytest.approx([0,2])
    assert r['credito_solar_tracao_kwh']==pytest.approx(1.8)


def test_servicos_ciclicos_consumem_fv_e_respeitam_causalidade():
    r=solve([0,4,0],[True,True,True],services=1.2,initial=.5)
    assert r['credito_solar_tracao_kwh']==pytest.approx((4-1.2/.8)*.9)
    assert r['energia_servicos_kwh'][0]==pytest.approx(r['energia_servicos_kwh'][-1])
    assert np.min(r['energia_servicos_kwh'])>=-1e-9
    assert solve([0,4,0],[True,True,True],services=1.2,initial=0)['status']=='servicos_inviaveis_nesta_janela'


def test_energia_solar_nao_excede_capacidade_credito():
    r=solve([20],[True])
    assert r['credito_solar_tracao_kwh']==pytest.approx(10)


def test_entrada_negativa_recusada():
    with pytest.raises(ValueError):solve([-1],[True])
