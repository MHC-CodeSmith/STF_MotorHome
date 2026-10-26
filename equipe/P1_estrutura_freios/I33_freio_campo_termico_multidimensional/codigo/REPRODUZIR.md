# I33 — reprodução

Executar na raiz da worktree:

```bash
PYTHONPATH=src .venv/bin/python -m pytest tests/test_freios_axisimetricos.py -q
.venv/bin/python scripts/calcular_freios.py --destino /tmp/aurora-freios-reproducao
.venv/bin/python scripts/consolidar_freios.py --origem /tmp/aurora-freios-reproducao
```

Destino deve ser novo. Configuração`config/freios_proposta.yaml`;
código`src/motorhome/freios_axisimetricos.py`. Config não aprovada, preservando
os parâmetros globais. Consolidar compara SHA256 antes de transferir resultados.
Fontes/teoria/limites em[docs/FREIOS_2D.md](../../../../docs/FREIOS_2D.md).
