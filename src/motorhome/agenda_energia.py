"""Verificação temporal I27/I29; não é otimizador nem modelo de geração solar.

Potências constantes por intervalo, solar e cargas no mesmo barramento terminal.
SOC representa fração de energia de uma capacidade de referência explícita.
"""

from dataclasses import dataclass
from datetime import datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

from .sistemas_termicos import numero


@dataclass(frozen=True)
class Intervalo:
    inicio: datetime
    fim: datetime
    velocidade_m_s: float
    demanda_terminal_w: float
    solar_terminal_w: float
    fonte: str

    def __post_init__(self):
        for t in (self.inicio, self.fim):
            if not isinstance(t, datetime) or t.utcoffset() is None:
                raise ValueError('Datas devem possuir fuso horário explícito')
        if self.fim.timestamp() <= self.inicio.timestamp():
            raise ValueError('Fim deve ser posterior ao início')
        for nome in ('velocidade_m_s', 'demanda_terminal_w', 'solar_terminal_w'):
            numero(getattr(self, nome), nome, 0)
        if not isinstance(self.fonte, str) or not self.fonte.strip():
            raise ValueError('Fonte/proveniência de cada intervalo é obrigatória')


def _fracao(valor, nome, positivo=False):
    v = numero(valor, nome, 0, positivo)
    if v > 1:
        raise ValueError(f'{nome} deve estar em [0,1]')
    return v


def verificar_agenda(intervalos, capacidade_referencia_j, soc_inicial,
                     eficiencia_carga, eficiencia_descarga, soc_reserva,
                     max_conducao_diaria_s, distancia_alvo_m,
                     tolerancia_distancia_m, fuso='America/Sao_Paulo',
                     alvo_soc_final=None, tolerancia_soc=None,
                     permitir_corte_solar=False):
    """Verifica energia em TODOS os passos, capacidade, distância e calendário.

    Intervalos devem cobrir também paradas/noites, sem sobreposição ou lacunas.
    Recarga externa não faz parte do contrato. Corte solar é opcional e explícito.
    Retorna violações; não torna uma agenda inválida viável por clipping de déficit.
    """
    if not intervalos:
        raise ValueError('Agenda vazia')
    capacidade = numero(capacidade_referencia_j, 'capacidade de referência [J]', 0, True)
    soc0 = _fracao(soc_inicial, 'SOC inicial')
    reserva = _fracao(soc_reserva, 'SOC reserva')
    ec = _fracao(eficiencia_carga, 'eficiência carga', True)
    ed = _fracao(eficiencia_descarga, 'eficiência descarga', True)
    limite_dia = numero(max_conducao_diaria_s, 'limite condução [s]', 0, True)
    alvo_m = numero(distancia_alvo_m, 'distância alvo [m]', 0)
    tol_m = numero(tolerancia_distancia_m, 'tolerância distância [m]', 0)
    if not isinstance(permitir_corte_solar, bool):
        raise TypeError('permitir_corte_solar deve ser booleano')
    if (alvo_soc_final is None) != (tolerancia_soc is None):
        raise ValueError('Alvo e tolerância de SOC devem ser fornecidos juntos')
    if alvo_soc_final is not None:
        alvo_soc_final = _fracao(alvo_soc_final, 'alvo SOC final')
        tolerancia_soc = _fracao(tolerancia_soc, 'tolerância SOC')
    zona = ZoneInfo(fuso)
    energia = soc0*capacidade
    inicial = energia
    distancia = solar = demanda = perdas = corte = 0.
    diarios, historico, violacoes = {}, [], []
    if soc0 < reserva:
        violacoes.append('SOC inicial abaixo da reserva')
    anterior = None
    for indice, trecho in enumerate(intervalos):
        if not isinstance(trecho, Intervalo):
            raise TypeError('Todos os registros devem ser Intervalo')
        inicio = trecho.inicio.astimezone(timezone.utc)
        fim = trecho.fim.astimezone(timezone.utc)
        if anterior is not None and inicio != anterior:
            raise ValueError('Agenda deve ser contínua, sem lacunas ou sobreposição')
        anterior = fim
        cursor = inicio
        # Dividir em meias-noites LOCAIS preserva o limite por dia de calendário.
        while cursor < fim:
            local = cursor.astimezone(zona)
            meia_noite = datetime.combine(local.date()+timedelta(days=1), time(), zona)
            proximo = min(fim, meia_noite.astimezone(timezone.utc))
            dt = (proximo-cursor).total_seconds()
            dia = local.date().isoformat()
            diarios[dia] = diarios.get(dia, 0.) + (dt if trecho.velocidade_m_s > 0 else 0.)
            distancia += trecho.velocidade_m_s*dt
            epv, ecarga = trecho.solar_terminal_w*dt, trecho.demanda_terminal_w*dt
            net = epv-ecarga
            cortado = 0.
            if net >= 0:
                if permitir_corte_solar:
                    cortado = max(0., net-max(0., capacidade-energia)/ec)
                delta = (net-cortado)*ec
                perda = (net-cortado)*(1-ec)
            else:
                delta = net/ed
                perda = (-net)*(1/ed-1)
            energia += delta
            solar += epv
            demanda += ecarga
            perdas += perda
            corte += cortado
            # Tolerância apenas de arredondamento da soma em ponto flutuante.
            eps = max(1., capacidade)*1e-12
            if energia < capacidade*reserva-eps:
                violacoes.append(f'Intervalo {indice}: energia abaixo da reserva em {proximo.isoformat()}')
            if energia > capacidade+eps:
                violacoes.append(f'Intervalo {indice}: capacidade excedida em {proximo.isoformat()}')
            historico.append({'fim': proximo.isoformat(), 'energia_j': energia,
                              'soc': energia/capacidade, 'distancia_acumulada_m': distancia})
            cursor = proximo
    for dia, segundos in diarios.items():
        if segundos > limite_dia+1e-8:
            violacoes.append(f'{dia}: condução {segundos} s excede {limite_dia} s')
    if abs(distancia-alvo_m) > tol_m:
        violacoes.append('Distância final fora da tolerância')
    if alvo_soc_final is not None and abs(energia/capacidade-alvo_soc_final) > tolerancia_soc+1e-12:
        violacoes.append('SOC final fora do alvo e tolerância')
    return {'viavel_no_modelo': not violacoes, 'violacoes': violacoes,
            'soc_final': energia/capacidade, 'energia_inicial_j': inicial,
            'energia_final_j': energia, 'solar_terminal_j': solar,
            'demanda_terminal_j': demanda, 'perdas_j': perdas,
            'corte_solar_terminal_j': corte,
            'residuo_energia_j': energia-inicial-solar+demanda+perdas+corte,
            'distancia_m': distancia, 'conducao_por_dia_s': diarios,
            'historico': historico, 'otimizacao_executada': False,
            'recarga_externa_modelada': False}
