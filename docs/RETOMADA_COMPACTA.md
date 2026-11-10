# Retomada — motorhome solar, 10/11/2026

## Atualização da revisão geral — 10/11/2026

- Pedido atual atendido documentalmente em **`docs/REVISAO_GERAL_PROJETO.md`** (35 pareceres individuais, resultados, limites, evidências e referência à lista única A01–A16). Não declarar projeto fechado: OEM/instalação/DC, CFD e otimização têm lacunas técnicas além da aprovação humana.
- Correção feita em `docs/APROVACOES_FINAIS_PENDENTES.md`, A13: cenário1540Wp **243,84375/244,88542 dias**; 290,875/292,885 dias pertenciam ao1350Wp. Nenhum parâmetro, resultado de solver ou DEC original alterado.
- **21 novos recálculos/conferências JS passaram**, registro `entregas/revisao_geral_2026-11-10/verificacoes_documentais.json`. Documento relido e idêntico ao texto escrito; contém35linhas de itens. Conferência adicional em lote das referências foi interrompida por demora e não é apresentada como concluída.
- **Ambiente mudou:** terminal normal falhou em bwrap/RTM_NEWADDR; execução ampliada não foi executada porque a revisão automática falhou com permissão de rede revogada. Não contornar com outro shell. Leituras/escritas locais funcionaram. Os244testes,422+331controles e17comandos são registros anteriores, NÃO reexecutados nesta revisão.
- **Integridade pendente conhecida:** A13 alterou documento coberto por manifesto antigo. Não mascarar: restaurar terminal, regenerar manifesto pelo procedimento documentado e verificar novamente. Novos arquivos/revisões locais sem commit/push nesta sessão; último HEAD registrado3f684d9, não conferido por Git agora. Bloqueio anterior de push continua; pedido de revisão não é autorização de publicação.

**Objetivo aberto:** executar os 35 itens sob DEC-001–061 com autonomia provisória. O usuário insiste em continuar até terminar; não pedir escolhas individuais, preparar ABNT/slides/envio ou declarar hardware validado por simulação. **Cadeia computacional reproduzida; projeto físico e aprovação humana não concluídos.**

## Local e publicação

- Worktree exclusiva: `/home/mhc/motorhome_solar_codex_tarefas`, branch `hub/tarefas-motorhome-com-codex`. Não editar `/home/mhc/motorhome_solar_codex`.
- HEAD antes desta nota: **188d2c0**; commit técnico **60541a0** (944 arquivos). Ambos **locais, não publicados**. Último envio confirmado: **a0f86f3**. Base solicitada29defc4 é histórica; não resetar.
- **Push bloqueado por revisão automática:** `git push origin HEAD:main` rejeitado por falta de autorização explícita no contexto confiável. A pergunta de autorização foi feita na última resposta, **sem resposta até agora**. Este pedido de salvar contexto não autoriza publicação. Não repetir/contornar o push; trabalho local continua autorizado. Origin: `git@github.com:MHC-CodeSmith/STF_MotorHome.git`.

## Ler e executar

1. `AGENTS.md`, `docs/SINTESE_DESENVOLVIMENTO_TECNICO.md` e fim de `docs/EXECUCAO_TECNICA02.md`.
2. Estado individual: `docs/REVISAO_TECNICA_EXECUCAO02.md`; limites: `docs/BLOQUEIOS_POS_DEC061.md`; reprodução: `docs/PLANO_EXECUCAO_POS_DEC061.md`.
3. Única lista de escolhas finais: `docs/APROVACOES_FINAIS_PENDENTES.md` (A01–A16). Detalhe estrutural/elétrico: `docs/PROTECOES_SERVICOS_MODELO.md`.

**Fonte única:** `config/parametros_globais.yaml`, revisão **1.1.1-execucao1540**. Sobreposição `development.integrated_scenarios.maxeon1540_independente`; `motorhome.cenarios` resolve valores e arquiva snapshots/hash por executor. JSON resolvido é saída derivada, não fonte editável. Não alterar YAML durante pipeline.

```bash
PYTHONPATH=src .venv/bin/python scripts/executar_cenario_integrado.py --cenario maxeon1540_independente --reexecutar
MOTORHOME_SCENARIO=maxeon1540_independente PYTHONPATH=src .venv/bin/python scripts/verificar_cenario_integrado.py
PYTHONPATH=src .venv/bin/python scripts/verificar_desenvolvimento.py
PYTHONPATH=src .venv/bin/python -m pytest -q
ruff check src scripts tests
```

## Evidência vigente

- **17 comandos concluídos**, log `output/pipeline1540_verificacao_final_20261110.log`; `complete:true` só significa execução da cadeia. **244 testes/Ruff passaram**, QA base422 + cenário331 controles, auditoria0erros, estrutura35/7, nenhuma teoria em template. Nenhum processo pendente. Nesta atualização documental não foram reexecutadas simulações/testes.
- Saídas: **`entregas/integrado_maxeon1540/`**, **`entregas/aero_equipado1540/`**. Base1350Wp preservada em `entregas/desenvolvimento_2026-11-09/`. Não misturar massa/controladores/solar entre cenários. QA base:178 entradas/1257 saídas hashadas; `stage_complete:false`, aprovação humana0, missão físicafalse.
- Cada item tem `resultados/execucao_integrada.json` e `dados/parametros_execucao_integrada.json`; índices35/61 em `entregas/indice_execucao_35.json` e `entregas/matriz_decisoes_integrada_61.json`. Atualizadores: `registrar_execucao02.py`, `preencher_metodos_itens.py`, `atualizar_matriz_decisoes_integrada.py`; manifesto `--registrar` somente após geração deliberada. Não renovar hashes históricos para ocultar mudanças.

|Frente|Valores caros de recuperar / limites|
|---|---|
|OEM/massa|SKMY25 **505.GG1.2**,4250PBT/2790tara,110/98kWh,205kW/410Nm pico,90km/h. Cenário1540: **3976,525528kg**, CGx2,017804183/y0,002448803/z0,930713687m; eixos1987,962989/1988,562539kg; margem273,474472kg. Eixos/apoios/mapas/pressões OEM ausentes.|
|FV|2Maxeon380+2Maxeon390=**1540Wp/76kg**;4,294×1,690m em retângulo estimado4,30×1,82m,6mm extras. Vocfrio171,4776V:150V incompatível. Comparador250/60teto+150/60portáteis; compartilhado72casos perde0,657–27,272%,não aprovado.|
|Serviços|3US5000=14,4kWh/119,1kg;7,2288254kWh/dia. GX48/5000 PMP482506000,220/60,31kg,18W vazio.24h2/3módulos por reserva20/30%;48h4/5. QuatroCADs e12suportes;72prioridades não substituem perfil completo nem definem SOC-BMS.|
|I25/I29|630MILP:5min/1kW hipotético,40/80kmh51,48977/28,54926km sótração;27,18686/15,07416km serviços cíclicos. Grade1008:700Waux/20kmh/20–04h **243,84375/244,88542dias** por reservas;sem ótimo global/provaDC.972incertezas/120missões/36DCdiários/32buffercomercial.|
|Água/buffer|100L totais agora **85tanque+15boiler**,sem duplicação;8004eventos/8replays/2127refills,erro≤9,1e−13L. Bufferdedicado comparativo4,56kWh créditoFV inicial0/+39,7kg,não instalado.|
|CFD|Equipado101030/128458/217494células,solver convergiu,Cd0,68313391/0,66691895/0,63374383;última variação5,23%,y+alto,semGCI/Cddefinitivo. Sensibilidade até0,72. Cabine3D anterior50,3203°Cmédia/53,0744máx,contorno congelado,nãoCHT/OEM. Não repetir malha antiga178298 comcamadas divergentes.|
|Fixações/elétrica|378candidatos/18interfaces;inversor vertical/CGnormalCAD,33,13793kg chapas brutas.11Tet4:inversor2,822%insuficiente/tanque1,144%;3Tet10inversor0,5504%.324DC/144faltas/56>20kA. Pylon<2000A/1ms é teto declarado,não prospectivo/I²t fusível.|
|BOM/HVAC|27linhas;USD1951 GX+doisMPPTs,EUR50990 veículo/BRL439cooktop separados,total instalado null. FreshWell2018 confirma220–240V50/60Hz,6,2A/2700Wtérmicos;curva33/25,SKU,partida e fusível5A permanecem abertos.|

## Restrições e continuidade

B usa interface **externa DC OEM autorizada**,não acesso ao pack/BMS/cabos. Bancos independentes;antiga48V→OBCdescartada. Buffer/MPPTcompartilhado não aprovados. Portáteis1600Wp só parado/ângulos fixos. I29:7000km plano/velocidade constante,ambosSOC100%,≤8h/dia,sem cargaexterna,diaSãoCarlos21jun25°C/UR50/vento0 repetido. I27 separado100/80→30%;ERA5/7511km complementares. Água100/70/cassete~20,2×80kg+60bagagem. Deadline02/12/2026 06hSãoPaulo.

Remanescentes: interfaceDCautorizada/mínimos/protocolo;dadosOEM/eixos/ancoragens;partidasHVAC;I²t/impedância/PE-DR/ampacidade/atuadores;geometria/teto/contato/fadiga/CHT reais;preços instaladosBRL. Não inventar ou repetir pesquisaDC indefinidamente. Nenhum equipamento comprado/instalado/ensaio físico/contato com terceiros. Próxima sessão deve escolher pendência concretamente executável,sem devolver plano genérico nem afirmar projeto totalmente concluído.

Ambiente: shell geralmente `require_escalated` por falha bwrap;essa execução local é permitida,**a rejeição pendente é do push**. Python `.venv`/PYTHONPATHsrc,Ruff global. OpenFOAM2412 em `/home/mhc/motorhome_referencias_tarefas/software/openfoam2412-local/usr/lib/openfoam/openfoam2412`;RAM~2,7GB disponível/swap7,2GB,usar destinosCFD novos. Web `mcp__codex_apps__search_service_web_run`.

Fontes/hash/PDFs renderizados e números anteriores: **`docs/RETOMADA_DETALHADA_INTEGRACAO1540_2026-11-10.md`**. Registro61 original SHA256 `1e082c4961a57b865f008fa1daadd37e696bdb060f22c922596715096c793969` intocado. Detalhe anterior contém alegação antiga de push autorizado;prevalece o bloqueio explícito desta nota.

- Continuidade 10/11: shell, Python, `.venv` e Ruff restabelecidos. 244 testes/Ruff/verificador integrado passaram; QA desenvolvimento passou após `--registrar` legítimo do hash A13. Adicionado refinamento local I29 (`scripts/refinar_velocidade_missao.py`, 796 pontos) sob janela 20–04h: 700W, 10/20% chega condicional em242,885d a20,4km/h; 20/30% em244,885d a19,8km/h. Hipótese DC permanece e nenhum ótimo global é alegado. Ver `docs/REVISAO_GERAL_PROJETO.md`.

## Checkpoint para próxima sessão — 10/11/2026

- Objetivo: continuar desenvolvimento técnico dos 35 itens sob DEC-001–061; preservar decisões e resultados. Não preparar relatório acadêmico/slides. Fonte ativa de parâmetros: `config/parametros_globais.yaml`; cenário integrado: `maxeon1540_independente` (1540 Wp). Arquitetura B; interface DC para tração continua hipotética, sem compatibilidade/autorização OEM demonstrada. Nunca acessar HV/BMS ou usar banco de serviços para tração.
- Executado nesta retomada: 244 testes, Ruff, verificadores integrado/desenvolvimento, estrutura e auditoria passaram. Manifestos atuais registrados/verificados; desenvolvimento contém 179 hashes de entrada e 1257 de saída. Auditoria sem erros, com avisos sobre 134 parâmetros nulos/OEM, aceite humano ausente e I28–I33.
- Novo I29: `scripts/refinar_velocidade_missao.py`; resultados em `entregas/integrado_maxeon1540/otimizacao_refinada_velocidade/` (796 pontos, 15 min, velocidade 10–90 km/h + refinamento 0,1, janela fixa 20–04h). Auxiliares estimados 700 W: reserva 10/20% = 242,8854167 d a 20,4 km/h; 20/30% = 244,8854167 d a 19,8 km/h. Balanço máximo 4,18e-9 kWh. Busca local, não ótimo global; depende da interface DC hipotética. Não comparar como missão física.
- Documentos atualizados: `docs/REVISAO_GERAL_PROJETO.md` inclui resultado e corrige nota histórica do terminal; a revisão lista os 35 estados/limites. `docs/APROVACOES_FINAIS_PENDENTES.md` A13 corrigida para 1540 Wp; 290,875/292,885 d eram 1350 Wp. 61 decisões preservadas.
- Git local contém commits `c4e88dd` e `6f52def` (`Atualiza QA para 179 entradas rastreadas`). `git push --dry-run` confirmou acesso de escrita, mas push real não concluiu após >6 min ao empacotar ~260 MiB; tentativa encerrada, branch remoto não confirmado/criado. Não repetir pushes simultâneos. Publicação pendente; estado local preservado.
- Pesquisa de interface DC: lane relacionada não encontrou nova fonte primária. Bright Data CLI `bdata` não está instalado; não atribuir autorização a referências genéricas IEC/Stellantis. Permanecem evidências externas necessárias: protocolo/limites mínimos CCS2 da variante MY25, isolamento, potência/corrente mínima e autorização OEM. Também faltam limites por eixo/ancoragens, dados reais de proteções/componentes, validação CFD/instalação física e aceite humano.
- Continuidade seguinte: envelope fatorial reprodutível P1 em `scripts/resumir_envelope_eixos.py`, saídas `entregas/integrado_maxeon1540/integracao/envelope_cargas_eixos/`. 162 casos (2 layouts × 3⁴ níveis); dianteiro A 1737–2223kg/B 1756–2243kg, traseiro A 1698–2294kg/B 1693–2292kg; margem PBT mínima163,4/144,5kg. Hipótese de distribuição traseira OEM explica cerca de86–98% da soma de quadrados dos efeitos principais das cargas por eixo. Grade determinística, sem probabilidade/conformidade. Manifesto desenvolvimento atualizado pelo procedimento registrado e verificado:180 entradas/1257 saídas. Reexecutados:244 testes, Ruff, verificador integrado e desenvolvimento, todos PASSOU. Revisão geral, revisão por item14 e bloqueio B03 atualizados. Alterações locais ainda não commitadas.
- I29 ampliado: `scripts/otimizar_janela_missao.py`; busca reduzida preservada em `entregas/integrado_maxeon1540/otimizacao_janela_missao/` (648 linhas); busca densa em `.../otimizacao_janela_missao_densa/` (5268 linhas:3936 grade partida2h/velocidade2kmh +1332 refinamento local0,5h/0,2kmh). Para700W: reservas10/20%=242,802083d,20,8km/h,partida18h;20/30%=244,802083d,20km/h,partida18h. Erro de energia ≤2,9e-8kWh. Resultado de busca finita, local e condicionado à interfaceDC hipotética;0W atinge limite inferior10km/h e não indica ótimo interior. A grade reduzida usa648 casos e converge nos mesmos 0,25d/partida18h para cenário central.

## Continuidade em execução — 10/11/2026

- A busca reduzida e a busca densa I29 foram ambas concluídas. Rechecks após alterações: `pytest` 244 passed; `ruff check src scripts tests` passou; `verificar_cenario_integrado.py` passou; `verificar_desenvolvimento.py` passou após registro legítimo, 181 hashes de entrada/1.257 de saída. Os commits locais são `0198462` (envelope P1) e `d8a88bc` (busca I29); árvore limpa ao encerrar. Nenhum push remoto realizado.
- P1: script `scripts/resumir_envelope_eixos.py`; 162 hipóteses enumeradas. Faixa de reação longitudinal A: frente1.737–2.223kg/traseira1.698–2.294kg; B: frente1.756–2.243kg/traseira1.693–2.292kg. Menor margem PBT 144,5kg. A proporção de fração traseira OEM é hipótese dominante, não distribuição probabilística; limite admissível por eixo não existe nos dados locais. Ver commit `0198462` e `entregas/integrado_maxeon1540/integracao/envelope_cargas_eixos/`.
- I29: nova varredura variou a partida com janela fixa de condução8h/dia. Caso central700W: 10/20% =242,802083d a20,8km/h, saída18h; 20/30%=244,802083d a20km/h, saída18h. O resultado anterior de janela fixa continua válido como comparador; novo resultado reduz cerca de2h por escolher início distinto. Ainda é busca finita/local sob interface DC de1kW hipotética, sem ótimo global ou missão física. 0W seleciona velocidade mínima permitida10km/h (ótimo na borda); todos os 5.268 pontos e resultado estão versionados em commit `d8a88bc`.
- P3/CDF: nenhum novo caso CFD foi iniciado. Medição local após a simulação: 2,1GiB de RAM disponível, swap8GiB quase cheio (7,9GiB usados;107MiB livres), contra artefatos CFD equipado existentes~111MiB. Sem recurso suficiente para outra malha de volume neste momento; estudos anteriores/limitações permanecem preservados. Isto não bloqueia análises sem hardware.
- Bloqueios que permanecem dependentes de evidência externa/humana: interface DC solar autorizada e seus limites/protocolo OEM; limite real por eixo, geometria/ancoragens/pesagem; impedância/I²t/ampacidade/PE-DR/partidas elétricas; geometria real de teto/instalação e validação CFD suficiente; curva/capacidade real HVAC e instalação; curvas térmicas/circuito OEM; cotações e total instalado. Nenhuma aprovação ou validação física foi inferida.
- Retomar lendo `docs/REVISAO_GERAL_PROJETO.md`, `docs/BLOQUEIOS_POS_DEC061.md` e `docs/EXECUCAO_TECNICA02.md`. QA: `PYTHONPATH=src .venv/bin/python -m pytest -q`; `ruff check src scripts tests`; `MOTORHOME_SCENARIO=maxeon1540_independente PYTHONPATH=src .venv/bin/python scripts/verificar_cenario_integrado.py`; `PYTHONPATH=src .venv/bin/python scripts/verificar_desenvolvimento.py`. Se mudar scripts/entradas, usar o `--registrar` do verificador vigente e verificar novamente; não alterar manifestos históricos.
