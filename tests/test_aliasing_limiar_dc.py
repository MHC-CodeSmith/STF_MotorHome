import pytest

from scripts.analisar_aliasing_limiar_dc import (
    integrate_linear_above_threshold_kwh,
    interval_gate_energy_kwh,
)


def test_integrates_linear_ramp_crossing_threshold_exactly():
    # 0 -> 2 kW for 1 h; only the final half-hour is above 1 kW.
    assert integrate_linear_above_threshold_kwh(0, 2, 1, 1) == pytest.approx(0.75)


def test_integrates_descending_crossing_symmetrically():
    assert integrate_linear_above_threshold_kwh(2, 0, 1, 1) == pytest.approx(0.75)


def test_integrates_full_interval_when_both_endpoints_clear_threshold():
    assert integrate_linear_above_threshold_kwh(2, 4, 0.5, 1) == pytest.approx(1.5)


def test_returns_zero_when_interval_stays_below_threshold():
    assert integrate_linear_above_threshold_kwh(0.2, 0.9, 1, 1) == 0


def test_existing_mean_gate_can_miss_a_valid_subinterval():
    current = interval_gate_energy_kwh(0.2, 1.8, 1, 1 / 0.9, 0.9)
    reference = 0.9 * integrate_linear_above_threshold_kwh(0.2, 1.8, 1, 1 / 0.9)
    assert current == 0
    assert reference > 0


def test_existing_mean_gate_passes_full_interval_when_mean_clears_threshold():
    current = interval_gate_energy_kwh(0.2, 2.2, 1, 1 / 0.9, 0.9)
    reference = 0.9 * integrate_linear_above_threshold_kwh(0.2, 2.2, 1, 1 / 0.9)
    assert current == pytest.approx(1.08)
    assert reference < current
