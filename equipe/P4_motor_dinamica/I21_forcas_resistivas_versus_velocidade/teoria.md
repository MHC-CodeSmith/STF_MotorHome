# Fundamentação teórica — item 21

## Objetivo e fenômeno
Produzir força aerodinâmica e de rolamento versus velocidade; cenário plano e sem vento.

## Equações e hipóteses
F_D=½ρ·Cd·A_ref·v_rel².

## Entradas e unidades
Dependências diretas: I18 (P1), I19 (P3), I20 (P4).

## Modelo / procedimento
Vento externo0 implica v_rel=v_veículo. Usar a mesma área de normalização doCFD;limiteCd0,72 é sensibilidade conservadora,não valorOEM.

## Limitações
Cd/Crr/ρ condicionais; pista plana e vento0.

<!-- execucao-integrada:inicio -->
Método técnico integrado: F_D=½ρ·Cd·A_ref·v_rel².

Vento externo0 implica v_rel=v_veículo. Usar a mesma área de normalização doCFD;limiteCd0,72 é sensibilidade conservadora,não valorOEM.

Escopo: Rampa/vento e coeficientes são hipóteses, não rota medida; sem aceleração, mapas OEM ou limites de pneus/eixos.

Fonte dos parâmetros: `config/parametros_globais.yaml`;dadoOEM,hipótese e resultado mantêm status próprios. Simulação não é aprovação humana.
<!-- execucao-integrada:fim -->
