# Retomada rápida — STF, 25/11/2026

**Estado:** relatório publicado em `adb794dc3d5da2ff7085114c6d218365fe57a710`, nas refs
`main` e `hub/tarefas-motorhome-com-codex`. CI verde: 45613552886 / 45613552731.
41 páginas, 6.323.519 bytes, 38 figuras; 299 testes locais aprovados (8 avisos pvlib).
**Encerramento desta lane:** usuário pediu salvar a passagem e fechar o chat. Nesta
última retomada, conferidos inbox (sem notas), árvore limpa e refs remotas: ambas
estavam em `d1ca3587a9532c949ce9de77d005e7def17914ce` (somente documentação após
`adb794d`; PDF e cálculos não mudaram). Esta atualização também é só documental;
não confundir o CI verde do relatório acima com uma consulta nova de CI.

Última pergunta técnica respondida: houve CFD com/sem painéis — **sim**, resultados
conferidos diretamente no JSON e em `relatorio/tabela_deck.tex`. A remoção inclui
**painéis + deck/suportes**, não apenas os módulos; seção **3.1.12, p. impressa 19**.
Nenhuma simulação foi reexecutada nesta conferência. Não há edição técnica aberta
nesta lane; continuar pelos limites reais ao final, ou por nova orientação do usuário.

## Onde e como trabalhar

Repo público: https://github.com/MHC-CodeSmith/STF_MotorHome . Clone/branch de trabalho:
`/tmp/claude-1000/-home/2dcdde84-75b4-409a-a2e6-53a659ce1495/scratchpad/stf`, `integ`.
Autor autorizado: `MHC <carvalho.matheush@gmail.com>`, sem trailer.
Publicação autorizada: `git push origin integ:main integ:hub/tarefas-motorhome-com-codex`.
`rg` indisponível; usar grep/find/Python. Terminal exigiu `require_escalated` por falha bwrap.

Ler inbox ao iniciar/antes de decisões grandes: `sys_duet_inbox`. Antes de editar clone,
consultar/reivindicar `stf-report-worktree`; CPU de simulação: `lab-cpu-profile`.
Liberar ao terminar. Sem hardware. Lane antiga cedeu o clone e não edita:
`d2e23af7c2d74dc4b9f99e629252ca53`; respostas por `sys_duet_say` usando esse ID.
Nossa sessão: `fe638a06ed4941eda061b0b61b1c14ee`. Não criar subagentes sem autorização.

## Decisões do usuário

Relatório fluido, simples e desenvolvido como Cuca, inclusive frases aplicáveis com
atribuição. Sem listas itemizadas nem código/anexo de código no PDF. Manter imagens,
campos, gráficos, equações e comparações dos PRs junto da explicação/interpretação.
35 requisitos rastreados em tabela final, sem impor formato de checklist à narrativa.
Vídeo excluído. Capa exatamente como `relatorio/autores.tex` (8 nomes; não corrigir grafia).
Dados faltantes: pesquisar/calcular e declarar hipóteses; não pedir decisões rotineiras.

Todos os PRs #1/#2/#4/#5/#6/#8/#9 e issues #3/#7 conferidos; sem abertos na última consulta.
Fael: 27 pedidos/subpedidos; Alonso e Herick: comparações elétricas/térmicas preservadas.
Não dizer que tudo está fisicamente validado só porque PRs foram mesclados/testes passaram.

## Evidências que não precisam ser refeitas

- Auditorias: `AUDITORIA_ENUNCIADO_E_PRS.md`, `AUDITORIA_PR9_REESCRITA.md`;
  desenvolvimento e comparações: `REVISAO_LEITURA_E_COMPARACOES.md`.
- Enunciado reenviado é idêntico ao versionado; extração Cuca também idêntica à anterior.
  Hashes dos PDFs em `relatorio/referencias_fornecidas.json`. Não publicar PDF integral do Cuca.
- CFD com/sem **conjunto fixo (painéis + deck/suportes)**:
  `entregas/aero_equipado1540/comparacao_deck/resumo.json`, casos em
  `familia_gci/bg_55x20x10/` e `sem_deck_bg_55x20x10/`, mesmo diretório pai.
  Cd 0,62153633 / 0,55548590; CdA 3,000678 / 2,681797 m²; delta 0,318881 m² (+11,89%).
  Mesma área 4,827840 m², velocidade 22,22 m/s, solo móvel, rodas paradas, tratamento
  de malha equivalente (750.513 / 524.241 células). Não houve independência de malha
  demonstrada nem validação experimental. Mesma massa para isolar arrasto.
  Consumo com/sem: 40 km/h 0,22756/0,22084; 80 km/h 0,40848/0,38161 kWh/km.
  Geração perdida ao remover teto: 5,9399 kWh/dia; empate 884/221 km/dia a 40/80.
  Script `scripts/comparar_cfd_deck.py`; tabela `relatorio/tabela_deck.tex`.
  Pasta chama1540 por histórico: geometria/massa módulos1560 iguais; energia/massa
  recalculadas para1560. Não refazer CFD só pela mudança de potência nominal.
- Config SHA256: `047c725c8f26f5dbf4c824aaffeb92d09272f12a4e5e181e5e059c5eb3a4396b`.
  Cenário `maxeon1560_independente`; massa 4042,78262976 kg; margem PBT 207,21737 kg.
  Cama +66,257102 kg líquidos; estrado30mm, quadro50×50×3, postes45×45×4.
- Viagem: 20,5 km/h, primeira saída18h, 214,755556 dias, reservas10/20%; alternativa
  20/30%:215,793056 dias. Mesmos horário/reservas a40/80:248,767361/457,750694 dias.
  Recibo completo: `entregas/integrado_maxeon1560/revisao_relatorio/execucao.json`.
- Novos estudos em `relatorio/dados_comparacoes/`:20 casos um parâmetro por vez,
  140 janelas MILP pisos0,5/1kW,6 políticas de dias parados. Recibo `execucao.json`.
  Diurno08–16 diário falha serviços em7,20dias; pausas1/2dias permitem chegada
  condicional40km/h628,3/417,4dias e80km/h1156,3/765,3dias. Não é ótimo global.
- Térmica: freios p23–24, cabos p24, cabine/A/C p26, bateria p28, radiador p29
  (páginas impressas). Freios pico297,82°C; regeneração hipotética40/80kW256,98/217,34°C.
  Cabos489A pico:120/185mm²217,5/149,6°C permanente; normal382A158/118°C no cofre.
  Bateria486casos; pior para45°C em0,66h (25°C inicial) /0,37h (35°C).
  UA≥1093W/K para65°C/22,9kW; com redutor29,02kW exige1952W/K; vazões31,9/26,4/23,1L/min.
- Custo: aquisições/componentes768.536,40; reserva mista25.000; total793.536,40 reais.
  Não inventar rateio materiais/mão de obra. Diagrama FV não transfere energia
  armazenada do banco48V para tração; CCS2/alocação permanecem hipóteses.

## Reprodução / aberto

`bash relatorio/compilar.sh` gera tabelas/figuras, novos estudos e PDF (não roda CFD).
`PYTHONPATH=src MOTORHOME_SCENARIO=maxeon1560_independente .venv/bin/python scripts/verificar_cenario_integrado.py`
`PYTHONPATH=src .venv/bin/python scripts/verificar_desenvolvimento.py`
`.venv/bin/python -m pytest tests -q`; `.venv/bin/ruff check src scripts tests`.
Não repetir busca longa sem mudança física. Após alterar entradas/saídas rastreadas,
rodar verificadores `--registrar` após conferir os cálculos, e então sem essa opção.

Pendências reais: interfaceCCS2, limites/ancoragens OEM, ampacidade/I²t e ensaios físicos;
não fabricar aprovações. Seminário/envio e autorização docente para8nomes não realizados.
Código no PDF/vídeo são exceções explícitas do usuário, não cumprimento literal do enunciado.
