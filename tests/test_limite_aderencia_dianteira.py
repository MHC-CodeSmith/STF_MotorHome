import pytest

from scripts.calcular_limite_aderencia_dianteira import front_drive_traction_limit


def test_level_front_drive_limit_satisfies_force_balance():
    result = front_drive_traction_limit(1000.0, 2.0, 0.5, 4.0, 0.5, 0.0)
    assert result["acceleration_limit_g"] == pytest.approx(0.25 / 1.0625)
    assert result["can_hold_grade_at_zero_acceleration"] is True
    assert result["force_balance_residual_n"] == pytest.approx(0.0, abs=1e-9)


def test_six_percent_grade_holding_depends_on_front_adhesion():
    poor = front_drive_traction_limit(1000.0, 2.0, 0.5, 4.0, 0.1, 6.0)
    adequate = front_drive_traction_limit(1000.0, 2.0, 0.5, 4.0, 0.2, 6.0)
    assert poor["can_hold_grade_at_zero_acceleration"] is False
    assert poor["acceleration_limit_g"] < 0.0
    assert adequate["can_hold_grade_at_zero_acceleration"] is True
    assert adequate["acceleration_limit_g"] > 0.0


@pytest.mark.parametrize("values", [
    (0.0, 2.0, 0.5, 4.0, 0.5, 0.0),
    (1000.0, 0.0, 0.5, 4.0, 0.5, 0.0),
    (1000.0, 2.0, 0.0, 4.0, 0.5, 0.0),
    (1000.0, 2.0, 0.5, 0.0, 0.5, 0.0),
    (1000.0, 2.0, 0.5, 4.0, 0.0, 0.0),
])
def test_rejects_invalid_inputs(values):
    with pytest.raises(ValueError):
        front_drive_traction_limit(*values)
