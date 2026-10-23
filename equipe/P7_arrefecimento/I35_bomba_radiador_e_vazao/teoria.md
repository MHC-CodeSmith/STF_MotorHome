# Fundamentação e método — item 35

## Objetivo

Bomba, radiador e vazão para resfriar o motor em potência máxima; perfis térmicos e ponto da bomba.

## Equações e fonte

Ch=m_dot_h cp_h; Cc=m_dot_c cp_c; NTU=UA/Cmin; Q=epsilon Cmin(Th,in−Tc,in). Interseção: dp_bomba(Qvol)=dp_sistema(Qvol).

Apostila Eqs. 49–62 pp. 31/38, tabela 4 p. 39 e Eqs. 92–93 p. 56. Consulta local em 23/10/2026. A derivação, unidades, condições de contorno e testes estão na [frente térmica](../../../docs/FRENTE_TERMICA.md).

## Método disponível e limitações

O código suporta trocador paralelo/contracorrente e perfil somente paralelo; não substituir um radiador cruzado por esse exemplo. Faltam perdas máximas do motor, fluido, UA/arranjo reais, curvas de bomba/sistema e NPSH. Converter altura em pressão com rho g H quando necessário.

Implementação própria em [sistemas_termicos.py](../../../src/motorhome/sistemas_termicos.py) e [termica_2d.py](../../../src/motorhome/termica_2d.py). Temperaturas absolutas em K, tempo em s, energia em J, potência em W; demais propriedades em SI. Não foram importadas propriedades didáticas como dados reais.

## Estado

Métodos verificados com dados SYNTHETIC; entradas físicas e revisão humana **PENDENTES**. O status é desenvolvimento parcial. Consulte a [revisão completa](../../../docs/REVISAO_35_ITENS.md).
