import pytest

from scripts.fechar_i29_velocidade import primeira_reserva


def test_primeira_reserva_nao_e_ocultada_por_recarga_no_mesmo_dia():
    result = {'trace': [
        {'day': 1, 'hour_end': 2, 'soc_traction': .6, 'distance_km': 20},
        {'day': 1, 'hour_end': 8, 'soc_traction': .1, 'distance_km': 90},
        {'day': 1, 'hour_end': 12, 'soc_traction': .3, 'distance_km': 90},
    ]}
    first = primeira_reserva(result, .1)
    assert first['elapsed_days'] == pytest.approx(8/24)
    assert first['distance_km'] == 90


def test_reserva_nao_alcancada_fica_indefinida():
    result = {'trace': [{'day': 1, 'hour_end': 24, 'soc_traction': .4, 'distance_km': 50}]}
    assert primeira_reserva(result, .1) is None
