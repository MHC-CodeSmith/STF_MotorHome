import pytest

from scripts.calcular_envelope_frenagem_eixos import loads_under_braking


def test_static_axle_loads_conserve_mass():
    front, rear, transfer = loads_under_braking(4000.0, 2.0, 0.9, 4.0, 0.0)
    assert front == pytest.approx(2000.0)
    assert rear == pytest.approx(2000.0)
    assert transfer == 0.0


def test_braking_moves_load_forward_and_conserves_total():
    front, rear, transfer = loads_under_braking(4000.0, 2.0, 0.9, 4.0, 0.3)
    assert transfer == pytest.approx(270.0)
    assert front + rear == pytest.approx(4000.0)
    assert front == pytest.approx(2000.0 + transfer)
    assert rear == pytest.approx(2000.0 - transfer)


@pytest.mark.parametrize("values", [
    (0.0, 2.0, 0.9, 4.0, 0.1),
    (4000.0, 0.0, 0.9, 4.0, 0.1),
    (4000.0, 4.0, 0.9, 4.0, 0.1),
    (4000.0, 2.0, 0.9, 4.0, -0.1),
    (4000.0, 2.0, 0.9, 0.0, 0.1),
])
def test_rejects_invalid_inputs(values):
    with pytest.raises(ValueError):
        loads_under_braking(*values)
