# Fundamentação teórica — item 23

## Objetivo e fenômeno
Dimensionar energia útil/nominal, SOC, limites e margens.

## Equações e hipóteses
N=ceil[E_dia·(autonomia_h/24)/(E_módulo·min(DoD,1−reserva)))].

## Entradas e unidades
Dependências diretas: I06 (P2), I08 (P5), I13 (P6), I22 (P4).

## Modelo / procedimento
Comparar24/48h semSol para ambas reservas. Capacidade nominal não é energia útil;110/98kWh da tração são conceitos distintos.

## Limitações
3módulos atendem24hbase/reserva30%,48h exige4/5; não aprovar capacidade final.

<!-- execucao-integrada:inicio -->
Método técnico integrado: N=ceil[E_dia·(autonomia_h/24)/(E_módulo·min(DoD,1−reserva)))].

Comparar24/48h semSol para ambas reservas. Capacidade nominal não é energia útil;110/98kWh da tração são conceitos distintos.

Escopo: Massa/rack/CAD estimados;uso móvel/BMS/folgas/retençãoOEM e capacidade final não validados.

Fonte dos parâmetros: `config/parametros_globais.yaml`;dadoOEM,hipótese e resultado mantêm status próprios. Simulação não é aprovação humana.
<!-- execucao-integrada:fim -->
