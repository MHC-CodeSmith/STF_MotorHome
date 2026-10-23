# Fundamentação e método — item 30

## Objetivo

Cabos na potência máxima do motor; campo de temperatura multidimensional.

## Equações e fonte

qv = (I/A)² rho_e [W/m³]; rho_e(T)=rho_ref[1+alpha_e(T−Tref)]. Balanço: rho cp dT/dt = div(k grad T)+qv.

Apostila pp. 9–10: Fourier/Newton; geração Joule é complemento elétrico. Consulta local em 23/10/2026. A derivação, unidades, condições de contorno e testes estão na [frente térmica](../../../docs/FRENTE_TERMICA.md).

## Método disponível e limitações

Fornecer corrente RMS/DC apropriada, seção, material, isolamento e resistividade com fonte. O solver atual é cartesiano homogêneo e usa fonte fixa; o acoplamento rho_e(T), isolamento e cabo real ainda precisam ser implementados.

Implementação própria em [sistemas_termicos.py](../../../src/motorhome/sistemas_termicos.py) e [termica_2d.py](../../../src/motorhome/termica_2d.py). Temperaturas absolutas em K, tempo em s, energia em J, potência em W; demais propriedades em SI. Não foram importadas propriedades didáticas como dados reais.

## Estado

Métodos verificados com dados SYNTHETIC; entradas físicas e revisão humana **PENDENTES**. O status é desenvolvimento parcial. Consulte a [revisão completa](../../../docs/REVISAO_35_ITENS.md).
