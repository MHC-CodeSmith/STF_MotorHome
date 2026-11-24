import numpy as np
import pytest

from motorhome.despacho_diario import alocar_dia
from motorhome.reconciliacao import passo_solar


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


@pytest.mark.parametrize('eta',[.7,.9,1.])
def test_minimo_dc_usa_a_mesma_convencao_de_saida_que_o_replay(eta):
    # Especificação de carregador é potência ENTREGUE à bateria. I25 e I29
    # precisam concordar em qual ponto da cadeia o piso é comparado; caso
    # contrário o mesmo 1 kW vale 1/eta a mais em um dos modelos.
    for pv in (1.,1.05,1.1,1.15,1.3,2.):
        a=alocar_dia([pv],[True],1,minimo_dc_kw=1,eta_dc=eta,eta_servicos=1,
            consumo_servicos_kwh=0,capacidade_servicos_kwh=1,
            energia_servicos_inicial_kwh=.5,capacidade_credito_tracao_kwh=10)
        b=passo_solar(pv,0,True,eta,1,1,hipotetico=True)
        assert a['credito_solar_tracao_kwh']==pytest.approx(b['tracao_kwh'])


def test_minimo_compara_potencia_entregue_e_nao_a_entrada_fv():
    # 1,0 kW de FV bruta não habilita um piso de 1 kW de saída quando eta<1.
    assert solve([1.0],[True],minimum=1)['credito_solar_tracao_kwh']==0
    r=solve([1/.9],[True],minimum=1)
    assert r['credito_solar_tracao_kwh']==pytest.approx(1.0)


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
