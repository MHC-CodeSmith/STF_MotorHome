> Revisão editorial posterior: o PDF foi enxugado, mantendo os 27 pedidos/subpedidos,
> os quatro fluxogramas, o mapa e as comparações. As listagens foram retiradas por
> instrução expressa. A introdução/revisão/objetivos usam frases adaptadas do Cuca com
> atribuição. A cobertura geral dos PRs e do enunciado está em
> [AUDITORIA_ENUNCIADO_E_PRS.md](AUDITORIA_ENUNCIADO_E_PRS.md).

# Auditoria integral do PR #9 e adaptação do relatório

Revisão de 25/11/2026. Fonte: [PR #9 do Fael](https://github.com/MHC-CodeSmith/STF_MotorHome/pull/9),
patch original de 81 linhas, documento `Revisao_Motorhome_P5_e_Projeto.md` e comentário de integração.
O PR está mesclado; sua descrição é vazia, não há reviews nem comentários de linha. Foram conferidos
os **27 pedidos marcáveis**, incluindo os subpedidos dentro de cada parágrafo e os quatro fluxogramas.

A marcação do checklist significa que o pedido recebeu cálculo, texto ou limite explícito. Não
representa autorização de instalação, ensaio ou aprovação humana dos componentes.

## Rastreabilidade dos 27 pedidos

| Nº | Pedido e todos os seus aspectos | Tratamento e evidência |
|---|---|---|
| 1 | Quatro Maxeon390, 2S2P, 1560 Wp, 76 kg; atualizar cenário, figuras e BOM | I08; `config/parametros_globais.yaml`, cenário `maxeon1560_independente`; saídas em `entregas/integrado_maxeon1560/`. Arranjo1540 preservado como histórico. Geração do teto 5,940 contra5,864 kWh no mesmo dia. |
| 2 | Ligação, 129 V/12,10 A, Voc frio171,59 V, saída32,5 A, 250/60, problema de quatro paralelos | I08 deriva cada grandeza e o caso de49 V a85 °C; I09 explica a conversão e os dois rastreadores. A verificação é por ficha, não um ensaio do conjunto. |
| 3a | Comparação de modelos e versões, potência, energia por parada | I08, tabela de portáteis; `scripts/analisar_geracao_portateis_p5.py`. ZOUPW explicitamente450 W N-Type16BB; dados de outra versão não são transferidos. Renogy identificado como RSP400LSC-G1, sem equivalência inventada com E.FLEX. |
| 3b | Massa incluindo acessórios e dimensões abertas/dobradas | I08 distingue massa documentada com bolsa do EcoFlow e massas de painel; acrescenta hipótese de1 kg/unidade de acessórios para candidatos sem esse dado. São dadas as dimensões e os limites dos conectores salientes. |
| 3c | Tempo de montagem, custo e compatibilidade MPPT | Hipótese comum30 min montar +30 min recolher, sem alegar medição por marca. Preço Renogy USD495,99/unidade, loja oficial, acesso25/11; sem estoque na consulta. Verificação2S2P no150/60 a−20 °C com limite de tensão/corrente. |
| 3d | Quantidade no CAD, acesso, retenção e abertura sem sombra | Quatro envelopes dobrados no volume1,10×0,38×0,98 m; retirada pelas portas traseiras; requisito de duas cintas5 kN e contenção positiva, carga5g=4,12 kN. Olhais OEM explicitamente não demonstrados. Abertura em uma fileira leste–oeste e distâncias para segunda fileira. |
| 4 | Quatro operações no mesmo clima/data; gráfico horário e montagem/recolhimento | I08 e `p5_geracao_portateis/horario_casos.csv`: só teto, parado integral,08–16 e18–02; geração5,94/14,49/6,31/14,49 kWh. Figura com condução sombreada e transições dos portáteis. O antigo00–08 é identificado como comparação adicional. |
| 5 | Inclinar pelo eixo longitudinal, orientação e janela; energia líquida ao falar de recarga | I08, sensibilidade5/10/20°, norte/sul/leste/oeste;20° norte7,65 kWh. Mecanismo não projetado e uso estacionado explícitos. Não se anuncia número de dias de recarga a partir da potência nominal. |
| 6 | Nova curvaI25, mesmo lado de medição e crédito inicial zero | I25; `desenvolver_despacho_i25.py`; mínimo0,38 kW na saída e correspondente entradaPmin/eta, igual ao replayI29;630 casosMILP. |
| 7 | Casos com/sem habitação,40/80; geração, serviços, perdas, corte, tração e distância | I25, tabela de balanço e tabela gerada por resultado. A interfaceCC é hipótese em ambos. Geração e corte não são confundidos. |
| 8 | Investigar corte0,4 kWh e ganho antigo0,78 | I25 explica que0,4 não se confirma no novo cenário:0,19 kWh de corte na saída e aproximadamente0,05 de geração perdida pela partida antecipada. O ganho antigo0,78 era outro limiar/cenário, não resultado vigente. Com serviços cíclicos, corte nulo no teste. |
| 9 | km/kWh e kWh/km; calculado no lado da bateria; arrasto quadrático; recalcular com massa nova | I26 deriva unidades e inversão, mostra dobrarv→quadruplicarFa. Massa da cama incorporada; I26/I25/I27/I28/I29 e freios reexecutados. `relatorio/atualizar_tabelas.py` gera macros, evitando valores anteriores em tabela e texto. |
| 10 |30% vêm do enunciado;100→30;68,6 kWh; sem solar | I27 define o orçamento0,7×98 e o modelo sem reposiçãoHV. |
| 11 | Comparar até24h e8h; velocidade, duração, potência e hipóteses | I27 e `energia_sistemas/I27_autonomia_otima_modelo_sem_HV.csv`; Jensen e mínimo de e(v); auxiliares/arrasto, pista plana, velocidade constante e rendimento declarados. Valores recalculados após a cama. |
| 12 | Melhor velocidade,40 e80 sob mesmo horário/reservas; dias, horas, ritmo após reserva e bateria inicial | I29, macro/tabela `IbComparacao`, geradas por `fechar_i29_velocidade.py --figura`; `i29_fechamento/comparacao_velocidades.json`. Horário e reservas comuns isolam a velocidade. A primeira chegada à reserva é apurada intervalo a intervalo, sem a aproximação pelo SOC de fim do dia, que pode ocultar uma descarga seguida de recarga. Há teste desse caso. Comparações com horários otimizados separadas nas buscas. |
| 13 | Por que busca em grade e alcance da palavra ótima | I29 distingue mínimo analítico de consumo do mínimo de tempo dependente da agenda, portáteis, mínimoCC e reservas. Resultado identificado como melhor combinação na grade/refinos; ótimo global não alegado. |
| 14 |17h45: janela recorrente versus primeira partida física | `simular_missao(..., primeira_partida_h=...)` e fechamentoI29 impedem condução antes da primeira saída. O horário final é aquele recalculado, não herdado do cenário anterior. |
| 15 | Acumular vários dias como opção | I29 descreve a política opcional e suas restrições de capacidade, reservas, céu claro e portáteis; não se inventa ganho nem se apresenta como resultado simulado do cenário principal. |
| 16 | Variante, introdução com teto/portáteis, alternativas e parâmetros decisivos; teoria→dados→método→resultado→interpretação | Introdução e Projeto técnico; SK MY25 505.GG1.2, tabela de escolhas, subseções de especificação e deduções dos11 problemas. Fotografias oficiais com fontes, CAD e campos preservados. Comparações típicas sem fonte equivalente foram retiradas. |
| 17a | Mapa de dependências e ordem de propagação | Mapa entreP1–P7; massa/CG e CdA→consumoI26→I25/I29/I27; esta ordem foi respeitada na reexecução. |
| 17b | Fluxo geração/elétrica, bancos distintos, recarga externaCC e ponto do mínimo | I09, `fig:fluxo_eletrico`: sol→teto/portáteis→MPPT→serviços; inversor/cargas e ramo hipotéticoCCS2 separados. |
| 17c | Fluxo autonomia/viagem com geração, consumo, SOC, reservas, portáteis, dirigir/esperar | I25–I29, fluxograma operacional e equações por intervalo. |
| 17d | Fluxo cabos: corrente→Joule→contorno→Tmax e método | I30, fluxograma e memorial de volumes finitos, malha multidimensional e contorno realista declarado. |
| 17e | Fluxo cabine: ganhos→ventilação→temperatura/carga→potênciaCOP | I31–I32, `fig:fluxo_cabine`, equações e tabela de capacidade. |
| 18 | MPPT/inversor/perdas, bancos distintos, mínimo, cargaCA e troca20 Wp | I08/I09; inversor dimensionado pela simultaneidadeCA; perdas por etapa separadas;20 Wp de teto não implica novo inversor. |
| 19a | Por aparelho: potência, tempo/ciclo, CA/CC, energia e fonte | I13, tabela e notas de origem: fichas de aparelho versus hipóteses de energia/uso. Potência nominal e média não são confundidas; ciclos semanais rateados explicitamente. |
| 19b | Perdas e vazio separados; perfil por horário paraP5;33h com média/SOC | `scripts/gerar_perfil_habitacao_p5.py`→`perfil_habitacao/{por_aparelho,perfil_24h}.csv`;7,228825 kWh/dia,0,301201 kW, vazio18 W. I06:0,7×14,4/0,301≈33h. Rotina horária é hipótese; resultados principais usam média e não alegam invariância de SOC/cortes. |
| 20 |98 úteis+14,4 nominais;13,7 utilizáveis; basesSOC/reservas | I23 distingue112,4 de111,7 kWh e define bases de cada simulação. |
| 21 | Fechar56 faltas acima20kA ou registrar dimensionamento | I07,144 casos com10–40mΩ:2,75–16,05kA antesBMS, nenhum acima20kA.63 casos limitados peloBMS. Os56 vinham da varredura antiga1–50mΩ. Ampacidade instalada/I²t continuam limites reais, sem aprovação fictícia. |
| 22 | Eixos, transferência em frenagem, pneus/eixos, i=10 e tombamento idealizado | I02/I03/I05/I14/I18; reações e envelope recalculados; transferência dinâmica emI28/I33; pneus com ficha identificada; limitesOEM por eixo desconhecidos explícitos; i=10 hipótese;0,95g atual é limite de corpo rígido, não ensaio dinâmico. |
| 23a | Vistas técnicas cotadas e posição do banco sob a cama | I17 e figuras geradas: vistas ortogonais e layout cotado; banco com topo0,863m acima do piso, sob estrado; critérios de acesso/circulação substituem relato de edição. |
| 23b | Fixações e segurança da cama | `verificar_estrutura_cama.py`: distribuída, ajoelhada,3g vertical,5g lateral; estrado30mm, quadro50×50×3, postes45×45×4, peso dos postes, carga concentrada da longarina, flechasL/300 e M8 verificados. Aprovação do cálculo separada de soldas, base e ancoragemOEM. Massa incorporada aoI18, sem duplicar reserva12kg. |
| 24a | CFD comparável com/sem teto: malha, contorno, rodas, área | I19 e `scripts/comparar_cfd_deck.py`; malha de fundo55×20×10, refinamento5–6, solo móvel, rodas paradas, mesmaAref4,82784; explicada diferença no total de células por retirar deck. |
| 24b | CdA, potência, kWh/km40/80; portáteis transportados; geração perdida; rolamento | I19 mostra deltaCdA0,319m², potências e consumos; massa84kg dos portáteis incluída. Cruzamento da economia aerodinâmica com5,94kWh/dia do teto; comparação mantém a massa para isolar arrasto. I20 explica histerese/deformação, rótuloC2 eCr=0,012 conservador. |
| 25 |0–90 original e0–100 teórico, RPM, variante4250 eCTB61 | I28 recalculado; hipótese de torque/potência, comparação cinemática100/130=76,9%, n≈7128/9267rpm parai10. A ficha não vira nmax nem mapaOEM. Sensibilidade independente do raio em `mecanica_termica/I28_sensibilidade_raio.csv`:10,58/12,49s com0,361m versus10,82/12,72s nominal, mesmos parâmetros; quadratura confere a integração temporal em menos de0,0001s. Limitador90 e regra de trânsito tratados separadamente; sinalização e categoria “demais veículos” conformeCTB. |
| 26 |489A: ponto, capacidade instalada, volumes finitos e fluxograma | I30 deriva205kW/(eta√3VLLFP), SVPWM400/√2, eta0,95 eFP0,90 hipotéticos;382A no normal. Contornos de instalação,185mm², pico transitório e limite de125°C; sem alterar chicoteOEM. |
| 27 | Fórmulas térmicas, símbolos/unidades/hipóteses, COP, uma/duas pessoas e margens | I31/I32; balanço sol-ar, vidros, UA, psicrometria, ocupantes e ventilação; COP=Qfrio/Pel, hipótese2,5. Tabela1/2 pessoas,30/62m³/h, déficit sem cortina e margem com ela; IAC e curva real do aparelho não demonstrados. |

## Limites físicos que receberam tratamento explícito

O pedido de revisão foi atendido por cálculo e documentação, com hipóteses onde não há dado OEM.
Não são apresentados como conhecidos: nmax real/curvaOEM, relação final real, limites por eixo,
resistência de olhais/pontos de teto, homologação veicular das baterias de serviço, coordenaçãoI²t,
IAC medido da cortina ou capacidade doFreshWell exatamente a33/25°C. A interfaceCCS2 permanece
condicional; um requisito de interoperabilidade não é prova de que um carregador específico opera
nessa arquitetura. As vistas e envelopes não constituem desenho de fabricação da carroceria.

## Estilo e capa

O relatório do Cuca orienta organização e linguagem: Introdução com Objetivos, Revisão bibliográfica
em subseções, Projeto técnico com Especificações/Análise de custo/Simulações, deduções e tabela final.
O conteúdo foi adaptado aos35 itens e às simulações deste projeto; não foram importados resultados
ou alegações técnicas do outro veículo. Fotos oficiais, desenhos e gráficos têm identificação e fonte.

A capa usa exatamente os oito nomes fornecidos pelo usuário em25/11, em `relatorio/autores.tex`:
Matheus Hipolito; Matheus Alonso; Eduardo Barros Guimarães; Sabrina; Amanda; Vitor Dutra; Martinez;
Henrick. Essa instrução prevalece sobre grafias dos perfis e pareceres antigos. O vídeo está fora
do escopo por instrução expressa do usuário.

## Referências de verificação após a massa nova

O verificador mantém as referências históricas1540. Para1560, as durações esperadas
foram atualizadas somente após executar a cadeia com massa4042,78262976kg:
refino extra214,781250/216,760417dias; sensibilidade temporal15/5/1min
214,781250/216,760417/213,763889/214,802083/212,797222/214,773611dias.
São estudos locais anteriores ao fechamento com primeira partida física; não substituem
o resultado doI29 publicado em `i29_fechamento`. O diagnóstico de aliasing depende
da geração, que não mudou com a cama, e conserva sua referência. Além das durações,
o verificador confere consumo por força, conservação de energia, massa/momentos,
reservas, limite diário e as novas parcelas da cama por volume de material.

Conferência documental adicional de25/11: a página institucional USP Aberta deSEM0571
(`https://uspaberta.ime.usp.br/disciplinas/SEM0571`, turma2026201) relaciona Cristiano Bigonha
Tibiriçá e Paulo Seleghim Junior, coerentes com a capa de referência. O registro oficial
Pylontech/US5000 e seu manualV1.0 mantêm48V,4,8/4,56kWh,442×420×161mm e39,7kg;
a consulta não altera os parâmetros da simulação.

## Fechamento da viagem

Resultado final da viagem após o reforço da cama: 20,5 km/h, primeira saída às 18h,
214,755556 dias com reservas 10/20%; alternativa 20/30%: 20,7 km/h e 215,793056 dias.
Comparação a horário/reservas comuns: 40 km/h → 248,767361 dias; 80 km/h → 457,750694 dias.
Primeira reserva do líder em 3,845139 dias/538,645874 km; ritmo posterior 30,635538 km/dia.
Recibo dos 30 comandos principais, cinco suplementos, três preparações recuperadas e três
rechecagens históricas em `entregas/integrado_maxeon1560/revisao_relatorio/execucao.json`.
As preparações sem código de saída no log são identificadas como tal, sem inventar registro.
