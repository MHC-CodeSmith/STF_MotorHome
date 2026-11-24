#!/bin/bash
# Gera figuras e compila o relatório.
# Requer TeX Live com texlive-lang-portuguese, texlive-science.
set -euo pipefail
cd "$(dirname "$0")/.."
.venv/bin/python relatorio/gerar_figuras.py > /dev/null
# Renderizações de CAD (geometria em entregas/) e de CFD (só se o VTK do cache existir).
CACHE=${CACHE:-/home/mhc/motorhome_referencias_tarefas}
VTK="$CACHE/cfd-familia-gci-20261116/bg_55x20x10/case/VTK/case_344"
.venv/bin/python relatorio/renderizar_cad.py $( [ -d "$VTK" ] && echo --cfd-vtk "$VTK" ) > /dev/null
.venv/bin/python relatorio/figura_cortina_i32.py > /dev/null
cd relatorio
latexmk -pdf -interaction=nonstopmode -halt-on-error relatorio.tex
ls -la relatorio.pdf
