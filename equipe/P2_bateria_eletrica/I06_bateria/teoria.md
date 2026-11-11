# Fundamentação teórica — item 06

## Objetivo e fenômeno
Escolher células/pack/BMS: tecnologia, tensão, massa, limites, curva e segurança.

## Equações e hipóteses
E_nom=N_módulos·E_módulo; E_disponível=E_nom·min(DoD,1−SOC_reserva).

## Entradas e unidades
Dependências diretas: I04 (P4).

## Modelo / procedimento
Pack de tração110brutos/98úteis da mesma variante. Serviços3US5000=14,4kWh nominal,uso móvel/BMS/fixação ainda condicionados.

## Limitações
Uso móvel, fixação/BMS e corrente/partidas documentais faltam; buffer não instalado.

<!-- execucao-integrada:inicio -->
Método técnico integrado: E_nom=N_módulos·E_módulo; E_disponível=E_nom·min(DoD,1−SOC_reserva).

Pack de tração110brutos/98úteis da mesma variante. Serviços3US5000=14,4kWh nominal,uso móvel/BMS/fixação ainda condicionados.

Escopo: Uso móvel, fixação/BMS e corrente/partidas documentais faltam; buffer não instalado.

Fonte dos parâmetros: `config/parametros_globais.yaml`;dadoOEM,hipótese e resultado mantêm status próprios. Simulação não é aprovação humana.
<!-- execucao-integrada:fim -->
