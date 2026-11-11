# Fundamentação e método — item 31

## Objetivo

Cabine estacionada fechada ao meio-dia, sem A/C nem passageiros.

## Equações e fonte

C dT/dt = Q_solar + Q_equipamentos − Q_perdas; exemplo concentrado implementa Q_perdas=UA(T−Ta), com coeficientes constantes.

Apostila cap. 2, pp. 9–23, e Eq. 112 p. 74. Consulta local em 23/10/2026. A derivação, unidades, condições de contorno e testes estão na [frente térmica](../../../docs/FRENTE_TERMICA.md).

## Método disponível e limitações

Fornecer superfícies, vidros, materiais, absorção/transmissão, radiação solar e regime/condição inicial. A função concentrada isolada não é um modelo completo de cabine; justificar gradientes desprezíveis antes de usá-la.

Implementação própria em [sistemas_termicos.py](../../../src/motorhome/sistemas_termicos.py) e [termica_2d.py](../../../src/motorhome/termica_2d.py). Temperaturas absolutas em K, tempo em s, energia em J, potência em W; demais propriedades em SI. Não foram importadas propriedades didáticas como dados reais.

## Estado

Métodos verificados com dados SYNTHETIC; entradas físicas e revisão humana **PENDENTES**. O status é desenvolvimento parcial. Consulte a [revisão completa](../../../docs/REVISAO_35_ITENS.md).

<!-- execucao-integrada:inicio -->
Método técnico integrado: C_i·dT_i/dt=Σ(T_j−T_i)/R_ij+Q_solar,i; noCFD,empuxo≈ρ0gβ(T−T0).

Cabine fechada,parada,sem pessoas/AC;manhã→meiodia25°Cexternos. CFD3D é complemento de contorno congelado,nãoCHT matinal ou ensaio veicular.

Escopo: SIMPLErejeitado;CFDtransiente é complemento com contornos congelados,sem CHT/mobiliário/y+convergente.

Fonte dos parâmetros: `config/parametros_globais.yaml`;dadoOEM,hipótese e resultado mantêm status próprios. Simulação não é aprovação humana.
<!-- execucao-integrada:fim -->
