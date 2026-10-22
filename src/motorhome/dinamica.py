"""Modelo longitudinal simplificado para testes e scripts dos itens 20–22 e 26.

Todas as entradas são explícitas em unidades SI. Não representa CFD nem curva real do motor.
"""
from math import pi

G = 9.80665

def forca_aerodinamica(rho_kg_m3: float, cd: float, area_frontal_m2: float, velocidade_m_s: float) -> float:
    if min(rho_kg_m3, cd, area_frontal_m2) < 0: raise ValueError('Parâmetros não negativos')
    return 0.5 * rho_kg_m3 * cd * area_frontal_m2 * velocidade_m_s ** 2

def forca_rolamento(cr: float, massa_kg: float, inclinacao_rad: float = 0.) -> float:
    from math import cos
    if cr < 0 or massa_kg < 0: raise ValueError('Parâmetros não negativos')
    return cr * massa_kg * G * cos(inclinacao_rad)

def potencia_rodas_w(f_resistiva_n: float, velocidade_m_s: float) -> float:
    return f_resistiva_n * velocidade_m_s

def potencia_eletrica_tracao_w(potencia_rodas_w: float, eficiencia_0a1: float) -> float:
    if not 0 < eficiencia_0a1 <= 1: raise ValueError('Eficiência deve estar em (0, 1]')
    return potencia_rodas_w / eficiencia_0a1
