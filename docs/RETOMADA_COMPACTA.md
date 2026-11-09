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
