"""Ensaios analíticosSYNTHETIC para geografia, limites e energia em rampa."""

import pandas as pd
import pytest

from motorhome.rota import Rota, preparar_rota
from motorhome.viagem_rota import simular_viagem


def fixture(grade=0.):
    steps = pd.DataFrame({'end_km': [1., 2.], 'model_max_km_h': [40., 80.],
                          'approximate_cap_km_h': [40., 90.]})
    elevation = pd.DataFrame({'distance_km': [0., 1., 2.], 'elevation_m': [0., grade*1000, grade*2000]})
    d = {'air_density_kg_m3': 1., 'frontal_area_m2': 1., 'mass_kg': 1000., 'driving_auxiliary_power_w': 0.}
    p = {'drag_coefficient_assumed': 0., 'rolling_coefficient_assumed': 0., 'traction_efficiency_assumed': 1.}
    return Rota(steps, elevation, d, p, regen=.5)


def test_piecewise_speed_cap_and_exact_distance():
    route = fixture()
    result = route.mover(0., 1., 90)
    assert [r['speed_km_h'] for r in result] == [40., 80.]
    assert sum(r['duration_h'] for r in result) == pytest.approx(1/40+1/80)
    assert result[-1]['end_km'] == pytest.approx(2.)


def test_grade_potential_energy_and_regeneration_sign():
    up, down = fixture(.01), fixture(-.01)
    positive = sum(r['battery_kwh'] for r in up.mover(0., 1., 60.))
    negative = sum(r['battery_kwh'] for r in down.mover(0., 1., 60.))
    # sin(arctan(grade))*distance: projetado ao comprimento horizontal da rota.
    expected = 1000*9.80665*20/(3_600_000*(1+.01**2)**.5)
    assert positive == pytest.approx(expected)
    assert negative == pytest.approx(-expected*.5)


def test_target_stops_without_changing_geographic_distance():
    result = fixture().mover(.5, 1., 90., target_km=1.5)
    assert result[-1]['end_km'] == pytest.approx(1.5)
    assert sum(r['end_km']-r['start_km'] for r in result) == pytest.approx(1.)


def test_osrm_ferry_rejected_instead_of_becoming_free_road_energy():
    payload = {'code': 'Ok', 'routes': [{'distance': 1000., 'geometry': {'coordinates': [[0, 0], [0, .01]]},
                'legs': [{'annotation': {'distance': [1000.]}, 'steps': [{'mode': 'ferry', 'distance': 1000., 'duration': 100., 'name': 'balsa'}]}]}]}
    c = {'vehicle_limiter_km_h': 90, 'approximate_caps_km_h': {'federal': 90, 'state': 80, 'urban': 40, 'other': 60}}
    with pytest.raises(ValueError, match='Balsa'):
        preparar_rota(payload, c)


def test_real_route_distance_is_not_scaled_to_prescribed_7000():
    payload = {'code': 'Ok', 'routes': [{'distance': 1000., 'geometry': {'coordinates': [[0, 0], [0, .01]]},
                'legs': [{'annotation': {'distance': [1000.]}, 'steps': [{'mode': 'driving', 'distance': 1000., 'duration': 60., 'name': 'Rua', 'ref': ''}]}]}]}
    c = {'vehicle_limiter_km_h': 90, 'approximate_caps_km_h': {'federal': 90, 'state': 80, 'urban': 40, 'other': 60}}
    geometry, steps = preparar_rota(payload, c)
    assert geometry.distance_km.iloc[-1] == 1.
    assert steps.model_max_km_h.iloc[-1] == 40.
    assert not steps.posted_limit_verified.any()


def test_two_batteries_no_solar_can_still_drive_from_initial_traction():
    class Solar:
        def at(self, *args):
            return 0., 0.

    route = fixture()
    geometry = pd.DataFrame({'distance_km': [0., 2.], 'latitude_deg': [-1., -1.], 'longitude_deg': [-48., -48.]})
    c = {'integration_minutes': 5, 'portable_setup_minutes': 30, 'portable_teardown_minutes': 30,
         'traction_initial_soc': 1., 'service_initial_soc': .8, 'traction_reserve_soc': .1,
         'service_reserve_soc': .2, 'start_date': '2025-06-21', 'timezone': 'America/Sao_Paulo',
         'max_days': 1, 'night_driving_end_hour': 6, 'night_driving_start_hour': 22,
         'driving_hours_per_day_max': 8, 'traction_keep_next_day_kwh': 1,
         'service_target_before_trip_soc': .8}
    battery = {'traction_capacity_kwh': 98., 'service_capacity_kwh': 10.24}
    spec = {'inverter': {'efficiency_assumed': .9, 'continuous_power_kw_at40c': 3.7,
                         'apparent_power_kva_at25c': 5., 'household_power_factor_assumed': .9, 'idle_power_kw_published': 0.},
            'charge': {'current_modes_a_assumed': [0, 6], 'voltage_v_assumed': 230, 'power_factor_assumed': 1.,
                       'onboard_efficiency_assumed': .9, 'evse_standby_kw_assumed': 0.},
            'household': {'hvac_start_hour_assumed': 12, 'hvac_duration_h_assumed': 3,
                          'cooktop_start_hour_assumed': 19, 'cooktop_duration_h_assumed': .5,
                          'dc_dc_efficiency_assumed': .9}}
    budget = {k: 0. for k in ['cold_wash_once_week_daily_average_kwh', 'hvac_two_people_3h_assumed_cop2_5_kwh',
                             'cooktop_half_hour_kwh', 'fridge_55w_assumed_50percent_duty_kwh', 'lights_pump_electronics_assumed_kwh']}
    summary, frame, drive = simular_viagem(route, Solar(), geometry, c, battery, spec, budget, 90, 'clear', interface=False)
    assert summary['arrived'] and summary['distance_km'] == pytest.approx(2.)
    assert summary['traction_final_soc'] == pytest.approx(1.)
    assert frame.transfer_dc_kw.sum() == 0
    assert drive.duration_h.sum() == pytest.approx(1/40+1/80)
