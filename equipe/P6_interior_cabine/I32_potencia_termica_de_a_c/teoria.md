# Fundamentação e método — item 32

## Objetivo

Manter 25 °C internos com 33 °C externos ao meio-dia, passageiro e regime permanente.

## Equações e fonte

Qs=UA(Te−Ti)+Qsolar+Qequip+N Qpessoa,s+Qvent,s; Ql=N Qpessoa,l+Qvent,l; potência elétrica = capacidade de resfriamento/COP.

Apostila caps. 2 e 6, sobretudo pp. 69–72. Consulta local em 23/10/2026. A derivação, unidades, condições de contorno e testes estão na [frente térmica](../../../docs/FRENTE_TERMICA.md).

## Método disponível e limitações

Separar calor sensível, latente e energia elétrica. Calcular ganhos nas superfícies, psicrometria e ocupação com dados reais, sem dupla contagem; COP precisa de fonte. Ainda não há ciclo/equipamento dimensionado.

Implementação própria em [sistemas_termicos.py](../../../src/motorhome/sistemas_termicos.py) e [termica_2d.py](../../../src/motorhome/termica_2d.py). Temperaturas absolutas em K, tempo em s, energia em J, potência em W; demais propriedades em SI. Não foram importadas propriedades didáticas como dados reais.

## Estado

Métodos verificados com dados SYNTHETIC; entradas físicas e revisão humana **PENDENTES**. O status é desenvolvimento parcial. Consulte a [revisão completa](../../../docs/REVISAO_35_ITENS.md).
