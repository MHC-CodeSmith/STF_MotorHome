# Fundamentação teórica — item 02

## Objetivo e fenômeno
Definir pneus/rodas reais, dimensões e pressão interna.

## Equações e hipóteses
F_rol=Crr·m·g; cargas estáticas N_f+N_r=m·g.

## Entradas e unidades
Dependências diretas: I15 (P1).

## Modelo / procedimento
PneusOEM preservados. Não especificar pressão,medida ou índice de carga sem ficha da varianteSK505.GG1.2;Crr é sensibilidade.

## Limitações
Medida/índices/pressões da varianteSK exata e massa da roda não obtidos; não copiar de UK/NL.

<!-- execucao-integrada:inicio -->
Método técnico integrado: F_rol=Crr·m·g; cargas estáticas N_f+N_r=m·g.

PneusOEM preservados. Não especificar pressão,medida ou índice de carga sem ficha da varianteSK505.GG1.2;Crr é sensibilidade.

Escopo: Medida/índices/pressões da varianteSK exata e massa da roda não obtidos; não copiar de UK/NL.

Fonte dos parâmetros: `config/parametros_globais.yaml`;dadoOEM,hipótese e resultado mantêm status próprios. Simulação não é aprovação humana.
<!-- execucao-integrada:fim -->
