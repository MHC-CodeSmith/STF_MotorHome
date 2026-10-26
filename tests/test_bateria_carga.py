from pathlib import Path

import pytest
import yaml

from motorhome.bateria_carga import corrente_carga, resolver


def inputs():
    c = yaml.safe_load(Path('config/bateria_termica_proposta.yaml').read_text())
    return c['assumed'] | c['official']


def test_raiz_potencia_e_limites():
    i = corrente_carga(80000, 400, .06, 250, 450)
    assert 400*i+.06*i*i == pytest.approx(80000)
    assert corrente_carga(80000, 400, .06, 100, 450) == 100
    assert corrente_carga(80000, 440, .1, 250, 450) == 100


def test_carga_ideal_analitica():
    c = inputs() | {'resistance_ref_ohm': 0, 'ocv_v': [400]*5}
    r = resolver(c, 20000)
    assert r['duration_s'] == pytest.approx(245*.6*3600/50)
    assert r['final_battery_k'] == pytest.approx(298.15)
    assert r['final_soc'] == pytest.approx(.8, abs=1e-10)
    assert r['terminal_energy_j'] == pytest.approx(400*245*.6*3600)


def test_balancos_e_potencia_nao_vira_calor():
    r = resolver(inputs(), 80000)
    assert r['stop'] == 'target_soc'
    assert abs(r['thermal_residual_j']) < .1
    assert abs(r['electrical_residual_j']) < .1
    assert r['ohmic_energy_j'] < .1*r['terminal_energy_j']


def test_adiabatico_analitico_capacidade_sensivel():
    c = inputs() | {'battery_coolant_ua_w_k': 0, 'cooler_ambient_ua_w_k': 0}
    r = resolver(c, 80000)
    delta = r['ohmic_energy_j']/(650*900)
    assert r['final_battery_k']-298.15 == pytest.approx(delta, abs=1e-7)


def test_evento_temperatura():
    r = resolver(inputs() | {'temperature_stop_k': 298.2}, 80000)
    assert r['stop'] == 'temperature_limit'
    assert r['final_soc'] < .8
    assert r['final_battery_k'] == pytest.approx(298.2)


@pytest.mark.parametrize('bad', [{'soc_final': .1}, {'capacity_ah': 0}, {'ocv_v': [400]}, {'resistance_ref_ohm': -1}])
def test_invalidos(bad):
    with pytest.raises(ValueError):
        resolver(inputs() | bad, 20000)
