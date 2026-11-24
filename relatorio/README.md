# Relatório final, slides e roteiro do vídeo

Entrega oficial: **02/12/2026 até 06:00**, por e-mail aos dois docentes — PDF < 20 MB,
vídeo de 8–10 min < 50 MB com todos os integrantes, anexo com os códigos.

| Arquivo | Conteúdo |
|---|---|
| `relatorio.tex` | Memorial de cálculo (51 p., 5 MB, 29 figuras incluindo 10 renderizações de CAD/CFD): introdução, revisão bibliográfica, itens 1–35, resumo, limitações, referências e anexo de códigos |
| `roteiro_video.md` | Roteiro do vídeo: 7 blocos de ~75 s, um por integrante, com os slides de apoio |
| `montagem_cad.py` | Montagem CAD detalhada no referencial do projeto (traseira interna em x = −3,35 m, piso em z = 0,68 m): layouts A/B com os detalhes do interior de 24/10 encaixados nas caixas finais, tração e bancos OEM, caixas de roda, deck Maxeon sobre trilhos na posição do CFD, rotas e portáteis |
| `renderizar_cad.py` | Renderizações de CAD (exterior, teto, estacionado, interiores A/B em corte, plantas, rotas, corte longitudinal, banco e chapas) a partir de `montagem_cad.py`, e de CFD (Cp na superfície, velocidade no plano de simetria) a partir do VTK da malha fina |
| `figura_cortina_i32.py` | Figura do item 32: cortina refletiva desenhada 3 cm atrás do para-brisa do modelo exterior e carga de A/C sem/com cortina (`entregas/integrado_maxeon1540/i32_protecao_solar/resumo.json`) |
| `gerar_figuras.py` | Gera `figuras/` a partir de `entregas/` e `equipe/` (nenhum número é digitado à mão) |
| `valores_i19.tex`, `valores_i29.tex` | Macros escritas por `scripts/calcular_gci_aero.py` e `scripts/fechar_i29_velocidade.py --figura` |
| `compilar.sh` | Figuras + PDFs |

## Compilar

```bash
relatorio/compilar.sh        # na raiz do repositório
```

Requer TeX Live com `texlive-lang-portuguese`, `texlive-science` (siunitx v3) e
`texlive-latex-extra` (metropolis). Nesta máquina (mhc-lenovo) faltam babel-portuguese e
siunitx; os PDFs foram compilados na torre (`hipolito-Precision-5860-Tower`) com a mesma
árvore de arquivos.

## Antes de enviar

- Preencher os nomes dos integrantes na capa (`relatorio.tex`, tabela P1–P7).
- Conferir se o repositório GitHub citado no anexo está público para os docentes.
- Os resultados não têm aprovação humana registrada (A01–A16 em
  `docs/APROVACOES_FINAIS_PENDENTES.md`); cada integrante deve revisar a sua seção.
