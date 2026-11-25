> Documento de revisão histórica. Tratamento e comparações na versão atual:
> [leitura integrada das simulações](REVISAO_LEITURA_E_COMPARACOES.md) e
> [auditoria de todos os PRs](AUDITORIA_ENUNCIADO_E_PRS.md).

# Parecer P7: Herick Eliseu

Registro da revisão final por integrante ([guia](REVISAO_INTEGRANTES.md)). Os campos seguem o
modelo de issue **Revisão do integrante** (`.github/ISSUE_TEMPLATE/revisao_integrante.yml`).

| Campo | Valor |
|---|---|
| Integrante | P7 — Arrefecimento e térmica da bateria |
| Nome (como deve aparecer na capa) | **Herick Eliseu** |
| Itens | I10, I12, I34 e I35; decisões provisórias A14 e A15 |
| Data | 16/11/2026 |
| Parecer | **Aprovado com as correções abaixo** |
| Base revisada | [`relatorio/relatorio.pdf`](../relatorio/relatorio.pdf) no commit `5144702` (16/11/2026); páginas pelo número impresso no rodapé |

## Conferi

- [x] enunciado de cada item atendido (lacunas listadas nas correções)
- [x] valores com unidade, condição e fonte
- [x] método, hipóteses e limitações corretos
- [x] figuras legíveis, com eixos e unidades
- [x] decisões provisórias (A01–A16) em que sou responsável (A14 e A15, ver abaixo)

## Correções (item, página e o que muda)

### Obrigatórias antes da entrega

1. **I35, p. 27 (Figura 29, painel direito): a figura é de outro caso.** `i35_radiador.png` é o
   estudo antigo de `scripts/calcular_radiador_cruzado.py`: entrada a 80 °C, 0,5 kg/s e cerca de 29,6 kW. O
   título interno diz “refrigerante 0,5 kg/s”. O texto da p. 26 descreve 0,557 kg/s, 66,8/55,1 °C
   e 22,9 kW. A figura correta já existe:
   [`entregas/desenvolvimento_2026-11-09/arrefecimento/campos_equilibrio.png`](../entregas/desenvolvimento_2026-11-09/arrefecimento/campos_equilibrio.png),
   idêntica a `equipe/P7_arrefecimento/I35_bomba_radiador_e_vazao/resultados/hidraulica_campos_equilibrio.png` (mesmo SHA-256).
   Trocar o caminho em [`relatorio/gerar_figuras.py`](../relatorio/gerar_figuras.py), linha 249.
2. **Bibliografia [bosch], p. 29:** trocar “0392024453G” por **039202453G**. O título da ficha Bosch é
   “039202453G - PCE2-XL Electric cooling pump”, e o texto do I10 já usa o número certo. Trocar também o URL
   genérico pelo URL completo do PDF, que está em [`config/hidraulica_proposta.yaml`](../config/hidraulica_proposta.yaml).
3. **I10, p. 10:**
   - Informar que 10,9, 22,9 e 36,3 kW **incluem os 96 W da bomba**. Só as perdas, 205·(1/η − 1), dão
     10,8, 22,8 e 36,2 kW.
   - Declarar que η_comb = 0,90 é um **caso conservador**: o I04 e o I30 usam η_m = 0,95, e com o inversor
     a 97–98% o calor a 205 kW seria de 15,2 a 17,5 kW.
4. **I12, p. 11:** substituir “aquece o óleo e é rejeitada por convecção na carcaça”. Em regime
   permanente na potência de pico isso não fecha: 6,15 kW com hA de 10 a 20 W/K exigiria ΔT de 300 a 600 K.
   Texto sugerido: “o pico é transitório (0–90 km/h em 10,6 s aquece o óleo e a carcaça cerca de 2 K); em
   regime sustentado, a perda segue para o circuito de água pela carcaça integrada ou exige trocador
   óleo–água, e entra na carga do radiador do I35”.
5. **I34, p. 26:** a faixa citada (25,5–26,6 °C e 29,7–34,9 °C) varia só massa e UA. Acrescentar
   a varredura de resistência interna × dU/dT, que já está em
   [`equipe/P7_arrefecimento/I34_temperatura_da_bateria_em_carga/resultados/sensibilidade.csv`](../equipe/P7_arrefecimento/I34_temperatura_da_bateria_em_carga/resultados/sensibilidade.csv):
   **20 kW: 23,8 a 28,3 °C; 80 kW: 25,2 a 40,8 °C**. Dizer também que, no caso nominal, dU/dT = 0, ou seja,
   o calor reversível é nulo.
6. **I34 e I35, p. 26–27 (texto e Figuras 28 e 29):** trocar “refrigerante” por **“fluido de arrefecimento”**. “Refrigerante”
   pode ser lido como o fluido do A/C. Os rótulos vêm de `scripts/calcular_bateria_carga.py` e de
   `scripts/calcular_hidraulica.py`.

### Recomendadas (completam o enunciado)

7. **I10, p. 10:** o enunciado pede “material, dimensão, quantidade, marca/modelo, tipo, peso”. Acrescentar uma
   tabela de especificação com bomba, radiador, ventilador, fluido (MEG 50/50 e volume), mangueiras,
   vaso de expansão e tampa, e placa fria com chiller da bateria, marcando “OEM”, “estimado” ou “hipótese”.
   Incluir a ventilação do armário de 48 V, já calculada em
   [`equipe/P7_arrefecimento/I10_resfriamento_de_componentes_eletricos/teoria.md`](../equipe/P7_arrefecimento/I10_resfriamento_de_componentes_eletricos/teoria.md)
   mas ausente do relatório: 4000 W com η = 0,90 dão **444 W de perdas e exigem ≥ 0,040 m³/s (≈ 145 m³/h)**
   para um aquecimento do ar de 10 K.
8. **I12, p. 11:** tabela de lubrificantes:
   - **redutor:** fluido de transmissão de baixa viscosidade para VE, ≈ 1–2 L, em banho;
   - **rolamentos de roda:** graxa de complexo de lítio NLGI 2;
   - **juntas homocinéticas:** graxa própria para homocinéticas;
   - **compressor elétrico do A/C:** óleo POE dielétrico;
   - direção EPS, sem fluido.

   Rotular como “típico” o que não for dado OEM. Incluir a tabela de perdas que já existe em
   [`I10_I12_balanco_perdas.csv`](../entregas/integrado_maxeon1540/mecanica_termica/I10_I12_balanco_perdas.csv).
9. **I35, p. 26:** explicitar o **critério de projeto**, por exemplo entrada do líquido no inversor ≤ 65 °C, e
   relacionar a “potência máxima de utilização” ao **I21** (140 kW nas rodas no pior caso sustentado,
   ≈ 11–13 kW de perdas). Manter 205 kW em regime permanente como envelope conservador: o pico dura cerca de 10 s
   e aquece o circuito em cerca de 4 K. Com 1 kg/s de ar, a entrada ≤ 65 °C exige UA ≈ 1,1 kW/K para 22,9 kW;
   com UA = 1000 W/K, o caso nominal fica em 66,8 °C.
10. **I35, p. 26:** acrescentar a sensibilidade das quedas de pressão dos componentes, que respondem por 68% do Δp,
    ou 48,5 de 71,6 kPa. Com o dobro, a vazão cai para 26,4 L/min; com o triplo, para 23,1 L/min. Acrescentar
    também a verificação de NPSH: ≈ 12 m com tampa de 100 kPa(g) e ≈ 2,6 m sem pressurização a 90 °C, o que
    justifica o vaso pressurizado.
11. **I34, p. 26:** incluir o pior caso. Com R = 0,12 Ω, dU/dT = +0,02 V/K, 500 kg e UA de 125/250 W/K, a carga de
    80 kW **para a 45 °C** em 0,66 h, ou em 0,37 h se começar a 35 °C. Usar esse resultado para especificar um
    chiller de ≈ 3–5 kW térmicos.

## Decisões provisórias em que sou responsável

- **A14, parâmetros físicos e validação:** de acordo com a recomendação provisória, com a ressalva de que
  os modelos do P7 são representativos e **não calibrados com dados OEM**. Os parâmetros críticos precisam
  ter faixa publicada no relatório: R_pack, dU/dT e UA no I34; UA do radiador, Δp dos componentes e η no
  I35 (correções 5, 9 e 10).
- **A15, proteções, controle e monitoramento:** de acordo com o monitoramento básico comercial.
  Contribuição do P7: uma tabela de limites térmicos (parada da bateria a 45 °C, já usada no I34; entrada
  do líquido no inversor ≤ 65 °C, a confirmar; limite do óleo do redutor; faixas de operação do US5000 e
  do MultiPlus-II) e o derating do MultiPlus-II com a temperatura (4000 W a 25 °C pela ficha).

## Pedidos aos outros integrantes (interfaces)

| Para | Pedido | Usado em |
|---|---|---|
| P4 | Tabela única de η_m, η_inv e η_red no pico e no pior caso sustentado (140 kW nas rodas); confirmar se o redutor é integrado à carcaça arrefecida | I10, I12, I35 |
| P2 | Configuração do pack (células em série e paralelo, Ah, resistência da célula), massa, limites do BMS (corrente e temperatura), potência do OBC | I34, I10 |
| P1 | Lançar no I18 a massa e no I24 o custo dos componentes de arrefecimento adicionados (ventilação do armário, sensores) | I18, I24 |
| P6 | Confirmar que o FreshWell é independente do chiller OEM; avaliar a carga térmica do armário de 48 V no interior | I10, I32 |

## Reprodução

- **Testes:** os 51 testes dos módulos do P7 passaram:
  `PYTHONPATH=src python -m pytest tests/test_bateria_carga.py tests/test_hidraulica.py tests/test_radiador_cruzado.py tests/test_sistemas_termicos.py tests/test_termica_2d.py -q`.
- **Scripts:** `scripts/calcular_bateria_carga.py --destino <novo>` e `scripts/calcular_hidraulica.py --destino <novo>`
  reproduzem exatamente os números do relatório:

| Grandeza | Relatório | Reexecução |
|---|---|---|
| I34, 20 kW | 2,96 h; 25,9 °C | 10 666 s; 299,02 K (25,87 °C) |
| I34, 80 kW | 0,76 h; 32,0 °C | 2 721 s; 305,12 K (31,97 °C) |
| I35, ponto de operação | 31,9 L/min; 71,6 kPa; 96/38 W | 31,85 L/min; 71,63 kPa; 96,0/38,02 W (39,6%) |
| I35, η = 0,90 | 66,8 / 55,1 °C | 339,99 / 328,27 K (66,84 / 55,12 °C) |
| I35, η = 0,85 | 91,4 °C | 364,51 K (91,36 °C) |

As verificações independentes estão no [Anexo A](#anexo-a-verificações-independentes).

---

# Análise técnica completa

Legenda: ✅ atende · ⚠️ atende parcialmente ou com ressalva · ❌ não atende

## 1. Resumo

**Projeto como um todo.** O nível técnico é alto para uma disciplina de graduação. Destacam-se:

- rastreabilidade: um YAML único com fonte, unidade e situação de cada parâmetro, além do SHA-256 das entradas e de CI;
- verificação numérica: estudos de malha e de passo, resíduos de energia e comparação com soluções analíticas;
- honestidade sobre as limitações de cada item.

Os riscos para a nota estão em quatro pontos:

1. **Requisitos literais não cumpridos.** O tempo de 0 a 100 km/h do I28 não foi calculado. As especificações do I10 e do I12 não trazem material, dimensão, quantidade, marca/modelo, tipo e peso.
2. **Inconsistências entre itens.** O rendimento do motor difere entre os itens 4, 10, 22, 30 e 35. A energia solar é de 13,9 kWh no I08 e 14,4 kWh no I25.
3. **Dependência de uma hipótese.** Os itens 25, 27 e 29 dependem da interface CC hipotética (B01).
4. **Pendências formais.** Faltam os nomes na capa, o vídeo não foi gravado e os pareceres estão pendentes.

**Itens do P7.** O I34 e o I35 são os mais fortes em modelagem e verificação. O I10 e o I12 são os mais fracos frente ao enunciado.

## 2. Projeto frente ao enunciado

### 2.1 Requisitos gerais e formais

| Requisito do enunciado | Situação | Observação |
|---|---|---|
| Grupo de 10 alunos | ⚠️ | O grupo tem 7. Confirmar a autorização ([PERGUNTAS_PARA_PROFESSOR.md](PERGUNTAS_PARA_PROFESSOR.md)). |
| 21/06, São Carlos, 25 °C, UR 50%, vento nulo | ✅ | ρ_ar = 1,10 kg/m³ é uma hipótese central; o valor físico a 859 m e 25 °C é ≈ 1,07 kg/m³. |
| Introdução, revisão bibliográfica, memorial, resumo e referências | ✅ | A revisão bibliográfica não trata de gerenciamento térmico de VE (chiller, placas frias, circuitos). |
| Especificações 1–16 com material, dimensão, quantidade, marca/modelo, tipo e peso | ⚠️ | Boas nos itens 2, 6, 7, 8, 9, 11 e 13. Fracas no I10 e I12 (P7), no I03 (freio traseiro, pinças, pastilhas, fluido) e no I14 (só descritivo). |
| Anexo de códigos e PDF < 20 MB | ✅ | 6,6 MB. |
| Vídeo de 8–10 min, < 50 MB, todos com tempo semelhante | ⚠️ | Existe o roteiro ([`relatorio/roteiro_video.md`](../relatorio/roteiro_video.md)). Falta gravar. |
| Capa com os integrantes | ❌ | As linhas de nome estão em branco. |
| Seminário de 8 min com apresentador sorteado | ⚠️ | Qualquer integrante pode ser sorteado, então todos precisam dominar os 35 itens. |

### 2.2 Inconsistências entre itens

1. **Rendimentos não unificados.**
   - O I04 usa η_m = 0,95 no canto; o I30 usa η_m = 0,95; o I10 e o I35 usam η_comb = 0,90; o I22 usa η_bat→roda = 0,90.
   - O mapa do I04 dá η_m ≈ 0,855 em cruzeiro a 90 km/h ([Anexo A.2](#a2-rendimento-e-calor-pelo-modelo-de-perdas-do-i04)).
   - Proposta: uma tabela única de rendimentos (motor, inversor e redutor por ponto de operação), mantida pelo P4.
2. **Energia solar diária:** 13,9 kWh no I08 (5,86 + 8,04) contra 14,4 kWh gerados no I25.
3. **I23:** “112,4 kWh úteis” soma o útil da tração (98) com o nominal do banco (14,4). O útil seria 98 + 13,7 = 111,7 kWh.
4. **I27 e I29:** 20,7 km/h é o ótimo matemático, mas fica abaixo do mínimo legal em rodovia (CTB, art. 62: metade da máxima da via). Convém apresentar também uma versão com velocidade mínima de 40 a 60 km/h.
5. **I28:** 0–100 km/h é pedido no enunciado. Com o mesmo modelo, sem limitador, dá ≈ 12,3–12,9 s ([Anexo A.10](#a10-i28-estimativa-sem-limitador)).
6. **I32:** com a ventilação exigida pelo CO₂ são necessários 2,87 kW, mas o FreshWell entrega 2,7 kW. Fica um déficit de 0,17 kW na condição de projeto.
7. **I19:** Cd = 0,622 e C_dA ≈ 3,0 m² ficam 1,4 a 2 vezes acima da faixa citada para furgão (0,30–0,45). Sugestão: um caso de controle com a carroceria limpa, sem o deck.
8. **I07:** 56 casos de falta passam de 20 kA, a capacidade de interrupção do fusível, sem decisão final.

### 2.3 Observações por integrante (sugestões; a decisão é de cada responsável)

| Integrante | Pontos fortes | Sugestões |
|---|---|---|
| **P1** | Massa por parcelas com CG e 162 casos; custo com cascata tributária datada; I33 com campo r–z e verificação analítica | Completar a especificação do I03 e do I14; lançar no I18 e no I24 os componentes de arrefecimento adicionados |
| **P2** | US5000/Victron bem documentados; 324 casos de queda de tensão e 144 de falta; I30 com SVPWM e convecção natural mais radiação iteradas | Fechar a proteção dos 56 casos > 20 kA; corrigir o rótulo do I23; enviar ao P7 os parâmetros do pack e os limites do BMS |
| **P3** | Diagnóstico do limite do snappyHexMesh; família de malhas refeita; incerteza correta para convergência oscilatória | Caso de controle sem deck; massas e dimensões de vidros e aberturas no I16 |
| **P4** | Envelope e mapa de η rotulados como modelo; 8100 casos no I21; I28 com aderência | Calcular 0–100 km/h e Vmax sem limitador; unificar η com o I22; enviar ao P7 η no pico e no pior caso sustentado |
| **P5** | pvlib com Faiman; despacho MILP com 630 casos; estudo de resolução no I29 | Explicar os 13,9 e 14,4 kWh; versão dos I27 e I29 com velocidade mínima legal |
| **P6** | Balanço de CO₂; I31 em 0D e CFD 3D; I32 com carga latente | Resolver o déficit do FreshWell; especificar o ventilador de reserva |

## 3. P7: análise aprofundada

### 3.1 I10, resfriamento dos componentes elétricos (p. 10)

**Pontos fortes**
- Circuito de motor e inversor separado do circuito da bateria, com níveis de temperatura distintos.
- Manter o circuito OEM é coerente com a decisão de não modificar o trem de força.
- O dimensionamento é remetido ao I35.

**Problemas**
- Calor com os 96 W da bomba incluídos sem aviso (correção 3).
- η_comb = 0,90 sem vínculo com o I04 (correção 3).
- Falta de especificação (correção 7).
- “Placa fria no mesmo princípio” sem citar o chiller (correção 11).
- Ausência de critérios de temperatura e de esquema do circuito (P&ID).

**Proposta de tabela de especificação** (preencher com fonte; quando o dado for estimado, rotular como tal)

| Componente | Tipo | Marca/modelo | Material | Dimensões | Qtd | Massa | Situação |
|---|---|---|---|---|---|---|---|
| Bomba elétrica | centrífuga BLDC, 12 V | Bosch PCE2-XL 039202453G | — | ficha | 1 | 0,46 kg | fabricante |
| Radiador | tubo plano com aleta veneziana, fluxo cruzado | OEM (não publicado) | alumínio brasado | ≈ 650 × 500 × 65 mm para UA ≈ 1,0–1,1 kW/K | 1 | ≈ 3–5 kg | estimado |
| Ventilador | axial, 12 V | a definir | PA/PP | Ø ≈ 380–400 mm | 1 | ≈ 2–3 kg | estimado |
| Fluido de arrefecimento | MEG 50/50 com aditivo OAT | conforme OEM | — | ≈ 7–8 L no circuito | — | ≈ 8 kg | estimado |
| Mangueiras | borracha reforçada | — | EPDM | DI 20 mm, 6 m | — | ≈ 2 kg | hipótese do I35 |
| Vaso de expansão e tampa | pressurizado, ≈ 100–140 kPa(g) | — | PP | ≈ 1,5 L | 1 | ≈ 0,5 kg | estimado |
| Circuito da bateria | placa fria com chiller | OEM | alumínio | — | 1 | — | a confirmar |
| Ventilação do armário de 48 V | ventilador axial | a definir | — | ≥ 145 m³/h | 1–2 | — | já calculado no repositório |

### 3.2 I12, sistema de lubrificação (p. 11)

**Pontos fortes**
- Escopo correto para um VE: não há cárter nem bomba de óleo inventados.
- Lubrificante e fluido de arrefecimento são tratados como coisas distintas.
- A falta de dados OEM é declarada.

**Problemas**
- **A afirmação sobre convecção na carcaça não está demonstrada** (correção 4; números no [Anexo A.7](#a7-óleo-do-redutor)):
  - **no pico** o aquecimento é transitório: ≈ 2,4 K em 10,6 s;
  - **no pior caso sustentado** (2,2 a 4,3 kW de perda) é preciso um caminho até a água;
  - **em cruzeiro a 90 km/h** (0,6 a 1,2 kW), a convecção é plausível, com ΔT de 30 a 115 K. Falta conferir o limite do óleo.
- Falta a tabela de lubrificantes (correção 8).

### 3.3 I34, temperatura da bateria em carga (p. 26)

**Pontos fortes**
- **Formulação correta:**
  - a potência nos terminais é P = U_oc·I + R·I², com a corrente pela raiz positiva da equação quadrática;
  - o calor reversível I·T·dU/dT tem a convenção de sinal certa para a carga;
  - há limites de 250 A e 450 V e um evento de parada a 45 °C;
  - a carga vai de 20% a 80%, o que evita a fase de tensão constante (CV), não modelada.
- **Verificação:**
  - os resíduos de energia são menores que 2·10⁻⁷ J;
  - o estudo de passo (120, 60 e 30 s) dá erro menor que 2·10⁻⁵ K;
  - há caso adiabático de controle (35,0 °C a 80 kW).
- **Coerência física:**
  - 58,8 kWh a 20 kW dão 2,94 h, e o modelo dá 2,96 h por causa das perdas;
  - a taxa de carga é ≈ 0,21C a 20 kW e ≈ 0,81C a 80 kW;
  - o calor ôhmico médio é de ≈ 0,15 kW e ≈ 2,2 kW.

**Problemas**
- Incerteza subestimada (correção 5).
- Pior caso com parada por temperatura e falta de chiller (correção 11).
- Terminologia “refrigerante” (correção 6).
- **Parâmetros sem fonte, que precisam de uma justificativa mínima:**
  - **R_pack = 0,06 Ω:** cerca de 125 células LFP em série, mais barramentos e contatores; citar a ficha de uma célula representativa;
  - **UA_bc = 250 W/K:** placa fria de ≈ 4–6 m² com h efetivo de ≈ 50–100 W/m²·K;
  - **OCV de 360–440 V:** não tem o patamar plano do LFP, embora o efeito no calor seja pequeno;
  - **650 kg e 900 J/(kg·K):** manter a faixa.

**Melhorias**
- Curvas de Q_ôhmico, Q_reversível e Q_arrefecimento no tempo, com a linha de 45 °C.
- Caso com chiller.
- Gradiente interno estimado por condução 1D.
- Se a carga de 20 kW for em CA, as perdas do OBC vão para o circuito de motor e inversor, não para a bateria.

### 3.4 I35, bomba, radiador e vazão (p. 26–27)

**Pontos fortes**
- **Curva real de fabricante** digitalizada, com incerteza de ±3 kPa.
- **Ponto de operação bem calculado:** interseção por `brentq` com teste de unicidade e sem extrapolação.
- **Perdas de carga:** Darcy–Weisbach com transição laminar–turbulenta suavizada e Haaland no turbulento.
- **Radiador 2D verificado:** comparado contra o ε–NTU exato (erro de 5·10⁻⁶, ordem 2).
- **Números conferidos:**
  - Q·Δp = 38,0 W;
  - ε ≈ 0,543;
  - ΔT do líquido de 11,7 K;
  - saída do ar a 47,7 °C;
  - Re ≈ 2,4·10⁴ na mangueira.

**Problemas, por gravidade**
1. A figura do radiador é de outro caso (correção 1).
2. A potência máxima de utilização foi tratada como o pico em regime permanente (correção 9; [Anexo A.6](#a6-transiente-no-pico)).
3. η = 0,90 incoerente com o I04 e o I30 (correção 3; [Anexo A.2](#a2-rendimento-e-calor-pelo-modelo-de-perdas-do-i04)).
4. **UA = 1000 W/K é uma entrada, não o resultado de um dimensionamento.** O enunciado pede para *calcular* o radiador. O caminho é critério → UA necessário ([Anexo A.3](#a3-ua-necessário)) → geometria por correlações ([Anexo A.9](#a9-ordem-de-grandeza-da-geometria-do-radiador)). Nos tubos planos, o lado do líquido é laminar (Re ≈ 300) e responde por cerca de 27% da resistência térmica.
5. **Ar:** 1 kg/s, sem ventilador especificado. Na altitude de São Carlos isso equivale a ≈ 0,94 m³/s e ≈ 3,5 m/s na face. Faltam o modelo, a curva, a potência elétrica (≈ 0,1–0,4 kW, fora do balanço de auxiliares) e o ar de impacto.
6. As quedas de pressão dos componentes são hipóteses e dominam o Δp (correção 10; [Anexo A.4](#a4-sensibilidade-do-ponto-de-operação-da-bomba)).
7. **Falta o requisito da bomba antes da seleção.** A sequência seria:
   1. ΔT admissível do líquido, que dá a vazão (para ΔT ≤ 10 K a 22,8 kW, ṁ ≥ 0,65 kg/s ≈ 37 L/min);
   2. Δp do sistema nessa vazão;
   3. seleção do modelo de catálogo;
   4. interseção.

   A bomba opera no patamar de corrente limitada de 8 A, e o controle por PWM não foi modelado.
8. Faltam NPSH, vaso de expansão, termostato e volume (correção 10; [Anexo A.5](#a5-npsh-disponível)).
9. Não está declarada a fronteira em relação às perdas do redutor (ligação com o I12).
10. Propriedades do MEG 50% sem fonte (c_p = 3500 J/(kg·K), μ = 1,5 mPa·s, ρ = 1050 kg/m³). Fonte sugerida: ASHRAE Handbook – Fundamentals.
11. Os mapas 2D atendem ao pedido de “perfil de temperatura”. Curvas 1D (temperatura média ao longo do escoamento) e um diagrama T–Q deixariam a leitura mais clara.

---

## Anexo A: verificações independentes

Feitas com o código do repositório quando aplicável. As estimativas de ordem de grandeza estão indicadas como tal.
A reprodução dos resultados publicados (A.1) está na seção [Reprodução](#reprodução).

### A.2 Rendimento e calor pelo modelo de perdas do I04

O modelo é η_m = Tω / (Tω + k_c·T² + k_i·ω^1,5 + k_m·ω + P₀), calibrado com η = 0,95 em 410 N·m e 500 rad/s ([`relatorio/gerar_figuras.py`](../relatorio/gerar_figuras.py), função `motor`).

| Ponto | T [N·m] | ω [rad/s] | P_mec [kW] | η_m | Perda com η_inv 0,97 / 0,98 [kW] |
|---|---|---|---|---|---|
| Pico no canto | 410 | 500 | 205 | 0,950 | 17,5 / 15,2 |
| 205 kW a 90 km/h | 296 | 692 | 205 | 0,954 | 16,5 / 14,2 |
| Pior caso do I21 (140 kW nas rodas) | 209 | 692 | 144,3 | 0,947 | 12,8 / 11,2 |
| Cruzeiro a 90 km/h no plano | 56 | 692 | 38,8 | 0,855 | 8,0 / 7,5 |

### A.3 UA necessário

Fluxo cruzado com fluidos não misturados; ṁ_líq = 0,557 kg/s; ar a 25 °C.

| ṁ_ar [kg/s] | Q [kW] | UA para T_ent ≤ 65 °C | UA para T_ent ≤ 70 °C |
|---|---|---|---|
| 1,0 | 10,9 | 347 W/K | 299 W/K |
| 1,0 | 17,6 | 684 W/K | 570 W/K |
| 1,0 | 22,9 | 1096 W/K | 875 W/K |
| 1,5 | 22,9 | 894 W/K | 745 W/K |
| 2,5 | 22,9 | 788 W/K | 671 W/K |

### A.4 Sensibilidade do ponto de operação da bomba

Feita com `motorhome.hidraulica.ponto_operacao`.

| Δp dos componentes | μ = 1,5 mPa·s (≈ 60 °C) | μ = 3,5 mPa·s (≈ 25 °C) | μ = 9,0 mPa·s (≈ 0 °C) |
|---|---|---|---|
| ×0,5 | 36,3 L/min | 35,8 L/min | 34,9 L/min |
| ×1 (nominal) | 31,9 L/min | 31,4 L/min | 30,9 L/min |
| ×2 | 26,4 L/min | 26,1 L/min | 26,1 L/min |
| ×3 | 23,1 L/min | 22,9 L/min | 23,0 L/min |

Decomposição no ponto nominal: tubos 11,2 kPa, singularidades 12,0 kPa e componentes 48,5 kPa (68%).

### A.5 NPSH disponível

A pressão atmosférica a 859 m é ≈ 91,5 kPa. Por Raoult, a pressão de vapor do MEG 50% a 90 °C é ≈ 55 kPa. Considerando 10 kPa de perda na sucção:

- **sem pressurização:** NPSHa ≈ 2,6 m;
- **com tampa de 100 kPa(g):** NPSHa ≈ 12,3 m.

### A.6 Transiente no pico

Estimativa de ordem de grandeza:

- volume de ≈ 7,4 L, o que dá C_líq ≈ 27 kJ/K;
- motor com ≈ 80 kg, o que dá ≈ 38 kJ/K;
- energia de 22,8 kW durante 10,6 s.

Resultado: **ΔT ≈ 3,7 K**, considerando o sistema adiabático.

### A.7 Óleo do redutor

| Condição | η_red | Q [kW] | ΔT em regime (hA = 10 W/K) | ΔT em regime (hA = 20 W/K) |
|---|---|---|---|---|
| Pico de 205 kW | 0,97 | 6,15 | 615 K | 308 K |
| Pior caso do I21 | 0,97 / 0,985 | 4,33 / 2,16 | 433 / 216 K | 216 / 108 K |
| Cruzeiro a 90 km/h | 0,97 / 0,985 | 1,16 / 0,58 | 116 / 58 K | 58 / 29 K |

Com massa térmica de óleo e carcaça de ≈ 27 kJ/K, o pico de 10,6 s com 3% de perda aquece ≈ 2,4 K.

### A.8 I34: cenários extremos

Calculados com `motorhome.bateria_carga.resolver` e a configuração [`config/bateria_termica_proposta.yaml`](../config/bateria_termica_proposta.yaml).

| Caso | P | Parada | t [h] | T final [°C] |
|---|---|---|---|---|
| Nominal | 80 kW | SOC de 80% | 0,76 | 32,0 |
| Pior combinação (R = 0,12; dU/dT = +0,02; 500 kg; UA 125/250) | 80 kW | **45 °C** | 0,66 | 45,0 |
| Início a 35 °C, nominal | 80 kW | SOC de 80% | 0,75 | 35,9 |
| Início a 35 °C com a pior combinação | 80 kW | **45 °C** | 0,37 | 45,0 |
| Pior combinação | 20 kW | SOC de 80% | 2,98 | 30,9 |
| Carga de 10% a 90%, nominal | 80 kW | SOC de 90% | 1,01 | 33,4 |

A constante de tempo entre bateria e ambiente é τ ≈ C_b·(1/UA_bc + 1/UA_ca) ≈ 3510 s (≈ 0,97 h).

### A.9 Ordem de grandeza da geometria do radiador

Premissas: tubo plano com aleta veneziana, β ≈ 1100 m²/m³ e σ ≈ 0,75.

- **Núcleo:** 600 × 450 × 65 mm, com 0,27 m² de face. Com 1 kg/s de ar, a velocidade de face é de 3,5 m/s.
- **Lado do ar:** j ≈ 0,010, h_ar ≈ 64 W/m²·K e η_o·h·A ≈ 1,06 kW/K.
- **Lado do líquido:** 40 tubos de 1,8 × 61 mm, escoamento laminar (Re ≈ 300) com h ≈ 950 W/m²·K, o que dá h·A ≈ 2,9 kW/K.
- **Resultado:** UA ≈ 0,77 kW/K. Para 1,0–1,1 kW/K seria preciso ≈ 650 × 500 × 65 mm.
- **Lado do ar:** Δp ≈ 45 Pa no núcleo.

### A.10 I28: estimativa sem limitador

Feita com o mesmo modelo do relatório.

- **Validação do modelo:** com m_ef de 1,00 a 1,05·m, o tempo de 0 a 90 km/h é de 10,4 a 10,9 s; o relatório dá 10,6 s.
- **0 a 100 km/h:** ≈ 12,3 a 12,9 s.
- **Vmax teórica:** ≈ 171 km/h limitada por potência, ou ≈ 163 km/h por rotação, supondo 12 000 rpm com i = 10.
