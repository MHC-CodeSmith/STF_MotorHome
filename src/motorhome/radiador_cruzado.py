"""Trocador cruzado ideal, uma passagem, ambos fluidos não misturados.

Modelo de dois campos médios por célula; não CFD nem geometria de aletas.
UA total e capacidades são entradas, não derivados do envelope CAD.
"""
import numpy as np
from scipy.integrate import quad
from scipy.special import i0

from .sistemas_termicos import numero, temperatura


def efetividade_integral(ntu, cr):
    """Referência integral exata na faixa moderada NTU<=20, Cr>=.001.

    Fórmula publicada na documentação ht.hx, effectiveness_from_NTU,
    caso crossflow (unmixed/unmixed); implementação independente.
    Evita usar a expressão problemática da tabela 4 da apostila.
    """
    ntu = numero(ntu, 'NTU', 0)
    cr = numero(cr, 'Cr', 0)
    if cr > 1 or ntu > 20 or (0 < ntu < 1e-4) or (0 < cr < .001):
        raise ValueError('Referência restrita a NTU=0 ou 1e-4<=NTU<=20; Cr=0 ou .001<=Cr<=1')
    if ntu == 0:
        return 0.
    if cr == 0:
        return float(-np.expm1(-ntu))
    def integrand(v):
        return (1+ntu-v*v/(4*cr*ntu))*np.exp(-v*v/(4*cr*ntu))*v*i0(v)
    integral = quad(integrand, 0, 2*ntu*np.sqrt(cr), epsabs=1e-12, epsrel=1e-12)[0]
    return float(1/cr-np.exp(-cr*ntu)/(2*(cr*ntu)**2)*integral)


def resolver(ua_w_k, capacidade_quente_w_k, capacidade_fria_w_k, quente_entrada_k,
             fria_entrada_k, nx=64, ny=64):
    ua = numero(ua_w_k, 'UA [W/K]', 0)
    ch = numero(capacidade_quente_w_k, 'Ch [W/K]', 0, True)
    cc = numero(capacidade_fria_w_k, 'Cc [W/K]', 0, True)
    thi, tci = temperatura(quente_entrada_k), temperatura(fria_entrada_k)
    if thi <= tci:
        raise ValueError('Entrada quente deve superar entrada fria')
    if any(isinstance(n, bool) or not isinstance(n, int) or n < 2 for n in (nx, ny)):
        raise ValueError('Malhas exigem inteiros >=2')
    # Quente avança em x (nx células); frio avança em y (ny células).
    hot = np.full((ny, nx+1), thi)
    cold = np.full((ny+1, nx), tci)
    heat = np.zeros((ny, nx))
    g = ua/(nx*ny)
    channel_h, channel_c = ch/ny, cc/nx
    if g/max(channel_h, 1e-300) > 1 or g/max(channel_c, 1e-300) > 1:
        raise ValueError('Refinar malha para evitar oscilações do esquema centrado')
    for j in range(ny):
        for i in range(nx):
            # Q=g*(T_hot_média-T_cold_média); médias entre entrada e saída.
            q = g*(hot[j, i]-cold[j, i])/(1+g/(2*channel_h)+g/(2*channel_c))
            heat[j, i] = q
            hot[j, i+1] = hot[j, i]-q/channel_h
            cold[j+1, i] = cold[j, i]+q/channel_c
    tho, tco = float(hot[:, -1].mean()), float(cold[-1].mean())
    qh, qc = ch*(thi-tho), cc*(tco-tci)
    return {'quente_k': hot, 'fria_k': cold, 'calor_celula_w': heat,
            'calor_w': float(heat.sum()), 'quente_saida_media_k': tho,
            'fria_saida_media_k': tco, 'residuo_w': qh-qc,
            'efetividade': float(heat.sum()/(min(ch, cc)*(thi-tci)))}
