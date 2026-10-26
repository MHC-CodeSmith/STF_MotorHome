# Retomada compacta — 26/10/2026

## Objetivo e limites

Concluir os **35 itens** do motorhome **elétrico solar Aurora Solar**, seguindo
enunciado/apostila SEM0571 e requisitos do professor. Usuário quer autonomia,
pesquisa online quando necessária e CAD realista. **Ainda não concluído:**
35 em desenvolvimento, 0 aprovados. Este turno pediu só preservar contexto.
Logo/pintura externa foram pedidos **depois da parte técnica**; não antecipar.

Worktree exclusiva: `/home/mhc/motorhome_solar_codex_tarefas`, branch
`hub/tarefas-motorhome-com-codex`. Outra conversa usa
`/home/mhc/motorhome_solar_codex`: **não editar/copiar alterações dela**.
Último commit técnico **`9742cd5`**, árvore limpa antes desta nota;
anteriores `0cec31e` (freios), `d975212` (cabos/radiador).
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

Último resultado: **158 testes/6,37s**,ruffOK,estrutura/auditoria0erros;
124artefatos+PDF e entradas atuais conferidos; renderQA07/08. Não equivale a validação física.
Global intacto24nulls, SHA256
`7b8f5cd7891eb437cb89c41fd2ba440b0567ca1063998042d4828086aad523e2`.

## Próximo trabalho real

CFD equipado/malhas, massa/BOM/eixos/fixações, mapasOEM e óleo correto, custos completos,
agendasI27/I29 atuais com montagem portátil e interfaceHV. I27 terminaSOC **exatamente30%**;
limite8h/dia pertence sóI29,7000km, bateria inicial+solar, sem recarga externa.
Não substituir dados físicos por testes sintéticos ou dizer que35 foram concluídos.
Revisão cruzada e vídeo/seminário com integrantes continuam necessários.
