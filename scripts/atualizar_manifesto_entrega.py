"""Recalcula os hashes da entrega parcial; verificações são entradas declaradas."""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pytest', required=True, help='Resumo da última execução efetivamente conferida')
    parser.add_argument('--estrutura', required=True)
    parser.add_argument('--ruff', required=True, help='Informar também o escopo verificado')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    delivery = root/'entregas/parcial_2026-10-24'
    output = delivery/'manifesto_entrega.json'
    pdf = root/'output/pdf/memorial_revisao_aurora.pdf'
    result = {
        'status': 'PARCIAL_NAO_APROVADO',
        'updated_utc': datetime.now(timezone.utc).isoformat(),
        'generator': 'scripts/atualizar_manifesto_entrega.py',
        'checks': {'pytest': args.pytest, 'estrutura': args.estrutura, 'ruff': args.ruff,
                   'parametros_globais_sha256': sha(root/'config/parametros_globais.yaml')},
        'artefatos': {str(p.relative_to(delivery)): sha(p)
                      for p in sorted(delivery.rglob('*')) if p.is_file() and p != output},
        'memorial': {'path_relative_to_repo': str(pdf.relative_to(root)),
                     'bytes': pdf.stat().st_size, 'sha256': sha(pdf)},
        'warning': 'Testes e hashes não aprovam a engenharia; revisões físicas e humanas pendentes.',
    }
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    print(f'{len(result["artefatos"])} arquivos com hash; memorial{pdf.stat().st_size} bytes')


if __name__ == '__main__':
    main()
