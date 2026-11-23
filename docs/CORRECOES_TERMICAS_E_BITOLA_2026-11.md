# Correções térmicas, de bitola e de faltas (20/11/2026)

Revisão do item 30 (temperatura dos cabos de alimentação do motor), do item 7
(proteções e faltas), do item 34 (sensibilidade térmica da bateria) e de sete
inconsistências numéricas/textuais do relatório. Nenhuma aprovação humana foi
inferida e nenhuma modificação física do chicote HV OEM é proposta.

Duas conclusões técnicas mudaram: no item 30, o cabo de 120 mm² **não** atende
fora do caso mais favorável; no item 7, os "56 casos acima de 20 kA" eram artefato
de uma hipótese de resistência não física, não um problema de fusível.

## 1. Resumo executivo

O item 30 concluía que o cabo de referência de 120 mm² operava a 85 °C, abaixo do
limite de 150 °C, e que portanto estava aprovado. Essa conclusão só vale no caso
mais favorável possível: cabo isolado, ar parado a 25 °C, radiação plena, uma
única fase. Ao refazer o contorno térmico com o que o veículo realmente impõe
(três fases agrupadas, conduíte, cofre do motor, radiação parcial, perdas AC), o
mesmo cabo chega a **158 °C no modo normal** — acima da própria ficha.

| Contorno (modo normal, 382 A) | 120 mm² | 150 mm² | 185 mm² | 240 mm² |
|---|---:|---:|---:|---:|
| Referência antiga (25 °C, radiação plena) | 62 °C | 53 °C | 46 °C | 40 °C |
| Rota protegida (50/70 °C) | 134 °C | 114 °C | 101 °C | 89 °C |
| Cofre do motor (60/80 °C, conduíte) | **158 °C** | 134 °C | **118 °C** | 104 °C |

Com o critério de projeto de **125 °C** (25 K de margem sobre a ficha de 3000 h),
a menor bitola é **185 mm² no cofre** e **150 mm² em trecho protegido**.

O pico de 205 kW (489 A) não governa a bitola: a constante de tempo térmica é de
23–45 min conforme a bitola, então 180 s de pico elevam a temperatura em apenas
1–3 K. Em 185 mm² no cofre, o regime normal fica em 118 °C e o pico pode ser
mantido cerca de 7 min antes de atingir 125 °C. Por isso o dimensionamento usa o
**modo normal como regime** e trata o pico pelo **transitório**.

## 2. O que estava errado no modelo de contorno

O solver r–θ (`motorhome.cabos_polares`) estava correto e **não foi alterado**:
volumes finitos em dois materiais, geração Joule com R(T), malha convergente
(6,9 × 10⁻⁵ K entre as duas malhas mais finas) e verificações analíticas com ordem
observada 1,84–1,86 no perfil radial e 1,997–1,999 na solução harmônica 2D.
O problema era o contorno aplicado por `fechar_i30_corrente_maxima.py`:

| Item | Antes | Agora |
|---|---|---|
| Sink radiativo | igual à temperatura do ar | **separado** (`T_rad ≠ T_ar`), com fator de forma |
| Radiação | plena (`ε=0,9`, visão total) | fator de forma configurável (conduíte bloqueia) |
| Convecção | livre | fator de confinamento (conduíte) |
| Fases | uma | **três agrupadas** (fração de perímetro exposta) |
| Perdas AC | ausentes | fator multiplicativo (skin/proximidade/PWM) |
| Regime | permanente no pico | **normal em regime, pico em transitório** |
| Ambiente | 25 °C | 50 °C (rota) e 60 °C (cofre) |

O novo módulo `src/motorhome/cabo_hv.py` implementa esse contorno. A soma de
convecção e radiação com sinks diferentes é exata para a linearização em `T_sup`
usando o sink ponderado `(h_conv·T_ar + h_rad·T_rad)/(h_conv+h_rad)`.

**Regressão:** com `n_fases=1`, `fator_forma=1`, `T_rad=T_ar` e `f_ac=1`, o módulo
reproduz exatamente o resultado anterior — **85,37 °C em 1×120 mm² a 489 A**. Esse
caso é um teste automatizado (`tests/test_cabo_hv.py`), de modo que o novo modelo
não pode divergir do antigo sem que o teste acuse.

## 3. Bitola: como a decisão é tomada

`scripts/fechar_i30_corrente_maxima.py` monta a matriz contorno × bitola × ponto de
operacão e grava:

- `resumo.json` — decisão, limites de corrente e transitório;
- `sensibilidade.csv` — 24 combinações contorno × bitola × potência;
- `limites_bitola.csv` — corrente e potência equivalentes para 125 °C;
- `transitorio_pico.csv` — τ, temperatura após 60/180 s e duração máxima admissível;
- `campo_corrente_maxima.png` — temperatura × bitola nos dois pontos de operação.

Regra explícita: menor bitola da tabela que satisfaz `T ≤ 125 °C` no modo normal,
no contorno de projeto. O script também calcula a bitola para a rota protegida e a
bitola de referência da configuração.

**Sobre as bitolas 185/240:** a ficha RADOX 155 confirmada no repositório cobre
120 e 150 mm². As linhas de 185 e 240 mm² são **derivadas por geometria calibrada**
nos dois pontos de catálogo (fator de enchimento 0,665, espessura de isolação
1,45 mm, R20 = 1,063·ρ/A), com erro < 1 % em diâmetro e R20 nos pontos conhecidos.
Estão marcadas `origem: derivado_calibrado` no YAML e **exigem confirmação na ficha
antes de qualquer compra**. Nada foi apresentado como dado de fabricante.

## 4. O que NÃO mudou, e por quê

- **Chicote HV OEM:** DEC-001 e DEC-040 proíbem modificá-lo. O resultado do item 30
  é um **requisito de verificação** da bitola original e, se ela não for comprovada,
  um limite de potência contínua. Não é uma compra de cabo nem uma alteração da van.
- **Massa do veículo:** o chicote HV já está contido na tara OEM de 2790 kg e os
  cabos de serviço estão cobertos pela reserva de 15 kg (`cabos_protecoes_controle`).
  Somar a massa do cabo de novo seria dupla contagem, como já registra
  `docs/CABOS_E_RADIADOR_2D.md`. `assembled_typical_mass_kg` permanece 3974,03 kg
  (base) / 3976,53 kg (cenário), e I25/I26/I27/I29 não foram reexecutados por massa.
- **Custo:** não existe preço por metro no repositório; o cabo está dentro da faixa
  agregada de R$ 8–18 mil (`eletrica_hidraulica`). A troca de bitola não move a faixa.
- **Raio do cabo no CAD:** `cable_radius_m: 0,007 m` corresponde ao cabo de 70 mm²
  dos serviços (Ø ≈ 14 mm), não ao HV — está correto e não foi alterado.

## 5. Item 7 — faltas e proteções

A triagem usava R interna de módulo de 1/5/20/50 mΩ — valores fisicamente baixos para
um módulo LFP de 48 V/100 Ah — sem intervenção do BMS. Isso produzia correntes
prospectivas de até **160 kA** e a conclusão de que "56 casos excedem 20 kA", o que
levava a recomendar um fusível de classe superior.

Duas correções foram aplicadas:

1. **Faixa de DCIR plausível** (10/20/30/40 mΩ), que é a mudança decisiva. Com ela o
   envelope pré-BMS fica em **2,75–16,05 kA** — abaixo da interrupção de 20 kA do
   JLLN 200 A **em todos os 144 casos, sem precisar invocar o BMS**.
2. **Limite do BMS aplicado** (a ficha do US5000 dá < 2000 A/1 ms por módulo; 6 kA com
   três módulos), que reduz a corrente entregue em 63 casos.

O ponto importante é a ordem: a correção da resistência resolve o problema sozinha; o
BMS é uma segunda barreira. A recomendação de "fusível de classe superior" foi retirada,
porque o problema era a hipótese de resistência, não o fusível. Coordenação I²t,
impedância real e ampacidade continuam **não
demonstradas**.

## 6. Item 34 — sweep de sensibilidade completo

O sweep oficial variava apenas massa, UA e cooler (54 casos), mantendo fixos os
**parâmetros que governam a geração de calor**: resistência do pack e entropia.
Agora o sweep é o produto cartesiano completo — massa (3) × UA bateria-refrigerante
(3) × UA refrigerante-ambiente (3) × R (3) × entropia (3) × potência (2) = **486 casos**.

Consequência: a faixa publicada em 80 kW passa de 29,7–34,9 °C para **25,1–45,0 °C**,
e o sweep revela **3 casos que atingem o limite de 45 °C e interrompem a carga**
(massa 500 kg, R 0,12 Ω, entropia +0,02 V/K), chegando a 80 % de SOC apenas em
71–76 %. Esse comportamento estava invisível no sweep anterior.

Artefato renomeado de `I34_54sensibilidades.csv` para `I34_sensibilidades.csv`
(o "54" deixou de ser verdade), com os checks do CI atualizados.

**Duas sensibilidades conviventes (pendência identificada, não resolvida):** além do
artefato acima, existe `equipe/P7.../I34/resultados/sensibilidade.csv`, gerado por
`scripts/calcular_bateria_carga.py`, com 20 linhas e colunas diferentes — ele varia
apenas R e entropia, sendo um subconjunto da malha de 486 casos. Não é um erro de
cálculo, mas são duas fontes de "sensibilidade do item 34" com nomes de coluna
distintos, o que induz comparação equivocada. Unificar exige decidir qual vira a
fonte (ou fazer o gerador antigo ler `development.thermal_sweep`), então ficou
registrado como pendência e não foi alterado neste PR.

## 7. Inconsistências corrigidas

| # | Correção |
|---|---|
| 1 | Item 23: "112,4 kWh úteis" somava 98 kWh úteis (tração) com 14,4 kWh **nominais** (serviços). Passa a declarar 98 kWh úteis + 14,4 kWh nominais (13,7 kWh úteis); 112,4 é apenas a soma de referência do modelo do item 29 |
| 2 | Item 9: o 150/60 tem pico de **98 %**, não 99 % (só o 250/60 tem 99 %) — corrigido no relatório, slides e roteiro |
| 3 | Item 9: o 250/60 não tem "limite 35 A". A ficha dá 60 A de Isc PV e 60 A de bateria; o 35 A era do modelo 150/35. A rejeição do 250/60 permanece válida, mas pelas **perdas de descasamento (0,657–27,272 %)**, não por corrente |
| 4 | Item 30: a evidência apontava para `cabos_HV_referencia/resumo_cabos.json` (varredura antiga), enquanto o relatório citava `i30_corrente_maxima`. Corrigido o ponteiro e a limitação ("corrente de fase desconhecida" não é mais verdade) |
| 5 | Item 8/25: explica-se que 13,9 kWh/dia é a janela fixa 08–16 h e 14,4 kWh/dia é o dia inteiro com portáteis abertos |
| 6 | `integracao_eletrica.py`: removido o hardcode `51,2 × 100/1000`, que impedia ler a energia do banco do YAML |
| 7 | `desenvolver_integracao.py`: `str(np.float64(...))` gerava CSV não reprocessável (`np.float64(-0.641)`) no NumPy 2; o inventário agora normaliza tipos |

## 8. Arquivos alterados

**Código novo/alterado**
- `src/motorhome/cabo_hv.py` (novo) — contorno completo e transitório
- `src/motorhome/integracao_eletrica.py` — remove hardcode
- `scripts/fechar_i30_corrente_maxima.py` — matriz, limites e transitório
- `scripts/desenvolver_protecoes_fixacoes.py` — faixa de DCIR plausível e limite do BMS
- `scripts/desenvolver_mecanica_termica.py` — sweep genérico (486 casos)
- `scripts/desenvolver_integracao.py` — serialização NumPy corrigida
- `scripts/registrar_execucao02.py`, `scripts/preencher_metodos_itens.py` — textos/evidências
- `scripts/comparar_teto_maxeon.py` — nota dos 60 A
- `scripts/fechar_i29_velocidade.py` — texto de energia inicial
- `scripts/verificar_cenario_integrado.py`, `scripts/verificar_desenvolvimento.py` — checks
- `tests/test_cabo_hv.py` (novo) — 14 testes

**Configuração**
- `config/parametros_globais.yaml` — `development.cable_hv`, `motor_mode_power_kw`,
  `thermal_sweep` com R/entropia, faixa de DCIR de faltas, notas do 250/60

**Relatório, slides e docs**
- `relatorio/relatorio.tex`, `relatorio/slides.tex`, `relatorio/roteiro_video.md`
- `docs/PROTECOES_SERVICOS_MODELO.md`, `docs/CABOS_E_RADIADOR_2D.md`
- `README.md`, `docs/FECHAMENTO_35_ITENS.md` (links para este documento)
- artefatos e manifestos regerados pelos próprios scripts

## 9. Verificação e golden values atualizados

```bash
export PYTHONPATH=src MOTORHOME_SCENARIO=maxeon1540_independente
.venv/bin/python -m pytest tests -q
ruff check src scripts tests
.venv/bin/python scripts/verificar_cenario_integrado.py
.venv/bin/python scripts/verificar_desenvolvimento.py
```

Resultado local: **287 testes passam**, `ruff` limpo, os dois verificadores
retornam `PASSOU`.

Golden values alterados, com justificativa:
- `verificar_desenvolvimento.py` (faltas): antes exigia `(~breaking_screen_pass).sum() == 56`;
  agora exige que **nenhum** caso exceda e que o envelope pré-BMS
  (`pre_bms_envelope_a.max()`) fique abaixo da interrupção, além de
  `bms_limited_a.max() == 6 kA`. O check deixou de contar casos e passou a comparar
  o envelope com a interrupção, que é o critério físico.
- `verificar_cenario_integrado.py`: `len(battery)` de **54 → 486**, exigindo as
  colunas `resistance_ref_ohm` e `pack_entropy_v_k`.

Os manifestos foram regravados por `--registrar` (que reescreve o manifesto e só
então compara hashes); nenhum hash foi editado à mão, e os ~200 checks físicos
rodaram antes do registro.

## 10. Limitações remanescentes

- Bitola mínima depende das hipóteses de contorno declaradas em
  `development.cable_hv` (60/80 °C, conduíte 0,70, fator de forma 0,30, três fases,
  fator AC 1,10). São hipóteses de engenharia, não medições.
- Bitolas 185/240 são derivadas; confirmação na ficha é obrigatória antes de compra.
- A corrente de fase depende de eficiência, fator de potência e tensão de barramento
  que o fabricante não publica; o valor de 489 A não é dado OEM.
- Não há efeito pelicular resolvido, condução axial, terminais/contatos, chicote
  completo nem EMC.
- O chicote HV OEM não foi e não deve ser modificado; a bitola original precisa ser
  verificada e, se menor que a necessária, a potência contínua deve ser limitada.
- A verificação de ampacidade e coordenação fusível↔cabo do lado 48 V continua
  pendente de tabela de fabricante e curvas I²t. O fusível de 200 A sobre 70 mm²
  exige ampacidade ≥ 200 A no arranjo real — não verificado.

## 11. Pendências deixadas explicitamente abertas

Itens identificados na revisão que **não** foram alterados neste PR, por exigirem
decisão de escopo:

1. **Sensibilidades duplicadas do item 34** — descrito na seção 6.
2. **Corrente inicial de 112,4 kWh no item 29** — o texto foi corrigido para separar
   nominal/útil, mas o modelo continua somando 98 + 14,4 kWh. Usar 13,68 kWh (95 %
   DoD) reexecutaria I25/I27/I29. Não se aplica porque a reserva de 20/30 % já é mais
   restritiva que o DoD.
3. **Triagem legada de 35 A em `comparar_teto_maxeon.py`** — a nota foi corrigida para
   60 A, mas o booleano `conservative_35a_screen_pass` ainda é calculado com 35. Ele
   não governa decisão (a rejeição do 250/60 vem do descasamento de 0,657–27,272 %).
4. **Verificar a bitola do chicote HV OEM** — requisito que este PR emite, não resolve.
5. **Ampacidade 70/95/120 mm²** do lado 48 V — sem tabela de fabricante no repositório.
