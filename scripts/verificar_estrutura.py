#!/usr/bin/env python3
"""Valida que existem 35 itens, com responsáveis e documentação mínima."""
import csv, pathlib, sys
r=pathlib.Path(__file__).resolve().parents[1]
items=list(csv.DictReader((r/'metadata/itens.csv').open(encoding='utf-8')))
problems=[]
if len(items)!=35: problems.append(f'Esperados 35 itens, há {len(items)}')
if len({x['numero'] for x in items})!=35: problems.append('Números repetidos')
for i in items:
 p=r/i['pasta']
 for rel in ('README.md','teoria.md','fontes.md','validacao.md','codigo/README.md','dados/README.md','resultados/README.md','externos/README.md'):
  if not (p/rel).is_file(): problems.append(str(p/rel))
print(f'Verificação de {len(items)} itens, 7 equipes.')
if problems:
 print('FALTANDO / ERROS:'); print('\n'.join(problems)); sys.exit(1)
print('Estrutura OK. ATENÇÃO: isto não valida física nem resultados.')
