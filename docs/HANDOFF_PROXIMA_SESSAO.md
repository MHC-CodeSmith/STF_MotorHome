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
