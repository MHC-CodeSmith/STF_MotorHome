"""SYNTHETIC: perdas em série, discretização EVSE e limites compartilhados."""

import copy

import pandas as pd
import pytest

from motorhome.interface_carga import (
    otimizar_interface,
    potencias_interface,
    verificar_interface,
)


def fixture():
    c = {'setup_minutes_assumed': 60, 'teardown_minutes_assumed': 60, 'speed_modes_km_h': [10.],
         'traction_capacity_kwh': 2., 'service_capacity_kwh': 8., 'service_min_soc': 0.,
         'service_initial_soc': .5, 'service_final_soc': .5, 'traction_min_soc': 0.,
         'transfer_efficiency_assumed': .4, 'solver_time_limit_s': 5.}
    spec = {'inverter': {'efficiency_assumed': .8, 'continuous_power_kw_at40c': 2.,
                         'apparent_power_kva_at25c': 3., 'household_power_factor_assumed': 1.},
            'charge': {'current_modes_a_assumed': [0, 1], 'voltage_v_assumed': 1000,
                       'power_factor_assumed': 1., 'onboard_efficiency_assumed': .5},
            'household': {'dc12_power_limit_kw': .36}}
    data = pd.DataFrame({'fixed_kw': [2.5, 0., 0., 0.], 'portable_kw': 0., 'house_kw': 0.,
                         'house_ac_kw': 0., 'dc12_kw': 0.},
                        index=pd.date_range('2026-06-21', periods=4, freq='h', tz='America/Sao_Paulo'))
    return data, c, spec


def test_two_conversion_losses_and_quantized_current():
    data, c, spec = fixture()
    r = otimizar_interface(data, c, [1.], spec, 0., 0., 8.)
    assert r['feasible'] and r['optimal_in_grid']
    assert r['distance_km'] == pytest.approx(10.)
    assert r['verification']['transfer_input_kwh'] == pytest.approx(2.5)
    assert r['verification']['transfer_loss_kwh'] == pytest.approx(1.5)
    assert sum(x['charge_current_a'] > 0 for x in r['schedule']) == 2
    assert all(x['transfer_kw'] == pytest.approx(0.) or x['transfer_kw'] == pytest.approx(1.25)
               for x in r['schedule'])


def test_house_and_charger_share_active_output_limit():
    data, c, spec = fixture()
    spec['inverter']['continuous_power_kw_at40c'] = 1.1
    data['house_ac_kw'] = .2
    data['house_kw'] = .25
    r = otimizar_interface(data, c, [1.], spec, 0., 0., 8.)
    assert r['feasible'] and r['distance_km'] == pytest.approx(0.)


def test_apparent_power_limit_is_independent_of_active_power():
    data, c, spec = fixture()
    spec['inverter']['apparent_power_kva_at25c'] = 1.5
    spec['charge']['power_factor_assumed'] = .5
    spec['charge']['current_modes_a_assumed'] = [0, 2]
    # Mesma potência ativa1kW, mas2kVA excedem1,5kVA.
    r = otimizar_interface(data, c, [1.], spec, 0., 0., 8.)
    assert r['feasible'] and r['distance_km'] == pytest.approx(0.)


def test_excess_dc_load_is_infeasible_even_when_charger_off():
    data, c, spec = fixture()
    data['dc12_kw'] = .4
    assert not otimizar_interface(data, c, [1.], spec, 0., 0., 8.)['feasible']


def test_replay_rejects_subminimum_current_and_forged_export():
    data, c, spec = fixture()
    result = otimizar_interface(data, c, [1.], spec, 0., 0., 8.)
    rows = copy.deepcopy(result['schedule'])
    rows[0]['charge_current_a'] = .1
    with pytest.raises(ValueError, match='Corrente'):
        verificar_interface(rows, data, c, [1.], spec, 0., 0., 8.)
    rows[0]['transfer_kw'] = .125
    with pytest.raises(ValueError):
        verificar_interface(rows, data, c, [1.], spec, 0., 0., 8.)


def test_rejects_inconsistent_efficiency_or_current_modes():
    data, c, spec = fixture()
    c['transfer_efficiency_assumed'] = .9
    with pytest.raises(ValueError, match='Perdas'):
        otimizar_interface(data, c, [1.], spec, 0., 0., 8.)
    spec['charge']['current_modes_a_assumed'] = [6, 8]
    with pytest.raises(ValueError):
        potencias_interface(spec)
