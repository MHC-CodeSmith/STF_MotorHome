# Registro de decisões do projeto (ADR simplificado)

As perguntas e evidências necessárias ao marco inicial estão no [registro M0](REGISTRO_M0.md). São pendências para revisão; nenhuma resposta ou aprovação foi presumida.

| ID | Data | Decisão | Alternativas | Responsável | Itens impactados | Revisão |
|---|---|---|---|---|---|---|
| D000 | 21/10/2026 | Usar divisão P1–P7 do PDF mais recente; decisão operacional do grupo ainda a confirmar | Divisão mais antiga da conversa | Equipe | 1–35 | Pendente |
| D001 | a definir | Registro inicial sem veículo-base; proposta de trabalho posterior em D003 | Stella Vita (conceito), Fiat Ducato (CAD), Delica (CAD interior) | Equipe | 1–35 | Aprovação final pendente; desenvolver a proposta D003 |
| D002 | 23/10/2026 | Usar o exterior detalhado Ducato 2014/OpenX Assets 20261015 como geometria de trabalho, por instrução do usuário; bloco autoral fica restrito a teste de exportação. Sem reescala nem mistura automática com o interior Delica; conferir variante antes da integração física | Campers E-Ducato/Ducato do levantamento sem download recuperado; Delica para referência de interior; solar car MELVING22 para referência estrutural | Coordenação; P3 revisa | 16,17,19,31,32; interfaces de área/geometria | Arquivo efetivamente obtido; licença/atribuição e modificações registradas. Configuração global intacta; engenharia final pendente |
| D003 | 23/10/2026 | Adotar como proposta de arquitetura o Aurora Solar sobre E-Ducato MY25 L3H2 4250 kg, com tração BEV, motor OEM 205 kW/410 Nm, bateria 110 kWh nominal/98 kWh útil/400 V segundo ficha eslovaca de 20/03/2026. Solar e bateria alimentam a operação; sem motor a combustão ou gerador a combustível. SOC inicial 100% é hipótese de cenário explícita. Fonte e lacunas em `config/arquitetura_eletrica_proposta.yaml` | Conversão elétrica customizada do Ducato antigo e outras variantes E-Ducato; descartadas por ora para evitar misturar trem de força, massa e dimensões de versões diferentes | Coordenação; revisores P1/P2/P3/P4/P5 | 1–35 | Proposta fundamentada para desenvolver; curvas/mapas, geometria adaptada, massa e revisão humana ainda pendentes. Não altera o YAML aprovado |
| D004 | 24/10/2026 | Manter Cd dos três pilotos como exploratório; usar grade de hipóteses para estudar consumo e agendas. Separar maximização diária I27 (SOC final exatamente30%, dia completo) do menor tempo I29 (7000km,8h/dia,sem carga externa). Layout0.2 reduz reserva do banheiro após interferência visual; 81 raios são triagem, não validação de sólidos | Adotar Cd sem independência de malha; estender indevidamente8h a I27; tratar reserva retangular como encaixe comprovado | Coordenação; P3/P4/P5/P6 revisam | 13,17,19,21,22,25,26,27,29; interfaces geometria/energia/térmica/massa | Cenários condicionados e pendências explícitas; parâmetros globais aprovados intactos |
| D005 | 25/10/2026 | Desenvolver cabine equivalente condicionada a hipóteses explícitas e pneu Continental225/75R16C candidato. Rejeitar seleção automática do A/C2,2kW para carga nominal estimada2,52/2,65kW; comparar FJX7 nominal3kW sem alegar atendimento final. Gerar memorial PDF parcial | Promover temperaturas estimadas e pneu candidato a resultados OEM; tratar potência térmica como consumo elétrico | Coordenação; P1/P3/P5/P6 revisam | 2,11,13,17,18,24,25–29,31,32; ver INTERFACES_2026-10-25.md | Sem aprovação final; YAML global intacto |
| D006 | 25/10/2026 | Ampliar cobertura fixa para1540W e modelar extensão estacionada2890W como alternativa condicionada à carga de teto. Equipar interior com CAD autoral e dimensões documentadas; cama longitudinal elevada e HVAC sob cama | Manter900W e blocos; aceitar montagem empilhada171kg sem conferir150/200kg e pontos OEM | Coordenação; P1/P2/P3/P5/P6 revisam | 8,9,11,13,17,18,19,24–29,31,32 | Fontes e testes registrados; não homologa montagem, energia na tração ou massa completa |
| D007 | 25/10/2026 | Incluir envelopes estimados do trem de força e componentes documentados de serviços no CAD, sem duplicar massa OEM; banco51,2V200Ah/10,24kWh, BMS NG e inversor48/5000. Substituir induçãoCVI1350EMEA50Hz por IE3TP220V60Hz2000W do manual2025; bancada contínua para portátil | Tratar geometria ilustrativa como CAD OEM; usar apenas100Ah apesar de mínimo200Ah no manual; misturar1500W127V com2000W220V; conservar fogão50Hz | Coordenação; P1/P2/P3/P4/P5/P6/P7 revisam | 6,7,9,10,11,13,17,18,23,24–29,30,32,34,35 | Proposta de integração, com fontes/código/STEP/QA; ainda sem circuito, estrutura ou térmica final aprovados. YAML global intacto |

## D008 — 26/10/2026: métodos I30/I35 com hipóteses separadas

Adicionar cabo polar feixe/isolamento/R(T) e radiador cruzado conservativo; configurações propostas próprias. RADOX120/150mm² são candidatos de estudo, não substituição do chicoteOEM. Dois120mm² paralelos precisam divisão de corrente/resfriamento independentes. Não selecionar radiador/bomba a partir de UA/vazões arbitrários. Não alterar parâmetros globais/massa OEM. Interfaces P2/P4/P7: corrente RMS, mapa de perdas, materiais/UA/curvas ainda pendentes. [Evidências](CABOS_E_RADIADOR_2D.md).

## D009 — 26/10/2026: I33 em pistas anulares ventiladas simplificadas

Condução r–z transiente própria e proposta separada`freios_proposta.yaml`.
Brembo09.D018.11 apenas referência300×32mm; compatibilidadeMY25 não afirmada.
Material de artigo ferroviário tabela2 como hipótese rastreável, não fabricante.
Sem regeneração no caso nominal, mas inércias omitidas: não declarar limite superior
completo. Não duplicar massa de freios já na tara OEM. Interfaces P1/P4/P3:
centro de gravidade/distribuição, inércias e geometria física pendentes.
[Método/resultados/convergências](FREIOS_2D.md). Global intacto, aprovação pendente.

## D010 — 26/10/2026: I34/I35, limite de90km/h e alternativa solar no solo

AdicionarECM/térmica de bateria com entradas hipotéticas explícitas e curva
Bosch publicada para ponto hidráulico de circuito assumido. Preservar limitador
90km/h específico4250kg da fichaSKp3; I28 não promete0–100 eI33 segue ensaio
docente. Recalcular balanço do teto atual: habitação/perdas deixam déficit.
Alternativa4×EcoFlow400W no solo +MPPT dedicado, com bolsas verticais CAD;
substitui alternativa pesada, sem somar ambas no viewer. Sem interfaceHV
comprovada ou agenda atual ótima. Interfaces P1–P7 registradas em
[FECHAMENTO_TERMICO_E_MISSAO.md](FECHAMENTO_TERMICO_E_MISSAO.md).
YAMLglobal preservado;35itens não foram aprovados.

## D011 — 26/10/2026: mecânica retida, pneu comparativo e BOM incompleta

Confirmar arquitetura elétrica/suspensão/direção em fonteFiatUK primária,
sem transplantar dados elétricos contraditórios ou placa de outra variante.
Camper0451473/Cr por rótulo é alternativa, não mudança silenciosa do A/S.
Preservar lubrificaçãoOEM e registrar óleo/volume/intervalo desconhecidos.
IniciarBOM27linhas com preços ausentes null; R$439 é referência públicaIE3TP,
não orçamento final instalado/com impostos. Todos35itens têm trabalho em curso,
nenhum aprovado. Fontes/escopo em[MECANICA_ROLAMENTO_E_CUSTOS.md](MECANICA_ROLAMENTO_E_CUSTOS.md).

## D012 — 27/10/2026: agendas com portátil e bancos separados

Adicionar modelo diário com montagem/recolhimento e duas baterias; sem somar
capacidades. Comparar transferênciazero com interfaceHV2kW/90% hipotética,
somente parado. Serviços80→80%/reserva20% e tempos30min são hipóteses de operação,
não mudança do componente ou aprovação OEM. Tração I27 termina30% exatamente;
8h/dia aplica-se só aI29. Política repetida7000km/202dias é limite superior
condicionado, não ótimo global. Exportar potência nas rodas; eixo motor null
até obter perdas reais. YAMLglobal preservado; suplemento separado e revisão
humana pendente. [Método/limites/interfaces](AGENDA_PORTATIL_2026-10-27.md).

## D013 — 27/10/2026: solar12/48V e despachoAC discretos

Separar0,658097kWh/dia do PV12V, sem creditar à missão48V/HV até demonstrar rota
elétrica. Adicionar EVSE candidatoNRGkick16A50/60Hz, sem afirmar aceitação do
OBCMY25 em monofásico60Hz, seleção/aprovação ou mudança da BOM final.
Correntes0/6/8/10A por30min, perfisAC/DC, perdas por conversão e limites
compartilhados produzem I27condicionado344,767978km e construçãoI29de276dias,
não ótimo global ou previsão da rota. Fonte primária conferida e catalogada;
PDF no cache externo. Preservar entrega anterior e parâmetros globais.
[Evidências e limitações](INTERFACE_CARGA_2026-10-27.md); revisão humana pendente.

## D014 —28/10/2026: rota real, limites aproximados e calendário

Por instrução do usuário, avançar com vias reais e velocidades aproximadas.
Corredor costeiroOSRM7511,282km por21pontos; manter marco7000km sem reescalar.
Usar DEM5km e dois cenários solares por local/data: céu limpo eERA5histórico,
partida21/06/2025. Comparar tetos60/80/90km/h com perfil da via e limitador90.
Cauda meteorológica indisponível descartada e declarada; nada de inventar clima.
Política com duas baterias e8h/calendário, interfaceOEM ainda hipótese. Documentar
tanto chegadas em céu limpo quanto falhas por reserva com nuvens; não promover
a política a ótimo global nem ao veículo validado. Revisão35atualizada após
executar/reabrir os resultados. [Evidências](ROTA_REAL_2026-10-28.md).


## Conciliação pós-DEC061 — 09/11/2026

O usuário autorizou execução técnica provisória e preservação das61decisões. O registro não estava no repositório nem no remoto; foi localizado em `/home/mhc/Downloads/decisoes_motorhome_61.md` e incorporado byte a byte em `docs/decisoes_motorhome_2026-10-28.md` (SHA256 `1e082c4961a57b865f008fa1daadd37e696bdb060f22c922596715096c793969`,298721bytes). O arquivo original permanece inalterado.

`config/parametros_globais.yaml` foi migrado do scaffold0.0.0 para1.0.0-pos-DEC061, com registros por parâmetro e proveniência. O estado anterior é recuperável no commit `2ef84f67c3aa820633b0565e92c0a23ea810302b`; não é substituído no histórico. Alteração deliberada afeta os35itens: arquiteturaB, independência dos bancos,220V60Hz, consumo diário simplificado,100%SOC inicial nos dois bancos da missão,7000kmplano, equipamentos e seleções provisórias.

`config/servicos_proposta.yaml` é agora explicitamente histórico e não descreve caminho via banco auxiliar como proposta vigente. Os runners antigos de interface/agenda/rota/viagem exigem `--historico`; o novo runner lê exclusivamente parâmetros compartilhados da fonte canônica. Os resultados anteriores não tiveram seus hashes ou números reescritos. Modelo de freios foi estendido para receber potência de atrito já descontadas resistências e recuperação, preservando a API anterior. A conferência atual está em `docs/INTEGRACAO_POS_DEC061.md`; nenhuma aprovação humana foi acrescentada.


## Execução técnica02 — revisão1.1.0,09/11/2026

DEC001–061 preservadas. Sob DEC061, layoutA provisório, massa3973.0255kg estimada, inventário/CG/eixos hipotéticos, FEMtrilhos, CFDcabine3D, grade1008missões, auxiliares de tração700W e sensibilidade0/300/700/1500W. Fontes/limites e reprodução em `EXECUCAO_TECNICA02.md`. Não altera deliberações;0aprovações finais. Baseline29defc4 preservado, executor conciliar antigo bloqueia revisão1.1 para impedir atualização indevida de evidências históricas.
