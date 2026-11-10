"""Recomendação energética de estágios; não define limiaresSOC ou aciona hardware."""
import math
from itertools import pairwise


def recomendar_estagio(available_kwh,remaining_h,daily_by_stage,*,bms_allow=True):
    """Usa orçamento previsto, não patamares fixosSOC escolhidos para o veículo.

    Na falta de orçamento para todo o horizonte,preserva cargas essenciais
    enquanto houver energia;não promete que sejam mantidas indefinidamente.
    """
    if not all(math.isfinite(x) for x in [available_kwh,remaining_h,*daily_by_stage]) or min(available_kwh,remaining_h,*daily_by_stage)<0:
        raise ValueError('Orçamento inválido')
    if len(daily_by_stage)!=3 or any(a<b for a,b in pairwise(daily_by_stage)):
        raise ValueError('Três estágios de consumo decrescente são necessários')
    if not bms_allow or available_kwh<=1e-12:return {'stage':3,'forecast_covered':False,'reason':'inibicao_ou_sem_energia_operacional'}
    for stage,daily in enumerate(daily_by_stage):
        if daily*remaining_h/24<=available_kwh+1e-10:return {'stage':stage,'forecast_covered':True,'reason':'orcamento_previsto_coberto'}
    return {'stage':2,'forecast_covered':False,'reason':'preservar_essenciais_ate_reserva'}


def simular_servicos_priorizados(capacity_kwh,reserve,horizon_h,daily_by_stage,*,managed=True,step_h=.25):
    if not all(math.isfinite(x) for x in [capacity_kwh,horizon_h,step_h,reserve]) or min(capacity_kwh,horizon_h,step_h)<=0 or not 0<=reserve<1:raise ValueError('Autonomia inválida')
    energy=capacity_kwh;time=0.;trace=[];used=0.
    while time<horizon_h-1e-10:
        room=max(0.,energy-capacity_kwh*reserve);remaining=horizon_h-time
        recommendation=recomendar_estagio(room,remaining,daily_by_stage)
        stage=recommendation['stage'] if managed else (0 if room>1e-12 else 3)
        if stage==3:break
        power=daily_by_stage[stage]/24;dt=min(step_h,remaining)
        if power>0:dt=min(dt,room/power)
        if dt<1e-10:break
        draw=power*dt;energy-=draw;used+=draw
        trace.append({'start_h':time,'end_h':time+dt,'stage':stage,'forecast_covered':recommendation['forecast_covered'],
            'load_kw':power,'energy_used_kwh':draw,'energy_remaining_kwh':energy,'soc':energy/capacity_kwh})
        time+=dt
    return {'hours_supported':time,'horizon_completed':time>=horizon_h-1e-8,'soc_final':energy/capacity_kwh,
        'energy_used_kwh':used,'energy_residual_kwh':capacity_kwh-energy-used,'trace':trace,
        'hardware_control_demonstrated':False,'project_soc_thresholds':None}
