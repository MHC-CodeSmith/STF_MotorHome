"""Balanços térmicos em SI, com entradas explícitas; não selecionam componentes.

Métodos e limites: docs/FRENTE_TERMICA.md. Nenhum valor é lido do YAML global.
"""

from itertools import pairwise
from math import exp, expm1, isfinite
from numbers import Real


def numero(valor, nome, minimo=None, estrito=False):
    """Valida escalar finito; bool e valores ausentes não são números físicos."""
    if isinstance(valor, bool) or not isinstance(valor, Real) or not isfinite(valor):
        raise ValueError(f'{nome}: escalar finito obrigatório')
    if minimo is not None and (valor <= minimo if estrito else valor < minimo):
        sinal = '>' if estrito else '>='
        raise ValueError(f'{nome}: deve ser {sinal} {minimo}')
    return float(valor)


def temperatura(valor):
    return numero(valor, 'temperatura [K]', 0, estrito=True)


def transiente_concentrado(capacidade_j_k, ua_w_k, inicial_k, ambiente_k,
                          geracao_w, duracao_s):
    """Solução exata de C dT/dt = Q - UA(T-Ta), coeficientes constantes.

    UA=0 usa o limite adiabático. Q é calor, não potência elétrica nominal.
    O resíduo considera a energia convectiva integrada analiticamente.
    """
    c = numero(capacidade_j_k, 'C [J/K]', 0, True)
    ua = numero(ua_w_k, 'UA [W/K]', 0)
    ti, ta = temperatura(inicial_k), temperatura(ambiente_k)
    q = numero(geracao_w, 'Q [W]')
    t = numero(duracao_s, 't [s]', 0)
    if ua == 0:
        tf = ti + q*t/c
    else:
        ganho = -expm1(-ua*t/c)
        tf = ti + ((ta-ti) + q/ua)*ganho
    temperatura(tf)
    armazenado = c*(tf-ti)
    gerado = q*t
    perdido = gerado-armazenado
    return {'temperatura_final_k': tf, 'energia_armazenada_j': armazenado,
            'energia_gerada_j': gerado, 'energia_para_ambiente_j': perdido}


def carga_ac(ua_w_k, exterior_k, interior_k, solar_transmitido_w,
             equipamentos_w, ocupantes, sensivel_por_pessoa_w,
             latente_por_pessoa_w, ventilacao_sensivel_w,
             ventilacao_latente_w, cop):
    """I32: carga de resfriamento permanente e eletricidade para COP explícito.

    UA e solar devem evitar dupla contagem; ventilação depende de psicrometria
    externa ao método. Condensação, infiltração e ocupação não são inferidas.
    """
    ua = numero(ua_w_k, 'UA [W/K]', 0)
    te, ti = temperatura(exterior_k), temperatura(interior_k)
    if isinstance(ocupantes, bool) or not isinstance(ocupantes, int) or ocupantes < 1:
        raise ValueError('I32 exige número inteiro de ocupantes >= 1')
    solar = numero(solar_transmitido_w, 'solar [W]', 0)
    equipamentos = numero(equipamentos_w, 'equipamentos [W]', 0)
    sensivel = numero(sensivel_por_pessoa_w, 'ocupante sensível [W]', 0)
    latente = numero(latente_por_pessoa_w, 'ocupante latente [W]', 0)
    vs = numero(ventilacao_sensivel_w, 'ventilação sensível [W]')
    vl = numero(ventilacao_latente_w, 'ventilação latente [W]', 0)
    eficiencia = numero(cop, 'COP', 0, True)
    qs = ua*(te-ti) + solar + equipamentos + ocupantes*sensivel + vs
    ql = ocupantes*latente + vl
    # Separar cargas evita cancelar a desumidificação com perda sensível.
    frio = max(0., qs) + ql
    return {'carga_sensivel_w': qs, 'carga_latente_w': ql,
            'capacidade_resfriamento_w': frio, 'potencia_eletrica_w': frio/eficiencia}


def geracao_joule(corrente_a, resistividade_ohm_m, secao_m2):
    """I30: geração volumétrica I² rho_e/A² [W/m³], condutor uniforme DC."""
    i = numero(corrente_a, 'corrente [A]', 0)
    rho = numero(resistividade_ohm_m, 'resistividade [ohm m]', 0, True)
    a = numero(secao_m2, 'seção [m²]', 0, True)
    return numero((i/a)**2*rho, 'geração Joule [W/m³]', 0)


def resistividade_linear(referencia_ohm_m, alfa_por_k, temperatura_k,
                         referencia_k):
    """Lei linear local; usuário fornece faixa de validade e fonte de alfa."""
    rho = numero(referencia_ohm_m, 'resistividade de referência', 0, True)
    alfa = numero(alfa_por_k, 'coeficiente térmico [1/K]')
    t, tr = temperatura(temperatura_k), temperatura(referencia_k)
    return numero(rho*(1+alfa*(t-tr)), 'resistividade calculada', 0, True)


def frenagem_especifica(inicial_m_s, final_m_s, duracao_s):
    """I33: energia cinética translacional removida por kg, sem alocação ao disco.

    Potência média é exata no intervalo. Distância e potências nas pontas
    pressupõem desaceleração constante; não incluem rodas, arrasto ou regeneração.
    """
    vi = numero(inicial_m_s, 'velocidade inicial', 0)
    vf = numero(final_m_s, 'velocidade final', 0)
    t = numero(duracao_s, 'duração', 0, True)
    if vf >= vi:
        raise ValueError('Frenagem exige velocidade final menor que inicial')
    a = (vf-vi)/t
    e = (vi*vi-vf*vf)/2
    return {'energia_cinetica_removida_j_kg': e,
            'potencia_media_removida_w_kg': e/t,
            'aceleracao_media_m_s2': a,
            'distancia_se_desaceleracao_constante_m': (vi+vf)*t/2,
            'potencia_inicial_se_desaceleracao_constante_w_kg': -a*vi,
            'potencia_final_se_desaceleracao_constante_w_kg': -a*vf}


def carga_ohmica(potencia_terminal_w, tensao_terminal_v, resistencia_pack_ohm):
    """I34: parcela irreversível I²R a V/R constantes; não modela entropia/BMS.

    Potência terminal deve vir do protocolo real, não da placa do carregador.
    Não interpreta automaticamente potência de carga como potência térmica.
    """
    p = numero(potencia_terminal_w, 'potência terminal [W]', 0)
    v = numero(tensao_terminal_v, 'tensão terminal [V]', 0, True)
    r = numero(resistencia_pack_ohm, 'resistência do pack [ohm]', 0)
    i = p/v
    perda = i*i*r
    if perda > p:
        raise ValueError('Perda ôhmica maior que entrada: ponto de carga incompatível')
    return {'corrente_a': i, 'perda_ohmica_w': perda,
            'potencia_terminal_menos_perda_ohmica_w': p-perda}


def trocador(ua_w_k, capacidade_quente_w_k, capacidade_fria_w_k,
             quente_entrada_k, fria_entrada_k, arranjo):
    """I35: ε-NUT de correntes paralelas/contrárias, sem mudança de fase.

    Não se aplica diretamente a radiador de fluxo cruzado. Usa calor específico
    constante, sem perdas externas, e explicita os dois fluxos de capacidade.
    """
    ua = numero(ua_w_k, 'UA [W/K]', 0)
    ch = numero(capacidade_quente_w_k, 'C quente [W/K]', 0, True)
    cc = numero(capacidade_fria_w_k, 'C fria [W/K]', 0, True)
    th, tc = temperatura(quente_entrada_k), temperatura(fria_entrada_k)
    if th < tc:
        raise ValueError('Entrada quente deve ser >= entrada fria')
    cmin, cmax = min(ch, cc), max(ch, cc)
    cr, ntu = cmin/cmax, ua/cmin
    if arranjo == 'paralelo':
        efetividade = -expm1(-ntu*(1+cr))/(1+cr)
    elif arranjo == 'contracorrente':
        if cr == 1.:
            efetividade = ntu/(1+ntu)
        else:
            z = -expm1(-ntu*(1-cr))
            efetividade = z/(1-cr+cr*z)
    else:
        raise ValueError('Arranjo deve ser paralelo ou contracorrente')
    q = efetividade*cmin*(th-tc)
    return {'efetividade': efetividade, 'ntu': ntu, 'razao_capacidades': cr,
            'calor_trocado_w': q, 'quente_saida_k': th-q/ch,
            'fria_saida_k': tc+q/cc}


def ponto_bomba(vazoes_m3_s, bomba_pa, sistema_pa):
    """Todas as interseções por interpolação linear na malha de vazões comum.

    Não extrapola, não escolhe a bomba e não afirma estabilidade ou NPSH.
    Patamar de coincidência é ambíguo e rejeitado. Pressões são diferenciais.
    """
    if not (len(vazoes_m3_s) == len(bomba_pa) == len(sistema_pa) >= 2):
        raise ValueError('Curvas devem ter mesmo tamanho >= 2')
    qs = [numero(q, 'vazão [m³/s]', 0) for q in vazoes_m3_s]
    pb = [numero(p, 'pressão bomba [Pa]', 0) for p in bomba_pa]
    ps = [numero(p, 'pressão sistema [Pa]', 0) for p in sistema_pa]
    if any(b <= a for a, b in pairwise(qs)):
        raise ValueError('Vazões devem ser estritamente crescentes')
    pontos = []
    for i in range(len(qs)-1):
        a, b = pb[i]-ps[i], pb[i+1]-ps[i+1]
        if a == b == 0:
            raise ValueError('Intervalo inteiro coincidente: ponto indeterminado')
        if a == 0:
            pontos.append({'vazao_m3_s': qs[i], 'pressao_pa': pb[i]})
        if a*b < 0:
            f = -a/(b-a)
            pontos.append({'vazao_m3_s': qs[i]+f*(qs[i+1]-qs[i]),
                           'pressao_pa': pb[i]+f*(pb[i+1]-pb[i])})
    if pb[-1] == ps[-1]:
        pontos.append({'vazao_m3_s': qs[-1], 'pressao_pa': pb[-1]})
    return pontos


def perfil_paralelo(ua_w_k, capacidade_quente_w_k, capacidade_fria_w_k,
                    quente_entrada_k, fria_entrada_k, fracoes_area):
    """Perfil analítico em A/A_total; somente correntes paralelas monofásicas."""
    global_ = trocador(ua_w_k, capacidade_quente_w_k, capacidade_fria_w_k,
                      quente_entrada_k, fria_entrada_k, 'paralelo')
    ch, cc = capacidade_quente_w_k, capacidade_fria_w_k
    th, tc = quente_entrada_k, fria_entrada_k
    resultado = []
    for f in fracoes_area:
        f = numero(f, 'A/A_total', 0)
        if f > 1:
            raise ValueError('A/A_total deve estar em [0,1]')
        delta = (th-tc)*exp(-ua_w_k*f*(1/ch+1/cc))
        q = ((th-tc)-delta)/(1/ch+1/cc)
        resultado.append({'fracao_area': f, 'quente_k': th-q/ch, 'fria_k': tc+q/cc})
    return global_, resultado
