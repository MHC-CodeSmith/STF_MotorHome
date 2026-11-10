# Código do item 05

Adicionar scripts/notebooks originais ou dependências open-source autorizadas. Todo código deve indicar entrada, versão de biblioteca, comando de execução e arquivo de saída. Funções comuns vão para `src/motorhome`.

<!-- execucao-integrada:inicio -->
Reprodução integrada pelo repositório:

```bash
PYTHONPATH=src .venv/bin/python scripts/executar_cenario_integrado.py --cenario maxeon1540_independente --reexecutar
PYTHONPATH=src MOTORHOME_SCENARIO=maxeon1540_independente .venv/bin/python scripts/verificar_cenario_integrado.py
```

CFD e campos específicos preservam comandos em `docs/EXECUCAO_TECNICA02.md`;a cadeia integrada não substitui esses ensaios. Ver arquivos reais de evidência no índice local.
<!-- execucao-integrada:fim -->
