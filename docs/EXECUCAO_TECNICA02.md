# Execução técnica02 — 09/11/2026

Estado de desenvolvimento, **sem encerrar a etapa técnica completa e sem preparar submissão acadêmica**. Ponto de partida técnico `29defc4`; nota posterior `2ce7e81` preservada. As61decisões originais não foram editadas. Fonte ativa: `config/parametros_globais.yaml`, revisão **1.1.0-execucao02**.

## Resultados efetivamente produzidos

- Dois layouts e duas alternativas de teto em STEP/GLB, vistas principais cotadas e testes de caixas. LayoutA cama fixa escolhido provisoriamente; sem colisõesAABB entre equipamentos ou caixas de roda estimadas. Corredor frontal0,454m, reserva de abertura da lavadora0,59m versus0,48m exigidos pelo envelope. LayoutB exige revisão: abertura insuficiente em6mm e84kg de portáteis elevados. Não houve troca da carroceriaOEM.
- MassaA **3973,0255kg**, incluindo ocupantes/bagagem/água, mobiliário, revestimentos, isolamento e reservas explícitas de equipamentos/suportes. Margem **276,9745kg** até4250kg antes de eventual interfaceDC/buffer não instalados. CG de estudo x2,01669m do eixo dianteiro, y0,00126m, z0,92790m; reações1987,31/1985,72kg. CGbase, posição do piso/eixos e caixas de roda são hipóteses, **limites admissíveis por eixo continuam desconhecidos**.162casos propagam incertezas/níveis da água; não pesagem ou homologação.
- FEM1D dos dois trilhos40×40×3mm de aço representativo para119,1kg de bateria:12casos,4/8/16/32elementos,1/3/5g. A5g, tensão46,53MPa e flecha0,488mm; solução fechada e reações conferidas. Não verifica apoio na van, solda, parafuso/arrancamento ou flambagem local.5g é cenário, não requisito normativo inventado.
- CFD3D da cabine fechada/desocupada/ACoff:3malhas2400/8100/19200células. SIMPLE não convergiu e foi rejeitado como resultado final. ContinuaçãoPIMPLE300s, passo máximo0,1s e comparação0,05s na malha8100. Campo fino: média50,3203°C, máximo53,0744°C; diferença de média malha fina/intermediária0,10471K; redução do passo0,000511K. Balanço independente por faces versus armazenamento: erro máximo0,0482% da troca térmica absoluta no intervalo250–300s. CamposT/U, malhas, dicionários e logs preservados. **É complemento de meio-dia congelado, não CHT/transiente matinal3D nem validação física**. Rede equivalente anterior continua fornecendo evolução matinal49,0785°C ao meio-dia.
- Diagnóstico aerodinâmico real: y+ na malha166212, carro31,73–2123,14/média516,55. Isso reforça a insuficiência do tratamento de parede. Os3Cd anteriores e variação7,07% permanecem não independentes. Nenhuma nova simulação aerodinâmica equipada foi declarada; RAMdisponível≈2,45GB e swap já≈7,2GB usados no momento da avaliação limitaram nova malha volumosa.
-164pontos de dinâmica para2layouts×2massas×41velocidades. Nova potência fixa de auxiliares **de tração**, separada da habitação:700W de estudo e faixa0/300/700/1500W, todos estimados, não OEM. O modelo anterior zeroauxiliar favorecia velocidades excessivamente baixas.
- I27: otimização analítica restrita pelo modelo plano, eficiência constante e auxiliar ligado só em movimento. Minimização de e(v), junto de Jensen e limite de24h: a20,6904km/h, **351,701km em16,998h** para100→30% e **251,215km em12,142h** para80→30%. SOC finalexato30%; não recomendação de condução17h nem otimização solarDC demonstrada. Horizontes fixos8/12/24h também calculados;8h não foi transferido como regra do item27.
- I29:32replays adicionais com massa integrada/PBT e40/80km/h; depois busca exaustiva de **1008cenários** (6inícios×3janelas×7velocidades×2reservas×4auxiliares). Melhor da grade para700W: janela20–04h,20km/h, **290,875dias** com10/20% e **292,885dias** com20/30%. Comparação:0Wfavorece10km/h/216,844dias;1500Wfavorece30km/h/346,844dias. São **resultados condicionais**, mínimoDC1kW hipotético, clima21/06SãoCarlos repetido, sem prova de ótimo global ou missão física. Portáteis ficam45°/Norte por parada nos melhores casos. Não confundir essas velocidades acadêmicas com operação recomendada em rodovias.
- Logística hídrica inserida nos melhores replays:60L/dia,lavagem68,8L semanal, descarte/reabastecimento antes de exceder capacidades,15min/evento dentro da janela estacionária. Disponibilidade de instalações por parada é hipótese explícita, não mapa comprovado; nenhumkWh externo é adicionado. Água/massa conservadas.
- MPPT:150/60-Tr selecionado provisoriamente para o estudo compartilhado só em serviços48V:50AIsc,145Voperação,60Asaída;36,48A/135,4V passam na triagem. AssociaçãoIV/proteções/BMS ainda não demonstrada.36casos de I–V por trechos estimados mostram perda compartilhada0,18–25,99%; não curvas de fabricante. Isc36,48A; ficha250/60indica35A enquanto manualonlineindica60A: **conflito de revisão/hardware aberto;35A usado conservadoramente**, 250/60não escolhido. O150/60 evita esse conflito de limite de corrente, mas não valida associação heterogênea. GenasunGVB8boost pesquisado e rejeitado para190W/Isc9,17A por limiteIsc8A; não confundir corrente de entrada15A com Iscadmissível8A. Meta1540Wp mantida; apenas1350Wp com caminho48Vprincipal documentado são creditados.
- I28:36envelopes hipotéticos0–90=9,23–14,19s; relação8/10/12,ηredutor.95/.97/.99 e aderência.6/.8. Não são curvasOEM.0–100é não alcançável na candidata limitada90km/h.
- I33:24novoscasosr-z com3973/4250kg,regenhipotética0/40/80kW,3malhas e passo refinado. Subtração explícita de arrasto/rolamento; transferência de carga/aderência calculadas. Resíduo térmico máximo1,34e-9J. Geometria/material/partição/regenOEM continuam condicionados.
- I34:54novas sensibilidades20/80kW, massa500/650/800kg (somente térmica, não duplicada na tara),UA125/250/500 e cooler250/500/1000W/K. ECM2nós, não packOEM calibrado. I35radiador2D/Bosch e I30referênciaHVrθ reexecutados, com fontes e campos preservados.

## Arquivos e reprodução

Resultados: `entregas/desenvolvimento_2026-11-09/`. Revisão por item: [35itens](REVISAO_TECNICA_EXECUCAO02.md). A lista única continua [APROVACOES_FINAIS_PENDENTES.md](APROVACOES_FINAIS_PENDENTES.md), sem novos pedidos de aprovação durante desenvolvimento.

```bash
PYTHONPATH=src .venv/bin/python scripts/desenvolver_integracao.py
PYTHONPATH=src .venv/bin/python scripts/desenvolver_energia_sistemas.py
PYTHONPATH=src .venv/bin/python scripts/desenvolver_mecanica_termica.py
PYTHONPATH=src .venv/bin/python scripts/integrar_freios_massa.py
PYTHONPATH=src .venv/bin/python scripts/otimizar_grade_missao.py
PYTHONPATH=src .venv/bin/python scripts/registrar_execucao02.py
PYTHONPATH=src .venv/bin/python scripts/verificar_desenvolvimento.py
PYTHONPATH=src .venv/bin/python -m pytest -q
ruff check src scripts tests
```

Os executores científicos usam a.venv existente. `verificar_desenvolvimento.py --registrar` é usado **somente ao gerar uma revisão nova**, criando hashes, e depois executa os controles físicos independentes; na conferência normal, omitir--registrar. Não atualizar manifestos antigos para ocultar divergências. Os arquivos atuais de manifesto/qa informam contagens efetivamente verificadas. Logs: `output/*execucao02*`.

CFD exige OpenFOAMlocal em `/home/mhc/motorhome_referencias_tarefas/software/openfoam2412-local/usr/lib/openfoam/openfoam2412`. Para repetir sem sobrescrever campos entregues:

```bash
PYTHONPATH=src .venv/bin/python scripts/desenvolver_cabine_cfd.py --prefixo CAMINHO_OPENFOAM --destino NOVO_DIRETORIO/cabine_cfd
PYTHONPATH=src .venv/bin/python scripts/refinar_cabine_transiente.py --prefixo CAMINHO_OPENFOAM --origem NOVO_DIRETORIO/cabine_cfd --destino NOVO_DIRETORIO/cabine_transiente
```

Verificação de faces da execução entregue: `PYTHONPATH=src .venv/bin/python scripts/verificar_campos_cabine.py`. Diagnóstico y+: `scripts/diagnosticar_yplus.py --caso-cache NOVO_CACHE`; exige o caso aerodinâmico externo preservado. Reexecuções de `calcular_hidraulica.py` e `calcular_cabos_tracao.py` exigem--destino novo; não sobrescrevem resultados de fontes comerciais anteriores.

A tentativa de contornoCFD que depositava o ganho transmitido na própria face do vidro foi descartada; o contorno adotado distribui a absorção por área interior, hipótese documentada. Os primeiros empacotamentos com colisões foram corrigidos antes da seleçãoA. O hash do YAML completo inicialmente registrado noCFD foi retirado porque o YAML evoluiu durante a execução; ficam os dicionários efetivamente usados, hash da rede de origem e extração física conferida. Não se atribui retroativamente o CFD à configuração final de outras disciplinas.

## Limites que não encerram a etapa

RecargaDCexternaOEM/minimos/protocolo/autorização permanecem não demonstrados. Não houve modificaçãoHV/BMS/cabos, transferência entre bancos, compra/instalação, ensaio físico ou contato com terceiros. Buffer exclusivo continua comparação não instalada. O estudo físico não é bloqueado pela falta de aprovação individual; as limitações estão segregadas dos modelos condicionais.

Ainda há trabalho executável no detalhamento de fixações/rotasCAD, proteção elétrica/comandoSOC e adaptação da malha aerodinâmica equipada com camadas. ProprietáriosOEM ausentes: eixos, pressões de pneus, mapa de motor/redução/óleo e parâmetros térmicos. Preços instalados/importação, compatibilidade220V doHVAC e instalação física não foram inventados. A revisão dos35itens distingue estes casos; **0 aprovações humanas finais**.

## Verificação do checkpoint

208testes passaram;Ruff passou;estrutura35/7 passou;auditoria sem erros estruturais. QAintegrado:90controles físicos/integração,140entradas e676saídas por hash;STEP reimportados com volumes positivos. Campos da cabine e vistas deCAD inspecionados visualmente. O verificador foi reexecutado sem--registrar para conferir o manifesto. A guarda do executor antigo recusou revisão1.1 antes de alterar o manifesto histórico.

## Continuação técnica — 10/11/2026

I25 agora tem despacho temporal reproduzível, além do antigo teto de energia (preservado e identificado como tal). `scripts/desenvolver_despacho_i25.py` executou **630 MILP**:35partidas entre06–23h×3mínimosDC×2tratamentos de serviços×3passos30/15/5min. Cada janela admite uma parada inicial e condução posterior até24h; ângulo portátil fixo escolhido entre24orientações pela energia da parada. O MILP maximiza energia solar destinada à tração, com perdas, mínimoDC, energia/capacidade do banco de serviços e condição cíclica. Não transfere energia entre bancos. A grade de partidas e orientação por colheita FV não provam ótimo global de políticas com várias paradas. Não há limite8h importado doI29.

O crédito solar da tração inicia **zero**, sobre SOCbase30% que não pode ser gasto; só a geração do próprio dia financia a condução. Comparador com serviços parte/termina7,2kWh no banco14,4kWh, sem consumo líquido da energia inicial. Portáteis são retirados antes da partida e não voltam a operar naquele dia, mesmo que a condução termine antes24h. Mínimos0/1/3kW na **entrada FV da cadeiaDC** são hipóteses, assim como rendimento90%; não são mínimosOEM ou evidência de carregador existente.

|I25,passo5min|40km/h|80km/h|
|---|---:|---:|
|Só tração,mínimoDC1kW|48,0743km|26,6488km|
|Serviços cíclicos7,22883kWh/d,mínimoDC1kW|24,1633km|13,3943km|
|MínimoDC3kW|0km|0km|

No caso1kW/sótração, a melhor partida da grade foi16h30; com serviços,18h30. Diferença15→5min≤0,04076km nos casos40/80;30→5min chega0,88036km por sensibilidade ao limiar de potência. Sem interface demonstrada, o controle de autonomia solar da tração continua **0km**. Resultados estão em `entregas/desenvolvimento_2026-11-09/despacho_i25/`:resumo,curva10–90km/h,partidas,36perfis completos e sensibilidade de passo. A figura foi inspecionada visualmente.

**Correção de integração:** os32replays de `energia_sistemas/I29_missoes_massas_integradas.json` omitiam o auxiliar de tração na chamada a `consumo_plano`, embora a grade1008 já o incluísse. Corrigida a chamada para700W;32casos reexecutados, com consumo e potência auxiliar registrados por cenário. Exemplo3973kg:0,22502767kWh/km a40km/h; controle reserva10% agora391,9518km. A grade1008 não mudou e não precisou reexecução. Resultados anteriores estão no históricoGit9e70fd7; não foram promovidos a medições.

**Água:** `scripts/detalhar_paradas_hidricas.py` gerou9.572eventos nos8melhoresreplays, com tomada de água em lotes distribuídos pela janela estacionária. Reabastecimento/descarte15min precede o uso quando necessário; os horários são distintos, não coincidem com condução nem com montagem/recolhimentoFV. Consumo-base60L/dia, lavanderia68,8L semanal; último dia proporcional à duração. Conservação erro máximo≈9,1e−13L;capacidades100/70/20 respeitadas. Arquivos `otimizacao_grade/sanitaria_cronologia*.{csv,json}`. É uma escala hídrica condicional, não disponibilidade geográfica de instalações nem duração validada dos ciclos; energia continua médiaDEC046, sem recargaexterna e sem reexecutar missão elétrica. O CSV sanitário diário anterior permanece histórico de agregação, não escala detalhada.

Novos parâmetros de estudo estão nas seções `development.daily_dispatch` e `development.water_chronology` da fonte única, com fontehyp,responsável,data,versão,confiança/status. As61decisões permanecem intactas. Testes novos usam casos analíticos de alocação/perdas/mínimoDC/energia inicial e agenda hídrica; a QA confere o consumo dos32replays por equação independente e confronta os eventos com os perfis efetivos de condução.

```bash
PYTHONPATH=src .venv/bin/python scripts/desenvolver_despacho_i25.py
PYTHONPATH=src .venv/bin/python scripts/desenvolver_energia_sistemas.py
PYTHONPATH=src .venv/bin/python scripts/detalhar_paradas_hidricas.py
PYTHONPATH=src .venv/bin/python scripts/registrar_execucao02.py
PYTHONPATH=src .venv/bin/python scripts/verificar_desenvolvimento.py --registrar
PYTHONPATH=src .venv/bin/python scripts/verificar_desenvolvimento.py
PYTHONPATH=src .venv/bin/python -m pytest -q
ruff check src scripts tests
```

216testes passaram;Ruff passou. A contagem vigente de verificações integradas/hashes está em `qa.json`. A etapa completa continua aberta: próxima frente executável é proteção/comandoSOC/fixações, seguida de integração geométricaCFD. InterfaceDC permanece não demonstrada; nenhum equipamento comprado/instalado e nenhuma aprovação final inferida.

## Continuação elétrica, fixações e CFD — 10/11/2026

Implementados `src/motorhome/protecoes.py`, `scripts/desenvolver_protecoes_fixacoes.py`, `scripts/detalhar_rotas_cad.py`, `scripts/refinar_camadas_aerodinamica.py` e `scripts/estabilizar_aero_fina.py`. Métodos,fontes e limites elétricos no [modelo de proteções](PROTECOES_SERVICOS_MODELO.md). As pesquisas primárias acrescentadas aoYAML incluem integração oficialPylontech–Victron, manuaisMultiPlus/MPPT e fichaLittelfuseJLLN2025. **A combinaçãoUS5000–Victron documentada requerGX/CAN-BMS/DVCC**;hardware adicional ainda não incorporado automaticamente sobDEC056. Não assumir que oBMS integrado sozinho fecha essa integração.

Resultados em `protecoes_fixacoes/`:324casosDC,144faltas,256combinações de simultaneidade,6históricos de falha e648casos de grupo de parafusos. CorrenteDC10,384–102,936A;resíduo de potência≤1,24e−12W. Fusíveis candidatosJLLN200/JLLN080,125VDC20kA;56casos hipotéticos excedem interrupção20kA,semI²t real/impedância do banco/coordenação demonstrados. LimiaresSOC continuamnull;máquina de estados recebe estágio abstrato e travaOFF por falha,sem alegar atuador instalado. Picos comerciais desconhecidos são recusados em vez de preenchidos como dados. Chapa2/3/4mm tem10casos de esmagamento>limite de estudo;máximautilização2,236 versus0,622 nos parafusos. AncoragemOEM/fadiga/prying/tração não simulados sem geometria/dados.

**Erro geométrico corrigido:** o inversor no layoutA estava deitado565×328×148mm. Agora328×148×565mm, posição local[0,61;1,40;0,28]m,com100mm de reserva de acesso de estudo sem colisões. A primeira rotação testada colidia com oHVAC;reposicionamento eliminou a colisão antes da entrega. ReexecutadosCAD,massa/CG/eixos,162sensibilidades e24casos de freios dependentes da alturaCG. Massa mantém3973,02553kg; **CG atualizado** x2,01758466/y0,00209254/z0,92871773m;reações1986,4294/1986,5961kg. ValoresCG/eixos anteriores neste documento são do estado pré-correção. LimitesOEM por eixo continuamnão documentados.

NovoCAD `rotas_instalacoes/layoutA_rotas_reserva.{step,glb}` eJSON:2cabos48V+3rotas potáveis. Laço estimado1,783946m com20%folga;70mm²/90°C/4000W/43,5V resultam102,306A,queda0,13176% e5,86363W. ContatosAABB apenas nos terminaisconceituais de inversor/bomba/boiler,explicitamente listados;terminalreal/curvatura/chaparia/painéis de mobiliário/passagensnão comprovados. Esses trajetos são reservas, não instalação liberada. Custos/massas de cabos/proteções permanecem cobertos por reservas anteriores,sem dupla soma ou orçamento comercial fictício. O comparadorB ainda precisa corrigir orientação/acesso.

**Aero efetivamente executado:**3casos novos a partir das malhas existentes,solicitando3camadas absolutas,final2mm/expansão1,2. Duas menores29527/63668 não conservaram células de camada;resíduosSIMPLE convergiram,mas são rejeitadas como estudo novo de camadas. Fina passa `checkMesh`,178298células (+12086),porém diverge em23iterações/saída−8;Cd4e24 é lixo numérico, **não resultado físico**. Segunda tentativa independente comPCG/DIC,2correções nãoortogonais e relaxaçõesp0,1/U,k,omega0,25 também diverge. Dados/dicionários/malhas/logs e campos escritos estão em `aero_camadas/`,≈99MB. `validated_cd:null` e nenhum desses números substitui faixaCd anterior. A geometria ainda é piloto,não carro equipado;convergência/parede/independência continuamabertas. Não repetir essa mesma malha/solver como se fosse nova validação.

Protegidos mais3executores históricos com`--historico`: `gerar_cad_eletrico.py`, `calcular_integracao_eletrica.py`, `consolidar_eletrica.py`;config antiga marcadaHISTORICO,sem apagar seusdados. Assim2NG/AGM12V/MPPTs antigos não voltam a ser confundidos combaselineUS5000/150-60. Oshelpers geométricos continuamreutilizáveis.3testes verificam rejeiçãoantescriararquivos.

Reprodução adicional:

```bash
PYTHONPATH=src .venv/bin/python scripts/desenvolver_integracao.py
PYTHONPATH=src .venv/bin/python scripts/integrar_freios_massa.py
PYTHONPATH=src .venv/bin/python scripts/desenvolver_protecoes_fixacoes.py
PYTHONPATH=src .venv/bin/python scripts/detalhar_rotas_cad.py
# Os dois executoresCFD exigem destinos ausentes; preservar diretórios entregues.
PYTHONPATH=src .venv/bin/python scripts/refinar_camadas_aerodinamica.py
PYTHONPATH=src .venv/bin/python scripts/estabilizar_aero_fina.py
```

Última suíte227testes passou;Ruff passou. A reexecuçãoI25 após atualização doYAML preserva números e registra configuração efetiva. A revisão35,lista únicaA01–A16 eQA foram atualizadas;nenhuma decisãooriginal,aprovação final ou viabilidade física foi inferida. A etapa técnica completa continuaaberta,com camposCFDrejeitados segregados e dependências físicas explicitadas.

## Integração final deste checkpoint — varianteGX e BOM

A dependência deGX foi tratada por alternativa comercial **integrada ao inversor**,sem central própria ou gatewayexterno:seleção provisóriaMultiPlus-II GX48/5000/70-50,PMP482506000.220V/60Hz configuráveis,31kg565×323×148mm,4000/3700W e18Wvazio constam no manual. A saídaBMS-CAN500kbps serve aoUS5000;MPPT150/60 deveusarVE.Direct,não ligar comoVE.Can nessa porta. CANtipoA,DVCC/firmwares/limites epartidas continuam a configurar/ensaiar. Essa seleção substitui o candidato regular nas saídas atuais e está consolidadaA05/A15,sobDEC061/056.

**Parâmetros atuais que prevalecem sobre os parágrafos anteriores:**massa3974,02552776kg,margem275,97447224kg,CGx2,018029021/y0,002237209/z0,928796684m e eixos1986,491737/1987,533791kg. CGbase/instalação e limitesOEM seguem condicionados. ReexecutadosCAD,inventário,massas/dinâmica,FEM12casos,energia,I27/I29,36envelopes/54térmicos,24freios,648fixações e rotas. Os16perfis antigos da massa3973,026kg foram retirados do diretórioativo;bytes preservados noGit91be8af e lista de retirada em `output/perfis_massa_anterior_apos_gx_20261110.json`. Perfis4250kg e demaisresultados atualizados permanecem identificados.

A grade1008 foi reexecutada com a nova massa;melhores700Wmantêm290,875/292,8854167dias na resolução15min,por reservas. Sensibilidade1500W/reserva20/30 passa348,8541667dias. Cronologiahídrica foi regenerada:9572eventos e erro≤9,1e−13L. I25a5min/1kWhipotético agora48,06652/26,64640km,sótração40/80;comserviços24,15936/13,39311km. Não extrapolar essas casas decimais como precisão física ou operação segura de estrada.

`consolidar_bom_atual.py` resolve26linhas canônicas e exportaJSON/CSV em `bom_atual/`. Preços primários de listaVictron2026Q2USD C,semVAT:GX1093USD,MPPT150/60-Tr393USD,subtotal1486USD. Mantém50990EUR do veículoSK e439BRL histórico do cooktop **separados**,sem total convertido. Todas as linhas de preço instalado seguemnull;frete,tributos,montagem e disponibilidade não inventados. O catálogo de preços tem envelope ligeiramente diferente do manualGX;CAD mantém565×323×148mm do manual,com medição antes de congelar. MPPT3kg já integra a reserva15kg;BOMnão duplica essa massa.

Nenhuma seleção técnica provisória é aprovação humana ou comprovação da missão. Permanecem limitações reais de interfaceDC,apoios/eixosOEM,partidasHVAC eCFDequipado/CHT. Não declarar a etapa integral concluída. Comandos executados e hashes estão nos logs20261110 e no manifestoQA atualizado.
