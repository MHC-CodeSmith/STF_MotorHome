# Revisão geral do projeto motorhome elétrico solar

**Documento técnico para revisão do usuário — SEM0571/USP**  
**Referência:** resultados de 10/11/2026; fonte única de parâmetros `1.1.1-execucao1540`.  
**Cenário principal revisado:** `maxeon1540_independente`.  
**Base de código registrada:** commit técnico local `60541a0`; checkpoint documental `3f684d9`. Este documento e a correção A13 são posteriores a esses commits.

## 1. Parecer geral

**O conjunto de cálculos e simulações é aproveitável como estudo acadêmico condicionado. O projeto ainda não reúne evidência para ser considerado tecnicamente fechado, liberado para construção ou capaz de realizar fisicamente a missão solar de 7.000 km.**

Os **35 itens foram trabalhados e possuem evidências**; a cadeia integrada registra 17 comandos concluídos. Isso demonstra execução e integração numérica dentro das hipóteses, sem equivaler ao atendimento integral dos requisitos. Permanecem resultados restritos, dados OEM ausentes, verificações de instalação não concluídas e componentes sem compatibilidade de conjunto demonstrada. Nenhum item recebeu aprovação humana final.

O principal bloqueio é a **interface externa DC compatível e autorizada para receber energia solar na tração**. A arquitetura B está escolhida, mas não há demonstração de equipamento, tensão/corrente mínimas, protocolo, isolamento e operação com a potência FV variável. Um balanço de kWh favorável ou um buffer não resolve essa lacuna.

Este documento não é relatório acadêmico final, memorial de homologação ou certificado. Seu objetivo é permitir a revisão técnica do desenvolvimento já realizado e evitar aprovar hipóteses como se fossem evidências físicas.

## 2. O que esta revisão conferiu e o que não pôde reexecutar

Foram lidos os registros de execução, QA, matriz dos 35 itens, inventário de layouts, resultados de consumo, bancos, geração solar, missão, HVAC e BOM. As fontes primárias e hipóteses continuam rastreadas no YAML e nos documentos técnicos anteriores; não houve nova verificação dos sites dos fabricantes nesta revisão.

**Resultados da execução anterior, confirmados pela leitura dos arquivos:**

| Registro | Resultado registrado | Alcance |
|---|---|---|
| `output/testes_integracao1540_20261110.log` | 244 testes passaram em 5,28 s | Testes de software executados anteriormente |
| `output/ruff_integracao1540_20261110.log` | Sem apontamentos | Análise estática registrada anteriormente |
| QA da base em `entregas/desenvolvimento_2026-11-09/qa.json` | 422 controles, nenhum erro | Verificação dos artefatos do checkpoint anterior |
| QA do cenário em `entregas/integrado_maxeon1540/qa.json` | 331 controles, nenhum erro | Verificação numérica do cenário, sem missão física demonstrada |
| `execucao_pipeline.json` do cenário | 17 comandos com código de saída zero | `complete:true` significa cadeia executada, não projeto validado |

**Verificação adicional feita nesta revisão:** 21 conferências documentais e recálculos escalares em JavaScript passaram. Incluíram IDs e responsáveis dos 35 itens, ausência de aprovações inferidas, soma das cargas por eixo, margem de PBT, consumo a 40/80 km/h, balanço agregado dos oito melhores replays, estados iniciais, distância/tempo, comprimento do arranjo FV e dimensionamento dos bancos. O registro está em [verificacoes_documentais.json](../entregas/revisao_geral_2026-11-10/verificacoes_documentais.json).

**Limitação da sessão que produziu esta revisão (superada em 10/11/2026):** naquela execução, o terminal padrão falhou por erro de sandbox e a execução ampliada não foi autorizada; testes Python, solvers e Git ficaram pendentes naquele momento. Na continuidade posterior, shell e `.venv` voltaram a funcionar: 244 testes, Ruff, verificadores integrado/desenvolvimento, estrutura e auditoria foram reexecutados. A busca de fontes OEM CCS2 não trouxe nova evidência; interface DC segue sem comprovação.

A alteração documental de A13 descrita adiante muda o hash desse documento em relação ao manifesto global antigo. O manifesto foi preservado. Sua atualização e nova conferência ficam explicitamente pendentes; não se deve apresentar o antigo “PASSOU” como nova certificação de integridade da árvore atual.

## 3. Requisitos obrigatórios preservados

- Arquitetura **B**, exclusivamente por interface externa DC OEM autorizada; sem acesso direto ao pack, BMS ou cabos HV.
- Bancos de tração e serviços independentes. A antiga via bateria de serviços → inversor/EVSE/OBC → tração permanece descartada.
- Meta de 1.540 Wp fixos e 1.600 Wp portáteis; portáteis apenas estacionados, com orientação/inclinação fixas em cada parada.
- Serviços LiFePO₄ nominal de 48 V e rede AC de 220 V / 60 Hz. Capacidade final, integração e proteções ainda condicionadas.
- Missão principal de **7.000 km, plana, com velocidades constantes por execução, até 8 h dirigidas por dia**, ambas as baterias iniciando em 100%, sem eletricidade externa durante a missão.
- Dia acadêmico de São Carlos em 21 de junho, céu limpo, 25 °C, UR 50% e vento nulo, repetido como hipótese. Rota OSRM de aproximadamente 7.511 km e ERA5 permanecem complementares.
- Item 27 separado: 100%→30% como principal e 80%→30% como sensibilidade. A reserva final de 30% não é transferida ao item 29.
- Item 31 fechado, estacionado, sem pessoas e sem A/C; item 32 com 33 °C externos, 25 °C internos e um ocupante, com duas pessoas em complemento.
- Água limpa total inicial de 100 L, cinzas de 70 L e cassete de aproximadamente 20 L; sem tanque negro duplicado. Dois ocupantes de 80 kg e 60 kg de bagagem.
- Pneus, suspensão e arquitetura OEM preservados. Os ensaios térmicos a 20/80 kW não representam potência solar disponível.
- Nenhuma aprovação de compra, instalação, homologação ou validação física é inferida da DEC-061.

## 4. Configuração integrada e resultados principais

### 4.1 Veículo, massa e CAD

Variante de estudo: **Fiat E-Ducato L3H2 SK MY25 505.GG1.2**, PBT de 4.250 kg, tara OEM usada de 2.790 kg, 110 kWh brutos / 98 kWh úteis, 205 kW / 410 Nm de pico e limitador de 90 km/h. Esses valores pertencem à mesma variante; os mapas e limites não publicados não foram preenchidos com dados de outro mercado.

| Grandeza | Resultado do cenário de 1.540 Wp | Natureza |
|---|---:|---|
| Massa operacional | 3.976,53 kg | Estimativa integrada, não pesagem |
| Margem até o PBT | 273,47 kg | Diferença aritmética; não comprova margem por eixo |
| CG longitudinal / lateral / altura | 2,01780 / 0,00245 / 0,93071 m | Dependente do CG de base e das posições estimadas |
| Reação dianteira / traseira | 1.987,96 / 1.988,56 kg | Cargas estáticas calculadas; limites OEM por eixo ausentes |
| Água limpa inicial | 85 L no tanque + 15 L no boiler | Total preservado em 100 L |

O layout A é a recomendação provisória. O teste de caixas não encontrou colisões entre os envelopes verificados, mas não demonstra acesso a todos os terminais, fixação na chapa, drenagem, estanqueidade ou ergonomia real. O layout B permanece um comparador com acesso da lavadora 6 mm inferior à reserva necessária e armazenamento elevado de painéis portáteis.

### 4.2 Solar, controladores e serviços

A configuração usa dois módulos Maxeon de 380 W e dois de 390 W, totalizando **1.540 Wp e 76 kg**. O comprimento com afastamentos é 4,294 m; no retângulo estimado de 4,30 × 1,82 m sobram apenas 6 mm longitudinais além dos afastamentos já modelados. A curvatura e os apoios reais do teto não estão validados.

A tensão de circuito aberto no frio, com a tolerância considerada, é aproximadamente 171,48 V. Isso exclui o controlador de 150 V para esse arranjo. O par **250/60 para o teto + 150/60 para os portáteis** é um comparador com rastreadores independentes, não aprovação da topologia definitiva. O MPPT compartilhado continua em estudo: 72 casos com curvas I–V aproximadas indicam perdas de 0,657% a 27,272%. Nenhuma saída de MPPT de serviços foi tratada como carregador HV compatível.

O consumo médio de serviços é **7,2288 kWh/dia**, com picos analisados separadamente. O banco provisório é de três US5000, 14,4 kWh nominais e 119,1 kg. O inversor candidato é o MultiPlus-II GX 48/5000, com saída 220 V / 60 Hz configurável e monitoramento comercial incorporado. Isso não demonstra partidas, compatibilidade móvel, firmware/BMS, atuação de contatores ou coordenação das proteções.

| Autonomia sem sol / reserva de serviços | Módulos calculados | Energia nominal | Energia utilizável no critério |
|---|---:|---:|---:|
| 24 h / 20% | 2 | 9,6 kWh | 7,68 kWh |
| 24 h / 30% | 3 | 14,4 kWh | 10,08 kWh |
| 48 h / 20% | 4 | 19,2 kWh | 15,36 kWh |
| 48 h / 30% | 5 | 24,0 kWh | 16,80 kWh |

Os CADs das quatro quantidades e 12 casos do suporte do banco foram comparados. A folga e a retenção reais não estão demonstradas. A simulação de prioridades pode estender a alimentação retirando cozinha, boiler e lavanderia; isso **não atende ao perfil habitável completo por 48 h** e não altera silenciosamente o consumo da missão.

### 4.3 Consumo, autonomia e missão

| Resultado central | 40 km/h | 80 km/h |
|---|---:|---:|
| Consumo de tração | 0,22515 kWh/km | 0,40608 kWh/km |
| Rendimento de tração | 4,441 km/kWh | 2,463 km/kWh |
| I25, mínimo DC hipotético de 1 kW, somente tração | 51,49 km | 28,55 km |
| I25, mesma hipótese com serviços cíclicos | 27,19 km | 15,07 km |

Os valores de I25 vêm do despacho temporal com crédito solar inicial zero, uma parada seguida de condução e discretização de 5 min. Não são autonomia física demonstrada, nem devem ser confundidos com os limites energéticos de outro cálculo que não impõe a mesma política temporal.

No item 27, o controle sem reposição HV fornece aproximadamente **351,47 km para 100%→30%** e **251,05 km para 80%→30%**, a 20,69 km/h no ótimo restrito. A duração calculada não é uma escala operacional segura e não resolve a otimização com recarga solar fisicamente implementada.

Na grade de 1.008 políticas do item 29, com 700 W de auxiliares de tração estimados, os melhores resultados são:

| Reserva tração / serviços | Dias condicionais | Política na grade |
|---|---:|---|
| 10% / 20% | 243,84375 | 20 km/h, janela 20:00–04:00, até 8 h/dia |
| 20% / 30% | 244,88542 | Mesma velocidade e janela |

A resolução temporal é de 15 min; as casas decimais identificam o modelo, não precisão física. Esses resultados **não são mínimo global, previsão de viagem real ou recomendação de operação rodoviária**. A energia inicial é 112,4 kWh e deve ser distinguida da geração durante o percurso.

Foram registrados também 972 combinações de incerteza, 120 missões complementares, 36 ensaios energéticos diários de recarga direta/buffer e 32 comparações com buffer comercial dedicado. O buffer não foi incorporado à configuração-base; começa com crédito FV zero, não usa a bateria de serviços e não resolve autorização ou protocolo OEM.

A cronologia hídrica registra 8.004 eventos em oito replays, com 2.127 abastecimentos/descartes e conservação numérica. A disponibilidade geográfica de instalações e os tempos operacionais permanecem hipóteses.

### 4.4 CFD, térmica, fixações e custos

- **Aerodinâmica:** 101.030 / 128.458 / 217.494 células; Cd de diagnóstico 0,68313 / 0,66692 / 0,63374. Os resíduos convergiram, mas a variação final é de 5,23%. Parede, geometria equivalente e refinamento local impedem tratar um Cd como definitivo ou inventar GCI. A faixa de sensibilidade foi ampliada até 0,72.
- **Fixações:** 378 alternativas e 18 interfaces locais; inversor em plano vertical. Tanque com Tet4 e inversor com Tet10 atingem variação de deslocamento de aproximadamente 1,144% e 0,550%. Isso não valida contato, pré-carga, fadiga, arrancamento ou apoios OEM. Os 33,138 kg de chapas são comparação bruta, não acréscimo líquido automaticamente instalado.
- **Freios e cabos:** campos multidimensionais, balanços e sensibilidades existem. Corrente DC não substitui corrente de fase RMS; regeneração e materiais representativos não são dados OEM.
- **Cabine:** rede matinal e CFD 3D complementar foram executados. A média de 50,32 °C do complemento usa contornos congelados e não é uma simulação conjugada da manhã inteira no CAD real.
- **A/C:** carga calculada de aproximadamente 2.516 W para um ocupante e 2.646 W para dois. As margens sobre 2.700 W nominais são de 184 W e 54 W; não comprovam capacidade na condição de 33 °C externos / 25 °C internos. Partida, SKU e aparente conflito entre fusível de 5 A e corrente nominal de 6,2 A continuam abertos.
- **Proteções:** 144 faltas paramétricas, incluindo 56 acima de 20 kA. A declaração Pylontech de “<2.000 A / 1 ms” não fornece corrente prospectiva pré-BMS ou I²t total do fusível; não elimina esses casos automaticamente.
- **Custos:** 27 linhas, com US$ 1.951 de referências Victron, € 50.990 do veículo e R$ 439 históricos do cooktop, separados. **Não há custo total instalado em reais com impostos.** Somar moedas ou preencher preços ausentes não atenderia ao item 24.

## 5. Parecer individual dos 35 itens

“Calculado”, “simulado” e “comparado” abaixo descrevem a evidência disponível; não significam aprovação final. Todos os itens permanecem sem aceite humano.

| Item / responsável | Requisito | Parecer da revisão | Evidência entregue e limite para fechamento |
|---|---|---|---|
| 01 / P1 | Conceito e identidade | **Definido provisoriamente** | Aurora Solar, BEV para duas pessoas, sobre E-Ducato L3H2. A variante é de estudo; conversão e configuração final não homologadas. [Evidência](../entregas/integrado_maxeon1540/integracao/layouts_massas.json). |
| 02 / P1 | Pneus e rodas | **Parcial — dados OEM** | Configuração OEM preservada e efeito do rolamento calculado. Medidas, índices, pressões e massa da roda da variante exata não confirmados. [Evidência](../entregas/integrado_maxeon1540/integracao/dinamica_massa_integrada.csv). |
| 03 / P1 | Sistema de freios | **Condicionado** | Modelo de disco representativo e transferência dinâmica por eixo. Disco, pastilha, repartição e limites ABS OEM não demonstrados. [Evidência](../entregas/integrado_maxeon1540/freios_integrados/transferencia_carga_aderencia.csv). |
| 04 / P4 | Motor e mapas | **Parcial — dados OEM** | 205 kW e 410 Nm de pico; 36 envelopes de engenharia. Curvas reais por RPM, eficiência por ponto e potência contínua não disponíveis. [Evidência](../entregas/integrado_maxeon1540/mecanica_termica/I28_envelope_0_90_sensibilidade.csv). |
| 05 / P4 | Transmissão | **Condicionado** | Redutor preservado; relações e eficiência sensibilizadas. Relação real, rotação e lubrificante OEM não confirmados. [Evidência](../entregas/integrado_maxeon1540/mecanica_termica/I10_I12_balanco_perdas.csv). |
| 06 / P2 | Baterias | **Dimensionado provisoriamente** | Tração de 98 kWh úteis e banco de serviços de 14,4 kWh separados. Uso móvel, BMS, retenção e partidas dependem de validação do conjunto. [Evidência](../entregas/integrado_maxeon1540/integracao/inventario_massas.csv). |
| 07 / P2 | Fiação e proteção | **Parcial — instalação** | 324 circuitos DC, 144 curtos paramétricos e rotas de reserva. Ampacidade instalada, terminais, curto real, I²t, PE e DR não fechados. [Evidência](../entregas/integrado_maxeon1540/protecoes_fixacoes/resumo.json). |
| 08 / P5 | Painéis fotovoltaicos | **Integrado sob hipóteses** | 1.540 Wp fixos e 1.600 Wp portáteis em séries e CAD próprios. Teto real, curvatura, fixações, disponibilidade e alocação elétrica não demonstrados. [Evidência](../entregas/integrado_maxeon1540/solar/resumo.json). |
| 09 / P2 | Controladores e inversor | **Comparação executada** | GX 48/5000 e comparação 250/60 no teto + 150/60 nos portáteis. Eficiências por carga, comutação, proteção e interface DC externa não demonstradas. [Evidência](../entregas/integrado_maxeon1540/energia_sistemas/mppt_parecer.json). |
| 10 / P7 | Resfriamento elétrico | **Modelo condicionado** | Perdas de motor, inversor e redutor separadas e circuito parametrizado. UA, vazão, controle e correspondência com o circuito OEM não validados. [Evidência](../entregas/integrado_maxeon1540/mecanica_termica/I10_I12_balanco_perdas.csv). |
| 11 / P6 | Climatização e ventilação | **Condicionado** | 48 casos de ventilação natural, CO₂ e umidade; candidatos HVAC comparados. Sem vento e sem diferença térmica, o modelo prevê vazão nula; renovação não garantida. [Evidência](../entregas/integrado_maxeon1540/integracao/ventilacao_natural_co2_umidade.csv). |
| 12 / P7 | Lubrificação | **Parcial — dados OEM** | Escopo BEV esclarecido e perdas do redutor separadas. Óleo, volume, intervalo e pontos de lubrificação OEM permanecem desconhecidos. [Evidência](../entregas/integrado_maxeon1540/mecanica_termica/I10_I12_balanco_perdas.csv). |
| 13 / P6 | Equipamentos internos | **Integrado sob hipóteses** | Inventário, cargas médias, lavanderia, água e gerenciamento comparados. Partidas, atuadores e instalação veicular de todos os equipamentos não demonstrados. [Evidência](../entregas/integrado_maxeon1540/integracao/agua_operacao_14dias.csv). |
| 14 / P1 | Suspensão e direção | **Estática condicionada** | 162 cenários de massa, CG, reações e indicador lateral com suspensão OEM. Limites por eixo, curso e rigidez OEM; estabilidade dinâmica não validada. [Evidência](../entregas/integrado_maxeon1540/integracao/massa_cg_eixos_sensibilidade.csv). |
| 15 / P1 | Chassi e fixações | **Modelos locais executados** | 378 alternativas, 18 interfaces e 14 casos FEM 3D de tiras. Material e apoios reais do chassi, contato, fadiga e furação não demonstrados. [Evidência](../entregas/desenvolvimento_2026-11-09/fixacoes_redimensionadas/resumo.json). |
| 16 / P3 | Carroceria, portas e vidros | **CAD de envelopes** | Reservas geométricas e rotas, incluindo posição vertical do inversor. Geometria OEM, passagens, drenagem, estanqueidade e folgas reais faltam. [Evidência](../entregas/integrado_maxeon1540/rotas_instalacoes/layoutA_rotas_reserva.step). |
| 17 / P3 | CAD 3D e vistas | **Comparação executada** | Dois layouts, alternativas de teto e vistas cotadas. Layout B falha por 6 mm no acesso da lavadora; CAD A não é instalação certificada. [Evidência](../entregas/integrado_maxeon1540/integracao/A_fixa_vistas.png). |
| 18 / P1 | Massa com passageiros | **Calculado, não pesado** | 3.976,53 kg estimados; água total distribuída em 85 L no tanque e 15 L no boiler. CG de base e posições estimados; margens por eixo não comprovadas. [Evidência](../entregas/integrado_maxeon1540/integracao/inventario_massas.csv). |
| 19 / P3 | Cd e área frontal | **CFD com incerteza** | Três novas malhas equipadas, resíduos convergidos e históricos de forças. Variação final de Cd de 5,23%; sem independência de malha, GCI defensável ou Cd definitivo. [Evidência](../entregas/aero_equipado1540/incerteza_observada.json). |
| 20 / P4 | Rolamento | **Sensibilidade calculada** | Crr de 0,008 / 0,012 / 0,016 propagado ao consumo. Não representa ensaio dos pneus da variante escolhida. [Evidência](../entregas/integrado_maxeon1540/integracao/dinamica_massa_integrada.csv). |
| 21 / P4 | Forças resistivas | **Calculado sob hipóteses** | Arrasto e rolamento em 164 pontos, dois layouts e duas massas. Cd, Crr e densidade condicionados; plano e vento nulo. [Evidência](../entregas/integrado_maxeon1540/integracao/dinamica_massa_integrada.csv). |
| 22 / P4 | Potência versus velocidade | **Calculado sob hipóteses** | Potência nas rodas e na bateria; auxiliares de tração separados. 700 W de auxiliares são estimados, com sensibilidade de 0–1.500 W. [Evidência](../entregas/integrado_maxeon1540/integracao/dinamica_massa_integrada.csv). |
| 23 / P2 | Capacidade em kWh | **24/48 h comparados** | 2/3 módulos para 24 h e 4/5 para 48 h; quatro CADs e 12 casos de suporte. Folgas, rack, BMS e retenção reais não aprovados; capacidade final pendente. [Evidência](../entregas/integrado_maxeon1540/bancos_24_48_cad/resumo.json). |
| 24 / P1 | Custo em R$ com impostos | **Incompleto** | BOM de 27 linhas e preços rastreados por moeda. Orçamento instalado em BRL com impostos, frete e todos os componentes não fechado. [Evidência](../entregas/integrado_maxeon1540/bom_atual/resumo.json). |
| 25 / P5 | Autonomia solar do dia | **Condicional** | 630 MILP; curvas e resultados a 40/80 km/h com crédito solar inicial zero. Sessão DC hipotética; uma parada seguida de condução; sem ótimo global. [Evidência](../entregas/integrado_maxeon1540/despacho_i25/resumo.json). |
| 26 / P5 | Consumo em km/kWh | **Calculado sob hipóteses** | 4,441 km/kWh a 40 km/h; 2,463 km/kWh a 80 km/h na hipótese central. Tração separada dos serviços; eficiência e resistências não calibradas ao veículo real. [Evidência](../entregas/integrado_maxeon1540/energia_sistemas/I25_I26_autonomia_solar_consumo.csv). |
| 27 / P5 | Autonomia diária e SOC 30% | **Ótimo restrito** | 100%→30% e 80%→30%; velocidade, potência e SOC calculados. Controle sem reposição HV; não fecha a maximização com recarga solar implementável. [Evidência](../entregas/integrado_maxeon1540/energia_sistemas/I27_autonomia_otima_modelo_sem_HV.csv). |
| 28 / P4 | Velocidade máxima e 0–100 | **Resposta de limite definida** | Variante de estudo limitada a 90 km/h; 0–100 não alcançável. Estimativas de 0–90 não são curvas ou tempos declarados pelo fabricante. [Evidência](../entregas/integrado_maxeon1540/mecanica_termica/I28_envelope_0_90_sensibilidade.csv). |
| 29 / P5 | Menor tempo nos 7.000 km | **Busca finita condicional** | 1.008 políticas, replays, sensibilidades, buffer e água integrados. Menor valor da grade não é mínimo global; recarga física e postos não demonstrados. [Evidência](../entregas/integrado_maxeon1540/otimizacao_grade/resumo.json). |
| 30 / P2 | Campo térmico nos cabos | **Multidimensional condicionado** | Campos espaciais, malha e sensibilidade de cabos de serviços e referência HV. Corrente de fase RMS OEM desconhecida; corrente DC não pode substituí-la. [Evidência](../entregas/desenvolvimento_2026-11-09/cabos_HV_referencia/resumo_cabos.json). |
| 31 / P6 | Cabine fechada ao meio-dia | **Modelo e CFD complementar** | Rede matinal e CFD 3D transiente, três malhas e verificação de balanço. Contornos do CFD congelados; sem modelo conjugado do CAD real, mobiliário ou validação física. [Evidência](../entregas/desenvolvimento_2026-11-09/cabine_transiente/balanco_convergencia.json). |
| 32 / P6 | Potência térmica do A/C | **Dimensionamento condicionado** | 1/2 ocupantes: 2.516/2.646 W; 72 sensibilidades e 12 casos elétricos. Margem nominal pequena; capacidade real a 33 °C/25 °C, partida e revisão exata não comprovadas. [Evidência](../entregas/desenvolvimento_2026-11-09/hvac_revisao/resumo.json). |
| 33 / P1 | Campo térmico dos freios | **Multidimensional condicionado** | 24 casos 2D r–z, 30→10 m/s em 5 s, inicialmente 25 °C. Disco, material e regeneração OEM não confirmados; ensaio prescrito excede o limitador do veículo. [Evidência](../entregas/integrado_maxeon1540/freios_integrados/convergencia.csv). |
| 34 / P7 | Bateria em carga 20/80 kW | **Modelo parametrizado** | 54 casos elétricos/térmicos e balanço de energia. Dois nós, não pack OEM calibrado; R(SOC,T), geometria e limites reais não confirmados. [Evidência](../entregas/integrado_maxeon1540/mecanica_termica/I34_54sensibilidades.csv). |
| 35 / P7 | Bomba, radiador e vazão | **Modelo comercial condicionado** | Curva de bomba candidata, radiador 2D e ponto de operação. Não demonstra componentes ou curva hidráulica do circuito OEM real. [Evidência](../entregas/desenvolvimento_2026-11-09/arrefecimento/resumo_hidraulica.json). |

## 6. Achados de revisão e correções desta entrega

| ID | Achado | Tratamento / consequência |
|---|---|---|
| RG-01 | A13 ainda apresentava 290,875 / 292,885 dias do cenário anterior | **Corrigido documentalmente** para 243,84375 / 244,88542 dias do cenário de 1.540 Wp; os números antigos foram identificados como comparação de 1.350 Wp |
| RG-02 | “17 comandos concluídos” poderia ser entendido como projeto concluído | Parecer separa execução computacional, cumprimento do requisito, validação física e aceite humano |
| RG-03 | Alocação FV flexível do modelo não tem implementação elétrica demonstrada | Resultados de missão e I25 permanecem condicionais; MPPTs de serviços não foram promovidos a carregador HV |
| RG-04 | Item 27 tem solução de um controle sem reposição HV, não do problema geral com recarga solar implementável | Classificado como ótimo restrito; o requisito completo não foi marcado como encerrado |
| RG-05 | Cd residual convergido não é independência de malha ou validação | Mantida faixa e limitação de 5,23%; sem Cd definitivo ou GCI inventado |
| RG-06 | Banco que dura 48 h mediante retirada de cargas não atende ao perfil moderado completo por 48 h | Mantida comparação de 4/5 módulos para o perfil completo; cortes não favorecem silenciosamente I29 |
| RG-07 | PBT com margem não prova cargas admissíveis por eixo, retenção ou suspensão | Massa/CG tratados como estimativas; limites OEM e instalação continuam bloqueantes |
| RG-08 | QA antigo e testes passados não comprovam integridade de novas alterações documentais | Testes históricos identificados; alteração de A13 exige atualização legítima e nova conferência do manifesto quando o terminal voltar a funcionar |

A correção RG-01 não altera código, parâmetros físicos, replays ou registro DEC-001–061. Os recálculos adicionais desta revisão não substituem as verificações completas dos scripts.

## 7. Bloqueios para declarar fechamento técnico

| Prioridade | Bloqueio | Responsável | Evidência necessária para fechamento |
|---|---|---|---|
| Crítica | Interface solar → tração | P2, P4, P5 | Conjunto externo DC real: compatibilidade/autorização OEM, tensão, corrente/potência mínimas, comunicação, isolamento, comportamento intermitente e perdas |
| Crítica | Cargas e ancoragens da variante | P1, P3, P4 | Limites por eixo/pneus, posições e CG de base, apoios e furações documentados; análise da instalação correspondente |
| Alta | Proteção e comando dos serviços | P2, P6 | Curto real, I²t, ampacidade, PE/DR, terminais, partidas, BMS/firmware e atuação segura dos dispositivos comerciais |
| Alta | Instalação FV e layout | P3, P1, P2 | Medição do teto curvo, suportes/vedação/manutenção, fixação e armazenamento dos portáteis, rotas e acessos reais |
| Alta | HVAC e qualidade do ar | P6, P3, P2 | SKU e capacidade na condição prescrita, dutos/rejeição externa/condensado, partida e proteção; renovação e umidade verificadas |
| Alta | Requisitos de ótimo e modelos físicos | P5, P3, P4, P6, P7 | Escopo de otimização demonstrado; refinamento/validação proporcionais à finalidade e dados reais para substituir hipóteses críticas |
| Média | Orçamento instalado | P1 | Cotações dos componentes selecionados, instalação, frete, tributos e conversão monetária documentados |
| Operacional nesta sessão | Nova reprodução e integridade | Agente executor | Restabelecer o terminal/revisão automática; conferir os manifestos sem mascarar a mudança documental de A13 |

Não é necessário reabrir decisões já aprovadas ou pedir escolhas individuais para continuar estudos compatíveis. Também não é possível encerrar esses bloqueios apenas por aprovação do usuário: faltam evidências técnicas específicas.

## 8. Escolhas provisórias para a revisão do usuário

A **única lista de aprovações finais** permanece em [APROVACOES_FINAIS_PENDENTES.md](APROVACOES_FINAIS_PENDENTES.md), entradas A01–A16. Ela contém opções, recomendação provisória, fonte, impactos, dependências e necessidade de aceite. Esta revisão não cria uma segunda lista concorrente.

As recomendações de estudo são: manter a variante SK 505.GG1.2 e o layout A; usar o cenário Maxeon de 1.540 Wp para integração; manter três US5000 como referência de 24 h, comparando quatro/cinco para 48 h; conservar GX e os equipamentos comerciais já rastreados como candidatos condicionados. O comparador com dois rastreadores não encerra a DEC-054. Buffer não é parte instalada da configuração-base.

**Não há recomendação de aprovar a interface DC, a missão física, a instalação elétrica completa, as ancoragens OEM, um Cd definitivo ou um orçamento fechado com a evidência atual.**

## 9. Arquivos, reprodução e continuidade

| Conteúdo | Arquivo / pasta |
|---|---|
| Fonte única | [parametros_globais.yaml](../config/parametros_globais.yaml) |
| Cenário integrado e snapshots derivados | [integrado_maxeon1540](../entregas/integrado_maxeon1540/) |
| CFD equipado, campos e logs | [aero_equipado1540](../entregas/aero_equipado1540/) |
| Matriz individual e evidências | [REVISAO_TECNICA_EXECUCAO02.md](REVISAO_TECNICA_EXECUCAO02.md) |
| Rastreabilidade das 61 decisões | [MATRIZ_DECISOES_61.md](MATRIZ_DECISOES_61.md) |
| Bloqueios técnicos | [BLOQUEIOS_POS_DEC061.md](BLOQUEIOS_POS_DEC061.md) |
| Métodos e comandos executados | [EXECUCAO_TECNICA02.md](EXECUCAO_TECNICA02.md) |
| Plano de reprodução vigente | [PLANO_EXECUCAO_POS_DEC061.md](PLANO_EXECUCAO_POS_DEC061.md) |
| Nova conferência documental | [verificacoes_documentais.json](../entregas/revisao_geral_2026-11-10/verificacoes_documentais.json) |

Com o terminal disponível, os comandos de conferência são:

```bash
PYTHONPATH=src .venv/bin/python -m pytest -q
ruff check src scripts tests
MOTORHOME_SCENARIO=maxeon1540_independente PYTHONPATH=src .venv/bin/python scripts/verificar_cenario_integrado.py
PYTHONPATH=src .venv/bin/python scripts/verificar_desenvolvimento.py
```

Após revisar a correção de A13, a regeneração legítima do manifesto global deve usar o procedimento `--registrar` documentado, seguida de nova execução sem essa opção. Não se deve alterar hashes históricos para simular aprovação. Novas simulações exigem a mesma configuração e destinos de CFD que preservem tentativas anteriores.

Os commits técnicos e de checkpoint continuam locais conforme o último estado registrado. **Não houve commit ou push nesta sessão**, pois o terminal não pôde ser utilizado. A autorização pendente de publicação não é suprida por este pedido de revisão. O relatório novo e a correção documental foram escritos localmente pelas ferramentas de arquivo.

## 10. Decisão de revisão

**Parecer:** aceitar o desenvolvimento entregue como base computacional rastreável para revisão e continuidade; **não encerrar o projeto como tecnicamente validado**.

A conclusão possível com os arquivos atuais é que há resultados numéricos coerentes e estudos substanciais para os 35 itens. Ainda não está demonstrado que o conjunto satisfaz integralmente o enunciado, que a montagem é compatível com a variante OEM ou que a missão solar pode ser executada fisicamente. Os itens 2, 4, 12 e 24 possuem lacunas documentais explícitas; os itens 19, 27 e 29 têm limites de convergência ou de otimização que precisam permanecer visíveis. A ausência de aprovação humana é adicional a essas lacunas, não a causa delas.


## Atualização técnica posterior — refinamento local de I29

O I29 recebeu uma busca adicional de velocidade, reproduzível por `PYTHONPATH=src .venv/bin/python scripts/refinar_velocidade_missao.py`. Ela fixa a janela líder 20:00–04:00, mantém montagem/recolhimento, reservas, consumo de serviços e as hipóteses físicas do cenário; varre 10–90 km/h em passos de 1 km/h e refina localmente em 0,1 km/h. Não reotimiza início/janela, não prova ótimo global e depende da interface DC direta hipotética de 1 kW.

Para 700 W de auxiliares estimados: 10/20% resultou em 20,4 km/h e 242,8854167 dias, ante 20 km/h e 243,84375 dias na grade original; 20/30% resultou em 19,8 km/h e 244,8854167 dias, igual à resolução temporal do melhor da grade. Os resultados e os 796 pontos estão em `entregas/integrado_maxeon1540/otimizacao_refinada_velocidade/`; erro máximo de conservação observado: 4,18×10⁻⁹ kWh. Não são previsão física da viagem nem demonstração da interface/autorizações.

A varredura inicial do novo script carregou por engano o cenário padrão de 1.350 Wp. Esse artefato foi removido antes de uso; a execução final define explicitamente `MOTORHOME_SCENARIO=maxeon1540_independente` e grava o cenário/hash de configuração no resumo e na entrada por executor.
