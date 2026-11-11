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

## HVAC — revisão documental e análise72+12casos

A pesquisa continuou após ocheckpointGX e localizou manualDometic **FreshWell3000-O-16s,12/12/2018**,espelhado no distribuidorJacksons. PDF8.039.424bytes,SHA256`12246bf2a261161a4b1778780fa59a8ba06edda53ba8670765d1b96f6265680b`,cache `/home/mhc/motorhome_referencias_tarefas/freshwell-conferencia-20261110/`. Página29 foi extraída e renderizada/conferida visualmente:2700WtérmicosISO5151,220–240V50/60Hz e5,1/6,2Anominais de refrigeração,21kg. **Há portanto suporte documental220V/60Hz para essa revisão**,superando a lacuna genérica anterior. Omanual não confirmaSKU adquirido;cadastros atuaisSKU9105306675mostram dados de capacidade conflitantes1758/2700W,não importados para a revisão2018. PDF oficial indexado98740excedeu limiteweb(76MB),e downloadterminal retornou403;foi usado manualoriginal espelhado comhash,sem fingir acesso primário completo.

Omesmomanualindicafusível5A,abaixo dos6,2Anominais60Hz:abrir questão de coordenação/curva/revisão,sem escolher5A automaticamente nem declarar impossibilidade sem curva.6,2A×220V=1364VA não são watts ativos nem corrente de partida. TriagemP2corrigida de989VA deoutrarevisão para1364VA de estudo,pf1estimado;256combinações reexecutadas. A energia média3kWh/dia continua hipóteseDEC046,separada da potência;por isso não há nova alteração das missões/massas.

`comparar_hvac_revisoes.py` executou72combinações de ocupantes1/2,ganhos solares0,8/1/1,3/1,6,condução0,8/1/1,3 ecapacidade70/85/100%nominal;12cenáriosPF/partidas hipotéticas. Carga-base continua2515,898/2645,898W;nominal2700deixa184,102/54,102W. Essa margem pequena não comprova suficiência33°C/25°C nemcurva em60Hz. Dados completos em `hvac_revisao/`. Webasto3,5kW/teto50Hz já foi comparado/rejeitado;ColemanUB11/UB15primário115V não foi adaptado ou instalado e não teve capacidadeBTU inferida pelo nome. Não são opções220V aprovadas. A06eitem32agora distinguem revisão elétrica documentada de placa/instalação/térmica ainda condicionadas.


## Interfaces espaciais, chapas e impacto de massa — continuação10/11/2026

Executados `redimensionar_fixacoes.py` e `verificar_chapas_3d.py`. Métodos e limites detalhados em [proteções/fixações](PROTECOES_SERVICOS_MODELO.md). Novo solver de grupo espacial verifica6equilíbrios e distingue tração do parafuso/compressão do apoio.378alternativas,54envelopes×216cargas e18seleções locais condicionais,utilização máxima0,97135. O estudo antigo648casos com10falhas não foi apagado. CADSTEP com18chapas perfuradas reimportáveis em mosaico,sem atribuir pontos de ancoragemOEM.

Elasticidade3D real em9casos de tira local,4malhas por componente e quinta0,75mm no inversor:deslocamento final varia1,547%inversor/1,817%tanque. Ambos satisfazem critério de estudo2%;picos de engaste não são tensões convergidas. Equilíbrio e energia conferidos independentemente;campos/malhas/tensores emNPZ. Não é modelo da chapa perfurada inteira ou carroceria. FixaçõesOEM/prying/contato/fadiga/estrutura da cama ocupada continuam delimitados.

Chapas somam55,7511kg **brutos de comparação**. Como suportes existentes são reservas agregadas, não foi inventada substituição líquida. Sensibilidade conservadora com adição integral:4029,77663kg,margem220,22337kg,eixos1993,1696/2036,6070kg;consumo40/80=0,227089/0,408010kWh/km(+14,1745kWh nos7000km). Massa-base3974,02553kg e missões existentes não foram alteradas;limitesOEM por eixo desconhecidos. Água do boiler15L verificada localmente sem somar massa hídrica global.

Corrigidas referências desatualizadas3973kg na revisão35/A10 para3974kg. Fonte única recebe `development.mounting_redesign`,com metadados/hipóteses;DEC001–061 intocadas. I25 reexecutado630casos para vincular a configuração vigente,sem mudar entradas energéticas. Nenhuma aprovação humana ou instalação física inferida.

```bash
PYTHONPATH=src .venv/bin/python scripts/redimensionar_fixacoes.py
PYTHONPATH=src .venv/bin/python scripts/verificar_chapas_3d.py
PYTHONPATH=src .venv/bin/python scripts/desenvolver_despacho_i25.py
PYTHONPATH=src .venv/bin/python scripts/registrar_execucao02.py
PYTHONPATH=src .venv/bin/python -m pytest -q
ruff check src scripts tests
PYTHONPATH=src .venv/bin/python scripts/verificar_desenvolvimento.py --registrar
PYTHONPATH=src .venv/bin/python scripts/verificar_desenvolvimento.py
```

230testes passaram,Ruff passou;QA integrada incorporaCAD perfurado,energia/elastostática3D,massa eproveniência. Etapa técnica integral continua aberta;próximas frentes são orientação/furação real das interfaces,contato/ancoragemOEM,carroceria equipadaCFD e compatibilidades documentais já delimitadas.


## Alternativa comercial de teto1540Wp — continuação10/11/2026

Pesquisa primária localizou a fichaMaxeon544454revA/abril2022 paraSPR-MAX3-380-COM e390-COM. PDF original espelhado emSolSol:923002bytes,SHA256d6c76ef9231cb1621d8401a46fbef617724e6bc6ea873bb3f4658261fef75757;extraído/renderizado e página2 conferida. AURLprimária indexada consta emsources.maxeon3_2022;download primário falhouTLS,não foi simulado acesso. Cache em `/home/mhc/motorhome_referencias_tarefas/maxeon-conferencia-20261110/`.

Implementado `comparar_teto_maxeon.py`,entradasdevelopment.roof_maxeon_comparison.2módulos380+2módulos390,total1540Wp/76kg;cada1,046×1,690×0,040m disposto transversalmente. Com20mm entre módulos e25mm em cada ponta,comprimento4,294m/cabine+teto estimados4,30m,sobra6mm extras;largura1,69m/envelope1,82m. CADSTEP/GLB com4corpos é arranjo plano,depen­dente de curvatura/tolerâncias/apoios/manutenção/estoque. Não se inventou SKU385W nem se reduziu a meta solar.

Duasstrings mistas380+390 iguais2S2P:Vocfrio com tolerância3%=171,4776V eIscquente13,9626A. **150V incompatível**;250/60 pode ser comparador para teto sozinho usando35A conservador do conflito documental. Portáteis2S2P somadosjá35,9626A mesmo usandoIscportátilSTC,não demonstram compatibilidade35A.4Sportáteis reduz a24,9626A,mas amplia mismatch e precisa validar limites térmicos/proteções.72comparações comI–V reduzidas estimadas,não curvas medidas:perdas0,657–27,272%;não usar superioridade energética como aprovação elétrica. Uma saídaMPPT não conecta bancos de armazenamento.

A11 registra alternativa preferida provisória para integração posterior,sem instalar ou mudar silenciosamente massa-base/replays1350Wp/MPPT150-60. Mantêm-se comparaçãoDEC054,meta1540Wp e interfaceDCexterna não demonstrada. Campos numéricos/CAD/JSON em `teto_maxeon/`. Novos testes verificam correntes/tensões de strings idênticas e efeito térmico;QA confere72comparações,limites eproveniência.

```bash
PYTHONPATH=src .venv/bin/python scripts/comparar_teto_maxeon.py
```

Teste analítico de strings idênticas detectou amostragem que omitia o cantoMPP (corrente5,99909 em vez6A). Corrigida a interpolação para incluir cadaImp exato;teste original preservado,72comparações reexecutadas. Falha inicial documentada emoutput/testes_teto_falha_20261110.log. Suíte final232testes/Ruff passaram.


## Cadeia integrada1540Wp — execução completa com configuração congelada

Ocenário `development.integrated_scenarios.maxeon1540_independente` na fonte única é resolvido por `motorhome.cenarios`;não é um segundoYAML editável. `MOTORHOME_SCENARIO` seleciona a sobreposição com saídas isoladas. Snapshots porhash e entradas por executor registram os valores efetivamente usados. Ocasobase1350Wp permanece separado. `executar_cenario_integrado.py` executou14comandos sem falhas,congelando a configuração entre etapas. QA independente do cenário passou297controles na primeira cadeia;novas conferências acrescentam controle sem interface.

Configuração de comparaçãoDEC054:2Maxeon380+2Maxeon390=1540Wp,250/60teto e150/60portáteis,ambos com saída de referência de serviços;nenhuma dessas saídas é ligada aoHV. AlocaçãoFV/recargaB são hipóteses energéticas sujeitas a interfaceexternaOEM não demonstrada. Comparação compartilhada72I–V permanece separada,não aprovada. Massa3976,52553kg,CGx2,01780418/y0,00244880/z0,93071369m,eixos1987,96299/1988,56254kg,margemPBT273,47447kg. CGbase,geometria e limites por eixo não validados. DoisMPPTs acrescentam3kg enquanto a troca de módulos reduz0,5kg,sem duplicar reserva.

**Correção física transversal:** a água limpa total100L é agora posicionada85L no tanque e15L no boiler cheio,sem duplicar massa. Isso corrigeCG/eixos/transferência dinâmica sem alterar a massa total ou o consumo plano. ReexecutadosCAD/massas,162sensibilidades,36envelopes e24freios nos dois cenários. Massa-base1350Wp permanece3974,02553kg,mas seuCG/eixos anteriores ficam substituídos pelos arquivos regenerados.

FVfixa gera5,86376kWh/dia no diaidealizadoSãoCarlos21junho/25°C/UR50/vento0;portáteis geram0,37133kWh na política08–16ou8,04051kWh na00–08,com ângulos fixos por parada e logística. Não é meteorologia real ou potência constanteSTC. I25reexecutou630MILP:5min/mínimo1kWhipotético,40/80km/h,crédito solar inicial0;51,4898/28,5493km sótração e27,1869/15,0742km com serviços cíclicos. Mínimo3kW não iniciaDCdireta. I27 mantémSOCfinal30%,100/80% iniciais separados.

Grade histórica de1008políticas para7000km:700Wauxiliar,massa atual e velocidades constantes;243,84375/244,88542dias por reservas10/20×20/30,20km/h na janela20–04,≤8h/dia. A busca densa posterior de5268 pontos encontrou242,802083/244,802083dias (partida18h;20,8/20km/h); refino extra local não melhorou esses tempos. A busca fixa de796 pontos é comparador com242,885417/244,885417dias. Sensibilidade local posterior de294 políticas em15/5/1min encontrou242,802083/244,802083 dias (15min),248,763889/250,760417 dias (5min) e248,784028/250,779861 dias (1min),reservas10/20×20/30. Diferença de≈6dias revela sensibilidade ao limiar mínimoDC1kW hipotético; ver seção de resolução temporal na revisão geral. Nenhum resultado é ótimo global ou missão fisicamente viável. Controle sem interface não recebeFV na tração. Cronologiahídrica8004eventos/8replays,2127reabastecimentos/descartes,erro≤9,1e−13L,apenas estacionado e fora montagemFV;postos reais continuam hipotéticos.

**Incerteza propagada:** `sensibilizar_cenario_integrado.py` executou972pontos(massa,velocidade,Cd,Crr,ρ,η,área),120missões de extremos/alocações/buffer e36ensaiosDCdiários. Serviços7,22883kWh/dia continuam médiaDEC046 com picos separados. Envelope40/80km/h na massa3976,53kg:0,15919–0,30607/0,30186–0,55134kWh/km;extremos de caixa,não intervalo estatístico. Bateria/PBT/teto/cargas coerentes;resíduo energético máximo≈2,11e−8kWh.

**Buffercomercial:**32casos usam umUS5000dedicado,4,8kWhnominais/4,56kWh de crédito acima da reserva constante,39,7kg adicionais;crédito inicial0. Massa4016,22553kg é limite inferior,sem suportes/conversor/cabos desconhecidos. Exemplo40km/h,00–08,reservas10/20:direta1kW327,0104dias;buffer1kW278,0313dias;direta3kW não conclui no horizonte1500dias,buffer3kW279,0104dias. São resultados condicionais,não prova de potência aceita/BMS/OEM. O buffer não integraCAD/BOMbase e não usa a bateria de serviços.

**CFDequipado efetivamente executado:** novo deck equivalente contínuo4,244×1,690×0,040m,gap40mm ao topo do corpo piloto;suportes/gaps entre módulos omitidos. Três malhas101030/128458/217494 passamcheckMesh e convergemSIMPLE,kOmegaSST,piso móvel,80km/h. Cd diagnóstico0,68313391/0,66691895/0,63374383,variação final5,23%. Históricos/forças,y+,campos,dicionários e gráfico extraídos. `validated_cd:null`;refinamento local com resolução do deckfixada não sustentaGCI. SensibilidadeCd ampliada até0,72;central antigo0,62487678 permanece hipótese,não substituição por medição. Aref é referência comum de normalização,sem confundir com área frontal equipada medida.

**CFD — malha de resolução adicional:** `scripts/executar_aero_malha_adicional.py` refinou corpo/deck para níveis5/6, manteve refinamento de esteira e gerou malha de1.034.158 células; `checkMesh` passou. SIMPLE paralelo em quatro subdomínios avançou394 iterações em900s. Cd=0,60058185 e faixa relativa0,0175% nas últimas50 iterações são somente diagnóstico de estabilidade do coeficiente. O limite encerrou o solver antes de `residualControl` (na última iteração completa: Uy inicial4,65e-5; p1,22e-4; erro global de continuidade4,22e-9); não se calculou y+. Resultado registrado em `entregas/aero_equipado1540/malha_adicional_1/resumo.json`, histórico em `historico_cd.csv`, sem alegar convergência formal, independência de malha, GCI, Cd validado ou validação física. Arquivos temporários de decomposição foram removidos; mesh e setup reexecutáveis ficaram preservados.

**P6 — sensibilidade de ventilação mecânica de apoio:** `scripts/sensibilizar_ventilacao_mecanica.py` combina ocupação1/2, metas de estudo800/1000/1200ppm, geração de CO₂12/18/24L/h·pessoa, queda de pressão20/50/100Pa, eficiência total20/35%, diferença térmica0/8/15K e operação8/24h, total648 casos. Sob a hipótese central já usada na ventilação natural (18L/h·pessoa; exterior420ppm), duas pessoas a1000ppm requerem62,07m³/h em balanço estacionário bem misturado;30m³/h corresponderiam a1620ppm. Para62,07m³/h,50Pa,20% e ΔT8K, a potência estimada é4,31W e a carga sensível de ventilação166,3W. Metas e parâmetros são sensibilidades, não limites normativos; não foi escolhido/instalado ventilador e a carga latente fica pendente sem umidade de projeto. A ventilação natural continua prioritária, mas não garante vazão em calma térmica.

**Fixações com orientação correta:** inversor usa planovertical e força gravitacional transformada;afastamentoCG vem das dimensõesCAD×fatores1/1,25/1,5,em vez da altura universal anterior.378alternativas/18seleções,utilização máxima0,99361 e33,13793kg brutos de chapas. Sem substituição líquida/ancoragemOEM inferida.11Tet4mostram que o inversor não satisfazia2%(última2,822%);não foi relaxado o critério. NovoTet10/4pontosGauss em3malhas satisfaz0,5504%;tanqueTet4satisfaz1,1443%. Testes verificam partição/gradiente,reprodução afim,translação/rotação rígidas e equilíbrio. Picos de engaste continuam não validados. Massa das chapas é comparação separada,não soma automática ao veículo.

Os35itens receberam índices locais com requisito,método,condições,fontes ehashda evidência. Teorias ainda emtemplate foram preenchidas com equações reais,sem apagar teoria anterior. `validacao.md` mantém aceite humanoPENDENTE. Documentos de bloqueios/plano foram conciliados para não descreverCFD existente como ausente nem mandar rodar o reconciliador histórico incompatível.

```bash
PYTHONPATH=src .venv/bin/python scripts/executar_cenario_integrado.py --cenario maxeon1540_independente --reexecutar
PYTHONPATH=src MOTORHOME_SCENARIO=maxeon1540_independente .venv/bin/python scripts/verificar_cenario_integrado.py
PYTHONPATH=src .venv/bin/python scripts/executar_aero_equipado.py # somente destino novo
PYTHONPATH=src .venv/bin/python scripts/analisar_aero_equipado.py
PYTHONPATH=src .venv/bin/python scripts/verificar_chapas_3d.py
PYTHONPATH=src .venv/bin/python scripts/verificar_chapa_quadratica.py
PYTHONPATH=src .venv/bin/python scripts/registrar_execucao02.py
PYTHONPATH=src .venv/bin/python scripts/preencher_metodos_itens.py
```

Resultados novos em `entregas/integrado_maxeon1540/`,`entregas/aero_equipado1540/` e índices por item.240testes/Ruff passaram antes da conferência final dos manifestos. DEC001–061 seguemintactas. O pacote computacional está reproduzido;validação física e aprovação humana não estão concluídas e permanecem explicitamente bloqueadas emB01–B12/A01–A16. Nenhum relatório acadêmico/slides/envio foi preparado.

## Complementos finais24/48h,prioridades e evidênciaPylon/custo

`simular_prioridades_servicos.py` acrescenta72casos e teste de conservação/limites,sem fixarSOCoperacional doBMS.3módulos podem estender a alimentação simulada para48h retirando cargas:isso não atende o perfil completo,que continua exigindo4/5módulos por reservas20/30%. Consumoextra docontrole0/5/15W é sensibilidade,não equipamento instalado;I29permanece com7,22883kWh/dia completos. MédiasDEC046 preservadas e notas de cada carga corrigidas:explicação doboiler estava indevidamente repetida em todos os aparelhos. Agora3kWh/diaHVACéhipótese de uso,referência comercial2018separada,sem atribuir hábitos ao fabricante.

`comparar_bancos_servicos_cad.py` produz4STEP completos para2/3/4/5US5000,com remoção geométrica dos3originais antes de inserir a alternativa. Todos sem colisõesAABB com sólidos existentes;folgas10mm eprodutoemuso móvel ainda não validados.24h2/3módulos:9,6/14,4kWh;48h4/5:19,2/24kWh.12casos de suporte de banco completo incluem≈4,53kg dos próprios trilhos,sem somá-los novamente à reserva de massa.5módulos/5ghipotético têm esforço de trilho e grupo de4parafusos calculados,masfuração/apoiosOEM/fadiga/contato permanecem bloqueantes.

`conferir_protecao_pylon_documentada.py` documenta dado primárioUSSeries2024:US5000<2000A/1ms. Download276588bytes,SHA2566b85fb621d4f102863e99208e5d3467adc65f376e75d37fbde4ee7ee928bd139,página renderizada e coluna confirmada. Triagem1–5módulos soma teto condicional de corrente entregue,no intervalo declarado;144curtos prospectivos e56>20kA são preservados,sem deduzirI²t de interrupção ou BMSseguro sob falha.

ListaVictron2026Q2USD C,página14renderizada/conferida,PDF2351739bytes/SHA25683275209e603872733eb06ea0761bd65820bf5b93f6068f9e5467b691862cd80:250/60-TrSCC125060221=465USD,3kg,200×250×95mm. BOM1540passaUSD1951(GX1093+150/60 393+250/60 465),mantendoEUR50990eBRL439histórico separados. Sem cotação instalada/frete/impostos. Preços de revendedores dePylon/Maxeon encontrados não tinham identidade/revisão suficiente para fechar compra;valoresnão confiáveis ouplaceholder não foram incorporados.

Revisão da fonte única:1.1.1-execucao1540,data10/11/2026. Cenário temversão/fontes por parâmetro;massas são hipóteses,não dadosMaxeon. Catálogo externo atualizado com fontes/hash;PDFs de fabricantes continuam emcache,sem redistribuição integral. Matriz61agora liga parâmetros e evidências vigentes comhashde seção original;61decisões intocadas. Os35itens têm teoria/método/índice/fontes específicas emsuas pastas,revisão humanaPENDENTE.


### 11/11/2026 — HVAC, integridade e QA de continuidade

Reexecutado `scripts/comparar_hvac_revisoes.py`: 72 casos térmicos, 12 elétricos e oito comparações nominais de capacidade foram gravados em `entregas/desenvolvimento_2026-11-09/hvac_revisao/`. O campo ISO5151 de 1758 da página oficial do FreshWell SKU 9105306675 conflita com o headline 2700 W; valor adjacente 5998.54 BTU/h sugere interpretação por conversão, sem resolver a unidade/capacidade aplicável. Margens 1/2 ocupantes: +184/+54 W a2700 W; −758/−888 W a1758 W. FreshJet FJX7 3000 consta apenas como comparador. Capacidade a33/25°C, partida, fusível e instalação permanecem não demonstrados.

Atualizado o registro do item32 e o índice de evidências pelo hash da nova saída; verificadores agora cobrem o conflito documental e a tabela comparativa. Resultado desta continuidade: `pytest -q` — 244 passed; `ruff check src scripts tests` — passou; verificador integrado — passou; verificador de desenvolvimento — passou com 181 entradas e 1.258 saídas. O verificador de desenvolvimento mantém `stage_complete:false`, zero aprovações humanas e missão física não demonstrada. Manifestos integrado e desenvolvimento foram registrados pelos seus modos oficiais e conferidos novamente sem registro. Os testes/verificações são de software e consistência, não ensaio de veículo. Perguntas para o professor em `PERGUNTAS_PARA_PROFESSOR.md`.
