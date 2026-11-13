# Fundamentação teórica — item 19

## Objetivo e fenômeno
Simular CFD; obter Cd, área frontal; documentar malha, domínio, solver, contornos e convergência.

## Equações e hipóteses
∇·U=0; ρ(U·∇)U=−∇p+∇·τ_eff; Cd=F_D/(½ρA_refU_ref²).

## Entradas e unidades
Dependências diretas: I17 (P3).

## Modelo / procedimento
RANS kOmegaSST com piso móvel e parede,3malhas equipadas. Relatar resíduos,histórico de força,y+ e variação de malha. GCI requer hipóteses não demonstradas;Cd permanece faixa condicional.

## Limitações
Variação final5.23%;GCI não justificável por refinamento local;geometria/parede não validadas,semCddefinitivo.

<!-- execucao-integrada:inicio -->
Método técnico integrado: ∇·U=0; ρ(U·∇)U=−∇p+∇·τ_eff; Cd=F_D/(½ρA_refU_ref²).

RANS kOmegaSST com piso móvel e parede,3malhas equipadas. Relatar resíduos,histórico de força,y+ e variação de malha. GCI requer hipóteses não demonstradas;Cd permanece faixa condicional.

Escopo: Malhas não aninhadas e Cd difere7.05% (grading2/base) e16.65% (grading4/base); y+ médio solo1146/913 e p inicial1.15e-4 no grading2. Sem GCI, independência, parede adequada ou validação física.

Fonte dos parâmetros: `config/parametros_globais.yaml`;dadoOEM,hipótese e resultado mantêm status próprios. Simulação não é aprovação humana.
<!-- execucao-integrada:fim -->
