# Fundamentação e método — item 33

## Objetivo

Frenagem 30 → 10 m/s em 5 s, temperatura inicial 25 °C; campo multidimensional.

## Equações e fonte

Delta E_trans/m=(vi²−vf²)/2=400 J/kg e potência média removida/m=80 W/kg. A média de aceleração é −4 m/s²; distância 100 m exige desaceleração constante.

Enunciado p. 2 I33; apostila cap. 2 para condução/convecção. Consulta local em 23/10/2026. A derivação, unidades, condições de contorno e testes estão na [frente térmica](../../../docs/FRENTE_TERMICA.md).

## Método disponível e limitações

Distribuir a energia entre arrasto, rolamento, regeneração e freios; incluir inércias e partição disco/pastilha. Gerar geometria/material/contornos e iniciar 298,15 K. O teste retangular 2D é verificação de método, não resultado do disco.

Implementação própria em [sistemas_termicos.py](../../../src/motorhome/sistemas_termicos.py) e [termica_2d.py](../../../src/motorhome/termica_2d.py). Temperaturas absolutas em K, tempo em s, energia em J, potência em W; demais propriedades em SI. Não foram importadas propriedades didáticas como dados reais.

## Estado

Métodos verificados com dados SYNTHETIC; entradas físicas e revisão humana **PENDENTES**. O status é desenvolvimento parcial. Consulte a [revisão completa](../../../docs/REVISAO_35_ITENS.md).
