#!/usr/bin/env python3
import csv
import pathlib

r=pathlib.Path(__file__).resolve().parents[1]
rows=list(csv.DictReader((r/'metadata/itens.csv').open(encoding='utf-8')))
for p in sorted({row['pessoa'] for row in rows}):
 data=[row for row in rows if row['pessoa']==p]
 print(p, ' '.join(row['numero'] for row in data))
