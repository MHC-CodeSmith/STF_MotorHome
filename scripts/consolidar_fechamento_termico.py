"""Consolida bateria/hidráulica/missão após conferir entradas SHA256."""

import argparse
import csv
import hashlib
import json
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ['bateria', 'hidraulica', 'missao', 'portatil', 'cad-portatil', 'bom']:
        parser.add_argument('--'+arg, type=Path, required=True)
    args = parser.parse_args()
    with Path('metadata/itens.csv').open() as f:
        items = {int(row['numero']): Path(row['pasta']) for row in csv.DictReader(f)}
    delivery = Path('entregas/parcial_2026-10-24')
    cases = [(args.bateria, 34, 'bateria_carga', 'resumo_bateria_carga.json', 'bateria_termica_proposta.yaml'),
             (args.hidraulica, 35, 'hidraulica', 'resumo_hidraulica.json', 'hidraulica_proposta.yaml'),
             (args.missao, 25, 'missao_atual', 'resumo_missao_atual.json', 'limites_operacionais_proposta.yaml'),
             (args.portatil, 8, 'solar_portatil', 'resumo_solar_portatil.json', 'solar_portatil_proposta.yaml'),
             (args.bom, 24, 'bom_rolamento', 'resumo_bom_rolamento.json', 'mecanica_comparativa_proposta.yaml')]
    for source, number, prefix, summary, config in cases:
        r = json.loads((source/summary).read_text())
        for name, sha in r['inputs_sha256'].items():
            if hashlib.sha256(Path(name).read_bytes()).hexdigest() != sha:
                raise ValueError(f'Entrada mudou: {name}; recalcular')
        for f in source.iterdir():
            if f.suffix in {'.csv', '.png', '.json'}:
                item_name = f'{prefix}_{f.name}' if prefix == 'hidraulica' and not f.name.startswith('resumo_') else f.name
                shutil.copy2(f, items[number]/'resultados'/item_name)
                name = f.name if f.name.startswith('resumo_') else f'{prefix}_{f.name}'
                shutil.copy2(f, delivery/name)
        shutil.copy2(Path('config')/config, delivery/config)
        print(number, r['status'])
    cad = json.loads((args.cad_portatil/'manifesto_cad_portatil.json').read_text())
    for name, sha in cad['inputs_sha256'].items():
        if hashlib.sha256(Path(name).read_bytes()).hexdigest() != sha:
            raise ValueError(f'EntradaCAD mudou: {name}')
    for f in args.cad_portatil.iterdir():
        if f.suffix in {'.png', '.step', '.glb', '.json'}:
            shutil.copy2(f, delivery/f.name)
    shutil.copy2('config/custos_proposta.yaml', delivery/'custos_proposta.yaml')
    shutil.copy2(args.bom/'rolamento_comparativo.csv', items[20]/'resultados'/'rolamento_comparativo.csv')


if __name__ == '__main__':
    main()
