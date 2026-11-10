"""Despacho FV diário: bancos separados, recarga DC exclusivamente estacionária.

MILP resolve alocação FV para uma janela de carga dada; mínimos e eficiências
são hipóteses fornecidas pelo cenário, nunca compatibilidade de hardware.
"""
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix


def alocar_dia(pv_kw, estacionado, dt_h, *, minimo_dc_kw, eta_dc,
               eta_servicos, consumo_servicos_kwh, capacidade_servicos_kwh,
               energia_servicos_inicial_kwh, capacidade_credito_tracao_kwh):
    """Maximiza crédito solar HV com SOC de serviços cíclico (Efinal=Einicial).

    Variáveis: energia FV para tração/serviços, energia no banco de serviços,
    sessão DC binária por intervalo. Mínimo refere-se à entrada FV da cadeia.
    Tração começa com crédito solar ZERO; energia OEM anterior não é recurso.
    SOC de serviços é um balanço separado, sem qualquer fluxo entre bancos.
    """
    pv=np.asarray(pv_kw,dtype=float);park=np.asarray(estacionado,dtype=bool);n=len(pv)
    scalars=[dt_h,minimo_dc_kw,eta_dc,eta_servicos,consumo_servicos_kwh,
             capacidade_servicos_kwh,energia_servicos_inicial_kwh,capacidade_credito_tracao_kwh]
    if (n==0 or park.shape!=pv.shape or not np.isfinite(pv).all() or (pv<0).any()
            or not np.isfinite(scalars).all() or dt_h<=0 or minimo_dc_kw<0
            or not 0<eta_dc<=1 or not 0<eta_servicos<=1 or consumo_servicos_kwh<0
            or capacidade_servicos_kwh<=0 or not 0<=energia_servicos_inicial_kwh<=capacidade_servicos_kwh
            or capacidade_credito_tracao_kwh<0):
        raise ValueError('Entradas de despacho inválidas')
    # y[0:n], z[n:2n], E[2n:3n+1], binary[3n+1:4n+1].
    nv=4*n+1;eb=2*n;on=3*n+1
    lo=np.zeros(nv);hi=np.full(nv,np.inf)
    hi[:n]=pv*dt_h*park;hi[n:2*n]=pv*dt_h
    hi[eb:on]=capacidade_servicos_kwh
    # Exclude subminimum intervals explicitly; MILP feasibility tolerances
    # must not create fictitious micro-sessions when solar never reaches Pmin.
    eligible=park & (pv>=minimo_dc_kw) & (pv>0)
    hi[on:]=eligible.astype(float);hi[:n]*=eligible
    lo[eb]=hi[eb]=energia_servicos_inicial_kwh
    lo[3*n]=hi[3*n]=energia_servicos_inicial_kwh
    matrix=lil_matrix((4*n+1,nv));lower=np.full(4*n+1,-np.inf);upper=np.zeros(4*n+1)
    load=consumo_servicos_kwh/n
    for i in range(n):
        matrix[i,i]=1;matrix[i,n+i]=1;upper[i]=pv[i]*dt_h
        row=n+i;matrix[row,eb+i+1]=1;matrix[row,eb+i]=-1;matrix[row,n+i]=-eta_servicos
        lower[row]=upper[row]=-load
        row=2*n+i;matrix[row,i]=1;matrix[row,on+i]=-hi[i]
        row=3*n+i;matrix[row,i]=-1;matrix[row,on+i]=minimo_dc_kw*dt_h
    matrix[4*n,:n]=eta_dc;upper[4*n]=capacidade_credito_tracao_kwh
    objective=np.zeros(nv);objective[:n]=-eta_dc
    integer=np.zeros(nv);integer[on:]=1
    result=milp(objective,integrality=integer,bounds=Bounds(lo,hi),
                constraints=LinearConstraint(matrix.tocsr(),lower,upper),
                options={'mip_rel_gap':1e-8,'time_limit':20.})
    if result.status==2:
        return {'status':'servicos_inviaveis_nesta_janela'}
    if not result.success:
        raise RuntimeError(f'Despacho sem solução certificada: {result.message}')
    x=result.x;y=np.maximum(0,x[:n]);z=np.maximum(0,x[n:2*n]);energy=x[eb:on]
    return {'status':'otimo_para_janela_discreta','fv_tracao_kwh':y,
            'fv_servicos_kwh':z,'energia_servicos_kwh':energy,
            'credito_solar_tracao_kwh':float(y.sum()*eta_dc),
            'fv_cortada_kwh':pv*dt_h-y-z,
            'residuo_servicos_kwh':float(np.max(np.abs(np.diff(energy)-eta_servicos*z+load))),
            'gap_milp':float(result.mip_gap)}
