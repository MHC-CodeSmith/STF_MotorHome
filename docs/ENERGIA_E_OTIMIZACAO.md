# Energia e otimização — resultados condicionados, 24/10/2026

**Não são resultados finais do veículo.** Os scripts ligam geometria, pilotos CFD,
geração solar e demanda longitudinal sem preencher parâmetros aprovados ausentes.
As hipóteses ficam em `config/energia_sensibilidade.yaml`; nenhum Cr, rendimento,
carga de habitação ou Cd exploratório se torna dado OEM por entrar no cálculo.

## Requisitos efetivamente conferidos

Enunciado 2026, p. 2, itens 25–29: I25 usa somente a eletricidade solar do dia;
I26 pede **km/kWh na bateria**; I27 termina com **30%**, descrevendo velocidade
e potência; I29 pede **7000 km, sem recarga externa, no máximo 8 h/dia**.
O limite de oito horas **não foi estendido a I27**. A primeira execução exploratória
o havia aplicado também a I27: seus 300 km foram substituídos pelo caso corrigido
de 335 km. SOC aqui significa fração da janela útil OEM de 98 kWh, uma convenção
de modelo ainda não equiparada ao SOC indicado pelo BMS.

As equações de dinâmica, pvlib e MILP são referências complementares; não são
atribuídas à apostila. A apostila apoia conservação e integração com as cargas
térmicas, mas não fornece mapas elétricos OEM ou um otimizador de viagem.

## I21, I22, I25 e I26

Para velocidade constante no plano, vento ambiente zero e sem aceleração:

`Fa = 0,5 rho Cd A v²`; `Fr = Cr m g`; `P_roda = (Fa+Fr) v`.

`P_terminal = P_roda/eta + P_aux`; `km/kWh = v[km/h] / P_terminal[kW]`.

`distância_solar[km] = E_solar_terminal[kWh] × km/kWh`.

A massa de 4250 kg é cenário no limite de massa total do veículo; não uma BOM.
Área 4,827840 m² é da superfície reparada do piloto, não área final homologada.
rho=1,1 kg/m³ mantém o fluido dos pilotos; Cr=0,008/0,012/0,016,
eta=0,85/0,90/0,95 e auxiliares de condução de 800 W são hipóteses explícitas.
Cd=0,580667/0,624877/0,653036 vêm de três malhas piloto sem camadas/y+ verificados.
O último refinamento ainda mudou Cd em 7,07%; nenhum deles é valor validado.

Saídas de `scripts/calcular_sensibilidade_energia.py`: **324 combinações**
(3 Cd × 3 Cr × 3 eta × 12 velocidades). Resultados arredondados:

| Velocidade | km/kWh, faixa das hipóteses | km usando apenas solar de dois módulos |
|---|---:|---:|
| 40 km/h | 3,25–5,78 | 10,50–18,67 |
| 80 km/h | 1,97–3,03 | 6,37–9,79 |

O cálculo solar usa o cenário de 21/06/São Carlos já documentado em
[AVANCO_2026-10-24.md](AVANCO_2026-10-24.md). Essa tabela não desconta a habitação
fora da condução e não prova transferência solar para o pack de tração.
Não confundir P_terminal, P_roda e potência mecânica do motor: faltam perdas e
curvas da transmissão para fechar a potência instantânea pedida em I27.

## I27: maximização diária executada

`scripts/calcular_agendas_provisorias.py` usa `maximizar_distancia`:
48 intervalos de 30 min, velocidades 0/20/30/40/60/80 km/h, SOC inicial 100%,
reserva 10%, **SOC final exatamente 30%** e horizonte completo de 24 h.
Cd intermediário 0,624877, Cr=0,012, eta=0,90; parado=100 W,
em condução=800 W além da tração. São escolhas de cenário, não dados aprovados.
Solar indisponível em condução; disponível estacionado, com cadeia elétrica
ainda hipotética. Eficiências de integração unitárias evitam contar duas vezes
as perdas já embutidas nas potências terminais, não afirmam bateria ideal real.

**335 km**, ótimo certificado pelo HiGHS somente nesta grade/modelo.
A agenda e os três gráficos são exportados, com checagem do balanço por passo.
Sem acelerações, o chaveamento de modos não é um perfil de condução executável
sem ajustes. Falta refinar tempo/velocidades e integrar cargas/componentes reais.

## I29: menor tempo e agenda construtiva

`src/motorhome/otimizacao_viagem.py` implementa MILP de menor tempo com distância
exata, modos discretos, último intervalo fracionário, reserva causal, corte solar,
capacidade e limite de condução por data local. Paradas contam para o tempo e
consomem energia; depois da chegada não se recebe sol nem se debita habitação.
Seis testes analíticos passaram; um caso condicionado de 100 km chega em 4500 s,
sem extrapolar isso para os 7000 km.

Para a missão longa há dois resultados diferentes, sem alegação de ótimo:

1. **Limite inferior otimista de 171 dias de calendário**: somente rolamento
   com Cr mínimo assumido, rendimento 100%, sem arrasto ou auxiliares, toda
   bateria inicial de 98 kWh disponível e dois módulos gerando 3,2325 kWh/dia.
   `E_min = Cr_min m g D = 648,33 kWh`; dias ≥ ceil((E_min−98)/3,2325).
   O sol de 21/06 é repetido; não é previsão de geração ao longo da rota real.
2. `scripts/construir_viagem_condicionada.py` gera uma **agenda construtiva de
   7000 km em 1621,77 dias** (1622 datas), a 20 km/h durante períodos sem sol,
   esperando quando falta energia e mantendo reserva extra para habitação.
   O perfil de 21/06/São Carlos é repetido integralmente todos os dias/anos.
   O verificador independente confirma 7.000.000 m, máximo 8 h/dia,
   SOC final 12,94%, ausência de recarga externa e resíduo energético de −0,00186 J.
   É um limite superior de tempo **apenas nesse cenário**, não tempo mínimo nem
   previsão de viagem de Belém a Chuí. O CSV completo fica no cache, com hash no
   resumo portável. O SOC final de I27 não foi imposto indevidamente a I29.

O intervalo 171–1622 dias combina limites de modelos/relaxações diferentes;
não é intervalo estatístico ou certificado do ótimo físico. A construção longa
mostra o impacto do orçamento residencial: 100 W contínuos gastam 2,4 kWh/dia;
200 W gastam 4,8 kWh/dia, acima do cenário de dois módulos. Resolver consumo
habitacional e integração elétrica é decisivo antes de otimizar a rota real.

## Reprodução

Usar a `.venv` desta worktree. Prefixo do cache: `/home/mhc/motorhome_referencias_tarefas`.
Diretórios de saída devem ser novos; os scripts recusam sobrescrever evidências.

```bash
.venv/bin/python scripts/calcular_sensibilidade_energia.py --config config/energia_sensibilidade.yaml --solar CACHE/solar-calculo-02/resumo_solar.json --destino NOVO
.venv/bin/python scripts/calcular_agendas_provisorias.py --config config/energia_sensibilidade.yaml --solar-csv CACHE/solar-calculo-02/pv_timeseries.csv --destino NOVO
.venv/bin/python scripts/construir_viagem_condicionada.py --cenario NOVO_AGENDAS/resumo_agendas.json --solar-csv CACHE/solar-calculo-02/pv_timeseries.csv --destino NOVO
```

Resultados atuais: `energia-sensibilidade-02/`, `agendas-condicionadas-03/` e
`viagem-condicionada-01/`. Resumos/figuras estão na
[entrega parcial](../entregas/parcial_2026-10-24/README.md).
