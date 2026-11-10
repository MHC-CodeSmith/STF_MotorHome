# Fundamentação e método — item 33

## Objetivo

Frenagem 30 → 10 m/s em 5 s, temperatura inicial 25 °C; campo multidimensional.

## Equações e fonte

Delta E_trans/m=(vi²−vf²)/2=400 J/kg e potência média removida/m=80 W/kg. A média de aceleração é −4 m/s²; distância 100 m exige desaceleração constante.

Enunciado p. 2 I33; apostila cap. 2 para condução/convecção. Consulta local em 23/10/2026. A derivação, unidades, condições de contorno e testes estão na [frente térmica](../../../docs/FRENTE_TERMICA.md).

## Avanço — 26/10/2026

Campo r–z transiente em duas pistas anulares simétricas de disco ventilado,
com volumetria cilíndrica, Crank–Nicolson, fonte e Robin conservativos.
[Método, fontes, resultados e limites](../../../docs/FREIOS_2D.md).
Código`src/motorhome/freios_axisimetricos.py`, configuração`config/freios_proposta.yaml`.
4250kg/0,7dianteira/0,9disco são cenário condicionado, não parâmetros aprovados.
I33 segue parcial: faltam geometria/material/distribuição reais e revisão humana.

## Método anterior e limitações

Distribuir a energia entre arrasto, rolamento, regeneração e freios; incluir inércias e partição disco/pastilha. Gerar geometria/material/contornos e iniciar 298,15 K. O teste retangular 2D é verificação de método, não resultado do disco.

Implementação própria em [sistemas_termicos.py](../../../src/motorhome/sistemas_termicos.py) e [termica_2d.py](../../../src/motorhome/termica_2d.py). Temperaturas absolutas em K, tempo em s, energia em J, potência em W; demais propriedades em SI. Não foram importadas propriedades didáticas como dados reais.

## Estado

Métodos verificados com dados SYNTHETIC; entradas físicas e revisão humana **PENDENTES**. O status é desenvolvimento parcial. Consulte a [revisão completa](../../../docs/REVISAO_35_ITENS.md).

<!-- execucao-integrada:inicio -->
Método técnico integrado: ΔE_c=400mJ para30→10m/s; a=−4m/s²; ρcp∂T/∂t=∇·k∇T+Q̇_fricção.

Ensaio5s/inicial25°C,disco2Drz,atrito e regeneração limitada em hipóteses. Subtrair arrasto/rolamento.108km/h é condição prescrita de componente,acima do limitador do veículo.

Escopo: Disco/material/repartição/regenOEM não confirmados;108km/h é ensaio prescrito,acima limitador90.

Fonte dos parâmetros: `config/parametros_globais.yaml`;dadoOEM,hipótese e resultado mantêm status próprios. Simulação não é aprovação humana.
<!-- execucao-integrada:fim -->
