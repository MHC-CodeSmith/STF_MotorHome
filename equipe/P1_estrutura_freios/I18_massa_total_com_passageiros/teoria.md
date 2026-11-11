# Fundamentação teórica — item 18

## Objetivo e fenômeno
Somar massas documentadas por componente, passageiros, água, bagagem e cargas.

## Equações e hipóteses
m_total=m_OEM+Σm_conversão+m_pessoas+m_bagagem+m_água; m_água é conservada entre reservatórios.

## Entradas e unidades
Dependências diretas: I02 (P1), I03 (P1), I04 (P4), I05 (P4), I06 (P2), I07 (P2), I08 (P5), I09 (P2), I10 (P7), I11 (P6), I12 (P7), I13 (P6), I14 (P1), I15 (P1), I16 (P3), I17 (P3).

## Modelo / procedimento
Partida100Ltotais:85Ltanque+15Lboiler. Cassete é o tanque negro,sem reservatório duplicado. CG/eixos são estimados,sem pesagem.

## Limitações
Tara/CGbase e posições assumidos; não pesagem. Limites por eixo permanecem desconhecidos.

<!-- execucao-integrada:inicio -->
Método técnico integrado: m_total=m_OEM+Σm_conversão+m_pessoas+m_bagagem+m_água; m_água é conservada entre reservatórios.

Partida100Ltotais:85Ltanque+15Lboiler. Cassete é o tanque negro,sem reservatório duplicado. CG/eixos são estimados,sem pesagem.

Escopo: Tara/CGbase e posições assumidos; não pesagem. Limites por eixo permanecem desconhecidos.

Fonte dos parâmetros: `config/parametros_globais.yaml`;dadoOEM,hipótese e resultado mantêm status próprios. Simulação não é aprovação humana.
<!-- execucao-integrada:fim -->
