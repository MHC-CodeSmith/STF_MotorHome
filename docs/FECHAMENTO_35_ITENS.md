# Fechamento dos 35 itens e entregáveis — 16/11/2026

Pedido do usuário (16/11/2026): terminar os 35 itens e o trabalho todo. Isso substitui a
regra anterior de "não preparar relatório/slides". Entregáveis em `relatorio/`
(memorial PDF, slides, roteiro do vídeo). DEC-001–061 preservadas; nenhum parâmetro
global foi alterado.

## Lacunas fechadas nesta etapa

| Item | Antes | Agora | Script / saída |
|---|---|---|---|
| I19 | Cd 0,60–0,70 entre malhas "não aninhadas" | As malhas antigas pararam no limite `maxGlobalCells 650000` do snappy (log: "reached limit"), antes de completar o refinamento de superfície e de esteira; não eram família. Nova família 33×12×6 / 44×16×8 / 55×20×10 sem limite (`--max-celulas 5000000`): 291k/523k/751k células, Cd 0,6220/0,6338/0,6215, convergência oscilatória (R = −1,04), portanto sem Richardson; incerteza pela meia amplitude (Stern et al. 2001): **Cd = 0,622 ± 0,006 (1,0 %)**, C_dA = 3,00 m². O Cd 0,625 dos modelos de energia difere 0,5 % | `scripts/executar_aero_malha_adicional.py --divisoes`, `scripts/calcular_gci_aero.py` → `entregas/aero_equipado1540/familia_gci/` |
| I24 | total em R$ `null` | R$ 794 mil nominal (725–888 mil; inclui a cortina REMIfront IV do I32) com II/IPI/PIS/COFINS/ICMS; preços com URL e data | `config/custos_brl_i24.yaml`, `scripts/calcular_custo_brl_i24.py` → `entregas/integrado_maxeon1540/i24_custo_brl/` |
| I29 | divergência de ~6 dias entre passos; líder na borda da grade de velocidade | 15 min estava sub-resolvido; 5 e 1 min concordam em 0,02 d. Busca ampla 12–40 km/h × 48 horários (5 min) + refino a 1 min: 20,7 km/h, partida 18h00, 212,8 d (10/20 %), 214,8 d (20/30 %), com piso CC de 0,38 kW (1 A × 380 V; antes 1 kW: 17h45, 248,8 d); líder fora da borda; igual ao mínimo analítico de e(v) | `scripts/fechar_i29_velocidade.py` (+ `--figura`) → `entregas/integrado_maxeon1540/i29_fechamento/` |
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
- Nomes dos integrantes na capa do relatório: a preencher. Repositório GitHub público (conferido em 16/11);
  revisão por integrante em `docs/REVISAO_INTEGRANTES.md`.

## Incidente

Em 16/11 às 12:31 o mhc-lenovo reiniciou de forma não limpa (fim abrupto do journal,
kernel 7.0.0-42 → -43) enquanto rodavam as malhas e a busca do I29, com swap já cheio
por navegadores. Os trabalhos foram relançados em `systemd-run --user -p MemoryMax=6G`.
