# Continuação vigente: leitura orgânica e comparações

Esta revisão prevalece sobre a edição de 39 páginas descrita abaixo. O memorial tem
41 páginas e 38 figuras/diagramas, sem código nem listas itemizadas. Especificações
em 12 grupos; simulações começam por freios, cabos, cabine, A/C, bateria e radiador.
As figuras acompanham o modelo e a interpretação. Ler `REVISAO_LEITURA_E_COMPARACOES.md`:
20 casos de consumo com um parâmetro por vez, 140 novas janelas MILP, seis missões de
acumular energia e figuras de R×entropia, UA/rendimento e perda de pressão.
O cenário nominal/configuração/massa não mudou. `simular_missao` ganhou período de
dias de condução com padrão 1, preservando o comportamento anterior; 299 testes passam.
A rotina `relatorio/compilar.sh` inclui a reprodução das novas comparações.

---

# Revisão editorial e de todos os PRs — estado vigente em 25/11/2026

O usuário pediu relatório curto com redação próxima à do Cuca, inclusive frases; manter
simulações, gráficos e imagens e retirar todo código/anexo de listagens do PDF.
A versão de 85 páginas em d7528ba é anterior à nova instrução. As hipóteses e 35 itens são
preservados no corpo enxuto, com tabelas para as especificações e detalhes numéricos.

Auditoria geral: `docs/AUDITORIA_ENUNCIADO_E_PRS.md`, PRs #1/#2/#4/#5/#6/#8/#9, issues #3/#7,
mais parecer P6. Conferir enunciado, não presumir que MERGED significa resolvido.
A matriz Fael continua em `docs/AUDITORIA_PR9_REESCRITA.md`. O parecer P7 recomendava
itens 7–11 que faltavam no PDF; foram incorporados, com rechecagens e ressalvas reais.

Complementos em `relatorio/gerar_complementos_termicos.py` e `relatorio/dados_termicos/`:
campo 2D do cabo no pico; Δp/NPSH/UA; extremos da bateria; ventilação 48 V. A proposta de 3–5 kW
para chiller não cobre pico interno de 6,35 kW; meta de 65 °C exige UA de 1093 W/K só para motor/inversor,
ou 1952 W/K com 6,15 kW adicionais do redutor. Isso é requisito condicional, não instalação.
Script antigo do teto corrigido de 35 A para 60 A; corrente quente portátil permanece desconhecida.
Fonte vigente da sensibilidade I34 identificada: 486 casos; 20 linhas antigas são históricas.

Versão final: 39 páginas, 6,03 MB e 33 figuras/diagramas; guia `REVISAO_INTEGRANTES.md`
com páginas atuais e sem referência ao anexo de código.

Nomes da capa seguem a lista do usuário. Código no PDF e vídeo foram excluídos por sua
instrução, embora o enunciado original os peça; não alegar cumprimento literal dessas
parcelas. Seminário, envio por e-mail e autorização para oito em vez de dez alunos não
foram realizados. Publicação nas duas refs e autor MHC sem trailer seguem autorizados.

---

# Continuação vigente — revisão integral de 25/11/2026

Esta seção prevalece sobre os registros históricos abaixo. O relatório segue a organização do
Cuca, preservando 35 itens: Introdução/Objetivos, Revisão bibliográfica e Projeto técnico com
especificações, custo, simulações, deduções e tabela final. Fontes em `relatorio/`, PDF no mesmo
local. Capa: exatamente os oito nomes em `relatorio/autores.tex`, por instrução do usuário.
Vídeo excluído do escopo. Nenhuma nova aprovação de grafia ou publicação é necessária.

O PR #9 do Fael foi conferido no GitHub (patch de 81 linhas, sem reviews/comentários de linha).
A matriz completa dos 27 pedidos e seus subpedidos está em `docs/AUDITORIA_PR9_REESCRITA.md`.
Renogy RSP400LSC-G1: USD 495,99 na loja oficial, sem estoque em 25/11; comparação com acessórios,
dimensões, tempo de instalação hipotético e retenção calculada. A fichaFiat dá 90/130/130 km/h:
a comparação de RPM é cinemática, sem inventar nmax/curva OEM. Professores conferidos na USP.

Cama: estrado de 30 mm, quadro de 50×50×3 mm, postes de 45×45×4 mm. Peso próprio, ajoelhamento,
flecha L/300 e cargas de 3g/5g incluídos; utilização máxima 0,833. A hipótese preliminar de 25 mm/40 mm
não foi adotada porque omitia casos e massas. Acréscimo líquido de 66,257102 kg, já no inventário:
massa A = 4042,78262976 kg, margem de 207,21737024 kg. Soldas/bases/ancoragem OEM não validadas.
Ver `cama_estrutura/resumo.json` e `HISTORICO_MASSAS.md` no cenário 1560. Resultados antigos
3976 kg/1540 Wp/1350 Wp permanecem históricos. Não os tratar como projeto vigente.

Reprodução completa: `PYTHONPATH=src:scripts .venv/bin/python scripts/reexecutar_revisao_relatorio.py
--executar` (uma linha; execução longa, dois workers). Perfil horário por aparelho tem rotina
hipotética; I25/I29 principais continuam usando carga média. O recibo da revisão distingue a
execução efetiva dos antigos manifestos. `relatorio/compilar.sh` atualiza tabelas/figuras e PDF.
Após modificar código/dados, atualizar índice, testes e manifestos; ver README do relatório.

Publicação autorizada no histórico da tarefa: autor MHC <carvalho.matheush@gmail.com>, sem trailer;
`git push origin integ:main integ:hub/tarefas-motorhome-com-codex`. Revisões dos integrantes são
pareceres acadêmicos, não validação física; instalação e interface CC continuam condicionais.

Resultado final da viagem após o reforço da cama: 20,5 km/h, primeira saída às 18h,
214,755556 dias com reservas 10/20%; alternativa 20/30%: 20,7 km/h e 215,793056 dias.
Comparação a horário/reservas comuns: 40 km/h → 248,767361 dias; 80 km/h → 457,750694 dias.
Primeira reserva do líder em 3,845139 dias/538,645874 km; ritmo posterior 30,635538 km/dia.
Recibo dos 30 comandos principais, cinco suplementos, três preparações recuperadas e três
rechecagens históricas em `entregas/integrado_maxeon1560/revisao_relatorio/execucao.json`.
As preparações sem código de saída no log são identificadas como tal, sem inventar registro.

---

# Handoff — STF MotorHome (16/11/2026, fim da sessão)

## O que é e por quê
Trabalho da disciplina (motorhome elétrico solar "Aurora Solar", Fiat E-Ducato L3H2, 35 itens).
Entrega oficial **02/12/2026 06:00** por e-mail aos dois docentes: PDF < 20 MB, vídeo 8–10 min
< 50 MB com os 7 integrantes, anexo de códigos. Em 16/11 o usuário pediu para terminar tudo
(revogada a regra antiga de "não fazer relatório/slides").

## Estado (commits `22143a6` e `8f4dcd2`, em `main` e `hub/tarefas-motorhome-com-codex`, CI verde)
- `relatorio/relatorio.pdf` (51 p., 5 MB, 29 figuras), `relatorio/slides.pdf` (15 quadros),
  `relatorio/roteiro_video.md` (7 blocos de ~75 s). Fontes `.tex` + `compilar.sh`.
- Lacunas fechadas e números: `docs/FECHAMENTO_35_ITENS.md`. Principais:
  I19 Cd = 0,622 ± 0,006 (malhas 291k/523k/751k: 0,6220/0,6338/0,6215, convergência oscilatória →
  meia amplitude, Stern 2001; GCI/Richardson inválidos); I24 R$ 789 mil (721–882);
  I29 20,7 km/h, partida 17h45, 248,8 d; I30 489 A RMS, 85 °C no 1×120 mm².
- Figuras: `relatorio/gerar_figuras.py` (gráficos) e `relatorio/renderizar_cad.py`
  (10 renderizações CAD/CFD; geometria do cache, Cp/velocidade do VTK da malha fina).

## Aberto (só o grupo/usuário)
1. Nomes dos integrantes na capa (`relatorio.tex`, tabela P1–P7) e recompilar.
2. Conferir se o GitHub `MHC-CodeSmith/STF_MotorHome` está visível aos docentes.
3. Revisão de cada integrante (A01–A16 sem aprovação registrada; B01 interface CC é hipótese).
4. Gravar o vídeo (ffmpeg 720p, ~600 kbit/s → < 50 MB). M6 30/11.

## Onde e como
- Repo no mhc-lenovo: `/home/mhc/motorhome_solar_codex_tarefas` (não mexer em `motorhome_solar_codex`). Commits como `MHC <carvalho.matheush@gmail.com>`, sem trailer.
- Cache externo: `/home/mhc/motorhome_referencias_tarefas/` — exterior `aurora-L3H2-01/`, portáteis `cad-portatil-01/`,
  malhas/campos CFD `cfd-familia-gci-20261116/bg_*/case` (503 MB; VTK em `bg_55x20x10/case/VTK/case_344`).
- PDFs: compilar na torre (TeX Live completo); o lenovo não tem babel-portuguese/siunitx.
- QA (igual ao CI, Python 3.11): `PYTHONPATH=src .venv/bin/python -m pytest -q`; `~/.local/bin/ruff check src scripts tests relatorio`;
  `MOTORHOME_SCENARIO=maxeon1540_independente PYTHONPATH=src .venv/bin/python scripts/verificar_cenario_integrado.py` e
  `scripts/verificar_desenvolvimento.py` (após mudar script/saída rastreados: `--registrar`, depois sem). O verificador
  hasheia tudo em `entregas/aero_equipado1540/`: não deixar arquivos ignorados lá.
- Referencial CAD: `relatorio/montagem_cad.py` monta tudo no referencial do projeto (traseira interna x = −3,35 m, piso z = 0,68 m,
  largura centrada; rotas e teto Maxeon exportados com y a partir da lateral). O deck fica na posição do `pvdeck.stl` do CFD
  (x − 3,482, y − 0,91, z + 0,648 sobre o arquivo do teto). O antigo offset −3,482/0,648 aplicado ao interior o enfiava 13 cm
  nas portas traseiras (corrigido em 16/11). Colisões resolvidas na montagem: banco US5000 sobre a caixa de roda (A) ou
  18,5 cm para o centro (B); cabos 48 V pela frente do inversor; linha da pia sob o piso. Os arquivos de rotas em
  entregas/ não mudaram (rastreados pelo verificador). Figuras: `fatiar()` divide triângulos longos (matplotlib sem z-buffer).

## Cuidados
- mhc-lenovo (15 GB, swap cheio) reiniciou sem shutdown em 16/11 12:31 durante CFD: rodar pesado com
  `systemd-run --user --scope -p MemoryMax=6G -p MemorySwapMax=0`.
- Torre roda o FR3 real ao vivo: nada de CFD lá.
- snappyHexMesh: `maxGlobalCells` corta o refinamento em silêncio — procurar "reached limit" no log.

## Revisão por integrante (16/11, pronto)
Repositório confirmado **público** (só MHC-CodeSmith tem escrita). Integrantes revisam pelo navegador e registram o
parecer numa issue com o formulário `.github/ISSUE_TEMPLATE/revisao_integrante.yml` (rótulo `revisao`), ou pelo WhatsApp.
Guia com itens, páginas e decisões A01–A16 de cada um: `docs/REVISAO_INTEGRANTES.md` (tabela de pareceres no fim, a
preencher quando as issues fecharem). Cada `equipe/Pn/Ixx/README.md` ganhou o bloco `revisao-final` apontando para a seção
do PDF. As páginas foram tiradas do sumário do PDF de 16/11 (52 p.): se o relatório mudar, rodar de novo o gerador
(o script ficou em /tmp/gerar_revisao.py do lenovo; a tabela PAG no topo).

## Revisões dos integrantes incorporadas (23/11/2026)
- PRs #2 (P7 Herick, parecer), #4 (P3 Sabrina: I16/I17/I19, sem a incerteza de 1 %) e #5 (P2 Mateus: I07 com DCIR
  10–40 mΩ, I23 sem "112,4 úteis", I30 com contorno térmico e bitola 185 mm², I34 com 486 casos) mergeados em `main`.
  O #5 apagou `slides.tex`/`slides.pdf` de propósito; `compilar.sh` e os links foram ajustados.
- Aplicadas as seis correções obrigatórias do P7: figura do I35 (campo de equilíbrio 0,557 kg/s), referência Bosch,
  I10 (inclui os 96 W da bomba; 90 % é conservador), I12 (pico transitório; regime vai para a água), I34 (faixas da
  varredura de 486 casos, 3 casos param a 45 °C, dU/dT nominal = 0) e "fluido de arrefecimento".
- Figura do I30 refeita (rótulos cortados e nomes internos na legenda). I07 e tabela-resumo alinhados com 185 mm².
- P6 Amanda aprovou pelo WhatsApp sem mudanças (déficit do A/C já descrito no I32).
- Faltam: P1, P4 e P5 revisarem; nomes na capa; vídeo. A revisão externa de 19/11 (I25 cenários, I27 eixo, I29
  "ótima", limiar CC, I28 0–100) não foi aplicada: o grupo considera o trabalho fechado com os pareceres.
- I32 (23/11): déficit do A/C resolvido sem trocar o FreshWell. O sol pelo para-brisa é 1,11 kW (39 % da carga);
  cortina refletiva interna Remis REMIfront IV fechada com o veículo parado (IAC 0,5; varredura 0,3–0,7) leva a carga
  de projeto (2 pessoas, 62 m³/h) a 2,31 kW (2,09–2,53 kW), margem sempre positiva frente a 2,7 kW. No I29 o
  deslocamento começa às 17h45, então ao meio-dia o veículo está parado. `config/protecao_solar_cabine.yaml`,
  `scripts/calcular_i32_protecao_parabrisa.py` → `entregas/integrado_maxeon1540/i32_protecao_solar/`; teste próprio.
  Avisar a Amanda (P6), que tinha aprovado sem mudanças.

## 24/11/2026 — pareceres P4 e P1

- PR #6 (Victor, P4) incorporado: raio do item 28 (0,372 m livre; 10,4 s com 0,361 m),
  equação de aceleração igual ao código e Cr = 0,012 como hipótese conservadora.
- Issue #7 (Eduardo Barros Guimarães, P1) incorporada no relatório: ficha norte-americana da
  Continental, pressões como referência, estepe dentro da massa OEM (não confirmado), Brembo
  como referência e 70/30 como hipótese, faixas por eixo do layout A (1737–2223 / 1698–2294 kg),
  chapa do boiler como caso de 0,99 e 33,1 kg fora do I18 (4009,7 kg se somadas), cortina
  REMIfront IV (EUR 458, art. 37482) somada ao I24 → R$ 794 mil (725–888), I33 com picos
  293,13/312,49 °C e diferença de malha de 0,026 K, título correto da referência Topczewska.
- Nome do P1 na capa. Ainda faltam P5 (Fael) e os demais nomes da capa.
- PR #8 (Mateus, P2) incorporado: mínimo DC do I25 comparado na saída da cadeia (Pmin/eta_dc na
  entrada), como no replay do I29; com 1 kW o I25 vai a 50,1/27,8 km. Saídas do I25 reproduzidas
  localmente (diferença < 1e-13). A troca do parâmetro de 1 kW por corrente (1 A, CharIN) ficou
  como proposta em docs/INTERFACE_DC_MINIMO_EQUIPAMENTO.md; o config não mudou.
- PR #8, segundo commit (a0e962d): piso CC derivado de 1 A × 380 V = 0,38 kW (CharIN; pack 90S),
  aplicado no I25 e no I29. I25 só tração: 56,6/31,4 km a 40/80 km/h (1 kW dava 50,1/27,8).
  I29: 20,7 km/h, partida 18h00, 212,8 d (10/20 %) e 214,8 d (20/30 %); antes 17h45 e 248,8 d.
  Na integração: gráfico autonomia_temporal.png usava max(varredura) = 3 kW (curva zerada) →
  passa a usar o menor piso positivo; gerar_figuras.py comparava "0" com "0.0" do CSV → compara
  número; textos com 17h45/1 kW atualizados (I32, introdução, roteiro, README, FECHAMENTO).
  Pasta 1350 Wp (desenvolvimento_2026-11-09) e 1540 Wp (integrado_maxeon1540) seguem distintas
  por desenho: o relatório usa a 1540; as figuras I31/I35 vêm da 1350, mas não dependem de Wp,
  massa nem inventário do teto.

## 25/11/2026 — PR #9 (checklist da P5 e do projeto)

- Cenário vigente passou a `maxeon1560_independente` (4×SPR-MAX3-390-COM, 2S2P, 1560 Wp), saídas em
  `entregas/integrado_maxeon1560/`. Scripts, figuras, CI e verificadores apontam para ele; o
  `maxeon1540_independente` fica registrado como histórico (valores de referência por cenário em
  `scripts/verificar_cenario_integrado.py`).
- Cadeia completa: `scripts/executar_cenario_integrado.py --cenario maxeon1560_independente`, depois
  `sensibilizar_resistencias_rota`, `sensibilizar_ventilacao_mecanica`, envelopes de eixo/aderência,
  `otimizar_janela_missao` (normal, `--densa`, `--refino-extra`), `refinar_velocidade_missao`,
  `refinar_resolucao_missao`, `analisar_aliasing_limiar_dc`, `fechar_i29_velocidade` (busca e `--figura`),
  `calcular_custo_brl_i24`, `fechar_i30_corrente_maxima`, `calcular_i32_protecao_parabrisa`. Densa: ~26 min.
- Novos: `scripts/analisar_geracao_portateis_p5.py` (I08), `scripts/comparar_cfd_deck.py` e o caso
  `entregas/aero_equipado1540/sem_deck_bg_55x20x10` (rodado no mhc-lenovo com `--sem-deck`, clone em
  `/home/mhc/stf_semdeck`).
- `simular_missao` ganhou `primeira_partida_h`; o I29 (fechamento) não dirige antes da primeira partida.
- Relatório: seção "Simulações e algoritmos", mapa de dependências, quatro fluxogramas (TikZ), tabela
  de escolhas, I08/I09/I13/I17/I19–I20/I23/I25–I32 revistos; 70 páginas.
- Pendente: cotação do Renogy; estrutura da cama; rotação máxima do motor; nomes da capa P2–P7; vídeo.
