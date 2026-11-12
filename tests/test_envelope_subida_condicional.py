import pytest

from scripts.modelar_envelope_subida_condicional import (
    front_normal_n,
    road_load_n,
    solve_steady_climb,
)


def test_front_normal_load_on_level_matches_static_axle_fraction():
    assert front_normal_n(1000, 2, 0.5, 4, 0) == pytest.approx(4903.325)
    assert front_normal_n(1000, 2, 0.5, 4, 0.1) < front_normal_n(1000, 2, 0.5, 4, 0)


def test_level_aero_force_uses_relative_air_speed_and_sign():
    still = road_load_n(1000, 10, 0, 0, 0, 0.5, 2, 1.2)
    headwind = road_load_n(1000, 10, 0, 5, 0, 0.5, 2, 1.2)
    tailwind = road_load_n(1000, 10, 0, -5, 0, 0.5, 2, 1.2)
    assert headwind > still > tailwind


def test_climb_solver_closes_force_balance_and_power_limit():
    result = solve_steady_climb(4000, 2, 0.9, 4, 60, 0.5, 0, 0.012,
                               0.62, 4.8, 1.1, 205, 0.9)
    assert result["level_motion_feasible_in_model"]
    assert not result["grade_search_capped_at_50_percent"]
    assert result["maximum_grade_percent_in_model"] > 0
    assert abs(result["force_balance_residual_n_at_limit"]) < 1e-6
    assert result["limiting_mechanism_at_grade"] in {"potencia", "aderencia_dianteira"}


def test_rejects_impossible_or_nonfinite_inputs():
    with pytest.raises(ValueError):
        solve_steady_climb(4000, 2, 0.9, 4, 0, 0.5, 0, 0.012,
                           0.62, 4.8, 1.1, 205, 0.9)
    with pytest.raises(ValueError):
        solve_steady_climb(4000, 2, 0.9, 4, 60, 0.5, 0, 0.012,
                           0.62, 4.8, 1.1, 205, 1.1)
