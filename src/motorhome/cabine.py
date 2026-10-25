"""Rede térmica de uma zona: resistências Fourier/Newton e armazenamento.

Não é CFD, não calcula conforto local e não valida os parâmetros da carroceria.
"""

from math import expm1, isfinite

import numpy as np

from motorhome.sistemas_termicos import numero


def transmitancia(camadas, h_interno, h_externo):
    """U [W/m²K] por resistências em série; cada camada é (espessura, k)."""
    hi = numero(h_interno, 'h interno', 0, True)
    ho = numero(h_externo, 'h externo', 0, True)
    if not camadas:
        raise ValueError('Ao menos uma camada obrigatória')
    resistencia = 1/hi + 1/ho
    for d, k in camadas:
        resistencia += numero(d, 'espessura', 0, True)/numero(k, 'k', 0, True)
    return 1/resistencia


def umidade_especifica(temperatura_c, ur, pressao_pa):
    """Razão kg vapor/kg ar seco; Buck Research CR-2 (2009), água líquida.

    Intervalo operacional restrito a 0..50°C. Expressão e origem no memorial.
    Usa EF=1 (vapor ideal); correção de enhancement do manual é desprezada.
    """
    t = numero(temperatura_c, 'temperatura Celsius', 0)
    rh = numero(ur, 'UR', 0)
    p = numero(pressao_pa, 'pressão', 0, True)
    if t > 50 or rh > 1:
        raise ValueError('T em [0,50]°C e UR em [0,1]')
    ps = 611.21*np.exp((18.678-t/234.5)*t/(257.14+t))
    pv = rh*ps
    if pv >= p:
        raise ValueError('Pressão parcial maior que pressão total')
    return float(0.621945*pv/(p-pv))


def integrar_zona(tempos_s, ganhos_w, ua_w_k, capacidade_j_k,
                  ambiente_c, inicial_c):
    """Exata por intervalo com ganho constante igual à média das pontas.

    C*dT/dt = ganho(t) - UA*(T-Ta). Ganho inclui somente calor, não UA*Ta.
    Calcula resíduo com integração analítica das perdas para cada intervalo.
    """
    ua = numero(ua_w_k, 'UA', 0, True)
    c = numero(capacidade_j_k, 'C', 0, True)
    ta = numero(ambiente_c, 'ambiente Celsius')
    ti = numero(inicial_c, 'inicial Celsius')
    if min(ta, ti) <= -273.15:
        raise ValueError('Temperatura absoluta inválida')
    t, q = np.asarray(tempos_s, dtype=float), np.asarray(ganhos_w, dtype=float)
    if (t.ndim != 1 or q.shape != t.shape or len(t) < 2
            or not np.isfinite(t).all() or not np.isfinite(q).all()
            or (np.diff(t) <= 0).any()):
        raise ValueError('Tempos crescentes e ganhos finitos de mesma dimensão')
    resultado = np.empty(len(t))
    resultado[0] = ti
    gerado, perdido = 0., 0.
    for i, dt in enumerate(np.diff(t)):
        medio = (q[i]+q[i+1])/2
        inicial = resultado[i]
        equilibrio = ta+medio/ua
        ganho = -expm1(-ua*dt/c)
        resultado[i+1] = inicial+(equilibrio-inicial)*ganho
        # Integral independente de UA*(T-Ta), usando solução exponencial.
        integral_perda = ua*((equilibrio-ta)*dt+(inicial-equilibrio)*c/ua*ganho)
        gerado += medio*dt
        perdido += integral_perda
    if not np.isfinite(resultado).all() or resultado.min() <= -273.15:
        raise ValueError('Temperatura calculada inválida')
    residuo = c*(resultado[-1]-ti) - (gerado-perdido)
    if not isfinite(residuo):
        raise ValueError('Balanço inválido')
    return resultado, float(residuo)
