# Dependências entre os 35 itens

Cada pasta de item lista entradas diretas necessárias aos dados finais. Dependências de implementação são **DAG de dados finais**, mas muitas equipes podem iniciar cálculos com estimativas **rotuladas como provisórias**. Relações úteis para interpretar resultados, sem bloquear o cálculo consumidor, ficam em `metadata/interfaces_contextuais.csv`; não são arestas do DAG. Retroalimentações de projeto (ex.: P5 solicita bateria maior a P2) são decisões/iterações, não dependências circulares silenciosas.

## Interfaces prioritárias
- Todos → P1: massas, quantidade e custos dos componentes para itens 18 e 24.
- P1/P6 → P3: chassi, envelopamento e distribuição interna → itens 17, 19.
- P3 → P4/P5/P6: `Cd`, área frontal, teto útil, áreas de vidros/paredes e volume.
- P4 → P2/P5/P7: potência, torque, eficiência, perdas e demanda por velocidade.
- P2 → P5/P7: tensão, capacidade útil e nominal, correntes e limitações térmicas.
- P5 → P2/P3: painéis/área; incompatibilidades de autonomia podem requerer nova decisão de arquitetura.
- P6/P7 → P5: perfis de potência auxiliar, ar-condicionado, bombas, ventiladores.

## Caminho de integração
Requisitos/veículo-base → chassi/carroceria/equipamentos → CAD/massa → Cd e rolamento → curvas de potência → consumo → geração solar/armazenamento → autonomia → otimização 7000 km.

## Simulações paralelas
- Item 30 (fios): P2, depende de motor/cabos.
- Item 33 (freios): P1, depende massa/freios.
- Item 34 (bateria): P7, depende bateria/limites.
- Item 35 (arrefecimento): P7, depende perdas de motor.
- Itens 31/32: P6, dependem da geometria, materiais e carga solar.

I28→I33 é uma interface contextual não bloqueante: o limite operacional de I28 (90 km/h) contextualiza o ensaio do componente, enquanto o cálculo prescrito de I33 usa o teste 30→10 m/s em 5 s e os dados de freio/massa I03/I18. A condição de 108 km/h é ensaio acadêmico de componente e não desempenho afirmado do veículo.

Veja o DAG legível em `docs/fluxograma_dependencias.mmd`, as arestas de dados em `metadata/itens.csv` e as interfaces contextuais em `metadata/interfaces_contextuais.csv`.
