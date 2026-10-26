"""Copia resultados I30/I35 já calculados, sem PDFs de terceiros."""

import argparse
import hashlib
import json
import shutil
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cabos', type=Path, required=True)
    p.add_argument('--radiador', type=Path, required=True)
    a = p.parse_args()
    delivery = Path('entregas/parcial_2026-10-24')
    cases = [
        (a.cabos, Path('equipe/P2_bateria_eletrica/I30_temperatura_de_cabos_multidimensional/resultados'),
         'cabos', 'resumo_cabos.json', Path('config/cabos_tracao_proposta.yaml')),
        (a.radiador, Path('equipe/P7_arrefecimento/I35_bomba_radiador_e_vazao/resultados'),
         'radiador', 'resumo_radiador.json', Path('config/arrefecimento_proposta.yaml')),
    ]
    for source, item, prefix, summary, config in cases:
        if not item.is_dir():
            raise ValueError(f'Item inexistente: {item}')
        result = json.loads((source/summary).read_text())
        for name, expected in result['inputs_sha256'].items():
            path = Path(name)
            if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                raise ValueError(f'Entrada alterada após cálculo: {name}; recalcular antes de consolidar')
        for path in source.iterdir():
            if path.suffix in {'.csv', '.json', '.png'}:
                shutil.copy2(path, item/path.name)
                portable = path.name if path.name.startswith('resumo_') else f'{prefix}_{path.name}'
                shutil.copy2(path, delivery/portable)
        shutil.copy2(config, delivery/config.name)
        print(f'{prefix}: {result["status"]}; dados transferidos sem aprovação de engenharia')


if __name__ == '__main__':
    main()
