# Fundamentação teórica — item 09

## Objetivo e fenômeno
Modelos reais, tensão de operação, potências, eficiências e limites.

## Equações e hipóteses
P_AC≤P_contínua(T); S_AC=V·I; P_AC=S_AC·FP; P_bateria≈P_AC/η+P_vazio.

## Entradas e unidades
Dependências diretas: I06 (P2), I08 (P5).

## Modelo / procedimento
220V60Hz configuráveis noGX. Comparador independente250/60teto+150/60portáteis não aprova MPPTcompartilhado nem saída48V paraHV.

## Limitações
250/60 usa35A conservador;saídas48V não são interfaceHV. BMS/proteções/comutação e interfaceDC não demonstrados.

<!-- execucao-integrada:inicio -->
Método técnico integrado: P_AC≤P_contínua(T); S_AC=V·I; P_AC=S_AC·FP; P_bateria≈P_AC/η+P_vazio.

220V60Hz configuráveis noGX. Comparador independente250/60teto+150/60portáteis não aprova MPPTcompartilhado nem saída48V paraHV;250/60 é rejeitado pelas perdas de descasamento medidas, não por limite de corrente.

Escopo: Saídas48V não são interfaceHV; 250/60 rejeitado pelas perdas de descasamento (até27%), não por limite de corrente. BMS/proteções/comutação e interfaceDC não demonstrados.

Fonte dos parâmetros: `config/parametros_globais.yaml`;dadoOEM,hipótese e resultado mantêm status próprios. Simulação não é aprovação humana.
<!-- execucao-integrada:fim -->
