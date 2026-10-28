"""Casos SYNTHETIC analíticos, sem validação física do motorhome."""

import copy

import pandas as pd
import pytest

from motorhome.agenda_portatil import otimizar_dia, verificar_agenda


def case(n=4):
    data = pd.DataFrame({'fixed_kw': [0.]*n, 'portable_kw': [0.]*n, 'house_kw': [0.]*n},
                        index=pd.date_range('2026-06-21', periods=n, freq='h', tz='America/Sao_Paulo'))
    c = {'setup_minutes_assumed': 60, 'teardown_minutes_assumed': 60, 'speed_modes_km_h': [10.],
         'traction_capacity_kwh': 2., 'service_capacity_kwh': 4., 'service_min_soc': 0.,
         'service_initial_soc': .5, 'service_final_soc': .5, 'traction_min_soc': 0.,
         'transfer_efficiency_assumed': .5, 'solver_time_limit_s': 5.}
    return data, c


def test_exact_soc_with_fractional_drive_and_separate_banks():
    data, c = case()
    r = otimizar_dia(data, c, [1.], 1., .3, 24., 0.)
    assert r['feasible'] and r['optimal_in_grid']
    assert r['distance_km'] == pytest.approx(14.)
    assert r['verification']['traction_final_soc'] == pytest.approx(.3)
    assert r['verification']['service_final_soc'] == pytest.approx(.5)
    assert r['verification']['drive_kwh'] == pytest.approx(1.4)


def test_portable_requires_setup_and_teardown_without_driving():
    data, c = case(6)
    data['portable_kw'] = [0., 2., 0., 0., 0., 0.]
    # 2kWh coletados, 50% transferidos: 1kWh de tração, exatamente 10km.
    r = otimizar_dia(data, c, [1.], 0., 0., 8., 2.)
    assert r['feasible'] and r['distance_km'] == pytest.approx(10.)
    assert r['schedule'][0]['state'] == 'setup_0'
    assert r['schedule'][1]['state'] == 'deployed'
    assert r['schedule'][2]['state'] == 'teardown_0'
    assert all(x['portable_kw'] == 0 for x in r['schedule'] if x['driving_h'] > 1e-7)
    assert r['verification']['transfer_loss_kwh'] == pytest.approx(1.)


def test_without_hv_interface_portable_cannot_feed_traction():
    data, c = case(6)
    data['portable_kw'] = 2.
    r = otimizar_dia(data, c, [1.], 0., 0., 8., 0.)
    assert r['feasible'] and r['distance_km'] == pytest.approx(0.)


def test_future_solar_cannot_pay_earlier_household_deficit():
    data, c = case()
    c['service_initial_soc'] = c['service_final_soc'] = 0.
    data['house_kw'] = [1., 0., 0., 0.]
    data['fixed_kw'] = [0., 2., 0., 0.]
    r = otimizar_dia(data, c, [1.], 0., 0., 8., 2.)
    assert not r['feasible']


def test_driving_cap_and_exact_target():
    data, c = case()
    r = otimizar_dia(data, c, [.1], 1., .95, 1., 0., target_km=10.)
    assert r['distance_km'] == pytest.approx(10.)
    assert max(r['verification']['daily_driving_h'].values()) == pytest.approx(1.)
    assert not otimizar_dia(data, c, [.1], 1., .9, 1., 0.)['feasible']


def test_verifier_rejects_forged_solar_transfer_or_mounting():
    data, c = case()
    r = otimizar_dia(data, c, [1.], 1., .5, 24., 0.)
    for key, value in [('portable_kw', 10.), ('transfer_kw', 1.), ('state', 'deployed')]:
        rows = copy.deepcopy(r['schedule'])
        rows[0][key] = value
        with pytest.raises(ValueError):
            verificar_agenda(rows, data, c, [1.], 1., .5, 24., 0.)


def test_multiple_setup_steps_and_no_solar_during_mounting():
    data, c = case(8)
    c['setup_minutes_assumed'] = 120
    data['portable_kw'] = [0., 0., 2., 0., 0., 0., 0., 0.]
    r = otimizar_dia(data, c, [1.], 0., 0., 8., 2.)
    assert r['distance_km'] == pytest.approx(10.)
    assert [x['state'] for x in r['schedule'][:3]] == ['setup_0', 'setup_1', 'deployed']


def test_invalid_temporal_grid_or_fractions():
    data, c = case()
    with pytest.raises(ValueError, match='SOC'):
        otimizar_dia(data, c, [1.], 1., 1.1, 24., 0.)
    data.index = pd.date_range('2026-06-21 23:30', periods=4, freq='h', tz='America/Sao_Paulo')
    with pytest.raises(ValueError, match='meias-noites'):
        otimizar_dia(data, c, [1.], 1., .5, 24., 0.)
