import pandas as pd
import pytest

from motorhome.otimizacao_viagem import minimizar_tempo


def run(**kwargs):
    # SYNTHETIC: bateria 2 kWh, velocidade 36 km/h, tração 1 kW.
    values = {'inicios': pd.date_range('2026-06-21', periods=4, freq='h', tz='America/Sao_Paulo'),
                  'duracao_s': 3600, 'velocidades_m_s': [0., 10.], 'demandas_w': [0., 1000.],
                  'solar_w': [0.]*4, 'capacidade_j': 7_200_000., 'soc_inicial': 1., 'soc_minimo': 0.,
                  'distancia_m': 54000., 'eficiencia_carga': 1., 'eficiencia_descarga': 1.,
                  'limite_diario_s': 28800, 'solar_durante_conducao': False}
    values.update(kwargs)
    return minimizar_tempo(**values)


def test_chegada_fracionaria_e_distancia_exata():
    r = run()
    assert r['feasible'] and r['optimal_in_grid']
    assert r['elapsed_s'] == pytest.approx(5400)
    assert r['distance_m'] == pytest.approx(54000)
    assert r['final_soc'] == pytest.approx(.25)
    assert r['schedule'][-1]['duration_s'] == pytest.approx(1800)


def test_energia_futura_nao_financia_conducao_anterior():
    r = run(soc_inicial=0., solar_w=[0., 2000., 0., 0.], distancia_m=36000.)
    assert r['elapsed_s'] == pytest.approx(10800)
    assert r['schedule'][0]['speed_m_s'] == 0


def test_sem_energia_reporta_inviabilidade():
    assert not run(soc_inicial=0.)['feasible']


def test_limite_diario_forca_espera_ate_dia_seguinte():
    times = pd.date_range('2026-06-21 23:00', periods=4, freq='h', tz='America/Sao_Paulo')
    r = run(inicios=times, distancia_m=54000., limite_diario_s=3600.)
    assert r['elapsed_s'] == pytest.approx(5400)
    assert max(r['daily_driving_s'].values()) <= 3600+1e-5
    assert not run(distancia_m=54000., limite_diario_s=3600.)['feasible']


def test_parada_consumidora_e_reserva():
    r = run(demandas_w=[100., 1000.], soc_minimo=.25)
    assert r['feasible'] and r['final_soc'] == pytest.approx(.25)
    assert not run(soc_minimo=.30)['feasible']


def test_rejeita_intervalos_cruzando_meia_noite():
    with pytest.raises(ValueError, match='meias-noites'):
        run(inicios=pd.date_range('2026-06-21 23:30', periods=4, freq='h', tz='America/Sao_Paulo'))
