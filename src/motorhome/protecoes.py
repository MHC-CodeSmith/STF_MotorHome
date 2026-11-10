"""Triagem elétrica e comandos de segurança; não certifica instalação/hardware."""
import math

import numpy as np


def circuito_dc(power_w,voltage_v,eta,loop_m,section_mm2,temperature_c,
                rho20=1.724e-8,alpha=.00393):
    """Carga de potência constante e queda I*R resolvidas conjuntamente.

    Vload=Vsource-I*R e I=Pdc/Vload; raiz de baixa corrente estável.
    Resistência cobre inclui ida+retorno, sem resistência de contatos.
    """
    values=[power_w,voltage_v,eta,loop_m,section_mm2,temperature_c,rho20,alpha]
    if not all(math.isfinite(x) for x in values) or min(voltage_v,eta,loop_m,section_mm2,rho20)<=0 or power_w<0 or eta>1:
        raise ValueError('Circuito inválido')
    resistance=rho20*(1+alpha*(temperature_c-20))*loop_m/(section_mm2*1e-6)
    if resistance<=0:raise ValueError('Resistência inválida')
    power_dc=power_w/eta;disc=voltage_v**2-4*resistance*power_dc
    if disc<0:return {'status':'sem_equilibrio_potencia_constante'}
    current=2*power_dc/(voltage_v+math.sqrt(disc))
    return {'status':'calculado','current_a':current,'loop_resistance_ohm':resistance,
            'load_voltage_v':voltage_v-current*resistance,'drop_percent':100*current*resistance/voltage_v,
            'loss_w':current*current*resistance,
            'energy_residual_w':voltage_v*current-power_dc-current*current*resistance}


def falta_prospectiva(voltage_v,module_r_ohm,parallel,loop_r_ohm):
    if min(voltage_v,module_r_ohm,parallel)<=0 or loop_r_ohm<0:raise ValueError('Falta inválida')
    return voltage_v/(module_r_ohm/parallel+loop_r_ohm)


def grupo_parafusos(force_n,moment_nm,coordinates_m):
    """Grupo plano elástico: cisalhamento direto + momento torsor no plano.

    Sem atrito/pre-carga; parafusos iguais, chapa rígida, origem CG do grupo.
    Não calcula prying, arrancamento ou resistência da carroceriaOEM.
    """
    xy=np.asarray(coordinates_m,dtype=float);force=np.asarray(force_n,dtype=float)
    if xy.ndim!=2 or xy.shape[1]!=2 or len(xy)<2 or force.shape!=(2,) or not np.isfinite(xy).all() or not np.isfinite(force).all() or not math.isfinite(moment_nm):
        raise ValueError('Grupo inválido')
    xy=xy-xy.mean(axis=0);polar=float((xy*xy).sum())
    if polar<=0:raise ValueError('Grupo degenerado')
    shear=force/len(xy)+moment_nm/polar*np.column_stack((-xy[:,1],xy[:,0]))
    return {'bolt_shear_n':np.linalg.norm(shear,axis=1).tolist(),
            'components_n':shear.tolist(),'force_residual_n':(shear.sum(axis=0)-force).tolist(),
            'moment_residual_nm':float(np.sum(xy[:,0]*shear[:,1]-xy[:,1]*shear[:,0])-moment_nm)}


class GerenciadorCargas:
    """Máquina de estados de referência; patamaresSOC ficam externos/não fixados.

    Pedido estágio0..3 vem de interfaceSOC/BMS a validar. Falha sensor,
    BMSinibido ou contator sem confirmação travaOFF até reset explícito.
    Redução automática imediata; recuperação exige permanência da solicitação.
    """
    def __init__(self,recovery_s):
        if not math.isfinite(recovery_s) or recovery_s<0:raise ValueError('Temporização inválida')
        self.recovery_s=recovery_s;self.stage=3;self.latched=False;self.pending=None;self.elapsed=0.

    def step(self,requested_stage,dt_s,*,bms_allow=True,telemetry_valid=True,actuator_ok=True,reset=False):
        if requested_stage not in range(4) or not math.isfinite(dt_s) or dt_s<=0:raise ValueError('Comando inválido')
        fault=not (bms_allow and telemetry_valid and actuator_ok)
        if fault:self.latched=True
        elif reset:self.latched=False
        if self.latched:self.stage=3;self.pending=None;self.elapsed=0.
        elif requested_stage>=self.stage:
            self.stage=requested_stage;self.pending=None;self.elapsed=0.
        else:
            if self.pending!=requested_stage:self.pending=requested_stage;self.elapsed=0.
            self.elapsed+=dt_s
            if self.elapsed>=self.recovery_s:
                self.stage=requested_stage;self.pending=None;self.elapsed=0.
        return {'stage':self.stage,'fault_latched':self.latched,'essential_allowed':self.stage<3,
                'intermediate_allowed':self.stage<2,'deferrable_allowed':self.stage<1}


def alocar_picos(loads,stage,limit_w,limit_va):
    """Admite por prioridade; recusa dado ausente e grandes cargas simultâneas."""
    if stage not in range(4) or min(limit_w,limit_va)<=0:raise ValueError('Limite inválido')
    accepted=[];rejected=[];watts=va=0.;large=0
    for load in sorted(loads,key=lambda x:x['priority']):
        power=load['w'];apparent=load['va'];reason=None
        if stage==3 or stage>=load['shed_at_stage']:reason='estagio_SOC_BMS'
        elif power is None or apparent is None:reason='pico_nao_documentado'
        elif min(power,apparent)<0 or apparent<power:raise ValueError('W/VA inválidos')
        elif large and load.get('large'):reason='intertravamento_grandes_cargas'
        elif watts+power>limit_w or va+apparent>limit_va:reason='limite_inversor'
        if reason:rejected.append({'id':load['id'],'reason':reason})
        else:
            accepted.append(load['id']);watts+=power;va+=apparent;large+=bool(load.get('large'))
    return {'accepted':accepted,'rejected':rejected,'w':watts,'va':va}
