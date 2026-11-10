# Retomada ativa — execução técnica02,09/11/2026

**Pedido atual:** executar autonomamente todo desenvolvimento técnico dos35itens sobDEC001–061; sem novas aprovações individuais e sem relatório acadêmico/slides. **Etapa completa ainda aberta**, não confundir este checkpoint com conclusão. Não esperar revisão do usuário para continuar frentes executáveis.

- Worktree exclusiva `/home/mhc/motorhome_solar_codex_tarefas`, branch `hub/tarefas-motorhome-com-codex`. Partida técnica29defc4;2ce7e81era só handoff. Nunca editar a outra worktree. Push paraorigin/main já autorizado na sessão. Registro61 intacto, mesmoSHA anotado abaixo.
- Primeiro ler `AGENTS.md`, `docs/EXECUCAO_TECNICA02.md`, `docs/REVISAO_TECNICA_EXECUCAO02.md`. Parâmetros **1.1.0-execucao02** em `config/parametros_globais.yaml`; seção development contém geometrias/posições/materiais/hipóteses. Lista únicaA01–A16 mantida em `docs/APROVACOES_FINAIS_PENDENTES.md`.
- **Novos resultados:** `entregas/desenvolvimento_2026-11-09/`,~135MB/676saídas hashadas+manifesto/QA.2layouts+2tetosSTEP/GLB,162massas/CG/eixos,164dinâmicas,12FEMtrilhos,CFDcabine3D3malhas+4transientes,36IVmismatch,32replays+1008gradeI29,36aceleraçõeshipotéticas,54bateriatérmica,24freios2D,radiador2D/caboHVreferência reexecutados.
- LayoutA cama fixa: **3973.02552776kg**, margem276.9745kg até4250antesinterfaceDC/buffer não instalados. CGx2.01669/y.001262/z.927898m; eixos1987.31/1985.72kg **condicionados** aCGbase/posições estimados. LimitesOEMeixos desconhecidos. AABBsemcolisões entre equipamentos/rodas estimadas; corredor.454m/porta lavagem.59m. Bconversíveltemreserva.474m<.48m e84kgportáteiselevados; não recomendado sem rever.
- **700W auxiliares de tração estimados**, separados dos serviços7.2288254kWh/d. Serviço3US5000/14.4kWh/119.1kg;48h exige4/5módulos conforme reserva. `consumo_plano(...,aux_traction_kw=...)` novo opcional mantémdefault0para reproduzirhistórico. Faixa0/300/700/1500W muda ótimo: grade1008melhor700W20km/h20–04h,290.875/292.8854dias;0W10km/h216.84375dias;1500W30km/h346.84375dias. **Só melhor grade, mínimoDC1kW hipotético, não global/físico**. FonteSãoCarlos21junho repetida; ambasSOC100%;≤8h/d;plano;semrecargaexterna. Portáteis45°Norte fixos por parada nos melhores casos. Água/sanitária nos replays por demanda diária agregada, fontes por parada hipotéticas; cronologia fina/locais não comprovados.
- I27Jensen+min e(v) sem recargaHV:20.6904km/h;100→30%=351.701km/16.998h;80→30%=251.215km/12.142h. Não condução segura17h nem otimização solar. I28limitador90:0–100nãoalcançável;9.23–14.19s0–90sóenvelope de hipóteses de redução/aderência, não curvaOEM.
- CFDcabine: SIMPLE2500iterações **não convergiu/rejeitado**. PIMPLE300s apósrestart,2400/8100/19200células,dtmax.1/.05médiaúltimofino50.3203°C,max53.0744°C,estrat3.2827K.Δmédiaentre2malhas.104709K/meiopasso.0005106K. Balançofaces250–300serromáx.0482% trocaabsoluta. Campos/dicionários/logs reais conservados. NãoCHT/CADOEM/transientematinal3D/y+validado;redeantiga49.0785°Cnoon preservada. HashYAMLcompleto retirado doCFD porqueevoluiuduranteexecução;extração física+dicionários usados+hashredeorigem conservados.
- Aero diagnóstico efetivo y+corpo31.733–2123.142,médio516.551 no166212células;Cdcontinuanãoindependente7.07%variação. Não novaCFDaeroequipada. Host tinha2.45GBRAMdisponível/7.2GBswapusados; evitar malha volumosa sem avaliarrecursos. `scripts/diagnosticar_yplus.py` reproduzsemalterarcasooriginal via --caso-cacheNOVO.
- MPPT: **150/60-Tr candidato provisório**somente serviços48V:50AIsc/60Asaída/145Voperacional;Isc36.48A/coldVoc135.408Vpassamtriagem;IV/proteções/BMSainda não demonstrados.250/60rejeitadoprovisoriamenteconflitoficha35A/manual60A. GenasunGVB8boostrejeitadopara190WpIsc9.17>8A. Meta1540Wpfixos mantida; só1350Wpcomcaminho48Vcreditados;1600Wpportátilsóparado. Nenhuma transferência de energia armazenada entre bancos/buffer novo.
- **QA:**208testes passaram,Ruff/estrutura35/7/auditoria passaram;QA90controles,140entradas/676saídas porhash. `output/*execucao02*`. STEP4arquivos reimportados sólidos positivos. Verificadoratual `scripts/verificar_desenvolvimento.py`; executar sem--registrar para conferência. Registro61SHA intacto. `conciliar_dec061.py`agora recusa1.1 antesdealterarmanifestohistórico: reproduzirbaseline no29defc4; não refrescarhashesantigos.

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

CFDusaOpenFOAM2412no cache referido abaixo; scripts `desenvolver_cabine_cfd.py`/`refinar_cabine_transiente.py` exigemdestinosnovospara não sobrescrevercampos. Verificação porfaces: `scripts/verificar_campos_cabine.py`. Manifestonovoéregistrado com--registrar só após alterações deliberadas. Não rodarconsolidadoresantigos que sobrescrevamlistaA01–A16.

**Próxima execução do agente:** detalharfixações/rotasCAD e proteção/comandoSOC; refinar aeroequipado/camadas com limites de recursos; confrontarcotas comcarroceriaimportada; completarI25despachotemporal começandocomenergiasolardodia emvezdesótetoenergético. Integração térmica atualécaixaequivalente, nãoCADOEMequipado. Não repetirpesquisaDCindefinidamente: mínimo/protocolo/autorizaçãoOEMnão demonstrados após fontesVenema/Sungrow; conservarcontrole e seguiroutrositens. Eixos/pressões/mapas/redutor/óleoOEM,HVAC220V/curvas33°C,custoBRLinstalado ehardwaredeproteção/controlepermanecemlacunas,não aprovados.

Ambiente: terminalcomrequire_escalated,defaultbwrapfalha. Houveumtimeoutautoreviewresolvidoporúnicoretry; nenhum bloqueio de permissão restante. Nada enviado a terceiros/comprado/instalado;nenhum ensaio físico/homologação. Esta nota éhandoff para continuaçãoautônoma, não nova lista detarefas para usuário.

---

## Histórico — estado anterior à execução02

# Retomada — pós-DEC061, 09/11/2026

**Estado:** execução solicitada concluída e publicada; próximo trabalho depende de evidências técnicas, não de perguntas genéricas. 35/35 itens iniciados, **0 aprovações humanas finais**. Usuário permite seleção técnica provisória (DEC061), preservando decisões anteriores e lista única de aprovações.

## Onde e o que ler

- Trabalhar somente em `/home/mhc/motorhome_solar_codex_tarefas`, branch `hub/tarefas-motorhome-com-codex`. Não editar a outra worktree `/home/mhc/motorhome_solar_codex`.
- Remoto SSH `git@github.com:MHC-CodeSmith/STF_MotorHome.git`; `main` remoto e HEAD técnico conferidos em **`29defc4318f7ebc3984782317b8a8b96654d2ef5`**. Implementação: `97b1f0c`; pacote final: `29defc4`. Árvore limpa antes desta nota. Push já autorizado na sessão.
- Ler `AGENTS.md`, registro integral `docs/decisoes_motorhome_2026-10-28.md`, depois `docs/INTEGRACAO_POS_DEC061.md`. Plano e bloqueios: `docs/PLANO_EXECUCAO_POS_DEC061.md`, `docs/BLOQUEIOS_POS_DEC061.md`.
- Fonte ativa **`config/parametros_globais.yaml`**, revisão `1.0.0-pos-DEC061` (161 parâmetros + fontes/cargas/BOM). Histórico/reuso: `config/registro_cenarios.yaml`. Matrizes: `docs/MATRIZ_DECISOES_61.md`, `docs/REVISAO_35_ITENS.md`. Lista única: `docs/APROVACOES_FINAIS_PENDENTES.md` (16 escolhas). Execução e arquivos: `docs/EXECUCAO_POS_DEC061.md`.

## Invariantes e bloqueios

- **Arquitetura B escolhida**, interface externa DC OEM autorizada; compatibilidade/mínimos/protocolo/isolamento **não demonstrados**. Não abrir/modificar HV/BMS/cabos OEM; não conectar diretamente ao pack. Antigo caminho PV→bateria de serviços48V→inversor/EVSE/OBC→tração descartado. Nenhuma energia armazenada cruza entre bancos. Buffer dedicado só comparação, inicia vazio, não instalado.
- E-Ducato L3H2 geométrico; candidata coerente **SK MY25 505.GG1.2**: PBT4250kg, tara2790kg,110/98kWh nominal/útil,400V,205kW/410Nm pico,limitador90km/h,50990EUR semIVA. Fonte FiatSK20/03/2026 em YAML; limites por eixo/mapas/redutor/importação faltam. Não misturar mercados. 0–100 não atingível nessa candidata. I33prescreve108km/h como ensaio acadêmico do componente, não velocidade atingível. Pneus/suspensão OEM inalterados.
- Meta1540Wp fixos +1600Wp portáteis só parado, ângulos fixos por parada. Arranjo antigo3JA450+190W tem módulo190W de baixa tensão sem caminho48V comprovado: novo replay credita **1350Wp**, mantendo meta1540 em aberto. MPPT compartilhado e comutação não validados.
- Serviços48V LiFePO4 modular/BMS integrado; AC220V60Hz; média diária + picos separados. Natural ventilação, HVACsob banco e indicadores comerciais prioritários. Nenhum shedding físico/limiarBMS validado. Novo candidato3US5000/14.4kWh tem aplicação móvel ainda não demonstrada.
- I29principal7000km plano/velocidadeconstante, ambosSOC100%,≤8h direção/dia,sem recargaexterna, SãoCarlos21junho25°C/UR50/vento0 repetido como idealização. ERA5/rota7511.282km são complementos. Reservas10/20 vs20/30; I27separado100→30principal/80→30sensibilidade. Nenhum ótimo global demonstrado.
- Água100Llimpa/70Lcinza/cassete~20L,2×80kg+60kg bagagem; conservar água e massa. Reabastecimento/descarte adequado permitido. **`config/hidraulica_proposta.yaml` é arrefecimento água/glicol, não rede potável.** Nova curvaShurflo12V separada; QuickB315L500W candidato com frequência/aplicação móvel pendentes; ElgenaKB6 rejeitado na combinação pressurizada.

## Resultados caros já produzidos

- `entregas/etapa_pos_dec061/`: **972 casos de consumo,36 DCdireta/buffer,56 missões**, CSV diários e séries completas `.csv.gz`, campos2D `.npz`, rede térmica, hidráulica e BOM26linhas; 142 arquivos no diretório. Não sobrescrever resultados históricos anteriores.
- Missões:8controles param por reserva de tração;32porserviços;4atingemhorizonte;12chegadas **condicionais** (303.02–703.01dias). MínimoDC1kW é hipótese, NÃO dadoOEM. Controle percorre192.51–405.35km. Erro energético máximo~2.8e-8kWh. Janelas08–16 vs00–08 são comparação parcial, não otimização. Água/paradas sanitárias e shedding ainda não completos no replay.
- Serviços-base7.2288254kWh/dia;24h requer2/3US5000comreservas20/30%;48h4/5. Banco provisório3módulos119.1kg. BOM:440kgconversão conhecida+2790tara+320carga=**3550kg subtotal**,700kgaté4250 antes de móveis/isolamento/suportes/etc; variante3500excede50kg antes dos faltantes. Custo instalado **null**, não somar moedas ou OEM duplicado.
- Consumo central4250kg:40km/h~0.218kWh/km;80~0.407. FaixasCd0.5806668/0.62487678/0.65303585;malhas29527/63668/166212células,última variação7.07%,semcamadas/y+; não Cd final/GCI validado.
- I30novos camposrθ70/95mm²,102.17A,3malhas;I33solverr-zestendido para potência real de atrito descontadas resistências+regenhipotética0/40/80kW,malha/passo/massa. Materiais/geometriasOEMnão validados. I31é **rede equivalente**, não CFD3D; CFD3Dcabine/novasmalhasaero/FEAcrítica NÃO executados. I34/35modelosparametrizados antigos preservados;20/80kWnão são solar.
- Registro61foi encontrado em `/home/mhc/Downloads/decisoes_motorhome_61.md` e copiado sem edição:298721bytes,SHA256 `1e082c4961a57b865f008fa1daadd37e696bdb060f22c922596715096c793969`. Base anterior para reproduzir histórico: `2ef84f67c3aa820633b0565e92c0a23ea810302b`.

## Reprodução e verificações

```bash
PYTHONPATH=src .venv/bin/python scripts/conciliar_dec061.py
.venv/bin/python scripts/consolidar_pacote_dec061.py
.venv/bin/python scripts/verificar_pos_dec061.py
PYTHONPATH=src .venv/bin/python -m pytest -q
ruff check src scripts tests
.venv/bin/python scripts/verificar_estrutura.py
.venv/bin/python scripts/auditar_projeto.py --json
```

Último estado: **197testes passaram**, Ruff/estrutura/QAatual passaram;QAconfere61decisões/35itens/15entradas/138saídas/9complementos. Logs `output/*pos_dec061*`; manifestos numérico e pacote no diretório da entrega. Verificador histórico `verificar_entrega_integrada.py` retorna1 com UMA proveniência desatualizada (`resumo_freios.json`→código alterado);124hashes de artefatos antigos conferem. Não atualizar hash antigo para esconder isso.

Quatro runners (`calcular_interface_carga.py`, `calcular_agenda_portatil.py`, `construir_viagem_condicionada.py`, `simular_rota_real.py`) exigem `--historico`;guardas4/4testadas. Não usar seus resultados como baselineB.

Próximo avanço: P2/P4interfaceDC+documentaçãoOEM;P1/P3massa/eixos/CAD/CFD/fixações;P6cargas/aparelhoscompatíveis/água;P7térmicaOEM;entãoP5reintegrar. Divisão: P1=1,2,3,14,15,18,24,33;P2=6,7,9,23,30;P3=16,17,19;P4=4,5,20,21,22,28;P5=8,25,26,27,29;P6=11,13,31,32;P7=10,12,34,35. Entrega02/12/2026às06hAmerica/Sao_Paulo.

Ambiente: `exec_command` sem escalonamento falhava no bwrap; `sandbox_permissions=require_escalated` funciona. Limite de uso interrompeu revisão automática, depois resolvido; nenhum bloqueio de aprovação restante. Sem ghCLI; GitSSH funciona. Não reenviar e-mails/comprar/instalar nada; não declarar certificação. Esta atualização é documental, sem novos cálculos.

---

## Histórico anterior — não prevalece sobre o estado acima

# Retomada compacta — fechamento da conversa30/10/2026


## Checkpoint para a próxima conversa

Último commit técnico confirmado: **`5eca6c0`** (rota, interfaces e revisão35).
Em30/10, `git status --short` estava vazio antes desta atualização. Esta nota é
uma atualização documental posterior; não foram rodadas novas simulações no
fechamento. Os178testes e os replays descritos abaixo são da etapa28/10.

O usuário quer execução autônoma até fechar os35itens e uma revisão concreta
por item; não quer que dúvidas rotineiras sejam devolvidas ao professor.
A última pergunta foi se já havia rodado: foi confirmado que os sete casos
terminaram e que os CSV foram reabertos. O pedido atual é só salvar a retomada.
Não iniciar novos cálculos durante este fechamento.

Entrega mais recente para abrir primeiro:
`entregas/etapa_2026-10-28_rota_real/revisao_35_itens.html`,
`REVISAO_35_ITENS.md`, `resumo_rota_real.json`, `qa_rota.json`,
`rota_e_progresso.png`. MD/HTML/JSON têm a revisão dos35itens, não apenas uma
contagem de aprovações. Não repetir a resposta vaga “faltam35”: todos têm
trabalho parcial, com pendências físicas distintas. Ver também
`docs/REVISAO_35_ITENS.md` e `docs/ROTA_REAL_2026-10-28.md`.

Próximo avanço recomendado: melhorar a gestão de energia com previsão/reserva
para dias nublados na rota, usando os caches já adquiridos. A política histórica
interrompe por reserva dos serviços; não apresentar isso como prova de
inviabilidade global. Depois refazer os cenários e o replay. Continuam em
paralelo: compatibilidadeOBC/EVSE e proteções reais; mapasOEM/redução/óleo;
massa completa/eixos/CG/fixações; cotações/impostos/frete; CFD equipado com
independência; envelope térmico da cabine e calibração dos componentes.
Faltam incorporar os suplementos27/28 ao memorial, revisão cruzada, seminário
e vídeo com integrantes. Logo/pintura seguem para depois da parte técnica.

Comandos úteis (rodar da worktree exclusiva):
```bash
PYTHONPATH=src OMP_NUM_THREADS=2 .venv/bin/python -m pytest -q
.venv/bin/python -m ruff check src scripts tests
.venv/bin/python scripts/verificar_estrutura.py
.venv/bin/python scripts/verificar_rota_real.py entregas/etapa_2026-10-28_rota_real --fontes /home/mhc/motorhome_referencias_tarefas/rota-litoral-fontes-02
```
Os CSV de viagem estão comprimidos em`.csv.gz`; o verificador abre ambos os
formatos e confere hashes dos CSV descomprimidos. Não carregar todos no contexto.
Ler JSON/MD pequenos; preservar caches de fontes e resultados. Rede pública
pode retornar429: o coletor tem espera/reuso de cache. No terminal atual, shell
normal falhou com`bwrap: loopback: Failed RTM_NEWADDR`; chamada com
`sandbox_permissions=require_escalated` funcionou para leitura autorizada.

## Nova etapa28/10 — prioridade

Usuário mandou usar rota real/limites aproximados e executar o necessário nos35,
sem parar para perguntas interpretativas. SOC explicado: I27assume100→30% útil;
I29parte100%/reserva10%, serviços80%/reserva20%. [Rota](ROTA_REAL_2026-10-28.md).
RotaOSRM21pontos costeiros7511,282km,969passos,95478vértices; mantém marco7000km,
sem reescalar. DEM5km/1504pontos,ERA5horário14nós(~578km),21jun2025 em diante.
Céu limpo varia data/local; ERA5inclui nuvens. Cauda99h ausente descartada,
última hora22out2026às20h. Fontesbrutas15MB cache`rota-litoral-fontes-02`.
Política22–06h/máx8h porcalendário; montagem06–06h30,recolher21h30–22h.
Compara tetos60/80/90kmh, reduzidos por classe/perfilOSRM e limitador90.
PV12V sem crédito; mantém cargas6,428118kWh/dia, sem secagem. InterfaceOEMhipotética.
Céu limpo chegaChuí330,925/428,923/430,921dias; marco7000km296,929/387,919/390,917.
ERA5interrompe por reserva dos serviços4112,66/3462,12/3459,51km; é falha da
política atual, não prova global de inviabilidade. Seminterface80kmh avança242,43km.
Não certificado mínimo global. Testar previsão/reserva de dias nublados a seguir.
Módulos`rota.py`/`viagem_rota.py`,scripts`obter_rota_e_clima.py`,`simular_rota_real.py`,
`verificar_rota_real.py`,`gerar_revisao_35_atual.py`;config`rota_belem_chui_proposta.yaml`.
Cachefinal`rota-simulacao-03`; entrega`entregas/etapa_2026-10-28_rota_real/`,
CSVcompletosgzipsemperda,QA,mapa, revisão35MD/HTML/JSON.178testes passaram;
replay7casos confere clima/local/vias/energia/reservas/8h, resíduo1,13e−10kWh.
35itens têm trabalho iniciado; nenhum aprovado. Fontecatalogada/proveniência.
MemorialPDF/viewer26/10 preservados, suplementos ainda precisam ser incorporados.

## Continuação27/10 — ler primeiro

Retomada de`fd8ae1e`. Atual:[interface de carga](INTERFACE_CARGA_2026-10-27.md).
Config`interface_carga_proposta.yaml`, módulo`interface_carga.py`, scripts
`calcular_interface_carga.py`/`verificar_interface_carga.py`; reutilizam estados
da agenda anterior sem alterar os arquivos/hashes dela. EVSE0/6/8/10A, perdas
inversor/OBC separadas90%cada, perfisAC/DC e limite compartilhado3700W.
**0,658097kWh/dia do PV12V agora separado, sem crédito48V/HV**. PV48fixo4,848752;
total com portátil12,968297kWh/dia. Casa/perdas/standby6,428118kWh/dia.
I27:326,402651km semHV/344,767978km com interface **hipotética**. Tração100→30%
exato, serviços80→80%/reserva20%; I27sem8h. I29até8h/calendário: política7000km
em276dias inteiros =primeiro312,331887+274ciclos24,376711+último8,449272;
**não ótimo global nem previsão da rota**,21junSãoCarlos repetido.
NRGkick16A candidato: manual2602-04-1p20,230V50/60Hz,2,55kg; cache
`interface-fontes-01`,PDFexterno. OBCMY25 monofásico60Hz/PE/DR/faixas220/230V
ainda não comprovados. Cinco inícios de carga/dia cíclico; handshake não medido.
Entrega`entregas/etapa_2026-10-27_interface_carga/`; caches`interface-carga-02`
e`interface-carga-sem-hv-02`;01históricos.172testes/ruffOK;CSV/hashes reabertos,
viagem7000km e até8h/dia conferidos, resíduo~3,46e−11kWh; global intacto.
Anterior:[agenda portátil](AGENDA_PORTATIL_2026-10-27.md), caches
`agenda-portatil-03`/`agenda-portatil-grade15-01`,351,997km/202dias pertencem
àquelas hipóteses agregadas e não à interface nova. Potência nas rodas exportada;
eixo motor`null`. PDF/viewer26/10 preservados; suplementos fora do memorial.
Nenhum item aprovado. Próximo: aceitaçãoOBC/proteções/faixas e perdas reais.

## Objetivo e limites

Concluir os **35 itens** do motorhome **elétrico solar Aurora Solar**, seguindo
enunciado/apostila SEM0571 e requisitos do professor. Usuário quer autonomia,
pesquisa online quando necessária e CAD realista. **Ainda não concluído:**
35 em desenvolvimento, 0 aprovados. A preservação anterior foi seguida da retomada27/10.
Logo/pintura externa foram pedidos **depois da parte técnica**; não antecipar.

Worktree exclusiva: `/home/mhc/motorhome_solar_codex_tarefas`, branch
`hub/tarefas-motorhome-com-codex`. Outra conversa usa
`/home/mhc/motorhome_solar_codex`: **não editar/copiar alterações dela**.
Último commit técnico **`5eca6c0`**, confirmado30/10; árvore limpa antes desta
atualização documental. Base anterior`fd8ae1e`/`9742cd5`; freios`0cec31e`,
cabos/radiador`d975212`.
Push autorizado **quando pronto** para `https://github.com/MHC-CodeSmith/STF_MotorHome.git`;
sem remote/push até aqui. Não enviar mensagens a terceiros nem repetir credenciais.

## Ler e abrir

- `docs/VERIFICACAO_INTEGRADA_35.md`: controles que passaram e lacunas concretas.
- `docs/REVISAO_35_ITENS.md`: matriz dos 35, requisitos e pendências por item.
- `docs/FECHAMENTO_TERMICO_E_MISSAO.md`: bateria, bomba, solar portátil e operação.
- `docs/MECANICA_ROLAMENTO_E_CUSTOS.md`, `FREIOS_2D.md`, `CABOS_E_RADIADOR_2D.md`.
- Entrega: `entregas/parcial_2026-10-24/visualizador.html` (offline), STEP/GLB e JSON.
  Memorial: `output/pdf/memorial_revisao_aurora.pdf`, **25 páginas/2741667 bytes**.
  Auditoria: `output/verificacao_integrada_35.json`, `all_35_finished=false`.

## Decisões e medidas caras

- Base proposta **E-Ducato MY25 L3H2 4250 kg / 505.GG1.2**, 5,998 m, WB4,035 m;
  motor205kW/410Nm pico, pack110bruto/98útil kWh/400V. **Tara2790kg já inclui tração**.
  Exterior detalhado OpenX adaptado, não CAD OEM. Interior157meshes, elétrica208.
- **Limitador90km/h de série em4250kg**, ficha FiatSK p3; tabela genérica p4 dá130.
  Conservar restrição específica. I28:0–100 inalcançável ativo; atingir90 ainda não provado.
  I33:108→36km/h continua ensaio exigido, não evento operacional alegado.
- Serviços51,2V200Ah/10,24kWh; HVACFreshWell3000 sob cama2700W vs carga2646W
  condicionada, margem estreita. Lavadora73kg; **energia da secagem ainda desconhecida**.
- Teto fixo1540W: **5,506849kWh/dia**; habitação assumida5,276506 antes de perdas.
  Saldo com90% agregado = **−0,355935kWh/dia**. Agendas antigas não representam esta versão.
- Alternativa à extensão empilhada pesada: **4EcoFlow400W no solo**, parado,
  MPPT150/35 dedicado2s2p; Voc frio111,552V/Isc22A; possíveis limites em baixa tensão.
  21kg/un com bolsa (15kg só painel); +85,25kg com controlador; subtotal3458,605kg,
  **não massa final/eixos**. Reservas verticais sob cama sem colisãoAABB com equipamentos;
  bolsa/ancoragem/acesso/estrado não validados. 324sólidosSTEP reimportados positivos.
  Geração portátil8,119545/total13,626394kWh/dia a45°norte, sem sombra e sob hipóteses;
  saldo com habitação/90%=7,763609, **sem interfaceHV ou agenda ótima demonstradas**.
- Viewer8GLB/23seletores; portátil e extensão mutuamente exclusivos. Chromium:
  0errosJS/0requisiçõesHTTP; 157+208+324meshes; screenshots em cache.
- I34: ECM/SOC +2nós térmicos, OCV/R(SOC,T)/entropia/UA/BMS **hipotéticos**;
  20→80%,20/80kW:2,9629/0,7558h e25,8705/31,9663°C. Não packOEM calibrado.
- I35: curva publicadaBosch039202453G +circuito assumido:31,85099L/min,
  71,62575kPa/0,557392kg/s;96Welétricos/38,0225Whidráulicos. UA/perdas reais ausentes.
- I33 condicionado:1,70MJ translacional,535,5kJ/disco dianteiro,334,9906°C superficial;
  não compatibilidadeBremboMY25 confirmada. Refinamentos/analítica documentados.
- CFD: pilotos29527/63668/166212células,Cd0,6530/0,6249/0,5807; diferença7,07%,
  **sem independência**. Casos com camadas divergidos rejeitados. Rodas/equipamentos pendentes.
- BOM27linhas;20linhas nãoOEM sem oferta;R$439 IE3TP é referência não confirmada220V,
  **total instalado/impostos/frete null**. Cr0,0068–0,0080 é comparação de outro pneuCamper,
  não aplicar ao A/S anterior. Óleo homologado do redutor permanece desconhecido.

## Arquivos, caches e comandos

Cache externo **`/home/mhc/motorhome_referencias_tarefas`**. Atuais:
`bateria-carga-01`, `hidraulica-calculo-01`, `missao-atual-02`, `solar-portatil-02`,
`cad-portatil-01`, `visualizador-portatil-01/qa`, `bom-rolamento-02`,
`cabos-calculo-04`, `radiador-calculo-02`, `freios-calculo-03`; fontes em
`hidraulica-fontes-01`, `freios-fontes-01`, `cabos-fontes-01`, `fichas-eletricas`.
Fontes/hashes nos YAML e `fontes_externas/catalogo.csv`; não rebaixar arquivos já obtidos.
Textos locais em `/home/mhc/motorhome_referencias/textos/`: ler trechos, nunca PDFs/ZIP/CAD brutos.

Scripts `calcular_{bateria_carga,hidraulica,missao_atual,solar_portatil,bom_e_rolamento}.py`
aceitam `--destino NOVO`; `gerar_cad_solar_portatil.py --resumo JSON --destino NOVO`.
Consolidador `consolidar_fechamento_termico.py` exige `--bateria --hidraulica --missao`
`--portatil --cad-portatil --bom` com os caches correspondentes; **confere SHA256**.
CamposI35 hidráulicos prefixados para preservar caso anterior de radiador80°C.
**Não rodar consolidadores antigos sobre entrega nova sem conferir origens.**

```bash
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python -m ruff check src scripts tests
.venv/bin/python scripts/verificar_estrutura.py
.venv/bin/python scripts/auditar_projeto.py --json
.venv/bin/python scripts/verificar_entrega_integrada.py
```

Resultado26/10: **158 testes/6,37s**,ruffOK,estrutura/auditoria0erros;
124artefatos+PDF e entradas atuais conferidos; renderQA07/08. Não equivale a validação física.
Global intacto24nulls, SHA256
`7b8f5cd7891eb437cb89c41fd2ba440b0567ca1063998042d4828086aad523e2`.

## Próximo trabalho real

CFD equipado/malhas, massa/BOM/eixos/fixações, mapasOEM e óleo correto, custos completos,
interfaceHV real/perfis de operação e minimização globalI29 a partir das agendas
condicionadas27/10. I27 terminaSOC **exatamente30%**;
limite8h/dia pertence sóI29,7000km, bateria inicial+solar, sem recarga externa.
Não substituir dados físicos por testes sintéticos ou dizer que35 foram concluídos.
Revisão cruzada e vídeo/seminário com integrantes continuam necessários.
