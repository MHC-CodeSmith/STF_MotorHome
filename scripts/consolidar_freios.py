"""Consolida I33 somente quando as entradas ainda coincidem com o cálculo."""

import argparse
import hashlib
import json
import shutil
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--origem', type=Path, required=True)
    args = p.parse_args()
    r = json.loads((args.origem/'resumo_freios.json').read_text())
    for name, sha in r['inputs_sha256'].items():
        if hashlib.sha256(Path(name).read_bytes()).hexdigest() != sha:
            raise ValueError(f'Entrada mudou: {name}. Recalcular antes de consolidar.')
    item = Path('equipe/P1_estrutura_freios/I33_freio_campo_termico_multidimensional/resultados')
    delivery = Path('entregas/parcial_2026-10-24')
    for path in args.origem.iterdir():
        if path.suffix in {'.csv', '.json', '.png'}:
            shutil.copy2(path, item/path.name)
            filename = path.name if path.name.startswith('resumo_') else f'freios_{path.name}'
            shutil.copy2(path, delivery/filename)
    shutil.copy2('config/freios_proposta.yaml', delivery/'freios_proposta.yaml')
    print('Freios: resultados condicionados transferidos, sem aprovação de engenharia.')


if __name__ == '__main__':
    main()
