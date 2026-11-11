# Retomada técnica — 10/11/2026 — integrado1540Wp

**Objetivo do usuário:** desenvolver todos35itens sobDEC001–061,autonomamente,até finalizar o possível;sem pedir16aprovações individuais,sem relatórioABNT/slides/envio. Usuário insistiu continuar atéfim. Não declarar hardware/viagem comprovados. Última rodada executou integração inteira e novos estudos;**cadeia computacional concluída,etapa física não concluída**. Síntese: `docs/SINTESE_DESENVOLVIMENTO_TECNICO.md`.

## Workspace / Git / leitura

- Exclusivo `/home/mhc/motorhome_solar_codex_tarefas`,branch `hub/tarefas-motorhome-com-codex`. Não editar `/home/mhc/motorhome_solar_codex`.
- Commit técnico desta rodada **`60541a0`**;anteriorHEAD/main`a0f86f3`,técnico`c509c4b`;base solicitada`29defc4`,não resetar. Push `git push origin HEAD:main` já autorizado;originSSH`git@github.com:MHC-CodeSmith/STF_MotorHome.git`.
- LerAGENTS,fim`EXECUCAO_TECNICA02.md`,`REVISAO_TECNICA_EXECUCAO02.md`,`PROTECOES_SERVICOS_MODELO.md`. `BLOQUEIOS_POS_DEC061.md`/`PLANO_EXECUCAO_POS_DEC061.md` agora conciliados,sem comandos históricos indevidos. Única lista finalA01–A16:`APROVACOES_FINAIS_PENDENTES.md`.
- Fonte única **`config/parametros_globais.yaml` revisão1.1.1-execucao1540**,base1350Wp preservada. Sobreposição **`development.integrated_scenarios.maxeon1540_independente`**,selecionada por`MOTORHOME_SCENARIO`;`motorhome.cenarios` geraJSONresolvido/snapshotshashados/entradaspor executor,que são saídas,não fonteeditável. Não alterarYAML durante pipeline.

## Estado técnico vigente

- Cenário1540 em **`entregas/integrado_maxeon1540/`**,base1350 em`entregas/desenvolvimento_2026-11-09/`. CFDequipado em **`entregas/aero_equipado1540/`**. Não misturar massa/controladores/solar/γ de cenários.
- **17comandos da cadeia passaram**,`execucao_pipeline.json complete:true` significa só execução da cadeia,não validação física. QAbasePASSOU422controles/178entradas1257saídas hashadas;QAcenárioPASSOU331controles. **244pytest/Ruffpassaram,estrutura35/7/auditoria0erros/0teoriasemtemplate.** Nenhum processo pendente ao preparar esta nota.
- Todos35 têmteoria/método/fontes/validaçãoPENDENTE eíndices locais `resultados/execucao_integrada.json`,`dados/parametros_execucao_integrada.json` comunidades/origem/versão/hash. `entregas/indice_execucao_35.json`;matriz61atual `entregas/matriz_decisoes_integrada_61.json`/docsMATRIZ. HistóricoJSONnão reescrito.

|Frente|Resultado e limite vigente|
|---|---|
|OEM|SKMY25**505.GG1.2**4250PBT2790tara,110/98kWh400V205kW410Nmpico,**90km/h**;50990EURsemIVA. Eixos/pressões/mapas/relação/óleo/apoios/suspensão desconhecidos,0–100inalcançável.|
|Solar|**2Maxeon380+2Maxeon390=1540Wp/76kg**,1,046×1,690×0,040cada. Com20mmgaps/25mmpontas4,294×1,690m,envelopeestimado4,30×1,82sobram6mmextras;curvatura/apoios não validados. Teto2S2P:Vocfrio+tolerância171,4776V,150V incompatível;250/60teto+150/60portáteis é comparador independenteDEC054. Compartilhado72I–Vestimadasperdem0,657–27,272%;não aprovado. SaídaMPPT48Vnão é interfaceHV.|
|Massa1540|**3976,52552776kg**,CGx2,017804183/y0,002448803/z0,930713687m;eixos1987,962989/1988,562539kg,margem273,474472kg. Inclui+3kgsegundoMPPT−0,5kgtroca módulos. Água **85Ltanque+15Lboiler=100L**,corrigiuCGsem massaextra. Base1350ainda3974,025528kg,CG/eixos agora diferentesdos checkpointsantigos.|
|Serviços|3US5000=14,4kWh119,1kg,**7,2288254kWh/dia**. GX48/5000PMP482506000220/60,31kg565×323×148mm18Wvazio,GX/BMS-CANintegrado,sem centralprópria. Hardware/partidas/DVCCnãoensaiados,SOCthresholdsnull.|
|24/48hCAD|24h2/3módulos porreserva20/30%;48h4/5. CADcompleto2/3/4/5semcolisãoAABB;massas3936,8255/3976,5255/4016,2255/4055,9255kg,rackextra desconhecido.12casos suporte banco inteiro incluem4,53kgtrilhos nasforças,sem duplicar inventário. Folga10mm deCADéhipótese.|
|Prioridades|72casos24/48semSol/minbaseMax/controleextra0/5/15W. Orçamento previsto,não limiaresSOC.3módulos semgestão38,2469h até20%ou33,4660h até30%;gestãoalcança48h retirandocozinha/boiler/lavanderia. **Não atende48hperfilcompleto**,I29não incorpora cortes.|
|I25/I29|630MILP5min/mínimo1kWhipotético:40/80kmh51,48977/28,54926km sótração;27,18686/15,07416comserviçoscíclicos.3kWdiretanãoinicia. Grade1008:700Waux20kmh20–04 **243,84375/244,8854167dias**. Semótimoglobal/missionfísica.120missões deincerteza/alocação,36DCdiários,32buffercomercial.|
|Buffer|US5000dedicado4,56kWhcréditoFVacimareserva/39,7kgextra,créditoinicial0,massa4016,22553kgélímiteinferior. Exemplo40kmh00–08reserva10/20:direta1kW327,0104dias;buffer1kW278,0313;direta3kWnãoconclui1500dias,buffer3kW279,0104. Nãoinstalado/custo/conversor/OEMnão demonstrados.|
|Água|8004eventos/8melhoresreplays,2127refill/disposal,erro≤9,1e−13L,conferidos independentemente contra condução/montagemFV. Disponibilidadede postos/temposhipotética.|
|CFDequipado|Deckcontínuo4,244×1,690×0,040m,gap40mm ao topo piloto,suportes/gaps20mmomitidos. **101030/128458/217494células**,checkMeshOK/SIMPLEconvergido;Cd**0,68313391/0,66691895/0,63374383**,últimadelta5,23%,y+alto. SemCddefinitivo/GCI;faixa sensibilidadeCdmax**0,72**propagada972combinações,central0,62487678hipótese antiga. Dados≈111MB,semarquivo>20MB. Tentativas antigas178298comcamadasdivergentespreservadas,nãorepetir.|
|Fixações|378candidatos/18seleções,**33,13793kgchapas brutas**,utilmax0,99361. Inversoragoraplanover­tical,gravidade transformada eCGnormalda caixa×1/1,25/1,5;substitui55,7511kg/envelopeuniversalantigo.11Tet4:inversorlinear2,822%insuficiente/tanque1,144%passa;**3Tet10inversor0,5504%passa**semrelaxar2%. Tensõesdeengaste/apoiosOEM/fadiga/pryingnão validados.|
|Elétrica|324DC/144faltas/256picos/6falhas.56prospectivos>20kA,JLLN200/80candidatos125VDC20kA. **Nova fichaPylon<2000A/1ms**:se3móduloslimitarem,tetodeentrega<6000A nointervalo;NÃOprospectivopréBMS/I²tfusível.144faltasantigasretidas;coordenaçãonão demonstrada.|
|BOM|27linhas1540;**USD1951=GX1093+150/60 393+250/60 465**,lista2026Q2exVAT. EUR50990veículo/BRL439cooktophistórico separados,totalinstaladonull. Módulos/bateria/importação/custosinstalação desconhecidos.|

## Invariantes e fontescaras

B por interface**externaDCOEMautorizada**,não packdireto/HV/BMS/cabosalterados;armazenamentostraçãoserviçosindependentes;antiga48V→OBCdescartada. Buffercomparação,nãobancoinstalado;MPPTcompartilhado não aprovado. Portáteis1600sóparado/ângulosfixos. Serviços48V220V60Hz,naturalvent/ACsobbanco/indicadorescomerciais. I297000kmplano,constspeed,ambosSOC100%,≤8h/dia,semcargaexterna,SãoCarlos21jun25°CUR50vento0repetido. ERA5/OSRM7511,282kmcomplementos. I27100/80→30%separado,semimportar8h. Água100/70/cassete~20,2×80kg+60bagagem. Deadline02/12/2026 06hSãoPaulo.

Registro61intocadoSHA256 **1e082c4961a57b865f008fa1daadd37e696bdb060f22c922596715096c793969**. MaxeonPDF923002byteshash**d6c76ef9231cb1621d8401a46fbef617724e6bc6ea873bb3f4658261fef75757**,cache`maxeon-conferencia-20261110/`,primárioTLSfalhou/espelhoSolSolconferidop2. PylonPDF276588byteshash**6b85fb621d4f102863e99208e5d3467adc65f376e75d37fbde4ee7ee928bd139**;listaVictron2351739byteshash**83275209e603872733eb06ea0761bd65820bf5b93f6068f9e5467b691862cd80**,cache`conferencia-pylon-preco-20261110/`,ambosrenderizados. FreshWell2018manual8MBhash**12246bf2a261161a4b1778780fa59a8ba06edda53ba8670765d1b96f6265680b**,p29220–240V50/60Hz2700Wtérmicos6,2A60Hz;curva33/25/placa/partida/fusível5Acontinuaaberto. Dadoscabin/PIMPLE300s50,3203média53,0744máx+balanço0,0482% jáentregues;nãoreexecutar por docs.

## Reprodução / limitesremanescentes

```bash
PYTHONPATH=src .venv/bin/python scripts/executar_cenario_integrado.py --cenario maxeon1540_independente --reexecutar
MOTORHOME_SCENARIO=maxeon1540_independente PYTHONPATH=src .venv/bin/python scripts/verificar_cenario_integrado.py
PYTHONPATH=src .venv/bin/python scripts/verificar_desenvolvimento.py
PYTHONPATH=src .venv/bin/python -m pytest -q
ruff check src scripts tests
```

Pipeline17estágios/logs/JSON17returncodes0;**último `output/pipeline1540_verificacao_final_20261110.log`**. Não repetir1008/CFD por mudança textual. Manifesto`--registrar` só apósgenerationdeliberada. Atualizaríndices/matriz35/61comscripts`registrar_execucao02`,`preencher_metodos_itens`,`atualizar_matriz_decisoes_integrada`antesdehashfinal. QAintegrado não devehashar se próprio log de verificação emaberto. Snapshotsantigosretidos como proveniência,sem mascarardivergência.

Bloqueiosreais:faltaautorização/mínimos/protocoloDCOEM,ancoragens/eixos/pressões/mapas/redutor/óleoOEM,partidasHVAC,fusívelI²t/impedância/PE-DR/ampacidade,atuadorescomissionados,mediçãoCAD/teto/curvatura/contato/fadiga/CHTreal,instalação/custoBRL. Não preencherporinvenção/nemconsideraraprovaçãohumanacompleta. Avançarapenasproblema concretamenteexecutável,nãorepetirpesquisaDCindefinidamenteouvoltar aplanosgenéricos. Nenhum equipamento comprado/instalado/ensaiofísico/contatoterceiro.

Ambiente:shellgeralmente`require_escalated`porbwrap,semrejeiçãopendente. PYTHONPATHsrc/.venvPython;Ruffglobal. OpenFOAM2412patch260127em`/home/mhc/motorhome_referencias_tarefas/software/openfoam2412-local/usr/lib/openfoam/openfoam2412`. RAMúltima2,7GB/swap7,2GB;CFDexige novosdestinos. Webvia`mcp__codex_apps__search_service_web_run`. Históricoantigo`RETOMADA_HISTORICO_ATE_2026-11-10.md`;númerosdesta nota prevalecem.

**Publicação desta rodada:** commit60541a0 é local. Revisão automática rejeitou pushHEAD:main por não encontrar autorização explícita no contexto confiável. Não repetir push/contornar. Completar verificações locais e pedir aprovação apenas para publicação remota;nenhum bloqueio aos estudos locais.
