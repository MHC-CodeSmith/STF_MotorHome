# Decisões vigentes por área — STF

Reconciliado em **26/11/2026**, com as evidências técnicas da revisão de 25/11.
Esta síntese atualiza a leitura do projeto; não cria aprovação nem altera parâmetros.
A fonte única é [parametros_globais.yaml](../config/parametros_globais.yaml), cenário
`maxeon1560_independente`, SHA-256
`047c725c8f26f5dbf4c824aaffeb92d09272f12a4e5e181e5e059c5eb3a4396b`.
O [recibo da revisão](../entregas/integrado_maxeon1560/revisao_relatorio/execucao.json)
registra as execuções anteriores; esta conciliação documental não reexecuta simulações.

## Decisão principal de cada área

| Área | Decisão mais importante em vigor | Evidência e consequência | Validação ainda necessária |
|---|---|---|---|
| **P1 — Estrutura, freios, massa e custo** | **Incorporar a cama reforçada na massa do layout A antes de avaliar PBT, eixos e freios.** DEC-022/033/059. | [Massa/CG](../entregas/integrado_maxeon1560/integracao/layouts_massas.json): 4042,782630 kg e margem de PBT de 207,217370 kg. [Cama](../entregas/integrado_maxeon1560/cama_estrutura/resumo.json): estrado 30 mm, quadro 50×50×3 mm, postes 45×45×4 mm; acréscimo líquido de 66,257102 kg substitui a reserva anterior. | Massa/CG são estimados; falta pesagem e limites por eixo. Cálculo dos tubos/parafusos não aprova soldas, bases nem ancoragens OEM; regeneração dos freios é sensibilidade. |
| **P2 — Bateria, elétrica e cabos** | **Preservar a independência dos bancos e o HV OEM: solar→tração somente pela arquitetura B de recarga externa, ainda condicional.** DEC-001/020/026/040. | [Interface CC](INTERFACE_DC_MINIMO_EQUIPAMENTO.md): 0,38 kW = 1 A × 380 V é hipótese de cálculo, não mínimo comercial comprovado. [Cabos I30](../entregas/integrado_maxeon1560/i30_corrente_maxima/resumo.json): 185 mm² atinge 118,1 °C no normal e 149,6 °C no pico permanente no cofre; não liberar pico contínuo. | Compatibilidade CCS2/handshake, autorização OEM, comutação FV, BMS, ampacidade/I²t e duração admissível do pico não demonstradas. Patamares SOC de hardware continuam `null`. |
| **P3 — Carroceria, CAD e CFD** | **Comparar a remoção do conjunto painéis + deck/suportes, mantendo o Cd como resultado numérico provisório.** DEC-023/030/031. | [CFD comparativo](../entregas/aero_equipado1540/comparacao_deck/resumo.json): Cd 0,62153633 com conjunto e 0,55548590 sem; ΔCdA = 0,318881 m² (+11,89%). Mesma massa no balanço de consumo isola o arrasto. | Sem independência de malha ou validação experimental. CAD adaptado não é CAD OEM; cargas, curvatura e apoios do teto precisam de validação física. |
| **P4 — Motor, transmissão e dinâmica** | **Preservar o trem de força OEM e o limite de 90 km/h da variante de estudo; não prometer 0–100 como desempenho operacional.** DEC-009/032/036/037. | [Dinâmica](../entregas/integrado_maxeon1560/mecanica_termica/I28_sensibilidade_raio.json): comparação cinemática com raio livre de 0,372 m e carregado de 0,361 m. [Consumo](../entregas/integrado_maxeon1560/dinamica_resistiva_sensibilidade/resumo.json) usa Cr = 0,012 como hipótese conservadora. | Faltam curva/mapas, rotação máxima, perdas e potência contínua OEM. Tempos de aceleração calculados não são ensaio do veículo; não combinar fichas de mercados diferentes. |
| **P5 — Solar, autonomia e otimização** | **Usar 1560 Wp fixos e 1600 Wp portáteis só parado; manter a viagem de 7000 km sem recarga externa como resultado condicional.** DEC-003/006/013/029/043. | [Fechamento I29](../entregas/integrado_maxeon1560/i29_fechamento/resumo.json): 20,5 km/h, primeira saída às 18h, 214,755556 dias, reservas tração/serviços 10/20%; alternativa 20/30% leva 215,793056 dias. Até 8 h de condução/dia. | Busca finita, não ótimo global nem previsão meteorológica de rota real. Alocação FV e interface CC não demonstradas; não somar capacidades dos bancos como energia intercambiável. |
| **P6 — Interior e conforto térmico** | **Manter FreshWell sob a cama fixa com proteção solar no para-brisa somente quando estacionado.** DEC-010/016/028/030/055. | [Proteção solar I32](../entregas/integrado_maxeon1560/i32_protecao_solar/resumo.json): para duas pessoas, carga nominal cai de 2,867 para 2,311 kW; faixa 2,089–2,534 kW compara-se à declaração de 2,7 kW. Em movimento o para-brisa fica livre. | IAC é hipótese, não medição do produto. Capacidade nas condições 33/25 °C, conflito documental, placa/revisão 60 Hz, partida/proteção e instalação não validados. Perfil horário por aparelho é suplemento hipotético; a missão principal usa média diária. |
| **P7 — Arrefecimento e térmica da bateria** | **Tratar UA, vazão e remoção de calor como requisitos condicionais; não declarar chiller, ventilador ou circuito OEM selecionado/instalado.** DEC-024/056. | [Complementos térmicos](../relatorio/dados_termicos/resumo.json): UA ≥ 1093 W/K para 65 °C com motor/inversor (~22,9 kW); com redutor (~29,02 kW), ≥1952 W/K. Vazões calculadas de 31,9/26,4/23,1 L/min. [Revisão](REVISAO_LEITURA_E_COMPARACOES.md) identifica os 486 casos da bateria. | Bateria modelada por ECM de dois nós, não pack calibrado; 45 °C é limite hipotético. 20/80 kW são condições de estudo, não FV disponível. Curvas reais, NPSH/pressão, capacidade do chiller e ensaios permanecem pendentes. |

## O que é vigente e o que permanece histórico

O [registro de 61 deliberações](decisoes_motorhome_2026-10-28.md) permanece **inalterado**,
SHA-256 `1e082c4961a57b865f008fa1daadd37e696bdb060f22c922596715096c793969`.
As aprovações históricas autorizam direções e métodos de projeto; não se reclassificam
como aprovações finais de componentes, resultados ou instalação. A execução técnica
provisória segue a DEC-061. Pareceres dos integrantes incorporados nos PRs/issue são
revisões acadêmicas, sem inferência de homologação física.

As referências a 1350/1540 Wp, massa próxima de 3976 kg, piso CC de 1 kW e agendas
anteriores nos relatos datados são históricas. O cenário atual tem 1560 Wp, cama
reforçada e piso CC hipotético de 0,38 kW. `aero_equipado1540` mantém o nome por
proveniência: a geometria/massa dos módulos de 1540 e 1560 Wp é a mesma. Não se
renomeiam nem recalculam evidências históricas para aparentar nova execução.
Estudos de cabine, ancoragens e radiador independentes de Wp mantêm suas origens;
os complementos atuais devem ser lidos junto das limitações desses modelos.

O [custo I24](../entregas/integrado_maxeon1560/i24_custo_brl/resumo.json) é estimativa
datada, não cotação de hoje: R$ 793.536,40 nominais, incluindo reserva mista de
R$ 25.000. Aquisições/componentes fora dessa reserva: R$ 768.536,40. Não inventar
rateio de materiais/mão de obra nem atualizar câmbio/preço sem nova pesquisa.

A [revisão vigente](REVISAO_LEITURA_E_COMPARACOES.md) e a [retomada](RETOMADA_CURTA.md)
prevalecem sobre instruções antigas: relatório de 41 páginas/38 figuras, oito nomes
exatos da capa, sem código no PDF; vídeo excluído por instrução do usuário. Seminário,
envio e autorização docente para oito nomes permanecem sem registro de realização.

## Rastreabilidade e manutenção

A [matriz das 61 decisões](MATRIZ_DECISOES_61.md) mantém IDs, títulos e hashes das
seções originais e atualiza evidências/limites por item. O JSON correspondente é
[matriz_decisoes_integrada_61.json](../entregas/matriz_decisoes_integrada_61.json).
Regenerar com `.venv/bin/python scripts/atualizar_matriz_decisoes_integrada.py`.
A síntese acima deve ser revista quando uma decisão ou entrada compartilhada mudar;
a regeneração da matriz não cria deliberações ou aceites humanos.
