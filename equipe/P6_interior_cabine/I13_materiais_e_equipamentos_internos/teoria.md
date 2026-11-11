# Fundamentação teórica — item 13

## Objetivo e fenômeno
Assentos, móveis, sanitário, chuveiro, eletrônicos, fogão, geladeira e lavadora/secadora.

## Equações e hipóteses
E_dia=ΣP_i·t_i+ΣE_ciclo·frequência; E_bat=E_AC/η_inv+E_DC/η_DC+E_vazio.

## Entradas e unidades
Dependências diretas: I15 (P1), I16 (P3).

## Modelo / procedimento
Método médio diárioDEC046 para duas pessoas;lavanderia ocasional,picos/simultaneidade em análise separada. Prioridades automáticas não fixam SOC/BMS arbitrários.

## Limitações
256combinações de picos e6históricos de falha simulados;partidas reais/atuadores e limitesSOC ainda não demonstrados.

<!-- execucao-integrada:inicio -->
Método técnico integrado: E_dia=ΣP_i·t_i+ΣE_ciclo·frequência; E_bat=E_AC/η_inv+E_DC/η_DC+E_vazio.

Método médio diárioDEC046 para duas pessoas;lavanderia ocasional,picos/simultaneidade em análise separada. Prioridades automáticas não fixam SOC/BMS arbitrários.

Escopo: 256picos,6históricos e72autonomias por orçamento previsto;partidas reais/atuadores e limiaresSOC continuam não demonstrados.

Fonte dos parâmetros: `config/parametros_globais.yaml`;dadoOEM,hipótese e resultado mantêm status próprios. Simulação não é aprovação humana.
<!-- execucao-integrada:fim -->
