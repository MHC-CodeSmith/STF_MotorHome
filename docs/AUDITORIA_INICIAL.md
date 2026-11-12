# Auditoria operacional inicial — 22/10/2026

Checkout `/home/mhc/motorhome_solar_codex`, branch `coord/auditoria-inicial`, base indicada `main` em `1ac5888`. Trabalho local de um único worker, sem outro worktree, commits, push, publicação ou envio a terceiros. `git remote -v` não produziu linhas. Nenhuma decisão de componente/veículo foi tomada.

## Diagnóstico

**35 itens presentes e não iniciados; 35 teorias são templates e 35 revisões humanas estão pendentes.** A existência das pastas não representa fundamentação, código, resultado físico ou aprovação. Distribuição preservada: P1=8, P2=5, P3=3, P4=6, P5=5, P6=4, P7=4. Único código de engenharia existente: `src/motorhome/dinamica.py`, funções longitudinais simplificadas, cinco testes sintéticos em `tests/test_dinamica.py`; não fornece CFD, mapa real de motor ou solução térmica.

CSV e Mermaid corrigidos têm **121 arestas de item**, todas com referência existente e sem ciclo. O `BASE→I01` do Mermaid é contexto e não conta como aresta entre itens. A expressão “DAG de dados finais” em `docs/dependencias.md` descreve intenção de integração: aciclicidade está verificada, mas necessidade e completude física de todas as arestas ainda exigem revisão humana. A possível sobre-restrição I28→I33 foi mantida e sinalizada. Não é caminho crítico calculado: faltam durações e disponibilidade.

`config/parametros_globais.yaml` permaneceu **byte a byte idêntico**, SHA256 `7b8f5cd7891eb437cb89c41fd2ba440b0567ca1063998042d4828086aad523e2`. Há **24 campos null**, e `project.vehicle_baseline_approved` continua false. O script não preenche lacunas nem aprova engenharia.

## Fontes locais lidas e divergências

Foram lidos o AGENTS, HUB/contextos, enunciado original (2 páginas), organização P1–P7 (12), levantamento de projetos (17), apostila (76), dependências/marcos/catálogo/configuração, os 35 READMEs e demais documentos, incluindo teorias e checklists que são templates. O [inventário documental](../fontes_externas/inventario_documental.csv) registra 322 documentos locais/arquivos documentais, com hash e tamanho no momento de leitura; quatro linhas são os PDFs integrais. Ele é um snapshot da leitura, não um índice que se atualiza automaticamente quando o diff evolui. Os novos entregáveis desta auditoria são listados ao final.

Extrações integrais estão **fora do repositório**, em `/home/mhc/motorhome_referencias/textos/`, com o nome de cada PDF e extensão `.txt`, produzidas por `pdftotext -layout`. Nenhum PDF da apostila foi copiado para o Git. O [mapa teórico](mapa_teorico.md) identifica seções, páginas físicas, equações, uso por item, exemplos/códigos lidos e limitações de inspeção visual. A apostila v0.4 é de **Prof. Cristiano Bigonha Tibiriçá**, 2025. A afirmação antiga em `docs/material_da_materia/README.md` e `docs/STATUS_INICIAL.md` de que material de aula não foi recebido está **superada** pela apostila local; esses arquivos permanecem como histórico do scaffold, não estado atual.

| Evidência | Constatação / ação dentro do escopo |
|---|---|
| Enunciado p. 1; organização p. 1–2 | Enunciado solicita dez alunos; divisão de sete permanece proposta pendente de autorização. Não redistribuir P1–P7 |
| Enunciado p. 2, I27; organização p. 2 | Final **30%**, não uma desigualdade livre. README I27 corrigido para alvo 30% com tolerância numérica a declarar; SOC inicial continua pendente. O levantamento p. 14 e o template `teoria.md` também repetem ≥30%; não são fonte autoritativa. YAML mantém chave histórica `minimum_soc_fraction_daily` sem alteração |
| Enunciado p. 1, I07/I10/I18; CSV original I24 | Fiação e arrefecimento compõem massa montada. I18 agora inclui I07/I10 no CSV, README e Mermaid; evitar dupla contagem de massas já embutidas em outros conjuntos |
| Enunciado p. 2, I26 | Saída em **km/kWh**: README descrevia “consumo energético por km”, razão inversa. Texto corrigido com proveniência; teoria continua template |
| Enunciado p. 2, I33; scaffold I33→entradas | Frenagem já fixa 30→10 m/s em 5 s, início 25°C. I28 (0–100) pode ser sobre-restrição para iniciar o método; P1/P4 decidem se remover a aresta final, nenhuma mudança silenciosa |
| Enunciado p. 1; comentário YAML | Ano de simulação 2026 é convenção computacional explícita, não ano prescrito pelo professor para a insolação (somente 21/06). Coordenadas/altitude continuam null; exemplos do levantamento não aprovados |
| Enunciado p. 2, I25/I26/I29 | Preservar solar do dia em I25, bateria em I26 e somente bateria inicial+solar/≤8 h de direção/dia nos 7000 km de I29. Não adotar hipótese solar da rota sem revisão |
| Enunciado pp. 1–2; organização pp. 2/11 | Entrega **02/12/2026 às 06:00 America/Sao_Paulo**; PDF<20 MB, vídeo<50 MB/8–10 min/todos, seminário≤8 min, código anexo, e-mail com cópia a ambos docentes |

Os templates de teoria I18/I26/I27 ainda contêm listas/redações históricas; a presente tarefa autoriza correções nos READMEs/CSV/grafo, não seu desenvolvimento teórico. Essa dívida fica explicitamente registrada, sem lhes atribuir aprovação.

## Estado por item, dependências e bloqueios

Todos os prazos abaixo são marcos internos **propostos** do plano P1–P7, ano 2026, para artefato preliminar; não prova de execução. M4 20/11 é o gate de fechamento técnico de todos, M5 27/11 revisão e M6 30/11 pacote final. Detalhes e critérios de artefato no [plano dos dez trabalhos](PLANO_10_TRABALHOS.md).

| Item | Dono | Estado observado | Entradas diretas de dados finais | Bloqueio concreto | Marco preliminar |
|---|---|---|---|---|---|
| I01 Nome e conceito do veículo | P1 | não iniciado / template | requisitos/conceito | Conceito, nome e veículo-base não aprovados | M1 30/10 |
| I02 Pneus e rodas | P1 | não iniciado / template | I15 | Pneu/roda/pressão e carga não escolhidos | M1 30/10 |
| I03 Sistema de freios | P1 | não iniciado / template | I02, I15 | Disco/pinça/material e distribuição de frenagem ausentes | M1 30/10 |
| I04 Motor elétrico | P4 | não iniciado / template | I15 | Curvas reais torque/potência/eficiência ausentes | M1 30/10 |
| I05 Transmissão | P4 | não iniciado / template | I04, I02 | Relação e eficiência da transmissão pendentes | M1 30/10 |
| I06 Bateria | P2 | não iniciado / template | I04 | Células/pack/BMS/tensão/limites não selecionados | M1 30/10 |
| I07 Fiação elétrica | P2 | não iniciado / template | I04, I06, I09 | Correntes, bitola, material e percurso pendentes | M1 30/10 |
| I08 Painel fotovoltaico | P5 | não iniciado / template | I17 | Teto útil, painel e montagem indefinidos | M1 30/10 |
| I09 Controladores de carga e inversores | P2 | não iniciado / template | I06, I08 | Compatibilidade elétrica e eficiências não documentadas | M1 30/10 |
| I10 Resfriamento de componentes elétricos | P7 | não iniciado / template | I04, I06, I09 | Perdas e arquitetura de resfriamento pendentes | M1 30/10 |
| I11 HVAC e ventilação interna | P6 | não iniciado / template | I13, I16, I17 | Tecnologia HVAC, carga e eficiência não definidas | M1 30/10 |
| I12 Sistema de lubrificação | P7 | não iniciado / template | I04, I05 | Lubrificação aplicável e dados de fluido pendentes | M1 30/10 |
| I13 Materiais e equipamentos internos | P6 | não iniciado / template | I15, I16 | Layout, materiais e perfis de equipamentos pendentes | M1 30/10 |
| I14 Suspensão e direção | P1 | não iniciado / template | I15, I02 | Cargas admissíveis e especificações ausentes | M1 30/10 |
| I15 Chassi | P1 | não iniciado / template | I01 | Base mecânica e dimensões não aprovadas | M1 30/10 |
| I16 Carenagem, portas, vidros | P3 | não iniciado / template | I15 | Envelope, materiais e áreas de vidros pendentes | M1 30/10 |
| I17 CAD 3D e vistas cotadas | P3 | não iniciado / template | I15, I16, I13 | Abertura nativa/cotas/unidades e geometria própria pendentes | M1 30/10 |
| I18 Massa total com passageiros | P1 | não iniciado / template | I02, I03, I04, I05, I06, I07, I08, I09, I10, I11, I12, I13, I14, I15, I16, I17 | Massas de todos, passageiros/água/bagagem ausentes; I07/I10 incluídos | M1 30/10 |
| I19 Coeficiente de arrasto e CFD | P3 | não iniciado / template | I17 | Sem caso CFD, malha, convergência ou Cd do motorhome | M2 06/11 |
| I20 Resistência de rolamento | P4 | não iniciado / template | I02, I18 | Cr exige pneu/superfície/pressão/carga documentados | M2 06/11 |
| I21 Forças resistivas versus velocidade | P4 | não iniciado / template | I18, I19, I20 | Massa, Cd/área e Cr não aprovados | M2 06/11 |
| I22 Potência resistiva e tração | P4 | não iniciado / template | I04, I05, I21 | Curvas de motor/transmissão e forças pendentes | M2 06/11 |
| I23 Capacidade das baterias (kWh) | P2 | não iniciado / template | I06, I08, I13, I22 | Capacidade útil/nominal e demanda não dimensionadas | M1 30/10 |
| I24 Custo total dos materiais | P1 | não iniciado / template | I02, I03, I04, I05, I06, I07, I08, I09, I10, I11, I12, I13, I14, I15, I16, I18 | BOM, preços/data e impostos sem fontes | M1 30/10 |
| I25 Autonomia usando somente solar | P5 | não iniciado / template | I08, I09, I22, I23, I26 | Energia solar do dia e demanda pendentes | M3 13/11 |
| I26 Consumo (km/kWh) | P5 | não iniciado / template | I21, I22, I23, I13 | km/kWh da bateria, eficiência e auxiliares pendentes | M3 13/11 |
| I27 Autonomia diária com SOC final 30% | P5 | não iniciado / template | I23, I25, I26 | SOC inicial e tolerância numérica pendentes; alvo final 30% | M3 13/11 |
| I28 Velocidade máxima e 0–100 km/h | P4 | não iniciado / template | I04, I05, I18, I19, I20, I22 | Curvas e limites ausentes; registrar se 100 km/h inalcançável | M2 06/11 |
| I29 Otimização viagem 7000 km | P5 | não iniciado / template | I25, I26, I27, I23 | Hipótese solar da rota e SOC inicial pendentes; sem recarga externa | M3 13/11 |
| I30 Temperatura de cabos multidimensional | P2 | não iniciado / template | I04, I07 | Cabos/perdas/malha/campo multidimensional não executados | M3 13/11 |
| I31 Cabine fechada ao meio-dia | P6 | não iniciado / template | I11, I13, I16, I17, I08 | Regime/estado inicial e propriedades/áreas pendentes | M3 13/11 |
| I32 Potência térmica de A/C | P6 | não iniciado / template | I11, I13, I16, I17, I31 | Ocupação, carga solar e materiais pendentes; regime permanente | M3 13/11 |
| I33 Freio: campo térmico multidimensional | P1 | não iniciado / template | I03, I18, I28 | Disco/massa/fluxo e solver pendentes; I28 em revisão | M3 13/11 |
| I34 Temperatura da bateria em carga | P7 | não iniciado / template | I06, I07, I09, I10, I23 | Pack/protocolo de carga/perdas/limites ausentes | M3 13/11 |
| I35 Bomba, radiador e vazão | P7 | não iniciado / template | I04, I05, I10, I12 | Perdas do motor, fluido, radiador e curvas de bomba ausentes | M3 13/11 |

## Parâmetros e interfaces bloqueadas

Lista exata de caminhos null detectados, sem preencher:

- `project.vehicle_name`
- `project.vehicle_reference`
- `scenario.latitude_deg`
- `scenario.longitude_deg`
- `scenario.altitude_m`
- `battery.nominal_capacity_kWh`
- `battery.usable_capacity_kWh`
- `battery.nominal_voltage_V`
- `battery.initial_soc_fraction`
- `vehicle.curb_mass_kg`
- `vehicle.passengers_mass_kg`
- `vehicle.water_and_cargo_mass_kg`
- `vehicle.total_mass_kg`
- `vehicle.frontal_area_m2`
- `vehicle.drag_coefficient`
- `vehicle.rolling_resistance_coefficient`
- `vehicle.tire_effective_radius_m`
- `motor.maximum_power_kW`
- `motor.efficiency_map_path`
- `solar.panel_area_m2`
- `solar.panel_module_efficiency`
- `solar.tilt_deg`
- `solar.azimuth_deg`
- `solar.inverter_efficiency`

As interfaces incluem dono e prazo no plano: todos→P1 massas/custos (30/10, 13/11, 20/11); P1/P6→P3 chassi/layout (23–30/10); P3→P4/P5/P6 áreas/volume/Cd (30/10 e 06/11); P4→P2/P5/P7 curvas/perdas (30/10/06/11); P2→P5/P7 tensão/capacidade/limites (30/10/06/11); P6/P7→P5 auxiliares/horários (06/11/13/11). Não fabricar esses arquivos com números plausíveis. Requisito de interface não significa que o artefato existe.

## Aquisição e licenças

Inspecionadas as **18 entradas originais**, mais **3 candidatos derivados** dos links do levantamento (NASA POWER p. 13, TU Delft motor p. 5, GrabCAD p. 7). Consultas de commits, árvores e licenças GitHub foram feitas pelo conector conectado; bytes de arquivos vieram de HTTPS com timeout e limite. Não se instalou/reconfigurou Bright Data nem se executou script externo. O checker usa timeout de socket de 25 s e limite de 40 MiB/arquivo, ZIP expandido até 250 MiB, `pdfinfo` até 20 s; não baixa repositórios inteiros.

O [catálogo atualizado](../fontes_externas/catalogo.csv) separa status de acesso, página e arquivo, HTTP/URL final, data UTC, licença e evidência, commit, extensão, bytes medidos, SHA256, cache e nível de validação. Campos desconhecidos ficam vazios (equivalentes a null no CSV). O [manifesto](../fontes_externas/verificacoes.json) contém resultados por tentativa e lista de membros ZIP/PDF; [registro de importações](../fontes_externas/registro_importacoes.csv) tem **25 arquivos distintos armazenados no cache**, incluindo licenças e cinco membros Delica extraídos. “Importação” aqui é **aquisição para estudo no cache externo**: nenhum código/CAD foi incorporado ao produto/Git. Páginas HTML de inspeção também ficaram no cache e não contam nesses 25 arquivos de material/licenças.

Status de acesso por **linha do catálogo** (Delica tem página e ZIP como duas linhas que referem o mesmo arquivo):

| Status | Linhas |
|---|---:|
| arquivo_baixado_validado | 12 |
| pagina_verificada | 2 |
| indexado_download_nao_validado | 2 |
| inacessivel | 5 |
| nao_verificado | 0 |

Licenças em coluna separada: **7 verificadas**, **5 sem_licenca**, **9 nao_verificado**. `sem_licenca` nunca apaga um download bem-sucedido. Histórico anterior fica em `verificacao_historica`, `licenca_historica` e observações rotuladas; alegações antigas não equivalem a licença verificada.

| Fonte prioritária | Evidência atual e limite |
|---|---|
| Delica página + ZIP | Página 200 e ZIP 200; **6.730.210 bytes** medidos, CRC OK; `_Delica_Assembly.FCStd`, `.iges`, `.step`, `.stl` e PDF de papercraft. FCStd é ZIP com Document.xml e shapes, IGES tem seções S/G/D/P/T, STEP tem delimitadores, STL tem estrutura, PDF passou `pdfinfo` (2 páginas). Sem abertura FreeCAD/solver, unidade/cotas ou geometria watertight verificadas; sem licença explícita localizada |
| MELVING22 | IGES **11.274.098 bytes** no commit fixado; seções IGES verificadas. Solar car, não motorhome; sem licença localizada, sem montagem SolidWorks/rebuild nem aptidão CFD demonstrados |
| Ducato L3H2 e E-Ducato | HTTP 200 hoje, **mesmo HTML genérico 3D Warehouse** (10.922 bytes de página), sem ficha específica nem URL SKP exposto. Histórico 403 é histórico. Download/conteúdo do modelo e licença não confirmados, não atribuir tamanho ao CAD |
| pvlib / EV_sim / FASTSim | Arquivos concretos em commits fixados: clearsky.py, model.py e hvac_utils.rs. Python analisado por AST, Rust apenas texto UTF-8; licenças BSD-3/MIT/Apache-2 verificadas; nenhuma execução/integração de biblioteca |
| Simscape | BatteryLumpedThermalParams.m concreto, licença exige uso com produtos/serviços MathWorks. Também armazenado pequeno utilitário HTML; validador inicial confundiu literal HTML no código com página, corrigido e revalidado. MATLAB/toolboxes/licenças dos estudantes não verificados |
| BatteryPack / PyBaMM | thermal.py contém LumpedThermal.step (modelo concentrado); exemplo DFN_ambient_temperature.py adquirido, ambos AST sem execução. MIT/BSD-3 verificadas. Não geram resultados do pack sem dados próprios |
| Solar optimizer / freios | Código concreto adquirido para estudo, sem licença explícita. main.py de freios contém início 600, duração 10 s e fluxo fixo; não é o cenário 25°C/5 s do enunciado. Estabilidade, contornos, dados e convergência exigem revisão própria |
| AutoCFD | README concreto lido, licença MIT do site/template conferida; isso não licencia automaticamente datasets/malhas de terceiros. Nenhum caso CFD nativo/malha do motorhome validado |
| Saoulis | URL sandbox 403; DOI leva ao repositório atual com desafio Anubis (HTTP 200, conteúdo inacessível). Purl timeout. Agregador abre, mas `rights_null`; CC BY-SA do rodapé é do portal, não da tese. **PDF não obtido**: sem link concreto recuperado; CC BY 4.0 anterior permanece não verificada |
| Batko / Ribeiro | Batko timeout; Ribeiro HTTP 410 na URL catalogada atual. Sem PDF adquirido; formatos/tamanhos históricos não usados como medidas atuais |
| NASA / TU Delft / GrabCAD adicionais | Documentação NASA 200, sem arquivo de dados baixado; TU Delft timeout; GrabCAD 403. Sem inventar URL de download, formato, licença ou tamanho |

Arquivos principais concretos (tamanhos e hashes completos no CSV/manifesto):

| Cache em `/home/mhc/motorhome_referencias/downloads/` | Bytes | Nível |
|---|---:|---|
| `Delica-Conversion-CAD.zip` | 6730210 | container_zip_crc |
| `05_Chassis .IGS` | 11274098 | assinatura_iges |
| `07_clearsky.py` | 38327 | sintaxe_python_sem_execucao |
| `08_BatteryLumpedThermalParams.m` | 1361 | texto_utf8_nao_html_sem_execucao |
| `09_model.py` | 12185 | sintaxe_python_sem_execucao |
| `10_hvac_utils.rs` | 544 | texto_utf8_nao_html_sem_execucao |
| `11_velocity optimization model for solar car` | 5180 | texto_utf8_nao_html_sem_execucao |
| `12_thermal.py` | 486 | sintaxe_python_sem_execucao |
| `13_DFN_ambient_temperature.py` | 1069 | sintaxe_python_sem_execucao |
| `14_main.py` | 4756 | sintaxe_python_sem_execucao |
| `15_README.md` | 26533 | texto_utf8_nao_html_sem_execucao |

**Validação significa somente o nível declarado:** CRC/listagem de ZIP, assinatura/estrutura CAD, leitura por pdfinfo ou texto/AST. Não significa abertura nativa, licença de reuso, capacidade de simular, malha estanque, convergência, precisão física ou aprovação humana. Repositórios e terceiros continuam candidatos; não houve redistribuição de CAD/código sem licença.

## Software, execução e testes

[Software disponível](software_disponivel.md) documenta caminhos, versões e imports separados da `.venv`. FreeCAD, Gmsh, OpenFOAM/simpleFoam, ParaView, MATLAB, Octave e EES não foram encontrados no PATH deste host. Esse diagnóstico não diz nada sobre licenças/instalações dos estudantes.

Preparação executada em primeiro plano:

```bash
uv venv .venv
uv pip install --python .venv/bin/python pytest ruff PyYAML build
```

Resultado observado: CPython 3.12.3; pytest 9.1.1, ruff 0.17.1, PyYAML 6.0.3, build 1.6.1. Reinstalação suportada: `uv pip install --python .venv/bin/python -e '.[dev]'`.

Verificação direcionada (não foi executada a suíte inteira do repositório):

```bash
.venv/bin/python -m pytest tests/test_dinamica.py tests/test_auditoria.py tests/test_fontes.py -x -q
.venv/bin/python scripts/verificar_estrutura.py
.venv/bin/python scripts/auditar_projeto.py
.venv/bin/ruff check scripts/auditar_projeto.py scripts/verificar_fontes.py tests/test_auditoria.py tests/test_fontes.py
```

Saída observada na rodada de preparação final: `34 passed`; estrutura `Verificação de 35 itens, 7 equipes.` e `Estrutura OK. ATENÇÃO: isto não valida física nem resultados.`; ruff `All checks passed!`. Os tempos variam por rodada. O stdout da conferência final fica fora do Git em `/home/mhc/motorhome_referencias/verificacao_final.log`.

Saída da auditoria:

```text
Auditoria: 35 itens; responsáveis {'P1': 8, 'P2': 5, 'P3': 3, 'P4': 6, 'P5': 5, 'P6': 4, 'P7': 4}
Erros estruturais: 0; parâmetros null: 24
24 parâmetros null: engenharia bloqueada
Veículo-base sem aprovação
I28 -> I33: possível sobre-restrição; revisar com P1/P4
Estrutura auditada; aprovação de engenharia: NÃO.
```

Semântica de saída: padrão **0** se estrutura coerente, mesmo com avisos/null; **1** para defeitos estruturais; `--exigir-parametros` retorna **2** se há null sem defeito estrutural. Não interpretar exit 0 como engenharia aprovada. `--json` imprime inventário local, estados individuais, contagens e caminhos null; o script não escreve no YAML.

Cobertura dos testes: projeto sintético completo positivo, grupos exatos, ID inválido/fora da faixa/duplicado, dependência inexistente/inválida/duplicada, ciclo, divergência README/CSV de dono, divergência Mermaid, README ausente, aprovação indevida com template e preservação do YAML. Checker usa fixtures originais em memória e respostas simuladas, sem rede: página/arquivo separados, HTML como ZIP, CRC corrompido, 403/timeout/limite, AST sem executar, assinatura CAD sem alegação nativa, HTTP 200 com desafio, pdfinfo simulado e catálogo com arquivo fixado.

Build executado:

```bash
.venv/bin/python -m build --outdir /home/mhc/motorhome_referencias/build
```

Saída: `Successfully built motorhome_solar_estudo-0.0.1.tar.gz and motorhome_solar_estudo-0.0.1-py3-none-any.whl`. É build do pacote Python existente, não dos relatórios nem de CAD/CFD; artefatos fora do Git. Não se adicionou typechecker ou mudou código de dinâmica nesta tarefa.

Reverificação de fonte específica ou do catálogo (rede opcional, fora dos testes):

```bash
.venv/bin/python scripts/verificar_fontes.py 'URL_DA_PAGINA'
.venv/bin/python scripts/verificar_fontes.py 'URL_FIXADA_DO_ARQUIVO' --arquivo exemplo.py
.venv/bin/python scripts/verificar_fontes.py --catalogo fontes_externas/catalogo.csv > /home/mhc/motorhome_referencias/reverificacao.json
```

Os dois primeiros exemplos usam placeholders, não fontes inventadas. O modo catálogo repete somente URLs registradas e não revalida licença automaticamente; `licenca_status_historico` não é nova autorização. Saída 1 sinaliza fonte inacessível ou arquivo não validado; preserva HTTP/erro e não mascara indisponibilidade. Descobertas de páginas genéricas ainda exigem leitura humana do conteúdo; a heurística anti-bot cobre somente desafios reconhecidos.

## Entregáveis e próximos gates

Novos: `docs/AUDITORIA_INICIAL.md`, `docs/PLANO_10_TRABALHOS.md`, `docs/mapa_teorico.md`, `docs/software_disponivel.md`, dois scripts, dois arquivos de teste e manifestos `fontes_externas/verificacoes.json`/`inventario_documental.csv`. Atualizados: catálogo/registro de aquisições, CSV I18, Mermaid I18, READMEs I18/I26/I27/I33, extra dev, gitignore e navegação do README. Nenhum arquivo de engenharia global foi preenchido.

Os [dez trabalhos](PLANO_10_TRABALHOS.md) especificam donos P1–P7, interfaces, entregas verificáveis e marcos. Decisões humanas pendentes: grupo, nomes/disponibilidade, veículo-base/componentes, interpretações I27/I31/I32/I29, tolerância SOC, ferramentas/licenças, necessidade I28→I33, aprovação CAD/CFD/campos térmicos, congelamento e distribuição futura. Nenhuma pergunta ao humano ou gate de aprovação foi aberto nesta execução; decisões ficam para a revisão da equipe.

## Arquivos concomitantes preservados

Durante a execução apareceram `docs/revisao_apostila.md` e `docs/referencias_complementares.md`, não criados por este worker e fora da lista de arquivos editáveis desta tarefa. Foram lidos e preservados sem alterações. Suas alegações de inspeção visual e novas referências não são evidência produzida por esta auditoria nem foram incorporadas aos números do catálogo. O mapa desta tarefa continua delimitando sua leitura textual e pendências visuais.


## Atualização de classificação — 12/11/2026

Esta auditoria é um registro histórico do estado inicial. A antiga aresta I28→I33 foi reavaliada: I33 recebe do enunciado a condição de frenagem (30→10 m/s em 5 s) e usa dados I03/I18; I28 fornece apenas contexto operacional do limitador nominal de 90 km/h. Portanto, I28→I33 foi removida das dependências de dados e mantida como interface `contextual_nao_bloqueante` em `metadata/interfaces_contextuais.csv`. A aresta Mermaid e o alarme da auditoria estrutural foram ajustados; não houve alteração das 61 decisões nem dos resultados físicos. A condição de 108 km/h segue sendo ensaio acadêmico de componente, sem afirmação de desempenho do veículo.
