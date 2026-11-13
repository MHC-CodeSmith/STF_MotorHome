# Fundamentação teórica — item 22

## Objetivo e fenômeno
Curvas de potência versus velocidade, eficiência e envelope de tração disponível.

## Equações e hipóteses
P_roda=(F_D+F_rol)·v; P_bat=P_roda/η_tração+P_aux,OEM.

## Entradas e unidades
Dependências diretas: I04 (P4), I05 (P4), I21 (P4).

## Modelo / procedimento
Auxiliar700W de estudo sensibilizado0/300/700/1500W somente em movimento. Serviços habitáveis vêm do banco48V e não entram na tração.

## Limitações
AuxiliaresOEM0/300/700/1500W sensibilizados, não confundidos com serviços.

<!-- execucao-integrada:inicio -->
Método técnico integrado: P_roda=(F_D+F_rol)·v; P_bat=P_roda/η_tração+P_aux,OEM.

Auxiliar700W de estudo sensibilizado0/300/700/1500W somente em movimento. Serviços habitáveis vêm do banco48V e não entram na tração.

Escopo: Eficiência0,90 e auxiliares700W estimados; potência na roda não é mapa/potência contínua do motor, sem validação OEM ou física.

Fonte dos parâmetros: `config/parametros_globais.yaml`;dadoOEM,hipótese e resultado mantêm status próprios. Simulação não é aprovação humana.
<!-- execucao-integrada:fim -->
