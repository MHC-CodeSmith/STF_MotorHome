# Relatório Aurora Solar — revisão de 25/11/2026

O memorial segue a organização do relatório de referência do Cuca: Introdução com Objetivos,
Revisão bibliográfica por tema e Projeto técnico com métodos, especificações, parâmetros,
análise de custo e simulações. Ao final estão a tabela de respostas dos 35 itens, conclusões,
referências e os códigos. Resultados e hipóteses pertencem ao motorhome deste projeto.

A capa usa os oito nomes e as grafias fornecidos pelo usuário, em `autores.tex`. O vídeo está
fora desta revisão por instrução expressa do usuário; `roteiro_video.md` é um artefato anterior.
A auditoria completa do PR do Fael está em [`../docs/AUDITORIA_PR9_REESCRITA.md`](../docs/AUDITORIA_PR9_REESCRITA.md).

| Arquivo | Função |
|---|---|
| `relatorio.tex`, `relatorio.pdf` | Fonte e PDF do memorial |
| `autores.tex` | Nomes fornecidos pelo usuário, isolados da estrutura do documento |
| `atualizar_tabelas.py` | Lê as saídas do cenário1560 e gera `valores_integrados.tex` e tabelas de massa, custo, cama e autonomia solar |
| `gerar_figuras.py` | Curvas, vistas cotadas e campos de freio da massa atual; copia campos térmicos que independem de massa/FV |
| `montagem_cad.py`, `renderizar_cad.py` | Montagem e renderizações de CAD; campos CFD arquivados quando o cache está disponível |
| `figura_cortina_i32.py` | Representação da cortina e balanço do ar-condicionado |
| `figuras/produtos/fontes.json` | Fonte, modelo e SHA-256 das fotografias oficiais |
| `valores_i19.tex`, `valores_i29.tex` | Resultados gerados pelos fechamentos de arrasto e viagem |
| `compilar.sh` | Regenera tabelas/figuras e compila o PDF |

## Compilação

Na raiz, com Python3.11 e dependências do projeto instaladas:

```bash
relatorio/compilar.sh
```

Requer TeX Live com português, `siunitx`, `latexmk`, `adjustbox`, `xurl`, TikZ e fontes Latin
Modern (`texlive-lang-portuguese`, `texlive-science`, `texlive-latex-extra`). A compilação
usa as saídas versionadas; não refaz CFD nem a busca longa da missão.

## Reprodução numérica da revisão

```bash
PYTHONPATH=src:scripts .venv/bin/python scripts/reexecutar_revisao_relatorio.py --executar
relatorio/compilar.sh
```

Essa execução usa `maxeon1560_independente`, incorpora a cama no inventário e repete dinâmica,
freios, consumos e as buscas da viagem. O arranjo1540 é histórico. A grade densa e o fechamentoI29
levam vários minutos; o script imprime a lista de comandos sem executar quando `--executar`
é omitido. Não roda CFD. Mudança de configuração durante a cadeia interrompe a execução.

Os resultados continuam condicionados às hipóteses descritas em cada item. A verificação dos
elementos da cama não comprova a ancoragem OEM, e a interfaceCCS2 permanece não demonstrada.
A auditoria do software e os manifestos conferem consistência computacional, sem substituir
validação física. O PDF deve ficar abaixo dos20 MB exigidos no enunciado.

O recibo efetivo desta revisão fica em
[`revisao_relatorio/execucao.json`](../entregas/integrado_maxeon1560/revisao_relatorio/execucao.json),
com logs e hashes. A busca fechou em 20,5 km/h, 18h, 214,8 dias (reservas 10/20%);
40/80 km/h sob o mesmo horário resultaram em 248,8/457,8 dias. O resultado é condicional.
O recibo anterior `execucao_pipeline.json` permanece histórico.
