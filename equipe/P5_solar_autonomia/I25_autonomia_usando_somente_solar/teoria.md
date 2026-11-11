# Atualização de26/10/2026

Resultados, fontes primárias, hipóteses, equações e limites atuais em
[FECHAMENTO_TERMICO_E_MISSAO.md](../../../docs/FECHAMENTO_TERMICO_E_MISSAO.md).
Os métodos abaixo preservam o histórico; nenhuma aprovação de engenharia foi concedida.

# Fundamentação teórica — item 25

## Objetivo e fenômeno
Calcular geração de 21/06 céu limpo em São Carlos e distância solar a 40/80km/h; curva versus velocidade.

## Equações e hipóteses
Crédito_solar(t+Δt)=crédito_solar(t)+E_FV→HV−P_tração·Δt; crédito inicial0.

## Entradas e unidades
Dependências diretas: I08 (P5), I09 (P2), I22 (P4), I23 (P2), I26 (P5).

## Modelo / procedimento
MILP de alocação por janela e partidas em grade,40/80km/h;serviços cíclicos separados. Uma sessão hipotética não demonstra interfaceOEM ou ótimo global.

## Limitações
Uma parada+carga seguida de condução;serviços cíclicos separados,mínimosDC hipotéticos,sem provaOEM/ótimo global.

<!-- execucao-integrada:inicio -->
Método técnico integrado: Crédito_solar(t+Δt)=crédito_solar(t)+E_FV→HV−P_tração·Δt; crédito inicial0.

MILP de alocação por janela e partidas em grade,40/80km/h;serviços cíclicos separados. Uma sessão hipotética não demonstra interfaceOEM ou ótimo global.

Escopo: Uma parada+carga seguida de condução;serviços cíclicos separados,mínimosDC hipotéticos,sem provaOEM/ótimo global.

Fonte dos parâmetros: `config/parametros_globais.yaml`;dadoOEM,hipótese e resultado mantêm status próprios. Simulação não é aprovação humana.
<!-- execucao-integrada:fim -->
