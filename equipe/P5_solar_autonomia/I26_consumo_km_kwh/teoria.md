# Atualização de26/10/2026

Resultados, fontes primárias, hipóteses, equações e limites atuais em
[FECHAMENTO_TERMICO_E_MISSAO.md](../../../docs/FECHAMENTO_TERMICO_E_MISSAO.md).
Os métodos abaixo preservam o histórico; nenhuma aprovação de engenharia foi concedida.

# Fundamentação teórica — item 26

## Objetivo e fenômeno
Distância por energia elétrica da bateria em km/kWh a 40 e 80 km/h; explicitar auxiliares.

## Equações e hipóteses
e(v)=P_bat(v)/v emkWh/km; rendimento espacial=1/e(v) emkm/kWh.

## Entradas e unidades
Dependências diretas: I21 (P4), I22 (P4), I23 (P2), I13 (P6).

## Modelo / procedimento
Avaliar40/80km/h constantes,plano,25°C/UR50/vento0,consumo habitável separado. Sensibilidade deCd/Crr/η/massa não equivale a previsão rodoviária.

## Limitações
Eficiência constante e dados de rolamento/aerodinâmica estimados.

<!-- execucao-integrada:inicio -->
Método técnico integrado: e(v)=P_bat(v)/v emkWh/km; rendimento espacial=1/e(v) emkm/kWh.

Avaliar40/80km/h constantes,plano,25°C/UR50/vento0,consumo habitável separado. Sensibilidade deCd/Crr/η/massa não equivale a previsão rodoviária.

Escopo: Eficiência constante e dados de rolamento/aerodinâmica estimados.

Fonte dos parâmetros: `config/parametros_globais.yaml`;dadoOEM,hipótese e resultado mantêm status próprios. Simulação não é aprovação humana.
<!-- execucao-integrada:fim -->
