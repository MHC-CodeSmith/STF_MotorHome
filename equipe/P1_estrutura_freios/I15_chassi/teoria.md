# Fundamentação teórica — item 15

## Objetivo e fenômeno
Dimensões do chassi, material, massa e compatibilidade com carroceria.

## Equações e hipóteses
EI·d⁴u/dx⁴=q; ΣF=F_aplicada; Σ(r×F)=M_aplicado; σ_eq=√(σ_tração²+3τ²).

## Entradas e unidades
Dependências diretas: I01 (P1).

## Modelo / procedimento
ChassiOEM é referência. FEM de trilhos/tiras e grupos de parafusos são modelos locais;sem inventar material/rigidez/ancoragens da carroceria.

## Limitações
Chassi/ancoragensOEM/furação/contato/fadiga não demonstrados;seleções locais não homologam carroceria.

<!-- execucao-integrada:inicio -->
Método técnico integrado: EI·d⁴u/dx⁴=q; ΣF=F_aplicada; Σ(r×F)=M_aplicado; σ_eq=√(σ_tração²+3τ²).

ChassiOEM é referência. FEM de trilhos/tiras e grupos de parafusos são modelos locais;sem inventar material/rigidez/ancoragens da carroceria.

Escopo: Chassi/ancoragensOEM/furação/contato/fadiga não demonstrados;seleções locais não homologam carroceria.

Fonte dos parâmetros: `config/parametros_globais.yaml`;dadoOEM,hipótese e resultado mantêm status próprios. Simulação não é aprovação humana.
<!-- execucao-integrada:fim -->
