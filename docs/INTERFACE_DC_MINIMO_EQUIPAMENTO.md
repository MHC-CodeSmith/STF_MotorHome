# Estado vigente após os dois commits do PR #8

O segundo commit, `a0e962d`, aplicou o equivalente de 1 A × 380 V = 0,38 kW
na saída CC, de forma coordenada em I25/I29. O cenário1560 foi reexecutado;
refinamento final e primeira saída física constam em `i29_fechamento`.
O texto abaixo descreve o diagnóstico/proposta anterior e deve ser lido como histórico.
O limite de corrente CharIN não comprova que um equipamento real opere com o veículo;
90S e 380 V são referências de hipótese, não medição do pack escolhido.

---

# Limite de potência da interface CC — verificação documental do "1 kW"

**Data da consulta:** 2026-11-24
**Responsável:** revisão P2
**Escopo:** verificar se o mínimo hipotético de 1 kW usado em I25/I29 corresponde a
algum equipamento real e qual é o limite físico correto.

> Conclusão antecipada: **o valor de 1 kW não é rastreável ao equipamento** que o
> originou. Os documentos primários especificam o limite como **corrente** (1 A),
> não como potência. Converter 1 A com a tensão do pack do e-Ducato dá
> aproximadamente **0,35–0,40 kW**, e a norma admite explicitamente **0 A** em
> pausa. O piso de 1 kW superestima o custo em cerca de 5,7× (34 → 6 dias na
> missão de referência).

---

## 1. Sungrow IDC30E — origem registrada da hipótese

Estado no repositório: `config/parametros_globais.yaml` (`sources.sungrow`) cita
"FAQ mínimo ajustável 1kW". Esta consulta verificou os documentos primários.

**Ficha técnica (V2, 2025-07-22)** — lida integralmente:
`https://info-support.sungrowpower.com/application/pdf/2025/08/04/DS_20250722_IDC30E_Datasheet_V2_EN.pdf`

| Parâmetro | Valor publicado |
|---|---|
| Potência de saída CC | 30 kW |
| Tensão de saída CC | 200–1000 Vdc |
| Corrente de saída CC | 80 A |
| Entrada CA | 3/N/PE, 380/400 Vac (±10%), 50/60 Hz |
| Eficiência máxima | 96,5% |

**Manual do usuário (Ver17, 2025-08)** — lido integralmente:
`https://info-support.sungrowpower.com/product-materials/f95dc235-ae85-4be6-9f20-879163c1953a.pdf`

Achados relevantes:

- O único controle de potência documentado é de **máximo**: *"Click to adjust the
  **maximum** current/power of the CCU... each CCU corresponds to the **maximum**
  current/power output by a connector"* (§4.2.1).
- **Não existe nenhum valor de potência mínima de 1 kW** na ficha nem no manual.
- Proteção de subtensão de saída dispara abaixo de **195 V** (não é limite de
  potência).
- Alimentação é **CA trifásica**. Não é entrada FV/CC.

**Sobre a expressão "compatível com PV"** — a ficha diz *"Compatibility with
PV-ESS system reserved"* e o material de marketing diz *"Integrated with PV and
battery system"*. Isso descreve a solução **FV → armazenamento (ESS) → carregador
CC**, não FV → veículo direto. Continua sendo uma arquitetura distinta da
"interface DC direta" (arquitetura B) do projeto.

**Veredito:** o "1 kW" atribuído ao IDC30E **não se confirma** nos documentos
primários. Não foi possível recuperar o texto do FAQ citado; a página de FAQs da
Sungrow consultada não o lista. O registro atual deve ser tratado como
**não verificado**, e o equipamento não é referência válida para entrada FV/CC.

---

## 2. Norma CharIN — o limite correto é corrente, não potência

**CharIN e.V., "DC CCS Power Classes", V7.2, 2021-12-09** — lido integralmente:
`https://www.charin.global/media/pages/technology/knowledge-base/c6574dae0e-1639130326/charin_dc_ccs_power_classes.pdf`

Tabela 1 (requisitos mínimos por classe), trecho literal:

| Classe | Potência | U min | U max | **I min** | I pico | P ref |
|---|---|---|---|---|---|---|
| LPC (Low-Power Charging) | xx kW | ≤200 V | ≥920 V | **< 20 A** | < 20 A | — |
| DC | xx kW | ≤200 V | ≥920 V | **≤ 1 A** | ≥20 A | ≥8 kW |
| FC | xxx kW | ≤200 V | ≥920 V | **≤ 1 A** | ≥125 A | ≥50 kW |
| UFC | xxx kW | ≤200 V | ≥920 V | **≤ 5 A** | ≥250 A | ≥100 kW |
| HPC | xxx kW | ≤200 V | ≥920 V | **≤ 5 A** | ≥500 A | ≥150 kW |
| DC L (legacy) | xx kW | ≤200 V | ≥500 V | **≤ 1 A** | ≥16 A | ≥5 kW |

Definição literal da norma:

> "*I min of a charging station is the **minimum output current** that the
> charging station is able to deliver **continuously** at specific environmental
> conditions.*"

E, na Figura 1:

> "*0 A min. current is a special case and **should always be possible**
> (e.g. charging pauses).*"

Consequências para o modelo do projeto:

1. O requisito é **I min ≤ 1 A**, isto é, o carregador deve descer **até 1 A**.
   Não é "pelo menos 1 kW".
2. O piso é **contínuo** — não é um limiar de partida de sessão. A hipótese de
   "latch" (abrir sessão e depois aceitar qualquer potência) discutida
   anteriormente **não se sustenta** pela norma. O modelo atual, com piso
   contínuo por intervalo, está estruturalmente correto.
3. **0 A é previsto** para pausas. FV abaixo do piso não é "energia perdida por
   incompatibilidade", é pausa momentânea.
4. Existe uma classe específica para este caso de uso: **LPC (Low-Power
   Charging)**, com I min < 20 A.

### 2.1 O que 1 A vale em potência

O pack do e-Ducato 110 kWh **não opera a 400 V**. A plataforma Stellantis Pro One
(MCA 110 kWh, comum a e-Ducato, ProMaster, Proace Max, Movano, Jumper e Boxer) é
**90S**, com tensão de aproximadamente **270 V no mínimo e 380 V no máximo**.
O "400 V" da ficha OEM é o valor **nominal comercial**, não a tensão de carga.

| Tensão de pack | 1 A → |
|---|---|
| 270 V (SOC baixo) | 0,270 kW |
| 330 V (nominal 90S) | 0,330 kW |
| **380 V (SOC alto)** | **0,380 kW** |
| 400 V (nominal de ficha, não é tensão de pack) | 0,400 kW |
| 1000 V (topo da janela CharIN) | 1,000 kW |

Com a tensão correta do pack, 1 A vale **0,27–0,38 kW**. A coincidência exata
**1 A × 1000 V = 1,0 kW** é a hipótese aritmética mais provável para a origem do
número: tomou-se o I min da norma e multiplicou-se pelo **topo** da janela de
tensão CCS, não pela tensão real do pack. Não é possível provar a origem, mas a
conta fecha.

---

## 3. Equipamentos reais de FV → CC → veículo (arquitetura B)

### 3.1 Ampernext — carregador CC solar 30 kW (entrada FV direta com MPPT)

`https://www.ampernext.com/products/first-30kw-dc-dc-solar-ev-charger/`
(consulta 2026-11-24)

| Parâmetro | Valor publicado |
|---|---|
| Entrada FV | 300–800 Vdc (plena carga > 650 Vdc) |
| MPPT | 350–750 Vdc |
| Saída | 30 kW, 150–1000 Vdc, **1 A .. 100 A** |
| Conversão | > 95%, isolação galvânica |
| Normas | CE, EN/IEC 61851, DIN 70121, ISO 15118 |

Este é o produto mais próximo da arquitetura do projeto. O limite inferior é
declarado como **1 A de corrente**, não como potência — coerente com a norma
CharIN. Em 400 V equivale a 0,4 kW.

### 3.2 Enteligent LDF20 — EVSE CC/CC 20 kW

`https://cdn.prod.website-files.com/68483e349da6067e40280280/68af9410adb0c4d03aaabff1_Enteligent%20DC-to-DC%20EV%20Charger%20LDF20%20Spec%20Sheet.pdf`
(consulta 2026-11-24)

| Parâmetro | Valor publicado |
|---|---|
| Saída | 20 kW, 200–600 Vdc, **máx. 40 A** |
| Entrada | 760–840 Vdc (nominal 800) ou 640–760 Vdc (nominal 700) |
| Eficiência | > 97% média |

A ficha **não declara mínimo** de potência nem de corrente. Não sustenta um piso
de 1 kW.

### 3.3 Venema / 4x4electric — fonte citada pelo projeto

`https://4x4electric.com/charging-technique/` (consulta 2026-11-24)

O relato diz: *"With this DC charger, we are **limited to 30kW** of charging
power"* — um **máximo**. E: *"we estimated that we need **at least 10kWp** of
solar panels"* — dimensionamento de painéis, não mínimo do carregador.
Confirma a nota já existente no `config` (`evidence: 30kW é máximo; 10kWp é
dimensionamento daquela missão, NÃO mínimo OEM`). **Não há qualquer mínimo na
fonte citada.**

---

## 4. Lado do veículo — onde o piso real pode estar

O e-Ducato é documentado publicamente apenas em termos de máximos:

- 79 kWh de bateria; CC até **50 kW** via CCS2; OBC CA de 7,4/11/22 kW.
  Fontes: `https://www.e-station.it/scheda-auto-elettrica/fiat-e-ducato-79-kwh`
  e `https://www.elbilgrossisten.no/en/products/fiat-e-ducato` (consulta 2026-11-24).
- Stellantis comunica OBC CA 22 kW e 0–80% em 55 min num carregador CC de
  150 kW, sem faixa DC, mínimos ou handshake
  (`fontes_externas/catalogo.csv`, entrada Stellantis 2026-05).

**Não foi localizada nenhuma fonte pública** com a corrente mínima de carga CC,
o piso de tensão do pack em carga, ou a política do BMS/VCU do e-Ducato para
potência variável. Isso permanece **lacuna real** — é o item que só documentação
de *body builder* da Stellantis ou resposta do OEM resolve.

Observação técnica: em CCS, o mínimo efetivo é a composição de
`I min` do EVSE (norma: ≤1 A) com o mínimo que o **veículo** aceita no
handshake ISO 15118-2/DIN 70121. O gargalo pode estar no veículo, não no
carregador. O projeto não tem esse dado.

---

## 5. Impacto quantificado

Modelo do projeto, missão de 7.000 km, 15 min, 20,8 km/h, reservas 0,1/0,2,
perfil de céu limpo de 21/06. O piso é aplicado à potência **entregue à bateria**
(convenção de `reconciliacao.passo_solar`).

| Piso | Dias | Δ vs sem piso | Δ vs 1 kW |
|---|---|---|---|
| sem piso (limite de coleta) | 208,79 | — | −34,01 |
| **0,38 kW (1 A @ 380 V, adotado)** | **212,79** | **+4,00** | **−29,60** |
| 0,50 kW | 214,76 | +5,97 | −28,04 |
| 0,80 kW | 233,76 | +24,97 | −9,04 |
| 1,00 kW (hipótese anterior) | 242,80 | +34,01 | 0,00 |

Valores de referência do modelo anterior, mantidos para comparação do efeito do
piso. O piso adotado de 0,38 kW leva a missão a **212,79 dias** contra
**242,80 dias** com 1 kW — redução de **30,0 dias** e **12,4%**.

Nota estrutural: com piso de 1 kW, o **teto sozinho (pico 0,905 kW) nunca
habilita** a cadeia. Com o piso derivado de 0,38 kW, o teto passa a contribuir.

---

## 6. A inconsistência entre I25 e I29 é o η_dc — e foi corrigida

Antes da correção:

- `despacho_diario.alocar_dia` (I25) comparava o piso com a potência **FV de
  entrada**: `eligible = park & (pv >= minimo_dc_kw)`.
- `reconciliacao.passo_solar` (I29) compara com a potência **entregue**:
  `extra*eficiencia_dc/dt_h >= minimo_dc_kw`.

O mesmo "1 kW" produzia exigências diferentes por exatamente **1/η_dc**:

| η_dc | I25 aceitava | I29 exige | Fator |
|---|---|---|---|
| 0,85 | 1,000 kW | 1,176 kW | 1,176 |
| **0,90** | **1,000 kW** | **1,111 kW** | **1,111** |
| 0,95 | 1,000 kW | 1,053 kW | 1,053 |
| 1,00 | 1,000 kW | 1,000 kW | 1,000 |

Fisicamente, um limite de carregador é especificação de **saída**; a convenção
do I29 é a correta e a do I25 lia a entrada como se fosse a especificação.

**Correção aplicada** em `src/motorhome/despacho_diario.py`: tanto o filtro de
intervalos elegíveis quanto a restrição MILP passaram a comparar a potência
entregue (`pv*eta_dc >= minimo_dc_kw`, e `minimo_dc_kw*dt_h/eta_dc` na
restrição). Dois testes novos travam a equivalência:

- `test_minimo_dc_usa_a_mesma_convencao_de_saida_que_o_replay` (η = 0,7/0,9/1,0)
- `test_minimo_compara_potencia_entregue_e_nao_a_entrada_fv`

Efeito no I25 (21/06, 5 min, só tração):

| Piso | Antes | Depois |
|---|---|---|
| 0 kW | 57,60 / 31,94 km | 57,60 / 31,94 km |
| 0,38 kW (adotado) | — | **56,57 / 31,37 km** |
| 1 kW | 51,49 / 28,55 km | 50,08 / 27,77 km |
| 3 kW | não inicia | não inicia |

O valor de 0 kW não muda (o piso é inativo), confirmando que a correção só afeta
a leitura do limiar. A linha de 1 kW é mantida porque o valor antigo está em
documentos históricos; o cenário ativo passou a usar 0,38 kW.

## 6.1 Derivação e adoção do piso de 0,38 kW

O parâmetro deixou de ser um kW solto e passou a ser derivado. Em
`config/parametros_globais.yaml`:

```yaml
hypothetical_min_dc_current_a: 1     # CharIN: Imin <= 1 A
hypothetical_min_dc_voltage_v: 380   # topo do pack 90S (~270-380 V)
hypothetical_min_dc_kw: 0.38         # 1 A x 380 V
```

Escolheu-se 380 V por ser o **extremo superior** da janela do pack: dá o maior
kW equivalente e, portanto, o **piso mais exigente** dentro da faixa, sem
recorrer ao nominal de ficha de 400 V. É uma escolha conservadora declarada, não
uma medida.

O sweep do I25 (`hypothetical_dc_min_input_kw`) passou de `[0, 1, 3]` para
`[0, 0.38, 3]`, preservando as 630 alocações MILP. Os scripts que fixavam
`==1` para escolher a curva plotada agora derivam o valor do config.

### Efeito nos resultados

| Item | Antes (1 kW) | Depois (0,38 kW) |
|---|---|---|
| I25, só tração, 40 km/h | 51,49 km | **56,57 km** |
| I25, só tração, 80 km/h | 28,55 km | **31,37 km** |
| I29, líder 15 min (0,1/0,2) | 242,80 d | **213,82 d** |
| I29, líder 1 min (0,1/0,2) | 248,78 d | **212,79 d** |
| I29, líder 1 min (0,2/0,3) | 250,78 d | **214,76 d** |

A missão encurta **30 dias** (12,4%). Note que com o piso derivado o resultado a
1 min passa a ser **melhor** que a 15 min — antes era o contrário. A divergência
de ~6 dias entre resoluções era em boa parte artefato do limiar alto interagindo
com a discretização, o que reforça o diagnóstico de aliasing.

---

## 7. Por que não basta "usar 400 V"

O 400 V do `config/parametros_globais.yaml` (`traction_voltage_v`) **não está
errado**: ele reproduz a ficha OEM SK MY25 ("110/98 kWh, **400 V nominais**",
p.4) e está marcado `confidence: alta`. Mas ele é uma tensão **nominal
comercial**, não a tensão em que a bateria se encontra durante a carga.

A plataforma real é **90S**, com cerca de **270 V no mínimo e 380 V no máximo**.
Isso importa porque o limite do carregador é de **corrente**: para um mesmo
`I_min`, a potência equivalente varia com a tensão instantânea.

| Critério | Valor | Situação |
|---|---|---|
| 400 V (ficha OEM, nominal) | 0,400 kW | rastreável, mas não é tensão de carga |
| **380 V (SOC alto, topo real)** | **0,380 kW** | **adotado: pior caso de coleta** |
| 330 V (nominal 90S) | 0,330 kW | ponto médio da arquitetura |
| 270 V (SOC baixo) | 0,270 kW | extremo inferior |

Usar 400 V seria defensável como aproximação do lado alto, mas apresentá-lo como
a tensão de operação do pack repetiria o erro de origem do "1 kW". Adotou-se
380 V, o topo real do pack, que é conservador sem invocar um valor nominal.

**Não se alterou `traction_voltage_v`**, porque ele é consumido pelo I30
(corrente de fase do motor) onde o nominal de ficha é o valor apropriado. A
tensão de carga do pack entrou como parâmetro separado do piso.

---

## 8. O que isto significa para o projeto

1. **O "1 kW" não está demonstrado.** Não aparece nos documentos primários do
   IDC30E, não aparece na fonte Venema, e não corresponde ao formato do limite
   (que é corrente).
2. **A hipótese foi usada sem saber o impacto final** — a suspeita se confirma.
   O valor entrou como plausibilidade de engenharia e acabou dominando a
   conclusão do I29 (+34 dias), porque ficou **acima do pico do gerador**.
3. **Forma correta do parâmetro:** `I_min` em ampères (≤1 A por norma), aplicado
   sobre a tensão do pack. Não um kW fixo.
4. **Magnitude correta:** ~0,27–0,38 kW no e-Ducato (90S), não 1 kW.
5. **A estrutura do modelo está certa** (piso contínuo, pausa a 0 A). O que está
   errado é a unidade e o valor.
6. **A inconsistência I25/I29 foi corrigida**, não apenas documentada. Ver §6.

### Pendências que continuam abertas

- Corrente mínima real de carga CC do e-Ducato (BMS/VCU) — **sem fonte pública**.
- Autorização/compatibilidade OEM para qualquer equipamento FV→CC.
- Texto original do FAQ Sungrow, caso se queira encerrar formalmente a rastreia
  do "1 kW".

### O que foi alterado nesta revisão

- `src/motorhome/despacho_diario.py`: piso passou a ser comparado na **saída**,
  igualando a convenção do I29. Dois testes novos em
  `tests/test_despacho_diario.py` travam a equivalência.
- `entregas/integrado_maxeon1540/despacho_i25/*`: regenerado. Valores de 1 kW
  mudaram de 51,49/28,55 km para 50,08/27,77 km.
- `relatorio/relatorio.tex`, `docs/REVISAO_GERAL_PROJETO.md`,
  `docs/EXECUCAO_TECNICA02.md`, `docs/SINTESE_DESENVOLVIMENTO_TECNICO.md`,
  `docs/RETOMADA_COMPACTA.md`, `docs/RETOMADA_DETALHADA_*`: valores atualizados.
- `entregas/indice_execucao_35.json`: reemitido, pois o `resumo.json` do I25 é
  evidência do item 25.
- Manifestos re-registrados pelos verificadores oficiais (`--registrar`).

### Recomendação de mudança ainda pendente (não aplicada)

O `config/parametros_globais.yaml` **não foi alterado**. O hash do YAML está
encadeado em `metadata`, `parametros_resolvidos.json` e nos
`entradas_por_executor`; mexer nele isoladamente quebra a cadeia. O registro de
que a fonte `sungrow` não se confirma ficou neste documento e no
`fontes_externas/catalogo.csv`.

Alterar o parâmetro exige uma reemissão coordenada. Proposta para deliberação:

1. Substituir `hypothetical_min_dc_kw: 1` por `hypothetical_min_dc_current_a: 1`
   com a tensão de pack do cenário, mantendo o kW equivalente explícito e
   declarando a tensão usada.
2. Reemitir I25/I29 com o novo parâmetro em passo de 1 min.
3. Regenerar manifesto, `parametros_resolvidos.json` e matriz de decisões na
   mesma alteração, para não deixar hash órfão.
4. Se a decisão for manter 1 kW como sensibilidade conservadora, rotular
   claramente como **hipótese não rastreável**, não como mínimo de equipamento.

Como o resultado publicado (242,8021 dias) depende de um parâmetro cuja origem
não se confirma, ele deve continuar rotulado como **condicional**. Não é
necessário retirar o número; é necessário deixar de apresentá-lo como se o
"1 kW" fosse um dado de projeto.

---

## Fontes consultadas (2026-11-24)

1. Sungrow, *IDC30E Datasheet V2* (2025-07-22) —
   https://info-support.sungrowpower.com/application/pdf/2025/08/04/DS_20250722_IDC30E_Datasheet_V2_EN.pdf
2. Sungrow, *IDC30E DC Charger User Manual*, Ver17-202508 —
   https://info-support.sungrowpower.com/product-materials/f95dc235-ae85-4be6-9f20-879163c1953a.pdf
3. CharIN e.V., *DC CCS Power Classes*, V7.2, 2021-12-09 —
   https://www.charin.global/media/pages/technology/knowledge-base/c6574dae0e-1639130326/charin_dc_ccs_power_classes.pdf
4. Ampernext, *30kW Solar DC to DC EV Charger* —
   https://www.ampernext.com/products/first-30kw-dc-dc-solar-ev-charger/
5. Enteligent, *LDF20 DC-to-DC EVSE Spec Sheet* —
   https://cdn.prod.website-files.com/68483e349da6067e40280280/68af9410adb0c4d03aaabff1_Enteligent%20DC-to-DC%20EV%20Charger%20LDF20%20Spec%20Sheet.pdf
6. 4x4electric / Venema, *Charging technique* (2022-04-30) —
   https://4x4electric.com/charging-technique/
7. e-Station, *Fiat E-Ducato (79 kWh)* —
   https://www.e-station.it/scheda-auto-elettrica/fiat-e-ducato-79-kwh
8. elbilgrossisten, *The charging guide — FIAT e-Ducato* —
   https://www.elbilgrossisten.no/en/products/fiat-e-ducato

Reprodução numérica: `scripts/analisar_aliasing_limiar_dc.py` (diagnóstico
existente) e sensibilidade de piso em corrente descrita neste documento.
