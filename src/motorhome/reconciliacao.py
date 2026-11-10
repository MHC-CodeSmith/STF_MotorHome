"""Balanços pós-DEC061. Valores hipotéticos nunca habilitam a interface OEM.

Energia em kWh; potências em kW; tempo em horas. O buffer é exclusivamente
um estado de estudo da recarga, sem qualquer conexão ao banco de serviços.
"""

import math


def _positive(value, name, zero=False):
    if isinstance(value, bool) or not math.isfinite(value) or value < 0 or (not zero and value == 0):
        raise ValueError(f'{name}: valor finito positivo obrigatório')


def consumo_plano(velocidade_kmh, massa_kg, cd, area_m2, crr, rho, eficiencia, *, aux_traction_kw=0.):
    """Consumo exclusivo da tração; não inclui cargas habitáveis ou rampas."""
    for name, value in locals().copy().items():
        _positive(value, name, zero=name == 'aux_traction_kw')
    if eficiencia > 1:
        raise ValueError('Eficiência maior que um')
    v = velocidade_kmh/3.6
    aero = .5*rho*cd*area_m2*v*v
    rolling = crr*massa_kg*9.80665
    rodas = (aero+rolling)*v/1000
    bateria = rodas/eficiencia+aux_traction_kw
    return {'aerodinamica_n': aero, 'rolamento_n': rolling, 'rodas_kw': rodas,
            'bateria_kw': bateria, 'kwh_km': bateria/velocidade_kmh,
            'km_kwh': velocidade_kmh/bateria}


def dimensionar_modulos(consumo_bateria_kwh_dia, dias, reserva, modulo_kwh, dod_max):
    """SOC relativo à energia nominal. Reserva e DoD não se multiplicam."""
    for name, val in [('consumo', consumo_bateria_kwh_dia), ('dias', dias), ('modulo', modulo_kwh)]:
        _positive(val, name)
    if not 0 <= reserva < 1 or not 0 < dod_max <= 1:
        raise ValueError('Reserva/DoD inválidos')
    janela = min(1-reserva, dod_max)
    n = math.ceil(consumo_bateria_kwh_dia*dias/(modulo_kwh*janela)-1e-12)
    return {'modulos': n, 'nominal_kwh': n*modulo_kwh,
            'utilizavel_kwh': n*modulo_kwh*janela,
            'autonomia_h': 24*n*modulo_kwh*janela/consumo_bateria_kwh_dia}


def passo_solar(pv_kwh, servicos_solicitados_kwh, estacionado, eficiencia_dc,
                minimo_dc_kw, dt_h, interface_demonstrada=False,
                hipotetico=False, buffer_kwh=0., buffer_capacidade_kwh=0.,
                eficiencia_buffer=.95, alocacao='prioridade_servicos',
                fracao_servicos=.5):
    """Um passo conservativo a jusante do FV, antes das conversões.

    Ordem: FV para serviços, restante para DC; ou divisão fixa. Não há energia
    armazenada de serviços nesta função. O buffer inicia vazio no simulador.
    Retorna todas as parcelas para conferir PV + buffer inicial = saídas +
    perdas + corte + buffer final. Despacho do buffer à potência mínima é uma
    hipótese matemática, sem alegar existência de carregador compatível.
    """
    for name, v in [('pv', pv_kwh), ('servicos', servicos_solicitados_kwh),
                    ('buffer', buffer_kwh), ('capacidade', buffer_capacidade_kwh)]:
        _positive(v, name, zero=True)
    _positive(dt_h, 'dt')
    if not 0 < eficiencia_dc <= 1 or not 0 < eficiencia_buffer <= 1:
        raise ValueError('Eficiências inválidas')
    if buffer_kwh > buffer_capacidade_kwh+1e-10 or not 0 <= fracao_servicos <= 1:
        raise ValueError('Buffer/fração inválidos')
    if minimo_dc_kw is not None:
        _positive(minimo_dc_kw, 'mínimo')
    if alocacao == 'prioridade_servicos':
        service = min(pv_kwh, servicos_solicitados_kwh)
        extra = pv_kwh-service
        service_cut = 0.
    elif alocacao == 'fixa':
        service = min(pv_kwh*fracao_servicos, servicos_solicitados_kwh)
        service_cut = pv_kwh*fracao_servicos-service
        extra = pv_kwh*(1-fracao_servicos)
    else:
        raise ValueError('Alocação desconhecida')
    entregue = loss = 0.
    final = buffer_kwh
    # Falta de mínimo ou evidência impede energia real de tração.
    enabled = (interface_demonstrada or hipotetico) and minimo_dc_kw is not None
    if not enabled:
        curtailed = extra
    elif buffer_capacidade_kwh == 0:
        if estacionado and extra*eficiencia_dc/dt_h >= minimo_dc_kw:
            entregue = extra*eficiencia_dc
            loss = extra-entregue
            curtailed = 0.
        else:
            curtailed = extra
    else:
        stored = min(extra*eficiencia_buffer, buffer_capacidade_kwh-final)
        consumed = stored/eficiencia_buffer
        loss = consumed-stored
        final += stored
        curtailed = extra-consumed
        requested = minimo_dc_kw*dt_h/eficiencia_dc
        if estacionado and final+1e-12 >= requested:
            discharged = min(final, requested)
            final -= discharged
            entregue = discharged*eficiencia_dc
            loss += discharged-entregue
    curtailed += service_cut
    residual = pv_kwh+buffer_kwh-service-entregue-loss-curtailed-final
    return {'servicos_kwh': service, 'tracao_kwh': entregue, 'perdas_kwh': loss,
            'cortada_kwh': curtailed, 'buffer_final_kwh': final,
            'residuo_kwh': residual, 'interface_habilitada': enabled,
            'status': 'hipotetico' if hipotetico else ('demonstrado' if enabled else 'nao_demonstrado')}


def reacoes_eixos(massas_x, entre_eixos_m):
    """x a partir do eixo dianteiro. Retorna kg equivalentes, não forças em N."""
    _positive(entre_eixos_m, 'entre eixos')
    if not massas_x:
        raise ValueError('Inventário vazio')
    for mass, x in massas_x:
        _positive(mass, 'massa', zero=True)
        if not math.isfinite(x):
            raise ValueError('Coordenada inválida')
    total = sum(m for m, x in massas_x)
    rear = sum(m*x for m, x in massas_x)/entre_eixos_m
    return {'total_kg': total, 'dianteiro_kg': total-rear, 'traseiro_kg': rear}


def indice_lateral(bitola_m, h_cg_m, y_cg_m=0.):
    """Indicador geométrico; não é limite real de manobra ou homologação."""
    _positive(bitola_m, 'bitola')
    _positive(h_cg_m, 'altura')
    if not math.isfinite(y_cg_m) or abs(y_cg_m) >= bitola_m/2:
        raise ValueError('CG fora da base')
    return (bitola_m/2-abs(y_cg_m))/h_cg_m


def simular_missao(roof_kw, portable_kw, driving_slots, *, speed_kmh, kwh_km,
                   service_kwh_day, traction_capacity_kwh, service_capacity_kwh,
                   reserve_traction, reserve_service, target_km=7000.,
                   max_days=1500, mode='sem_interface', allocation='flexivel',
                   min_dc_kw=None, eta_dc=.9, eta_service=.95, eta_buffer=.95,
                   buffer_capacity_kwh=0.):
    """Replay de dia-tipo: SOCs independentes e carga externa apenas parada.

    Janela portátil planejada não é ampliada por imobilização incidental.
    Cada array de entrada contém potências médias por intervalo (pontos médios).
    Resolução limita o horário de chegada a um intervalo. Não é otimizador.
    Desligamento por baixo SOC é falha do cenário de consumo médio completo;
    não se inventam limiares de shedding ou novos perfis de conforto.
    """
    n = len(roof_kw)
    if n < 1 or len(portable_kw) != n or len(driving_slots) != n:
        raise ValueError('Séries incompatíveis')
    dt = 24/n
    if sum(driving_slots)*dt > 8+1e-9:
        raise ValueError('Mais de8h de condução planejada')
    for name, val in [('velocidade', speed_kmh), ('consumo', kwh_km),
                      ('carga', service_kwh_day), ('tracao', traction_capacity_kwh),
                      ('servicos', service_capacity_kwh), ('distancia', target_km)]:
        _positive(val, name)
    if not 0 <= reserve_traction < 1 or not 0 <= reserve_service < 1 or not 0 < eta_service <= 1:
        raise ValueError('Reservas/eficiência inválidas')
    if mode not in ['sem_interface', 'direta_hipotese', 'buffer_hipotese']:
        raise ValueError('Modo não demonstrado ou hipótese explícita obrigatório')
    if allocation not in ['A', 'B', 'flexivel']:
        raise ValueError('Alocação desconhecida')
    if any(not math.isfinite(p) or p < 0 for p in list(roof_kw)+list(portable_kw)):
        raise ValueError('Potência inválida')
    if mode != 'buffer_hipotese' and buffer_capacity_kwh:
        raise ValueError('Buffer somente em cenário dedicado')
    traction, service, buffer, distance = traction_capacity_kwh, service_capacity_kwh, 0., 0.
    totals = dict.fromkeys(['pv_kwh', 'traction_solar_kwh', 'service_solar_kwh',
                           'loss_kwh', 'curtailed_kwh', 'traction_used_kwh',
                           'service_used_kwh', 'driving_h'], 0.)
    trace, daily = [], []
    reason = 'horizonte_sem_conclusao'
    for day in range(max_days):
        drove = 0.
        for slot in range(n):
            remaining = target_km-distance
            available = max(0., traction-traction_capacity_kwh*reserve_traction)
            drive = min(speed_kmh*dt, remaining, available/kwh_km) if driving_slots[slot] else 0.
            driving = drive > 1e-9
            p_roof = float(roof_kw[slot])
            p_port = 0. if driving else float(portable_kw[slot])
            pv = (p_roof+p_port)*dt
            need = service_kwh_day/n
            service_room = max(0., service_capacity_kwh-service+need)/eta_service
            if mode == 'sem_interface':
                frac, split = 1., 'fixa'
            elif allocation == 'flexivel':
                frac, split = 1., 'prioridade_servicos'
            else:
                frac = ((p_roof if allocation == 'A' else p_port)/(p_roof+p_port)
                        if p_roof+p_port else 0.)
                split = 'fixa'
            # O carregador também não pode injetar acima de100%SOC.
            # Cortar depois do passo é permitido, mas energia recusada vira corte.
            result = passo_solar(
                pv, service_room, not driving, eta_dc, min_dc_kw, dt,
                hipotetico=mode != 'sem_interface', buffer_kwh=buffer,
                buffer_capacidade_kwh=buffer_capacity_kwh,
                eficiencia_buffer=eta_buffer, alocacao=split, fracao_servicos=frac)
            buffer = result['buffer_final_kwh']
            traction_draw = drive*kwh_km
            traction_room = traction_capacity_kwh-traction+traction_draw
            accepted = min(result['tracao_kwh'], max(0., traction_room))
            refused = result['tracao_kwh']-accepted
            traction += accepted-traction_draw
            service_in = result['servicos_kwh']*eta_service
            available_service = max(0., service+service_in-service_capacity_kwh*reserve_service)
            consumed = min(need, available_service)
            service += service_in-consumed
            totals['pv_kwh'] += pv
            totals['traction_solar_kwh'] += accepted
            totals['service_solar_kwh'] += service_in
            totals['loss_kwh'] += result['perdas_kwh']+result['servicos_kwh']-service_in
            totals['curtailed_kwh'] += result['cortada_kwh']+refused
            totals['traction_used_kwh'] += traction_draw
            totals['service_used_kwh'] += consumed
            totals['driving_h'] += drive/speed_kmh
            drove += drive/speed_kmh
            distance += drive
            row = {'day': day+1, 'hour_end': (slot+1)*dt,
                   'distance_km': distance, 'soc_traction': traction/traction_capacity_kwh,
                   'soc_service': service/service_capacity_kwh, 'buffer_kwh': buffer,
                   'driving_h_interval': drive/speed_kmh, 'pv_kwh_interval': pv,
                   'traction_solar_kwh_interval': accepted,
                   'service_consumed_kwh_interval': consumed}
            trace.append(row)
            if consumed+1e-9 < need:
                reason = 'reserva_servicos_sem_perfil_de_reducao_validado'
                break
            if distance >= target_km-1e-8:
                reason = 'chegada_condicional'
                break
            if mode == 'sem_interface' and traction <= traction_capacity_kwh*reserve_traction+1e-9:
                reason = 'reserva_tracao_sem_interface'
                break
        daily.append({'day': day+1, 'distance_km': distance, 'driving_h': drove,
                      'soc_traction': traction/traction_capacity_kwh,
                      'soc_service': service/service_capacity_kwh})
        if reason != 'horizonte_sem_conclusao':
            break
    initial = traction_capacity_kwh+service_capacity_kwh
    residual = (initial+totals['pv_kwh']-traction-service-buffer
                -totals['traction_used_kwh']-totals['service_used_kwh']
                -totals['loss_kwh']-totals['curtailed_kwh'])
    return {'status': reason, 'mode': mode, 'allocation': allocation,
            'distance_km': distance, 'elapsed_days': (len(trace)*dt)/24,
            'elapsed_resolution_h': dt, 'initial_energy_kwh': initial,
            'soc_initial_traction': 1., 'soc_initial_service': 1.,
            'soc_final_traction': traction/traction_capacity_kwh,
            'soc_final_service': service/service_capacity_kwh,
            'buffer_final_kwh': buffer, 'energy_residual_kwh': residual,
            'external_electric_energy_kwh': 0., 'totals': totals,
            'trace': trace, 'daily': daily, 'physical_mission_demonstrated': False}
