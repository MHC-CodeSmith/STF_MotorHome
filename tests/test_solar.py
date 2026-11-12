from copy import deepcopy
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

from motorhome.solar import integrar_kwh, simular_dia


@pytest.fixture(scope='module')
def config():
    return yaml.safe_load((Path(__file__).resolve().parents[1]/'config/solar_proposta.yaml').read_text())


def test_integral_analitica_potencia_constante():
    time = pd.date_range('2026-06-21', periods=3, freq='30min', tz='America/Sao_Paulo')
    assert integrar_kwh(pd.Series([1000., 1000., 1000.], index=time)) == 1.


def test_integral_tempos_irregulares_usa_intervalos_reais():
    time = pd.DatetimeIndex([
        '2026-06-21T00:00:00-03:00',
        '2026-06-21T01:00:00-03:00',
        '2026-06-21T03:00:00-03:00',
    ])
    # 0→2 W over 1 h gives 1 Wh; 2 W over the next 2 h gives 4 Wh.
    assert integrar_kwh(pd.Series([0., 2., 2.], index=time)) == pytest.approx(.005)


def test_solar_limites_horizonte_simetria_quantidade_e_conversao(config):
    r = simular_dia(config, 5)
    assert len(r) == 289
    np.testing.assert_allclose(r.poa_w_m2, r.ghi_w_m2, atol=1e-8)
    np.testing.assert_allclose(r.dc_3_modules_w, r.dc_2_modules_w*1.5)
    assert r.iloc[0].module_dc_w == 0
    assert (r.module_dc_w[r.sun_elevation_deg < -1] == 0).all()
    assert (r.terminal_assumed_3_modules_w <= r.dc_3_modules_w).all()
    assert 1 < integrar_kwh(r.ghi_w_m2) < 10


def test_temperatura_e_passo_convergem(config):
    fine, coarse = simular_dia(config, 1), simular_dia(config, 5)
    e = integrar_kwh(fine.dc_2_modules_w)
    assert abs(e-integrar_kwh(coarse.dc_2_modules_w))/e < .001
    cool = deepcopy(config)
    cool['scenario']['ambient_temperature_c'] = 5
    assert integrar_kwh(simular_dia(cool, 5).dc_2_modules_w) > integrar_kwh(coarse.dc_2_modules_w)


def test_recusa_entradas_invalidas(config):
    with pytest.raises(ValueError):
        simular_dia(config, 7)
    bad = deepcopy(config)
    bad['assumptions']['converter_efficiency'] = float('nan')
    with pytest.raises(ValueError):
        simular_dia(bad)
