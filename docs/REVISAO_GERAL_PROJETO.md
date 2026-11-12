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

**Limitação da sessão que produziu esta revisão (superada em 10/11/2026):** naquela execução, o terminal padrão falhou por erro de sandbox e a execução ampliada não foi autorizada; testes Python, solvers e Git ficaram pendentes naquele momento. Na continuidade posterior, shell e `.venv` voltaram a funcionar: 244 testes, Ruff, verificadores integrado/desenvolvimento, estrutura e auditoria foram reexecutados. Pesquisa primária posterior confirmou somente capacidades máximas públicas para mercados/anos específicos; não confirmou limites mínimos, handshake, faixa operacional, compatibilidade FV variável ou autorização OEM para a variante brasileira MY25. A interface DC segue sem comprovação.

Naquela revisão, a alteração documental de A13 ainda não tinha sido registrada no manifesto. Estado atualizado em 11/11/2026: o registro de hashes foi executado pelo verificador oficial, seguido de conferência sem `--registrar`; a verificação atual passou com 181 entradas e 1.258 saídas, sem converter o resultado em validação física.

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
| 10% / 20% | 243,84375 | Grade histórica de 1.008 políticas; 20 km/h, janela 20:00–04:00 |
| 20% / 30% | 244,88542 | Grade histórica de 1.008 políticas; mesma velocidade e janela |

Atualização posterior: o refinamento de velocidade com janela fixa 20:00–04:00 percorreu 796 pontos e encontrou 242,885417 dias a 20,4 km/h (reserva 10/20%) e 244,885417 dias a 19,8 km/h (20/30%); essa resolução substitui a leitura simplificada de 20 km/h da grade histórica para esse comparador, sem trocar o resultado histórico. A busca densa distinta de 5.268 pontos, com partidas variáveis, encontrou 242,802083/244,802083 dias; o refino local extra não melhorou esses tempos. A análise posterior de 294 políticas a 15/5/1 min encontrou 242,802083/244,802083; 248,763889/250,760417; e 248,784028/250,779861 dias, respectivamente. As diferentes buscas e métodos ficam lado a lado para rastreabilidade: são resultados de grades finitas, locais e condicionais à interface DC de 1 kW hipotética, sem ótimo global ou viabilidade física demonstrada.

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
| 11 / P6 | Climatização e ventilação | **Condicionado com fallback sensibilizado** | Aos48 casos de ventilação natural somam-se648 sensibilidades mecânicas e16 casos integrados à autonomia/gestão do banco de serviços, mantendo o ventilador como carga essencial não cortada. No balanço estacionário de estudo (18 L/h·pessoa, exterior420 ppm, alvo1000 ppm), duas pessoas requerem62,1 m³/h;30 m³/h implicariam1620 ppm. A50 Pa/20% de eficiência, potência estimada4,31 W e carga sensível166 W para ΔT=8 K. Não é norma, escolha de ventilador ou projeto instalado; calor latente permanece sem cálculo por falta de umidade exterior/interior. [Evidência](../entregas/integrado_maxeon1540/ventilacao_mecanica_sensibilidade/resumo.json). |
| 12 / P7 | Lubrificação | **Parcial — dados OEM** | Escopo BEV esclarecido e perdas do redutor separadas. Óleo, volume, intervalo e pontos de lubrificação OEM permanecem desconhecidos. [Evidência](../entregas/integrado_maxeon1540/mecanica_termica/I10_I12_balanco_perdas.csv). |
| 13 / P6 | Equipamentos internos | **Integrado sob hipóteses** | Inventário, cargas médias, lavanderia, água e gerenciamento comparados. Partidas, atuadores e instalação veicular de todos os equipamentos não demonstrados. [Evidência](../entregas/integrado_maxeon1540/integracao/agua_operacao_14dias.csv). |
| 14 / P1 | Suspensão e direção | **Estática condicionada** | 162 cenários de massa, CG, reações e indicador lateral com suspensão OEM. Limites por eixo, curso e rigidez OEM; estabilidade dinâmica não validada. [Evidência](../entregas/integrado_maxeon1540/integracao/massa_cg_eixos_sensibilidade.csv). |
| 15 / P1 | Chassi e fixações | **Modelos locais executados** | 378 alternativas, 18 interfaces e 14 casos FEM 3D de tiras. Material e apoios reais do chassi, contato, fadiga e furação não demonstrados. [Evidência](../entregas/desenvolvimento_2026-11-09/fixacoes_redimensionadas/resumo.json). |
| 16 / P3 | Carroceria, portas e vidros | **CAD de envelopes** | Reservas geométricas e rotas, incluindo posição vertical do inversor. Geometria OEM, passagens, drenagem, estanqueidade e folgas reais faltam. [Evidência](../entregas/integrado_maxeon1540/rotas_instalacoes/layoutA_rotas_reserva.step). |
| 17 / P3 | CAD 3D e vistas | **Comparação executada** | Dois layouts, alternativas de teto e vistas cotadas. Layout B falha por 6 mm no acesso da lavadora; CAD A não é instalação certificada. [Evidência](../entregas/integrado_maxeon1540/integracao/A_fixa_vistas.png). |
| 18 / P1 | Massa com passageiros | **Calculado, não pesado** | 3.976,53 kg estimados; água total distribuída em 85 L no tanque e 15 L no boiler. CG de base e posições estimados; margens por eixo não comprovadas. [Evidência](../entregas/integrado_maxeon1540/integracao/inventario_massas.csv). |
| 19 / P3 | Cd e área frontal | **CFD parcialmente convergido, sem independência** | Malha 1.034.158 passou `checkMesh` mas não residualControl; grading 2 (743.286) terminou 1.800 passos sem convergir (p inicial 1,145e-4); grading 4 (510.281) convergiu em 505 iterações. Cd diagnóstico 0,60051 / 0,64287 / 0,70047; grading 2/base difere7,05%, grading 4/base16,65%. y+ médio solo≈1.146/913, teto FV229/255, carroceria262/261; parede/grade inadequadas para Cd representativo. Malhas não aninhadas, sem GCI, independência ou validação física. [Comparação](../entregas/aero_equipado1540/comparacao_malhas_adicionais.json). |
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
| 32 / P6 | Potência térmica do A/C | **Dimensionamento condicionado, ventilação acoplada** | Com o fluxo I32 existente de30m³/h, demanda1/2 ocupantes=2.516/2.646W; sob o fluxo de CO₂ calculado para duas pessoas (62,07m³/h), incluídas cargas sensível e latente psicrométricas, a demanda sobe a2.867W. Margens condicionais: −167W contra alegação nominal2700W e−1.109W contra campo oficial estruturado1758W. Condições/placa do produto e capacidade real a33/25°C, partida e instalação não comprovadas. [Evidência](../entregas/integrado_maxeon1540/ventilacao_mecanica_sensibilidade/resumo.json). |
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
| RG-08 | QA antigo e testes passados não comprovam integridade de novas alterações documentais | Resolvido para o estado registrado em 10/11: atualização oficial de hashes seguida de verificações sem registro. Qualquer alteração posterior ainda exige nova conferência |

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
| Operacional naquela sessão (resolvido em 11/11/2026) | Nova reprodução e integridade | Agente executor | Shell disponível; testes e verificadores reexecutados; hashes atualizados pelos registradores previstos e conferidos em seguida |

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

Comandos reexecutados nesta continuidade (11/11/2026):

```bash
PYTHONPATH=src .venv/bin/python -m pytest -q
ruff check src scripts tests
MOTORHOME_SCENARIO=maxeon1540_independente PYTHONPATH=src .venv/bin/python scripts/verificar_cenario_integrado.py
PYTHONPATH=src .venv/bin/python scripts/verificar_desenvolvimento.py
```

A verificação de 11/11/2026 usou `verificar_cenario_integrado.py --registrar` seguido da conferência sem registro, e o mesmo procedimento para `verificar_desenvolvimento.py`. Não foram alterados hashes históricos nem parâmetros canônicos. As duas conferências passaram; isto registra integridade computacional, não aprovação física.

**Estado deste checkpoint documental (substituído pela continuação de 11/11):** na revisão anterior, as alterações ainda não estavam commitadas nem sincronizadas. O estado posterior e verificável da implementação, testes e Git está registrado no fim de `docs/RETOMADA_COMPACTA.md`.

## 10. Decisão de revisão

**Parecer:** aceitar o desenvolvimento entregue como base computacional rastreável para revisão e continuidade; **não encerrar o projeto como tecnicamente validado**.

A conclusão possível com os arquivos atuais é que há resultados numéricos coerentes e estudos substanciais para os 35 itens. Ainda não está demonstrado que o conjunto satisfaz integralmente o enunciado, que a montagem é compatível com a variante OEM ou que a missão solar pode ser executada fisicamente. Os itens 2, 4, 12 e 24 possuem lacunas documentais explícitas; os itens 19, 27 e 29 têm limites de convergência ou de otimização que precisam permanecer visíveis. A ausência de aprovação humana é adicional a essas lacunas, não a causa delas.


## Atualização técnica posterior — refinamento local de I29

O I29 recebeu uma busca adicional de velocidade, reproduzível por `PYTHONPATH=src .venv/bin/python scripts/refinar_velocidade_missao.py`. Ela fixa a janela líder 20:00–04:00, mantém montagem/recolhimento, reservas, consumo de serviços e as hipóteses físicas do cenário; varre 10–90 km/h em passos de 1 km/h e refina localmente em 0,1 km/h. Não reotimiza início/janela, não prova ótimo global e depende da interface DC direta hipotética de 1 kW.

Para 700 W de auxiliares estimados: 10/20% resultou em 20,4 km/h e 242,8854167 dias, ante 20 km/h e 243,84375 dias na grade original; 20/30% resultou em 19,8 km/h e 244,8854167 dias, igual à resolução temporal do melhor da grade. Os resultados e os 796 pontos estão em `entregas/integrado_maxeon1540/otimizacao_refinada_velocidade/`; erro máximo de conservação observado: 4,18×10⁻⁹ kWh. Não são previsão física da viagem nem demonstração da interface/autorizações.

A varredura inicial do novo script carregou por engano o cenário padrão de 1.350 Wp. Esse artefato foi removido antes de uso; a execução final define explicitamente `MOTORHOME_SCENARIO=maxeon1540_independente` e grava o cenário/hash de configuração no resumo e na entrada por executor.

Uma busca subsequente permitiu variar também a hora de partida, mantendo janela diária de condução em 8 h e os demais pressupostos. `scripts/otimizar_janela_missao.py --densa` avaliou 3.936 combinações na grade de partida 2 h/velocidade 2 km/h e 1.332 pontos de refinamento local (partida 0,5 h/velocidade 0,2 km/h), totalizando 5.268. O resultado está em `entregas/integrado_maxeon1540/otimizacao_janela_missao_densa/`; a grade reduzida anterior, em `.../otimizacao_janela_missao/`, contém 648 pontos e é preservada separadamente.

Com 700 W de auxiliares estimados e interface DC hipotética: reserva 10/20% encontrou 20,8 km/h, partida 18:00 e 242,802083 dias; reserva 20/30% encontrou 20,0 km/h, partida 18:00 e 244,802083 dias. A janela permanece 8 h; o passo temporal do balanço é 15 min. Erro máximo de energia na busca densa: 2,89×10⁻⁸ kWh. Em 0 W, o melhor ponto da faixa fica no limite inferior de 10 km/h, devendo ser lido como resultado condicionado à borda, não como ótimo interior. A busca é finita com refinamento local, não prova ótimo global, e não reotimiza todas as dimensões continuamente. As diferenças de aproximadamente 2 h frente ao refinamento anterior de janela fixa vêm da partida variável. Nada demonstra viabilidade física, compatibilidade DC/OEM ou logística de paradas.

## Atualização técnica posterior — envelope de cargas por eixo

Para aprofundar o item 14 sem inventar limites OEM, `scripts/resumir_envelope_eixos.py` pós-processa a grade fatorial existente (2 layouts × 3 fatores de massa × 3 frações traseiras OEM assumidas × 3 alturas CG assumidas × 3 distribuições de água = 162 casos). A saída reproduzível está em `entregas/integrado_maxeon1540/integracao/envelope_cargas_eixos/`.

Na grade finita, as cargas dianteiras abrangem 1.737,2–2.223,1 kg no layout A e 1.756,2–2.242,9 kg no B; traseiras, 1.698,5–2.294,3 kg no A e 1.693,1–2.292,5 kg no B. A margem mínima calculada ao PBT de 4.250 kg é 163,4 kg (A) e 144,5 kg (B). A análise balanceada de efeitos principais atribui à fração traseira base assumida 98,2%/86,5% da soma de quadrados das cargas dianteira/traseira do A, e 98,1%/85,9% no B; fator de escala de massas responde pela maior parte restante. Altura do CG não muda a reação estática longitudinal neste modelo, embora afete o indicador geométrico lateral. Estas proporções descrevem apenas a grade enumerada, não probabilidades nem incerteza estatística.

O resultado reforça que obter distribuição OEM por eixo e pesar o conjunto instalado têm maior valor que refinar mais casas decimais do layout: sem limites admissíveis por eixo, a conformidade permanece indeterminada mesmo quando todos os pontos ficam abaixo do PBT. O modelo não inclui transferência dinâmica de carga, curso/rigidez de suspensão, frenagem/curva real ou certificação.

**Reconciliação de estado documental:** a limitação de terminal da primeira sessão foi superada e a verificação do manifesto já passou após registro deliberado do hash A13, com 179 entradas e 1.257 saídas; as frases anteriores de RG-08/§9 que ainda diziam “pendente” são históricas e não descrevem o estado atual. Os testes e verificações foram reexecutados novamente nesta continuidade: 244 testes, Ruff, verificador integrado e verificador de desenvolvimento passaram. Isso comprova integridade computacional dentro dos controles, não validação física.


## Atualização técnica posterior — HVAC e perguntas acadêmicas (11/11/2026)

O executável `scripts/comparar_hvac_revisoes.py` foi rodado novamente: 72 sensibilidades térmicas e 12 sensibilidades elétricas; resultados em `entregas/desenvolvimento_2026-11-09/hvac_revisao/`. A página oficial Dometic do FreshWell SKU 9105306675 mostra simultaneamente headline 2700 W/9200 BTU/h e campo estruturado ISO5151 1758 (ao lado, 5998.54 BTU/h; a unidade desse campo foi interpretada por conversão, não declarada claramente). A divergência não foi resolvida. Para demanda modelada de 2515,90/2645,90 W, a margem nominal fica +184,10/+54,10 W se prevalecer 2700 W, ou −757,90/−887,90 W se 1758 W for a capacidade comparável. São comparações nominais: capacidade efetiva a 33 °C externa/25 °C interna e instalação não foram demonstradas.

O FreshJet FJX7 3000 (3000 W ISO5151, massa 36,8 kg, envelope 1,09×0,70 m) consta apenas como comparador. O retângulo de teto e a área fotovoltaica são aproximações; não se declara incompatibilidade geométrica como fato. Nenhum aparelho foi selecionado ou trocado. As duas fontes primárias foram acrescentadas ao catálogo e a trilha de cálculo está no resumo/CSV HVAC.

A limitação de terminal descrita na primeira versão desta revisão era daquele turno e já foi superada: o shell desta continuidade funciona. O histórico de indisponibilidade permanece apenas como histórico, não como bloqueio atual. Nesta continuidade, pytest (244), Ruff, os dois verificadores e `git diff --check` foram executados; os manifestos foram atualizados pelo `--registrar` oficial e as conferências sem registro passaram. Após o complemento P6, QA de desenvolvimento: 186 entradas e 1.297 saídas; missão física não demonstrada e etapa técnica continua aberta.

Perguntas técnicas para o professor (I29 e interface DC, eixos, CFD, HVAC e critério de evidência física) foram preparadas em `PERGUNTAS_PARA_PROFESSOR.md`. Não se alteraram DEC-001–DEC-061 nem os parâmetros canônicos.


## Atualização I29 — refinamento local extra (11/11/2026)

Foi executado `scripts/otimizar_janela_missao.py --refino-extra`, acrescentando286 pontos locais e6sensibilidades auxiliares próximos/na política dos candidatos de700W com passos de0,1h na partida e0,1km/h na velocidade. Passo energético continua15min. Melhores pontos locais: reservas10/20%,17,9h e20,7km/h,242,802083dias; reservas20/30%,17,9h e20,0km/h,244,802083dias. Não houve redução do tempo frente aos melhores da busca densa; os empates refletem uma função objetivo discretizada pela simulação de15min, portanto velocidade e partida reportadas não devem ser interpretadas com precisão física decimal. Erro energético máximo nos candidatos líderes é aproximadamente1,21×10⁻⁹kWh. Arquivos em `entregas/integrado_maxeon1540/otimizacao_janela_missao_refino_extra/`. Busca local finita, interfaceDC1kW hipotética, sem prova de ótimo global nem viabilidade física.

## I29 — sensibilidade à resolução temporal (11/11/2026)

Foi criado `scripts/refinar_resolucao_missao.py` para reavaliar uma vizinhança de partida/velocidade a passos de 15, 5 e 1 minuto. Foram avaliadas 294 combinações locais: 98 por resolução, com partida 17,5–19,0 h, velocidade 19,6–20,8 km/h, reservas 10/20% ou 20/30% e auxiliares de tração assumidos de 700 W. Saídas reproduzíveis: `entregas/integrado_maxeon1540/otimizacao_resolucao_temporal/{resumo.json,candidatos.json}`.

| Passo | Reserva 10/20% | Reserva 20/30% |
|---|---|---|
| 15 min | 242,802083 d; 18:00; 20,8 km/h | 244,802083 d; 18:00; 20,0 km/h |
| 5 min | 248,763889 d; 17:45; 20,6 km/h | 250,760417 d; 17:45; 20,4 km/h |
| 1 min | 248,784028 d; 17:45; 20,8 km/h | 250,779861 d; 17:45; 20,6 km/h |

O resultado local de 1 min fica a aproximadamente 29 min do de 5 min, enquanto os tempos de 15 min são cerca de 6 dias menores. A mudança revela sensibilidade material à forma como o limiar mínimo de 1 kW é aplicado por intervalo e impede interpretar o resultado de 15 min como estável em resolução temporal. O balanço energético máximo observado foi `7,40×10⁻⁹ kWh`. Esta é uma comparação finita local, limitada às faixas indicadas; não prova ótimo global. As três resoluções mantêm arquitetura B, interface DC hipotética, e nenhuma viabilidade física/OEM é inferida. A verificação dedicada agora confere os 294 casos, os seis líderes, os balanços e esses limites.

## Itens 21/22 — força resistiva com rampa e vento (11/11/2026)

O novo `scripts/sensibilizar_resistencias_rota.py` expande o modelo de velocidade constante para rolamento, componente gravitacional da rampa e arrasto pelo vento relativo ao veículo. A grade contém **8.100 casos** (massa típica do cenário e PBT; 10/20/40/60/80/90 km/h; declives e aclives de 3/6%; vento longitudinal de −10 a +10 m/s; três valores cada de Crr, Cd e densidade do ar). Usa eficiência agregada central de 0,90 e auxiliares de tração estimados em 700 W. Não altera a missão I29 plana nem os parâmetros canônicos.

Para massa típica do cenário (3.976,526 kg), 40 km/h, Crr=0,012, Cd=0,62487678, densidade=1,10 kg/m³, eficiência=0,90 e auxiliares=700 W, o consumo estimado é 0,2252 kWh/km em plano; 3% e 6% de aclive isolados elevam-no a aproximadamente 0,5860 e 0,9458 kWh/km. A força de rolamento é projetada pela inclinação (`Crr·m·g·cos(θ)`). Em plano, vento frontal de 5 e 10 m/s resulta em 0,2949 e 0,3902 kWh/km. O maior pedido mecânico positivo da grade é 140,258 kW nas rodas (PBT, 90 km/h, 6% aclive, 10 m/s de vento frontal, resistências altas); isso não é comparação direta com potência de eixo do motor. O extremo de descida/vento de cauda gera 45,806 kW de demanda mecânica de frenagem; nenhuma regeneração é creditada.

Saídas: `entregas/integrado_maxeon1540/dinamica_resistiva_sensibilidade/envelope_grade_vento.csv` e `resumo.json`. A grade é análise de sensibilidade, não distribuição de rota nem previsão de alcance. Não inclui aceleração, mapas OEM, curva contínua, limites de pneus/eixos, transientes térmicos ou calibração; vento, rampa e coeficientes são hipóteses explicitamente enumeradas.

## Pesquisa primária de recarga DC — escopo e lacunas (11/11/2026)

Consulta às páginas oficiais Stellantis/Fiat Professional encontrou apenas limites máximos anunciados para contextos distintos: o lançamento do E-Ducato 2024 informa até 150 kW DC ([Stellantis Media](https://www.media.stellantis.com/uk-en/fiat-professional/press/fiat-professional-unveils-the-new-lineup-a-new-generation-at-work)); a comunicação de atualização da gama a partir de 1/5/2025 afirma OBC AC de 22 kW padrão e carga 0–80% em 55 min a 150 kW DC ([Stellantis Media](https://www.media.stellantis.com/uk-en/corporate/press/stellantis-announces-key-updates-to-large-van-line-up)). Nenhuma página consultada fornece faixa DC, corrente/tensão mínimas, handshake aplicável, suporte a fonte FV variável, arquitetura de isolamento, condições detalhadas do 0–80% ou autorização de adaptação para a unidade MY25 brasileira estudada. Os anúncios não provam sequer a especificação da variante nacional; não se inferiu compatibilidade CCS2 nem capacidade de carga em 1 kW. A arquitetura B e os resultados I29 que presumem essa interface permanecem hipóteses de estudo, sem viabilidade física demonstrada. Consulta efetuada em 11/11/2026; a lacuna exige documentação da variante e confirmação formal do fabricante/representante.

## Complemento P3 — solver convergido em uma variante, CFD ainda inconclusivo (11/11/2026)

O caso de 1.034.158 células foi continuado por 4.270,6 s até 1200 passos sem `residualControl`; Cd=0,60051043 é diagnóstico. A malha `simpleGrading (1 1 4)`, 510.281 células, passou `checkMesh` e SIMPLEC convergiu em505 iterações: Cd=0,70046995, span/50=0,0118%, continuidade3,10e-9. A terceira malha `simpleGrading (1 1 2)`, 743.286 células, passou `checkMesh` e chegou ao passo1800 em4.419,0s; não convergiu (Uy inicial6,78e-5 e p1,145e-4). Cd diagnóstico0,64286538, span/50=0,0190%, continuidade−3,50e-8. Os y+ médios no solo/teto/carroceria foram1.145,9/228,6/262,3. As diferenças contra a malha1 são7,05% (grading2) e16,65% (grading4). Na malha grading4, y+ médio foi aproximadamente 913 no solo, 255 no teto FV e 261 na carroceria, com máximos de4.963/1.059/1.705; na grading2, médias1.146/229/262 e máximos8.615/744/1.608. A resolução de parede permanece inadequada para assumir Cd representativo. Uma malha com fator de gradiente 20 falhou `checkMesh`; a tentativa de três camadas prismáticas excedeu o limite de geração antes da verificação. Nenhum Cd é selecionado/validado e não há GCI nem validação física. Detalhes e logs em [EXECUCAO_TECNICA02.md](EXECUCAO_TECNICA02.md) e em `entregas/aero_equipado1540/`.

## Proveniência dos artefatos da entrega histórica (11/11/2026)

A auditoria apontou que quatro arquivos do pacote datado `entregas/parcial_2026-10-24/` citam versões anteriores de configurações/código. Os artefatos e o manifesto assinado por hash continuam preservados como snapshot histórico. A auditoria não deve apresentá-los como resultados atuais; a conferência vigente é pelos manifestos integrado e de desenvolvimento, reexecutados após estas alterações. Nenhum hash histórico foi reescrito para remover divergência.

## Atualização OEM documental — 12/11/2026

Foi conferida novamente a fonte primária do cenário SK MY25 preservada no repositório de referências e comparada com a ficha técnica Fiat Professional Poland, edição 06/2024. A ficha SK MY25 confirma `505.GG1.2`, L3H2/4.250 kg, 2.790 kg em ordem de marcha sem motorista, bateria 110/98 kWh, 400 V, 205 kW/410 Nm, limitador 90 km/h, AC embarcado 11 kW, Combo CCS2 e máximo DC de 150 kW. Ela não publica limites por eixo. A ficha oficial polonesa MY24 relaciona o mesmo código à classe L3H2/4,25 t, mas informa 110,6/108 kWh e limites máximos de eixo 2.100/2.400 kg; é comparador de outra edição/mercado e não substitui os dados SK MY25. O comunicado britânico que altera AC para 22 kW a partir de maio de 2025 é também específico daquele mercado/oferta.

Aplicar os limites de eixo poloneses, apenas como triagem condicional, às 162 cargas da grade existente resulta em 54 casos acima de 2.100 kg no eixo dianteiro (27 por layout) e nenhum acima de 2.400 kg no traseiro. A excedência dianteira máxima é 142,9 kg no layout B; no A, 123,1 kg. Nenhum resultado autoriza afirmar reprovação da variante SK: os limites ainda não foram confirmados para ela, e a grade é hipotética e estática. O ponto-base anterior fica abaixo de ambos os limites comparativos, com margens de 112,0 kg dianteira e 411,4 kg traseira. Referências, reprodução e distinções de escopo estão em [Dados OEM do E-Ducato](DADOS_OEM_EDUCATO_FONTES.md).

Uma publicação oficial UK MY25.5 agora também lista eixos de 2.100/2.400 kg para L3H2 elétrico 4.250 kg, reforçando esses números somente como comparadores europeus. A mesma lista UK apresenta teto uniformemente carregado de 150 kg para L3, enquanto a tabela Poland MY24 indica 0 kg para L3H2 N2 elétrico 4,25 t. A divergência de variante/mercado/ano impede atribuir limite de teto à SK MY25. O conjunto de painéis e suportes estimado em 97,655 kg deixa margem aritmética de 52,345 kg apenas se o teto de 150 kg fosse aplicável; a aplicabilidade e as cargas locais/fixações não foram provadas.

Stellantis também documenta e-PTO 400 V/6,5 kW em certas ofertas e uso da bateria de tração para alimentar conversões. A direção documentada é saída da bateria de tração, não entrada solar para carregá-la. Não resolve a interface DC da arquitetura B e não foi incorporado; usar para alimentar serviços conflitaria com DEC-020. O comparador UK lista 272 PS, não os 205 kW da ficha SK MY25.

A triagem dos eixos permanece 54/162 acima do limite dianteiro comparativo e 0/162 acima do traseiro. Os 108 casos que passam ambos os limites estão sob distribuições traseiras assumidas de 0,42 ou 0,50; nenhum caso com hipótese 0,35 passa. É sensibilidade às hipóteses do envelope, não evidência probabilística ou conformidade. Os links oficiais, resultados por layout e reprodução estão em [Dados OEM do E-Ducato](DADOS_OEM_EDUCATO_FONTES.md).

O comparativo MY24 ainda evidencia diferença de energia líquida publicada (108 kWh) contra os 98 kWh da ficha SK MY25. Não atualizei o YAML nem recalculei missões com a capacidade de outro mercado. Mantêm-se sem evidência: variante efetivamente homologada no Brasil, limites por eixo/carga de teto exatos para SK MY25, mínimos/protocolo/interface externa DC e autorização OEM. Nada nesta consulta demonstra compatibilidade física da hipótese de 1 kW.

### Transferência longitudinal de carga na frenagem — 12/11/2026

Para aprofundar o P1 sem presumir dados de freio/ABS, a grade existente de 162 massas e CGs foi expandida por uma relação quase estática em piso nivelado: `ΔF = m·a·h/L`, com entre-eixos de 4,035 m e alturas/posições de CG de cada caso. O script `scripts/calcular_envelope_frenagem_eixos.py` gera 972 combinações para 0–0,5 g em passos de 0,1 g, preservando fatores de massa, fração traseira assumida, CG e água. O balanço entre reações dianteira/traseira conserva a massa com erro máximo inferior a 1e-12 kg.

Contra os comparadores britânicos de 2.100/2.400 kg (não confirmados para SK MY25), o número de casos acima do comparador dianteiro sobe de 54/162 a 0 g para 79, 108, 118, 152 e 162/162 a 0,1–0,5 g; nenhum caso ultrapassa o comparador traseiro nessa faixa. A 0,5 g, a carga dianteira calculada varia de 2.132,8 a 2.770,6 kg. Esses limites de massa por eixo não são, por si, limiares de força dinâmica instantânea; portanto a comparação apenas identifica situações que requerem classificação OEM adequada. O modelo não avalia suspensão, pneus, ABS, distribuição real de frenagem, fadiga, estabilidade ou conformidade e não converte a triagem em reprovação/aprovação. Saídas: `entregas/integrado_maxeon1540/integracao/envelope_frenagem_eixos/{casos.csv,resumo.json}`.

Após incluir o novo solver e o controle independente no verificador integrado, a suíte completa passou com 251 testes; Ruff, cenário integrado, verificador de desenvolvimento e `git diff --check` também passaram. Os manifestos oficiais foram regenerados deliberadamente e conferidos novamente sem `--registrar`: integrado 169 entradas/345 saídas; desenvolvimento 189/1.467. O estado continua `stage_complete:false`, sem aprovação humana ou demonstração de missão física.

### Limite de aderência de tração dianteira — 12/11/2026

Como complemento ao item P4, o solver `scripts/calcular_limite_aderencia_dianteira.py` cruza os mesmos 162 casos de massa/CG com cinco valores hipotéticos de `μ` (0,2–0,9) e rampas −6/0/+6%, totalizando 2.430 casos. A equação resolve o equilíbrio entre força disponível no eixo dianteiro, transferência longitudinal de carga e componente gravitacional da rampa. No caso nivelado, o teto de aceleração por aderência varia entre 0,083–0,108 g para μ=0,2 e 0,321–0,428 g para μ=0,9; em aclive de 6%, varia entre 0,026–0,051 g e 0,272–0,376 g, respectivamente. Resíduo máximo de força é inferior a 1,1e-11 N.

São limites superiores de pneus sob coeficientes de sensibilidade, não aceleração prevista: torque contínuo/pico, relação de redução, potência/inversor, rolamento, aerodinâmica, comportamento transiente do pneu e conformidade não estão incluídos. Os valores de μ não representam o pneu Continental nem piso medido. Resultados em `entregas/integrado_maxeon1540/integracao/limite_aderencia_tracao_dianteira/{casos.csv,resumo.json}`; o verificador integrado confere número de casos, equilíbrio e sinalização explícita dos limites.

Validação computacional após integrar os dois complementos P1/P4: 258 testes passaram, Ruff passou, verificadores integrado e de desenvolvimento passaram, e `git diff --check` passou. Manifestos após registro oficial e conferência sem registro: integrado 171 entradas/347 saídas; desenvolvimento 191/1.467. Continua `stage_complete:false`; nada disso valida aderência de pneus, freios, veículo, autorização OEM ou missão física.
