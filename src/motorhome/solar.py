"""Céu limpo/POA/potência com pvlib; hipóteses térmicas e elétricas explícitas."""

import numpy as np
import pandas as pd
import pvlib


def simular_dia(config, passo_min=1):
    if isinstance(passo_min, bool) or not isinstance(passo_min, int) or passo_min < 1 or 1440 % passo_min:
        raise ValueError('Passo deve dividir 1440 minutos e ser inteiro positivo')
    s, a, m, h = (config[k] for k in ('scenario', 'array', 'module', 'assumptions'))
    for name in ('other_losses_fraction', 'converter_efficiency'):
        value = h[name]
        if isinstance(value, bool) or not np.isfinite(value) or not 0 <= value <= 1:
            raise ValueError(f'{name}: fração finita em [0,1]')
    if h['converter_efficiency'] == 0 or h['faiman_u0_w_m2k'] <= 0:
        raise ValueError('Eficiência e U0 devem ser positivos')
    if any(isinstance(n, bool) or not isinstance(n, int) or n <= 0 for n in a['module_counts']):
        raise ValueError('Quantidade de módulos deve ser inteiro positivo')
    if m['p_stc_w'] <= 0 or not -1 < m['gamma_pdc_per_k'] <= 0:
        raise ValueError('Potência STC/coefficientes do módulo inválidos')
    start = pd.Timestamp(s['date'], tz=s['timezone'])
    end = start+pd.DateOffset(days=1)
    times = pd.date_range(start, end, freq=f'{passo_min}min')
    local = pvlib.location.Location(s['latitude_deg'], s['longitude_deg'],
                                    tz=s['timezone'], altitude=s['altitude_m'])
    position = local.get_solarposition(times, temperature=s['ambient_temperature_c'])
    clear = local.get_clearsky(times, model='ineichen', solar_position=position)
    poa = pvlib.irradiance.get_total_irradiance(
        a['tilt_deg'], a['azimuth_deg'], position['apparent_zenith'], position['azimuth'],
        clear.dni, clear.ghi, clear.dhi, albedo=a['albedo'], model='isotropic')
    tm = pvlib.temperature.faiman(poa.poa_global, s['ambient_temperature_c'], s['wind_speed_m_s'],
                                 u0=h['faiman_u0_w_m2k'], u1=h['faiman_u1_w_s_m3k'])
    power = pvlib.pvsystem.pvwatts_dc(poa.poa_global, tm, m['p_stc_w'], m['gamma_pdc_per_k']).clip(lower=0)
    result = pd.DataFrame({'ghi_w_m2': clear.ghi, 'dni_w_m2': clear.dni, 'dhi_w_m2': clear.dhi,
                           'poa_w_m2': poa.poa_global, 'temperature_module_c': tm,
                           'module_dc_w': power, 'sun_elevation_deg': position.apparent_elevation})
    for n in a['module_counts']:
        result[f'dc_{n}_modules_w'] = n*power
        result[f'terminal_assumed_{n}_modules_w'] = n*power*(1-h['other_losses_fraction'])*h['converter_efficiency']
    if not np.isfinite(result.to_numpy()).all():
        raise ValueError('Resultado não finito')
    return result


def integrar_kwh(series):
    """Trapézios em segundos reais, potência em W. Exige índice temporal ordenado."""
    if len(series) < 2 or not isinstance(series.index, pd.DatetimeIndex) or series.index.tz is None:
        raise ValueError('Série com ao menos 2 horários e fuso obrigatória')
    # Pandas pode armazenar ns ou us; não assumir unidade do inteiro interno.
    seconds = (series.index-series.index[0]).total_seconds().to_numpy()
    p = series.to_numpy(dtype=float)
    if (np.diff(seconds) <= 0).any() or not np.isfinite(p).all() or (p < 0).any():
        raise ValueError('Potências não negativas finitas e tempos crescentes obrigatórios')
    return float(np.trapz(p, seconds)/3_600_000)
