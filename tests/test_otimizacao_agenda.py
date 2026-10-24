import pandas as pd
import pytest

from motorhome.otimizacao_agenda import maximizar_distancia


def run(**kwargs):
    # Caso SYNTHETIC analítico: 1 kW por uma hora custa 0,5 SOC da bateria 2 kWh.
    values = {'inicios': pd.date_range('2026-06-21', periods=2, freq='h', tz='America/Sao_Paulo'),
              'duracao_s': 3600, 'velocidades_m_s': [0., 10.], 'demandas_w': [0., 1000.],
              'solar_w': [0., 0.], 'capacidade_j': 7_200_000., 'soc_inicial': 1.,
              'soc_minimo': 0., 'soc_final': .5, 'tolerancia_soc': 1e-8,
              'eficiencia_carga': 1., 'eficiencia_descarga': 1.,
              'limite_diario_s': 3600., 'solar_durante_conducao': False}
    values.update(kwargs)
    return maximizar_distancia(**values)


def test_otimo_analitico_uma_hora():
    r = run()
    assert r['feasible'] and r['optimal_in_grid']
    assert r['distance_m'] == pytest.approx(36000)
    assert r['final_soc'] == pytest.approx(.5)
    assert r['daily_driving_s'] == {'2026-06-21': 3600}


def test_soc_inalcancavel_na_grade_reporta_inviabilidade():
    r = run(soc_final=.3)
    assert not r['feasible']  # A grade só permite gastar 0, 0,5 ou 1 SOC.


def test_solar_posterior_nao_cobre_deficit_anterior():
    r = run(soc_inicial=0., solar_w=[0., 1000.], soc_final=.5)
    assert r['feasible'] and r['distance_m'] == 0


def test_limite_diario_e_eficiencia():
    r = run(limite_diario_s=7200., soc_final=0.)
    assert r['distance_m'] == pytest.approx(72000.)
    r = run(eficiencia_descarga=.8, soc_final=.375)
    assert r['final_soc'] == pytest.approx(.375)


def test_corte_solar_na_capacidade_maxima():
    r = run(solar_w=[2000., 0.], soc_final=.5)
    assert r['feasible']
    assert any(x['battery_charge_curtailed_j'] > 0 for x in r['schedule'])


def test_rejeita_grade_cruzando_meia_noite():
    with pytest.raises(ValueError, match='meias-noites'):
        run(inicios=pd.date_range('2026-06-21 23:30', periods=2, freq='h', tz='America/Sao_Paulo'))
