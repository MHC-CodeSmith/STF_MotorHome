**Começar por [RETOMADA_COMPACTA.md](RETOMADA_COMPACTA.md)**: checkpoint9742cd5, comandos, caches e pendências; o restante preserva histórico.

# Estado prioritário — 26/10/2026: revisão integrada dos35itens

Pedido atual: continuar autonomamente até concluir/verificar35itens. **Ainda não concluído.**
Ler `VERIFICACAO_INTEGRADA_35.md`, `FECHAMENTO_TERMICO_E_MISSAO.md` e
`MECANICA_ROLAMENTO_E_CUSTOS.md`. Estado35emdesenvolvimento/0aprovados; sem templates
vazios nos quatro itens antes não iniciados, mas dados físicos/custo/óleo seguem pendentes.

Novos métodos: I34ECM+SOC+dois nós térmicos20/80kW; I35curvaBosch039202453G +Darcy
interseção31,85099L/min/71,62575kPa/96W, circuito eUA assumidos. I34nominal25,8705/31,9663°C,
protocolo20→80% e todos parâmetros nãoOEM explícitos. Não confundir potência elétrica/calor.
FonteFiatSKp3: versão4250kg tem limitador90km/h;0–100 inalcançável ativo; I33ensaio108→36.
Teto1540W5,50685kWh/dia vs5,27651dehabitação: déficit com perdas90/95%; agendas antigas históricas.
Alternativa4EcoFlow400W no solo, bolsas verticais sob cama,21kg/un com bolsa,MPPT150/35 dedicado2s2p.
Geração portátil8,11954/total13,62639kWh,dia claro45°norte; sem sombra/agenda/interfaceHV comprovadas.
CAD324sólidosSTEP positivos +GLB solo/transporte. Viewer atualizado8GLB,23seletores,alternativas
exclusivas; Chromium0errosJS/HTTP. BolsaAABBsem colisões com equipamentos; ancoragem/acesso pendentes.
BOM27linhas/preçoIE3TPR$439só referência genérica,20linhas nãoOEM sem oferta; total finalnull.
Cr0,0068–0,0080 é outro pneuCamper0451473; não aplicado silenciosamente ao A/S anterior.

Caches vigentes: `bateria-carga-01`,`hidraulica-calculo-01`,`missao-atual-02`,
`solar-portatil-02`,`cad-portatil-01`,`visualizador-portatil-01/qa`,`bom-rolamento-02`.
Config/scripts nomes nos docs. Consolidador exige6origens,conferehashes; camposI35hidráulicos
agora prefixados para preservar caso anterior radiador80°C. Não sobrescrever com caches antigos.
158testes/6,37s,ruffOK,estrutura/auditoria0erros. `verificar_entrega_integrada.py` conferiu35itens,
124artefatos+PDF e entradas atuais; `all_35_finished=false`. PDF25p/2741667bytes,QA07/08.
Global intacto24nulls/SHA7b8f5cd7891eb437cb89c41fd2ba440b0567ca1063998042d4828086aad523e2.
Próximos: CFD equipado/malhas, massa/eixos/fixações, cotações completas, óleo/mapasOEM,
agendasI27/I29atuais com montagem portátil/interfaces. Logo/pintura só depois da técnica.
Outra worktree intocada; sem remote/push. Consultar gitlog para checkpoint desta etapa.

# Avanço mais recente — 26/10/2026, freios I33

Implementado campo transiente r–z para duas pistas anulares ventiladas simplificadas.
Ler [FREIOS_2D.md](FREIOS_2D.md): fonte Brembo300×32mm NÃO confirma MY25;
material ferroviário tabela2 via XML EuropePMC, dimensões internas/partição assumidas.
Cenário4250kg:1,70MJ translacional,535,5kJ/disco dianteiro,334,9906°C superficial.
Não é aprovação do freio: inércias/cubo/aletas/contato móvel/cotas reais ausentes.
Código`freios_axisimetricos.py`,config`freios_proposta.yaml`,scripts`calcular_freios.py`
e`consolidar_freios.py` (confere hashes). Cache vigente`freios-calculo-03/`;
fonte`freios-fontes-01/`; resultados noI33 e entrega parcial prefixo`freios_`.
143testes passaram em2,61s;ruffsrc/scripts/tests OK;estrutura35itens7equipes/auditoria0erros.
Memorial21p/2288146bytes, página12 conferida em`memorial-qa-06/`.
Global intacto24nulls;27parciais/8não iniciados/0aprovados. Nenhum push.
Próximos: pack I34/perdas reais, bomba/curvas I35, CFD equipado/malhas,
fixações/BOM/eixos e missões com geração/consumo atuais; fonte/distribuição real I03/I33.
Logo/pintura continuam ao final; outra worktree intocada.

# Atualização prioritária — 26/10/2026

Usuário mandou continuar; o pedido anterior de só preservar contexto foi superado.
Implementados I30 polar feixe+isolamento/R(T) e I35 campos cruzados/integral.
Ler [CABOS_E_RADIADOR_2D.md](CABOS_E_RADIADOR_2D.md). Configs`cabos_tracao_proposta.yaml`/`arrefecimento_proposta.yaml`.
Caches`cabos-calculo-04/` e`radiador-calculo-02/`; PDFs/fontes`cabos-fontes-01/`.
Resultados nos itensI30/I35 e entrega parcial, sem aprovar componentes.
132testes passaram/ruffOK/estrutura0erros; global intacto24nulls.
Memorial20p/QA`memorial-qa-05/`; nenhuma aprovação de engenharia.
Próximos: circuitos e fontes físicas OEM, freios/pack, CFD equipado/malhas, fixações/BOM/eixos e missões atualizadas.
Decoração continua depois da parte técnica. Outra worktree intocada; sem push.

# Retomada após compactação — 25/10/2026

**Não iniciar nova etapa durante o pedido de preservação.** Usuário informou janela
de5h a94%, reinício20:01; pediu somente salvar contexto. Não é cancelamento do projeto.

## Missão e autorizações

Concluir motorhome **elétrico solar**,35itens do professor/apostila, ao menos2pessoas.
Avançar autonomamente, pesquisar fontes primárias, instalar/baixar se necessário.
Usuário autoriza push para `https://github.com/MHC-CodeSmith/STF_MotorHome.git`
**quando pronto**; ainda sem remote/push. Logo Aurora Solar e pintura/grafismos externos
foram pedidos **só depois de terminar a parte técnica**: não antecipar decoração.

Worktree exclusiva `/home/mhc/motorhome_solar_codex_tarefas`, branch
`hub/tarefas-motorhome-com-codex`. Outra conversa possui
`/home/mhc/motorhome_solar_codex`: não editar/copiar trabalho dela.
Última implementação **`0f9c3b8`**, árvore limpa antes desta nota.

## O que foi feito e verificado

- CAD principal continua carcaça detalhada OpenX Ducato adaptadaL3H2; STEP/GLB
  autorais de integração, não CAD OEM. Tração/serviços agora **208sólidos**:
  pack15módulos ilustrativos, motor/redutor dianteiros, inversor/OBC/radiador,
  banco/BMS/inversor/MPPT/DC-DC/quadro, armário técnico/gaveta e rotas conceituais.
- **Cotas de tração estimadas**, explicitamente marcadas. Pack2,90×1,44×0,32m,
  vão livre230mm/folga130mm até piso assumidos; não usar como geometria térmicaOEM.
  Motor205kW/410Nm pico, pack110bruto/98útil kWh/400V da fichaMY25.
  **2790kg OEM já incluem pack/motor/transmissão: não somar novamente.**
- Serviços2×NG51,2V100Ah em paralelo=**200Ah/10,24kWh**,74kg estimados publicados;
  LynxBMSNG500A/MultiPlus-II48/5000,MPPTs,Orion48/12-30 eAGM22Ah.
  Manual inversor recomenda≥200Ah/fusível200A/70mm² por poloaté5m; não cabo de tração.
- Indução trocada para **IE3TP220V60Hz2000W**,280×358×62mm/2,3kg sobre tampo
  contínuo. Manual2025p17 conferido visualmente; loja genérica1500W mistura versões.
- Viewer offline **23seletores**,157meshes interior+208elétrica; vista técnica e
  isolamento doHVAC. Browsererrors[]/HTTPrequests[]. Reimportados todosSTEP positivos:
  interior157, fixa146, extensão recolhida239/aberta311, elétrica208.
- Triagem23envelopes equipamentos semsobreposição; não comprova estrutura/portas/rotas.
  Massa serviços+115,4kg; subtotal**3373,355178kg**,saldoPBT876,644822kg antes faltantes.
- Solar fixo1540W/5,506849kWhdia; extensão opcional2890W/9,188909–10,326774 em
  modelos diferentes de sombra, teto não validado. Habitação agora**5,276506kWhdia**
  semsecagem;saldo fixo**0,230343kWhdia** antes de armazenamento/conversão.
- **117passed (1,44s)**,ruffsrc/scripts/tests OK,estrutura/auditoria0erros.
  **27itens parciais/8não iniciados/0aprovados**; I07 iniciou apenas fiação de serviços.
  Global YAML intacto24nulls;SHA`7b8f5cd7891eb437cb89c41fd2ba440b0567ca1063998042d4828086aad523e2`.
  Memorial parcial**18páginas/1903237bytes**,renderizado/conferido;63artefatos com hashes.

## Onde continuar, sem carregar anexos pesados

Ler `AGENTS.md`, `docs/CAD_TRACAO_E_SERVICOS.md`, final de`docs/ESTADO_ATUAL.md`,
`docs/REVISAO_35_ITENS.md`. `CONTINUIDADE_CAD_ELETRICO.md` preserva detalhes anteriores.
Entrega: `entregas/parcial_2026-10-24/{visualizador.html,tracao_e_servicos.step,
resumo_integracao_eletrica.json,proveniencia_eletrica.json,manifesto_entrega.json}`.
Memorial:`output/pdf/memorial_revisao_aurora.pdf`.

Configs:`config/{instalacoes_eletricas_proposta,equipamentos_interior,servicos_proposta}.yaml`.
Scripts:`gerar_cad_eletrico.py`, `calcular_integracao_eletrica.py`,
`consolidar_eletrica.py`, `gerar_cad_instalacoes.py`, `gerar_visualizador.py`,
`visualizador/{scene.js,verificar.cjs}`, `gerar_memorial_revisao.py`.
Novo módulo/testes:`src/motorhome/integracao_eletrica.py`, `tests/test_integracao_eletrica.py`.

Cache foraGit `/home/mhc/motorhome_referencias_tarefas/`:
**cad-eletrico-02,instalacoes-05,visualizador-eletrico-03/qa,expansao-solar-03,
integracao-eletrica-02,tracao-fontes-01,memorial-qa-04**.
`consolidar_eletrica.py` recebe caches explicitamente; **não executar
consolidar_expansao.py antigo**, sobrescreveria os novos artefatos.
Textos de enunciado/apostila em`/home/mhc/motorhome_referencias/textos/`:usar`rg`/trechos.

Shell normal falha bwrap/loopback; `exec_command` com`require_escalated` funciona.
`.venv` própria; Node/esbuild/Playwright em cache`software/visualizador-dev/node_modules`,
Chromium`/snap/bin/chromium`. Comandos na worktree:

```bash
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python -m ruff check src scripts tests
.venv/bin/python scripts/verificar_estrutura.py
.venv/bin/python scripts/auditar_projeto.py
```

## Próxima etapa técnica, ainda aberta

Fechar circuito12/48V/EVSE/terra/DR/frequências/faixas de tensão e simultaneidade;
Orion é conversor, não carregador inteligente. Conferir geometriaOEM/rodas/estrutura,
fixações/ventilação/AC, BOM/custos/eixos. FreshWell2700W vs carga2646W só2%nominal:
curva33°C e vazão/retorno/condensador/drenagem ainda faltam. Novos tubos são conceituais.
Obter mapas/redução/Cr/pack e executar casos físicosI30/33/34/35, CFD equipado e missões.
Cd0,653/0,625/0,581 exploratórios sem independência/camadas; agendas históricas com
2painéis/100Westacionado não representam o veículo atual. I27SOCfinal**exatos30%**,
sem8h; I29**7000km/até8hdiárias/semcargaexterna**; heurística1621,77dias não é ótimo.
I26km/kWh na bateria. I33 30→10m/s5s:400J/kg translacionais,não todo calor nos discos.
I34carga20/80kW não é calor. Vídeo8–10min com integrantes não pode ser fabricado.
