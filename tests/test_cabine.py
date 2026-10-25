"""Verificações analíticas da rede e da psicrometria; não validam a van."""

import numpy as np
import pytest

from motorhome.cabine import integrar_zona, transmitancia, umidade_especifica


def test_resistencias_em_serie():
    assert transmitancia([(0.1, 0.05)], 10, 10) == pytest.approx(1/2.2)


def test_exponencial_e_conservacao():
    t = np.linspace(0, 1000, 11)
    temp, res = integrar_zona(t, np.full(11, 200), 10, 1000, 20, 20)
    assert temp == pytest.approx(40-20*np.exp(-t/100), abs=1e-12)
    assert abs(res) < 1e-8


def test_equilibrio_sem_sol():
    temp, res = integrar_zona([0, 500], [0, 0], 10, 1000, 25, 25)
    assert temp == pytest.approx([25, 25])
    assert res == 0


def test_umidade_referencia_e_pressao():
    # Psicrometria de referência: 25°C, 50%, 101325 Pa ~9.88 g/kg seco.
    assert umidade_especifica(25, 0.5, 101325) == pytest.approx(0.00988, abs=2e-5)
    assert umidade_especifica(25, 0, 101325) == 0
    assert umidade_especifica(25, 0.5, 91000) > umidade_especifica(25, 0.5, 101325)


@pytest.mark.parametrize('times,gains', [([0, 0], [0, 1]), ([1, 0], [0, 1]),
                                       ([0, 1], [0]), ([0, 1], [0, float('nan')])])
def test_dados_invalidos(times, gains):
    with pytest.raises(ValueError):
        integrar_zona(times, gains, 10, 1000, 25, 25)


def test_psicrometria_fora_do_dominio():
    with pytest.raises(ValueError):
        umidade_especifica(60, 0.5, 101325)
    with pytest.raises(ValueError):
        umidade_especifica(25, 1.1, 101325)
