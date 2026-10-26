# Atualização de26/10/2026

Resultados, fontes primárias, hipóteses, equações e limites atuais em
[FECHAMENTO_TERMICO_E_MISSAO.md](../../../docs/FECHAMENTO_TERMICO_E_MISSAO.md).
Os métodos abaixo preservam o histórico; nenhuma aprovação de engenharia foi concedida.

# Fundamentação e método — item 34

## Objetivo

Temperatura da bateria durante cargas em carregadores de 20 e 80 kW.

## Equações e fonte

Parcela irreversível simplificada Qdot_ohm=I²R, I=P_terminal/V; C dT/dt = Qdot_gerado − Qdot_arrefecimento.

Apostila cap. 2 e armazenamento sensível, Eq. 112 p. 74. Consulta local em 23/10/2026. A derivação, unidades, condições de contorno e testes estão na [frente térmica](../../../docs/FRENTE_TERMICA.md).

## Método disponível e limitações

A placa de 20/80 kW não define calor nem protocolo completo. Fornecer células, pack, R(SOC,T), tensão, protocolo CC/CV/BMS, limites e calor reversível quando relevante. O exemplo V/R constantes não resolve o pack real.

Implementação própria em [sistemas_termicos.py](../../../src/motorhome/sistemas_termicos.py) e [termica_2d.py](../../../src/motorhome/termica_2d.py). Temperaturas absolutas em K, tempo em s, energia em J, potência em W; demais propriedades em SI. Não foram importadas propriedades didáticas como dados reais.

## Estado

Métodos verificados com dados SYNTHETIC; entradas físicas e revisão humana **PENDENTES**. O status é desenvolvimento parcial. Consulte a [revisão completa](../../../docs/REVISAO_35_ITENS.md).
