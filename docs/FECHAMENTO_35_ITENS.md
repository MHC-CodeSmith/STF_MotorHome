# Fechamento dos 35 itens — revisão de 25/11/2026

Resultado final da viagem após o reforço da cama: 20,5 km/h, primeira saída às 18h,
214,755556 dias com reservas 10/20%; alternativa 20/30%: 20,7 km/h e 215,793056 dias.
Comparação a horário/reservas comuns: 40 km/h → 248,767361 dias; 80 km/h → 457,750694 dias.
Primeira reserva do líder em 3,845139 dias/538,645874 km; ritmo posterior 30,635538 km/dia.
Recibo dos 30 comandos principais, cinco suplementos, três preparações recuperadas e três
rechecagens históricas em `entregas/integrado_maxeon1560/revisao_relatorio/execucao.json`.
As preparações sem código de saída no log são identificadas como tal, sem inventar registro.

Pedido do usuário (16/11/2026): terminar os 35 itens e o trabalho todo. Isso substitui a
regra anterior de "não preparar relatório/slides". Entregáveis em `relatorio/`
(memorial PDF, slides, roteiro do vídeo). DEC-001–061 preservadas; nenhum parâmetro
global foi alterado naquela etapa. A revisão de25/11 altera explicitamente a massa do
cenário1560 e a geometria da cama, com justificativa em `docs/decisoes.md`.

## Estado vigente

A reescrita do memorial e o tratamento integral dos27 pedidos do PR #9 estão documentados
em [AUDITORIA_PR9_REESCRITA.md](AUDITORIA_PR9_REESCRITA.md). O cenário ativo é
`maxeon1560_independente`, com cama redimensionada e massa nominal4042,78262976kg.
O teto permanece1560Wp; o cenário1540 é histórico. Os números antigos abaixo preservam
contexto e não substituem as tabelas geradas no relatório atual.

A capa foi preenchida com os oito nomes fornecidos pelo usuário. O vídeo foi excluído
do escopo por instrução expressa. O preço do Renogy está registrado; a rotação de referência
foi inferida da ficha Fiat, sem inventar nmaxOEM. A cama foi verificada por elementos e os
limites das ancoragens físicas permanecem explícitos.

## Histórico de fechamento

| Item | Antes | Agora | Script / saída |
|---|---|---|---|
| I19 | Cd 0,60–0,70 entre malhas "não aninhadas" | As malhas antigas pararam no limite `maxGlobalCells 650000` do snappy (log: "reached limit"), antes de completar o refinamento de superfície e de esteira; não eram família. Nova família 33×12×6 / 44×16×8 / 55×20×10 sem limite (`--max-celulas 5000000`): 291k/523k/751k células, Cd 0,6220/0,6338/0,6215, convergência oscilatória (R = −1,04), portanto sem Richardson; a revisão P3 substituiu a antiga alegação de incerteza de1% pela faixa observada entre malhas, sem independência de malha demonstrada; C_dA≈3,00m². O Cd 0,625 dos modelos de energia difere 0,5 % | `scripts/executar_aero_malha_adicional.py --divisoes`, `scripts/calcular_gci_aero.py` → `entregas/aero_equipado1540/familia_gci/` |
| I24 | total em R$ `null` | R$ 794 mil nominal (725–888 mil; inclui a cortina REMIfront IV do I32) com II/IPI/PIS/COFINS/ICMS; preços com URL e data | `config/custos_brl_i24.yaml`, `scripts/calcular_custo_brl_i24.py` → `entregas/integrado_maxeon1540/i24_custo_brl/` |
| I29 | divergência de ~6 dias entre passos; líder na borda da grade de velocidade | 15 min estava sub-resolvido; 5 e 1 min concordam em 0,02 d. Busca ampla 12–40 km/h × 48 horários (5 min) + refino a 1 min: 20,7 km/h, partida 18h00, teto de 1560 Wp e primeira partida às 18h00 sem condução antes dela: 211,8 d (10/20 %), 212,8 d (20/30 %), com piso CC de 0,38 kW na saída (1 A × 380 V; antes, com 1540 Wp: 212,8 d; com 1 kW: 17h45, 248,8 d); líder fora da borda; igual ao mínimo analítico de e(v) | `scripts/fechar_i29_velocidade.py` (+ `--figura`) → `entregas/integrado_maxeon1560/i29_fechamento/` |
| I30 | só correntes hipotéticas 300/450/600 A e h fixo | 489 A RMS na potência máxima (limite SVPWM, η 0,95, FP 0,9); contorno Churchill–Chu + radiação iterado; 85 °C no 1×120 mm² (77–124 °C). **Revisado em 20/11/2026:** contorno completo (ar/entorno radiativo, conduíte, 3 fases, perdas AC) eleva 1×120 mm² a 158 °C no cofre; 185 mm² atende 125 °C. Ver [correções térmicas e de bitola](CORRECOES_TERMICAS_E_BITOLA_2026-11.md) | `scripts/fechar_i30_corrente_maxima.py` → `entregas/integrado_maxeon1540/i30_corrente_maxima/` |

Também: pressão dos pneus (I02) do manual Fiat Ducato para 225/75 R16C (4,5/5,0 bar);
mapa de eficiência do motor (I04) por modelo paramétrico de perdas, rotulado como não OEM;
vistas cotadas da geometria externa (I17) geradas da superfície do CFD.

Malhas e campos da família de CFD (503 MB) ficam fora do Git em
`/home/mhc/motorhome_referencias_tarefas/cfd-familia-gci-20261116/`; no repositório ficam
dicionários, logs, histórico de forças e resumos (reproduzíveis por
`scripts/executar_aero_malha_adicional.py --divisoes NX NY NZ --max-celulas 5000000`).

## Ressalvas que continuam

- Interface CC solar→tração (B01) segue hipótese; I25/I27/I29 dependem dela.
- Sem aprovação humana registrada (A01–A16); cada integrante revisa a própria seção.
- Nomes da capa fornecidos pelo usuário em25/11 e aplicados em `relatorio/autores.tex`. Repositório GitHub público (conferido em16/11);
  revisão por integrante em `docs/REVISAO_INTEGRANTES.md`.

## Incidente

Em 16/11 às 12:31 o mhc-lenovo reiniciou de forma não limpa (fim abrupto do journal,
kernel 7.0.0-42 → -43) enquanto rodavam as malhas e a busca do I29, com swap já cheio
por navegadores. Os trabalhos foram relançados em `systemd-run --user -p MemoryMax=6G`.
