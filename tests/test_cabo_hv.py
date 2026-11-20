"""Contorno de cabos HV: regressão contra o solver r–θ e limites físicos.

Os parâmetros de cabo aqui são os da ficha RADOX 155 (1×120 mm²); os contornos
são sintéticos e explícitos, não medições.
"""

import itertools
from dataclasses import replace

import numpy as np
import pytest

from motorhome.cabo_hv import (
    CondicoesContorno,
    coeficientes,
    h_conveccao,
    h_radiacao,
    resolver_estacionario,
    resolver_fases,
    resolver_transiente,
)
from motorhome.cabos_polares import Cabo, resolver

# 1×120 mm² RADOX 155: feixe Ø15,1 mm, externo Ø18 mm, R20 0,153 Ω/km.
C120 = Cabo(0.00755, 0.009, 200.0, 0.2, 0.000153, 0.00393, 293.15)
REFERENCIA = CondicoesContorno(t_ar_c=25, t_radiante_c=25, fator_forma_radiacao=1.0,
                               fator_confinamento_conveccao=1.0, n_fases=1,
                               fator_perda_ac=1.0)


def test_contorno_reduzido_reproduz_solver_r_theta():
    """O caso de referência deve reproduzir o código anterior (85,37 °C a 489 A)."""
    corrente = 489.4204651759762
    novo = resolver_estacionario(C120, corrente, REFERENCIA)
    # Reimplementação direta do contorno antigo: h_conv + h_rad linearizada.
    ts = 298.15 + 30.0
    for _ in range(200):
        h_conv = h_conveccao(ts, 298.15, 2 * C120.raio_externo_m)
        h_rad = h_radiacao(ts, 298.15, 0.9, 1.0)
        antigo = resolver(C120, corrente, 32, 128, h_conv + h_rad, 298.15)
        novo_ts = float(np.mean(antigo["temperatura_superficie_k"]))
        if abs(novo_ts - ts) < 1e-6:
            break
        ts = 0.5 * ts + 0.5 * novo_ts
    assert novo["temperatura_max_k"] == pytest.approx(
        float(antigo["temperatura_max_k"]), rel=1e-9)
    assert novo["temperatura_max_k"] - 273.15 == pytest.approx(85.37, abs=0.02)


def test_balanco_de_energia_e_residuo():
    r = resolver_estacionario(C120, 300.0, REFERENCIA)
    assert r["joule_w_m"] == pytest.approx(r["removido_w_m"], rel=1e-8)
    assert abs(r["residuo_w_m"]) < 1e-6


def test_temperatura_cresce_com_corrente_e_ambiente():
    t_base = resolver_estacionario(C120, 300.0, REFERENCIA)["temperatura_max_k"]
    t_maior = resolver_estacionario(C120, 400.0, REFERENCIA)["temperatura_max_k"]
    assert t_maior > t_base
    quente = replace(REFERENCIA, t_ar_c=60, t_radiante_c=60)
    assert (resolver_estacionario(C120, 300.0, quente)["temperatura_max_k"]
            > resolver_estacionario(C120, 300.0, replace(REFERENCIA, t_ar_c=25,
                                                        t_radiante_c=25))["temperatura_max_k"])


def test_bitola_maior_e_conduite_escoram_menos():
    grande = replace(C120, raio_feixe_m=0.0085, raio_externo_m=0.010,
                     resistencia20_ohm_m=0.000122)
    t_pequeno = resolver_estacionario(C120, 400.0, REFERENCIA)["temperatura_max_k"]
    t_grande = resolver_estacionario(grande, 400.0, REFERENCIA)["temperatura_max_k"]
    assert t_grande < t_pequeno
    confinado = replace(REFERENCIA, fator_confinamento_conveccao=0.7,
                        fator_forma_radiacao=0.3)
    assert (resolver_estacionario(C120, 400.0, confinado)["temperatura_max_k"]
            > resolver_estacionario(C120, 400.0, REFERENCIA)["temperatura_max_k"])


def test_coeficientes_ponderam_sinks_distintos():
    h_total, t_sink, h_conv, h_rad = coeficientes(330.0, C120,
                                                 replace(REFERENCIA, t_radiante_c=80))
    assert h_total == pytest.approx(h_conv + h_rad)
    assert 298.15 < t_sink < 353.15


def test_resolver_fases_uma_fase_igual_caso_isolado():
    contorno = replace(REFERENCIA, n_fases=3, fracao_perimetro_exposto=0.8)
    solitario = resolver_estacionario(C120, 300.0,
                                      replace(contorno, n_fases=1,
                                              fracao_perimetro_exposto=0.8))
    grupo = resolver_fases([C120], [300.0], contorno)
    assert grupo[0]["temperatura_max_k"] == pytest.approx(solitario["temperatura_max_k"])


def test_transitorio_parte_do_regime_e_tende_a_ele():
    tr = resolver_transiente(C120, 200.0, 300.0, REFERENCIA, duracao_pico_s=60.0,
                             t_limite_k=398.15, passo_s=2.0)
    assert tr["tau_s"] > 0
    assert tr["temperatura_regime_k"] == pytest.approx(
        resolver_estacionario(C120, 200.0, REFERENCIA)["temperatura_max_k"], rel=1e-9)
    # Pico sobe a temperatura, monotonicamente e abaixo do estacionário do pico.
    historico = [t for _, t in tr["historico"]]
    assert historico[0] == pytest.approx(tr["temperatura_regime_k"])
    assert all(b >= a - 1e-9 for a, b in itertools.pairwise(historico))
    assert tr["temperatura_pico_k"] < resolver_estacionario(
        C120, 300.0, REFERENCIA)["temperatura_max_k"]


def test_perda_ac_equivale_a_corrente_maior():
    """f_ac = 1,21 deve equivaler a 1,1× a corrente (I_eff = I·sqrt(f_ac))."""
    com_perda = resolver_estacionario(
        C120, 300.0, replace(REFERENCIA, fator_perda_ac=1.21))["temperatura_max_k"]
    corrente_equivalente = resolver_estacionario(
        C120, 330.0, REFERENCIA)["temperatura_max_k"]
    assert com_perda == pytest.approx(corrente_equivalente, rel=1e-6)


@pytest.mark.parametrize("kwargs", [
    {"emissividade": 1.1}, {"fator_forma_radiacao": -0.1},
    {"fator_confinamento_conveccao": 2.0}, {"n_fases": 0},
    {"fator_perda_ac": 0.5}, {"t_ar_c": -300.0},
])
def test_contorno_invalido(kwargs):
    with pytest.raises(ValueError):
        CondicoesContorno(**kwargs)
