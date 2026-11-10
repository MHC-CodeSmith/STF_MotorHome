import pytest

from motorhome.prioridades import recomendar_estagio, simular_servicos_priorizados


def test_orcamento_previsao_sem_limiares_fixos_soc():
    assert recomendar_estagio(8,24,[7,4,2])['stage']==0
    assert recomendar_estagio(8,48,[7,4,2])['stage']==1
    assert recomendar_estagio(3,48,[7,4,2])=={'stage':2,'forecast_covered':False,'reason':'preservar_essenciais_ate_reserva'}
    assert recomendar_estagio(100,24,[7,4,2],bms_allow=False)['stage']==3


def test_protecao_essencial_ate_reserva_e_conservacao():
    r=simular_servicos_priorizados(10,.2,48,[12,6,2])
    assert r['horizon_completed'] and r['soc_final']>=.2-1e-10
    assert r['project_soc_thresholds'] is None and abs(r['energy_residual_kwh'])<1e-10
    no=simular_servicos_priorizados(10,.2,48,[12,6,2],managed=False)
    assert no['hours_supported']==pytest.approx(16)
    assert no['soc_final']==pytest.approx(.2)


def test_nao_promete_essenciais_indefinidamente():
    r=simular_servicos_priorizados(1,.2,48,[12,6,2])
    assert not r['horizon_completed'] and r['hours_supported']==pytest.approx(.8/2*24)
    assert r['soc_final']==pytest.approx(.2)
    with pytest.raises(ValueError):recomendar_estagio(4,24,[2,4,1])
