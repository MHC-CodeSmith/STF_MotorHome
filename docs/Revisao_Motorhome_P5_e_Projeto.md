# Revisão do projeto Motorhome

Lista para consolidar as anotações do relatório inicial e as mudanças discutidas com a equipe. Os resultados já calculados estão indicados como referência. As demais ações são tarefas de revisão.

## 1. P5 · Geração solar, autonomia e viagem

### I08 · Teto e painéis portáteis

- [ ] **Incorporar ao relatório o teto com quatro Maxeon de 390 Wp, em 2S2P.** A configuração com duas strings de dois módulos iguais soma **1.560 Wp**, ante 1.540 Wp no arranjo anterior. As dimensões nominais e a massa de **76 kg** dos quatro módulos se mantêm. A simulação de geração do novo arranjo já existe. No mesmo dia claro, o teto passou de **5,864 para 5,940 kWh**, ganho de **0,076 kWh**. Atualizar a configuração usada nos itens dependentes, as figuras e a lista de materiais.
- [ ] **Explicar a ligação e a escolha do MPPT em conjunto com a P2.** Mostrar **129 V e 12,10 A** no ponto de máxima potência em condições-padrão, **171,59 V** em circuito aberto no frio de projeto e cerca de **32,5 A** na saída a 48 V, com conversão ideal. O SmartSolar **250/60-Tr** passou na verificação por ficha para o teto. Em quatro módulos em paralelo, a tensão de trabalho estimada a 85 °C cai para cerca de **49 V**, com pouca margem para carregar o banco. Deixar a explicação completa do inversor e das proteções no I09.
- [ ] **Comparar os portáteis com o conjunto EcoFlow atual.** Avaliar ZOUPW 450 W por versão, EcoFlow 400 W Lightweight e o candidato anotado como Renogy E.FLEX 400 W, cujo modelo exato ainda precisa ser confirmado. Comparar **kWh por parada**, potência nominal, massa com acessórios, dimensões abertas e dobradas, tempo de montagem, custo e compatibilidade com o MPPT. Conferir no CAD a quantidade que cabe, acesso para retirada, fixação durante a viagem e espaço para abrir os módulos no chão sem sombreamento entre eles.
- [ ] **Mostrar a geração com e sem portáteis.** Fazer um gráfico horário com teto, portáteis e soma. Comparar **só teto**, **dia inteiro parado com os portáteis prontos antes do amanhecer**, **condução diurna** e **condução no fim da tarde ou à noite**, usando a mesma data e o mesmo clima para isolar o efeito do horário. Marcar montagem e recolhimento. Os casos já simulados deram **8,04 kWh nos portáteis** com condução de 0h a 8h e **0,37 kWh** com condução de 8h a 16h. O dia todo parado precisa de uma execução própria.
- [ ] **Como sensibilidade, testar inclinação do teto pelo eixo longitudinal.** Comparar a energia diária em kWh e declarar inclinação, orientação e janela de uso. Para qualquer estimativa de “dias para carregar”, indicar **qual banco**, a faixa de SOC e a geração líquida disponível após serviços e perdas.

### I25 · Autonomia usando o sol do dia

- [ ] **Refazer a curva com o teto de 1.560 Wp e o limiar menor acertado com a P2.** Usar a mesma convenção de potência na **saída da interface DC** no I25 e no I29. O código anterior do I25 aplicava o mínimo na entrada. Registrar o valor aprovado em **kW**. O crédito solar do dia começa em zero.
- [ ] **Mostrar os casos com e sem consumo da habitação**, com destaque para 40 e 80 km/h. Informar em cada caso geração FV, energia para serviços, perdas, energia cortada pelo limiar, energia entregue à tração e distância. Manter explícita a condição de interface DC hipotética.
- [ ] **Confirmar a anotação de “corte de aproximadamente 0,4 kWh”.** Informar dia, cenário, limiar e lado da medição. Na sensibilidade anterior a 80 km/h, baixar de 1 para 0,5 kW na saída aumentou a energia entregue à tração de **5,13 para 5,91 kWh/dia**. Esses **0,78 kWh/dia** são o ganho naquele teste. O corte remanescente precisa ser apurado na nova execução.

### I26 · Consumo por velocidade

- [ ] **Apresentar as duas unidades e a origem do resultado.** A 40 km/h, **4,44 km/kWh ou 0,225 kWh/km**. A 80 km/h, **2,46 km/kWh ou 0,406 kWh/km**. Trocar “medido na bateria” por **“calculado no lado da bateria”**. Explicar que, para a mesma densidade do ar e o mesmo veículo, dobrar a velocidade quadruplica a força de arrasto no modelo. Atualizar as contas se a massa transportada, o arrasto ou os parâmetros de tração mudarem.

### I27 · Autonomia diária com SOC final de 30%

- [ ] **Explicitar que os 30% finais vêm do enunciado.** No caso publicado, a tração começa em 100%, tem **68,6 kWh** de orçamento até chegar a 30% e opera sem reposição solar durante o dia.
- [ ] **Colocar lado a lado os dois resultados.** Com janela de até 24 h, **351,5 km em cerca de 17 h ao volante**. Com limite de **8 h ao volante**, **309,5 km**. Explicar o ótimo perto de 20 km/h pelo equilíbrio entre o consumo dos auxiliares por tempo e o arrasto por distância. Identificar as hipóteses de pista plana, velocidade constante e rendimento adotado.

### I29 · Viagem de 7.000 km

- [ ] **Comparar a melhor velocidade da busca, 40 e 80 km/h**, inicialmente sob o mesmo horário, as mesmas reservas e condições de geração. Isso isola o efeito da velocidade. Se o grupo também quiser comparar a melhor estratégia para cada velocidade, fazer uma rodada em que o horário possa variar. Reportar **dias totais, horas ao volante e km/dia após a primeira vez que a tração atinge a reserva**. Distinguir a autonomia com a bateria inicialmente cheia do ritmo que a geração diária sustenta.
- [ ] **Explicar por que houve busca em grade.** O mínimo de consumo específico em pista plana pode ser calculado. O tempo total também depende da agenda solar, da abertura dos portáteis, das reservas e da energia disponível em cada horário. Identificar a velocidade publicada como a melhor combinação encontrada nas condições testadas.
- [ ] **Revisar o significado de 17h45.** O relógio atual começa à meia-noite, e a janela recorrente de 17h45 a 1h45 permite condução na madrugada do primeiro dia. Usar **“início da janela diária”** no relatório ou, se 17h45 tiver de ser a primeira saída física, ajustar a inicialização e recalcular.
- [ ] **Registrar como cenário opcional acumular energia por mais de um dia** para percorrer um trecho maior depois. Usar o teto atualizado e o limiar menor nas novas comparações e deixar explícitas as hipóteses de clima, recarga e operação dos portáteis.

## 2. Restante do projeto · Revisões por frente e do relatório

### Organização e fluxogramas

- [ ] **Conferir a variante exata da E-Ducato e tornar as escolhas rastreáveis.** Na introdução, incluir o teto e os portáteis na descrição da geração. Nas especificações, explicitar qual alternativa foi considerada e qual parâmetro decidiu a escolha. Usar referências de estado da arte onde houver comparação válida. Para cada resultado importante, registrar **teoria, entradas com fonte, método, resultado e interpretação**.
- [ ] **Incluir um mapa de dependências entre as frentes** e fluxogramas curtos nas seções em que o caminho da energia, a ordem das contas ou as decisões operacionais ajudam a leitura.

| Seção | Conteúdo do fluxograma |
|---|---|
| I08–I09 · Geração e elétrica | Sol, painéis, MPPT, banco de serviços, inversor e cargas. Mostrar em ramo próprio a recarga externa DC hipotética da tração e o ponto do limiar. |
| I25–I29 · Autonomia e viagem | Geração e consumo por horário, atualização dos bancos, reservas, abertura dos portáteis, decisão de dirigir ou esperar e distância. |
| I30 · Cabos | Corrente de fase, efeito Joule, troca de calor com o ambiente e temperatura máxima. |
| I31–I32 · Cabine e climatização | Ganhos térmicos, ventilação, temperatura interna, carga de resfriamento e potência elétrica pelo COP. |

### P2 e P6 · Arquitetura, baterias e habitação

- [ ] **I08–I09 · Explicar MPPT, inversor e perdas.** Mostrar os bancos de serviços e de tração como ramos distintos. A transferência solar para a tração depende da interface DC externa hipotética. Registrar o limiar menor acertado com a P5, em kW na saída. Explicar que o inversor é dimensionado pelas cargas em CA e que a troca de 20 Wp no teto não exige redimensioná-lo.
- [ ] **I06, I13 e I23 · Detalhar o balanço da habitação.** Por aparelho, listar potência, tempo ou ciclo de uso, alimentação CA ou CC, energia diária e fonte. Apresentar perdas por conversão e consumo em vazio separadamente. Entregar à P5 um perfil por horário e explicitar carga média e faixa de SOC para a estimativa de **33 h** da habitação.
- [ ] **I23 · Corrigir a denominação dos 112,4 kWh.** O valor soma **98 kWh úteis de tração** e **14,4 kWh nominais de serviços**, dos quais cerca de **13,7 kWh** são utilizáveis na hipótese do relatório. Indicar qual capacidade serve de base para SOC e reservas em cada simulação.
- [ ] **I07 · Fechar os 56 casos de falta acima da capacidade de interrupção do fusível analisado.** Identificar a proteção que cobre cada condição ou registrar a pendência de dimensionamento.

### P1, P3 e P4 · Mecânica, CAD e desempenho

- [ ] **I02, I03, I05, I14 e I18 · Revisar as hipóteses mecânicas.** Conferir distribuição de massa por eixo, transferência de carga em frenagem e capacidades dos pneus e eixos. Identificar a relação de transmissão **i = 10** como hipótese se ela continuar sem confirmação. Explicar **0,96 g** como limiar geométrico idealizado de levantamento da roda interna. Sustentar qualquer comparação com valores típicos com uma referência comparável.
- [ ] **I17 · Revisar vistas e fixações.** Usar vistas cotadas que se leiam como desenhos técnicos. Corrigir a figura em que o banco de 48 V aparece sobre a cama, verificar fixações e segurança da cama e substituir o relato de edição do CAD pelos critérios e verificações de projeto.
- [ ] **I19–I20 · Comparar CFD com e sem o conjunto fixo do teto.** Manter comparáveis malha, condições de contorno, configuração das rodas e área de referência. Explicar a hipótese de rodas paradas e o uso da área com espelhos. Mostrar a diferença em **CdA**, potência e kWh/km a 40 e 80 km/h. Considerar a massa dos portáteis recolhidos e, para avaliar retirar o teto solar, cruzar a economia de tração com a geração perdida. No rolamento, explicar a dissipação por deformação dos pneus e a origem do coeficiente.
- [ ] **I28 · Calcular o 0–100 km/h desconsiderando o limitador apenas no modelo.** Apresentar **0–90 km/h com a configuração de fábrica** e **0–100 km/h como estimativa teórica**, conferindo se a curva de torque e potência cobre a rotação necessária. A ficha Fiat da variante de 4.250 kg indica limitador de série de **90 km/h**. Para circulação no Brasil, citar o **art. 61 do CTB**, que dá prioridade à sinalização da via e estabelece **90 km/h para a categoria “demais veículos” em rodovias de pista simples ou dupla sem sinalização regulamentadora**. Identificar separadamente o limite de fábrica e a regra de trânsito.

### P2, P6 e P7 · Cabos e conforto térmico

- [ ] **I30 · Justificar os 489 A RMS.** Explicitar o ponto de operação que gera a corrente e conferir a capacidade do cabo nas condições reais de instalação consideradas. Explicar o método de volumes finitos junto ao fluxograma do balanço térmico.
- [ ] **I31–I32 · Preparar um memorial de fórmulas térmicas.** Definir símbolos, unidades e hipóteses. No ar-condicionado, explicar o **COP**, relação entre potência térmica removida e potência elétrica consumida, e mostrar a margem ou o déficit de capacidade para uma e duas pessoas.

## Ordem sugerida para integrar as mudanças

1. Fechar a entrada elétrica com a P2 e o perfil horário de consumo com a P6.
2. Incorporar o teto de 1.560 Wp e os horários de montagem na configuração usada pela P5. A comparação de portáteis no CAD e o CFD com e sem os painéis podem avançar em paralelo.
3. Se massa, CdA ou parâmetros de tração mudarem, atualizar primeiro o I26. Em seguida, rodar novamente I25 e I29 e revisar o I27 quando houver mudança em suas entradas.
4. Conferir que tabelas, gráficos, fluxogramas e texto usam a mesma versão do cenário.

## Referências para a revisão

- [Repositório STF_MotorHome](https://github.com/MHC-CodeSmith/STF_MotorHome), relatório, scripts e resultados por cenário.
- [Fiat Professional, ficha E-Ducato MY25, p. 3](https://www.fiat.sk/content/dam/fiat2023/sk/cenniky/2026/03/e_Ducato_pricelist_dodavka_200326.pdf), limitador da variante de 4.250 kg.
- [Código de Trânsito Brasileiro, art. 61](https://legis.senado.leg.br/norma/551379/publicacao/34619690), sinalização e velocidades máximas.
