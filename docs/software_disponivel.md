# Software observado neste host — 22/10/2026 UTC

Detecção local por `shutil.which`, execução do binário com argumento de versão/ajuda (timeout de 8 s) e `importlib.import_module` em `.venv/bin/python`. Não é inventário das máquinas dos estudantes nem comprovação de licença acadêmica, toolbox, experiência ou capacidade de simulação. Não se instalou CAD/CFD/MATLAB nem bibliotecas externas adquiridas. Executáveis ausentes no PATH podem existir em outra instalação não carregada.

| Executável / comando | Caminho observado | Saída resumida |
|---|---|---|
| `python3 --version` | /usr/bin/python3 | Python 3.12.3 |
| `uv --version` | /home/mhc/.local/bin/uv | uv 0.12.18 (x86_64-unknown-linux-gnu) |
| `git --version` | /usr/bin/git | git version 2.43.0 |
| `pdftotext -v` | /usr/bin/pdftotext | pdftotext version 24.02.0 |
| `pdfinfo -v` | /home/mhc/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdfinfo | pdfinfo version 26.05.0 |
| `curl --version` | /usr/bin/curl | curl 8.5.0 (x86_64-pc-linux-gnu) libcurl/8.5.0 OpenSSL/3.0.13 zlib/1.3 brotli/1.1.0 zstd/1.5.5 libidn2/2.3.7 libpsl/0.21.2 (+libidn2/2.3.7) libssh/0.10.6/openssl/zlib nghttp2/1.59.0 librtmp/2.3 OpenLDAP/2.6.10 |
| `FreeCAD --version / ajuda se presente` | ausente no PATH | não encontrado no PATH |
| `freecad --version / ajuda se presente` | ausente no PATH | não encontrado no PATH |
| `FreeCADCmd --version / ajuda se presente` | ausente no PATH | não encontrado no PATH |
| `gmsh --version / ajuda se presente` | ausente no PATH | não encontrado no PATH |
| `simpleFoam --version / ajuda se presente` | ausente no PATH | não encontrado no PATH |
| `foamVersion --version / ajuda se presente` | ausente no PATH | não encontrado no PATH |
| `paraview --version / ajuda se presente` | ausente no PATH | não encontrado no PATH |
| `matlab --version / ajuda se presente` | ausente no PATH | não encontrado no PATH |
| `octave --version / ajuda se presente` | ausente no PATH | não encontrado no PATH |
| `EES --version / ajuda se presente` | ausente no PATH | não encontrado no PATH |
| `ffmpeg -version` | /usr/bin/ffmpeg | ffmpeg version 6.1.1-3ubuntu5+esm15 Copyright (c) 2000-2023 the FFmpeg developers |
| `pandoc --version` | /usr/bin/pandoc | pandoc 3.1.3 |
| `xelatex --version / ajuda se presente` | ausente no PATH | não encontrado no PATH |

| Módulo importado em `.venv/bin/python` | Evidência |
|---|---|
| `yaml` | 6.0.3 |
| `pytest` | 9.1.1 |
| `ruff` | import OK sem __version__ |
| `build` | 1.6.1 |
| `numpy` | No module named 'numpy' |
| `scipy` | No module named 'scipy' |
| `pandas` | No module named 'pandas' |
| `matplotlib` | No module named 'matplotlib' |
| `pvlib` | No module named 'pvlib' |
| `pybamm` | No module named 'pybamm' |
| `OCC` | No module named 'OCC' |
| `gmsh` | No module named 'gmsh' |

Ambiente criado com `uv venv .venv`, Python 3.12.3, seguido de `uv pip install --python .venv/bin/python pytest ruff PyYAML build`. Saída: pytest 9.1.1, ruff 0.17.1, PyYAML 6.0.3, build 1.6.1 (mais dependências). O extra `dev` no `pyproject.toml` permite reinstalar com `uv pip install --python .venv/bin/python -e '.[dev]'`. Módulo ruff importa sem `__version__`; `.venv/bin/ruff --version` identifica a versão. Nenhum requisito de licença dos alunos foi inferido dessa detecção.

Para repetir imports no ambiente correto:

```bash
.venv/bin/python -c 'import sys, yaml, pytest, build; print(sys.executable, yaml.__version__, pytest.__version__, build.__version__)'
.venv/bin/ruff --version
```

O host tem utilitários de texto/PDF e FFmpeg/Pandoc; não se demonstrou abertura nativa de CAD, malhamento ou solução CFD. P3 precisa provar CAD/CFD em M1; P1/P2/P7 precisam provar execução dos modelos multidimensionais e revisão de estabilidade. Os exemplos EES da apostila foram lidos, não executados.
