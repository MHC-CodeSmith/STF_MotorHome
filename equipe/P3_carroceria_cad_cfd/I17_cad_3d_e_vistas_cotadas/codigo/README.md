# Preparação da carroceria

Usar `scripts/obter_carroceria.py` e `scripts/preparar_carroceria.py` pela raiz da worktree; comandos completos em [carroceria de trabalho](../../../../docs/CARROCERIA_DE_TRABALHO.md). Saída GLB/STL em metros e Z-up, sem reescala. Três testes analíticos estão em `tests/test_geometria_malha.py`.

<!-- execucao-integrada:inicio -->
Reprodução integrada pelo repositório:

```bash
PYTHONPATH=src .venv/bin/python scripts/executar_cenario_integrado.py --cenario maxeon1540_independente --reexecutar
PYTHONPATH=src MOTORHOME_SCENARIO=maxeon1540_independente .venv/bin/python scripts/verificar_cenario_integrado.py
```

CFD e campos específicos preservam comandos em `docs/EXECUCAO_TECNICA02.md`;a cadeia integrada não substitui esses ensaios. Ver arquivos reais de evidência no índice local.
<!-- execucao-integrada:fim -->
