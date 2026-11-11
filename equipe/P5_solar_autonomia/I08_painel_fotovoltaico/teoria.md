# Atualização de26/10/2026

Resultados, fontes primárias, hipóteses, equações e limites atuais em
[FECHAMENTO_TERMICO_E_MISSAO.md](../../../docs/FECHAMENTO_TERMICO_E_MISSAO.md).
Os métodos abaixo preservam o histórico; nenhuma aprovação de engenharia foi concedida.

# Fundamentação teórica — item 08

## Objetivo e fenômeno
Área, eficiência, tecnologia, potência, massa, montagem e configuração.

## Equações e hipóteses
P_FV≈P_STC·G_POA/1000·[1+γ(T_c−25°C)]·f_perdas; E=ΣP·Δt.

## Entradas e unidades
Dependências diretas: I17 (P3).

## Modelo / procedimento
1540Wp documentados por2×380+2×390 e1600Wp portáteis,somenteparados/ângulos fixos. FamíliaPV e limitesMPPT específicos por cenário;Wp não são kWh.

## Limitações
Retângulo estimado/curvatura/ancoragens/estoque não comprovados;rastreadores independentes são comparadorDEC054,compartilhamento não aprovado.

<!-- execucao-integrada:inicio -->
Método técnico integrado: P_FV≈P_STC·G_POA/1000·[1+γ(T_c−25°C)]·f_perdas; E=ΣP·Δt.

1540Wp documentados por2×380+2×390 e1600Wp portáteis,somenteparados/ângulos fixos. FamíliaPV e limitesMPPT específicos por cenário;Wp não são kWh.

Escopo: Retângulo estimado/curvatura/ancoragens/estoque não comprovados;rastreadores independentes são comparadorDEC054,compartilhamento não aprovado.

Fonte dos parâmetros: `config/parametros_globais.yaml`;dadoOEM,hipótese e resultado mantêm status próprios. Simulação não é aprovação humana.
<!-- execucao-integrada:fim -->
