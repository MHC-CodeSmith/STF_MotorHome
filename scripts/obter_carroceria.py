"""Obtém release fixada do Ducato e extrai apenas malha, metadados e avisos.

Downloads ficam no disco, fora do contexto. Não executa código do fornecedor.
"""

import argparse
import hashlib
import json
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

URL = 'https://github.com/vevalabs/openx-assets/releases/download/20261015/openx-assets-glb.zip'
SHA256 = 'a89e822fe6be4058150090a2624052c0bc8a4612743784f371f8c25cb9d82cbb'
MEMBROS = ('vehicles/fiat_ducato_2014/fiat_ducato_2014.glb',
           'vehicles/fiat_ducato_2014/fiat_ducato_2014.xoma',
           'LICENSES/CC-BY-4.0.txt', 'LICENSES/MPL-2.0.txt', 'REUSE.toml', 'README.md')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destino', type=Path, required=True)
    args = parser.parse_args()
    if args.destino.exists():
        raise FileExistsError('Destino deve ser novo; preservar fontes já obtidas')
    with TemporaryDirectory(prefix='motorhome-ducato-') as tmp:
        arquivo = Path(tmp)/'fonte.zip'
        request = urllib.request.Request(URL, headers={'User-Agent': 'motorhome-academic-study'})
        total, digest = 0, hashlib.sha256()
        with urllib.request.urlopen(request, timeout=30) as resposta, arquivo.open('wb') as stream:
            while bloco := resposta.read(1024*1024):
                total += len(bloco)
                if total > 32*1024*1024:
                    raise ValueError('Download excedeu limite de 32 MiB')
                digest.update(bloco)
                stream.write(bloco)
        if digest.hexdigest() != SHA256:
            raise ValueError('SHA256 diferente da release inspecionada; não incorporar')
        with zipfile.ZipFile(arquivo) as pacote:
            # Lista fechada e limite por membro; nenhuma extração de path externo.
            for nome in MEMBROS:
                info = pacote.getinfo(nome)
                if info.is_dir() or info.file_size > 5*1024*1024:
                    raise ValueError('Membro inválido ou maior que 5 MiB')
            args.destino.mkdir(parents=True, exist_ok=False)
            hashes = {}
            for nome in MEMBROS:
                data = pacote.read(nome)
                path = args.destino/nome
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
                hashes[nome] = hashlib.sha256(data).hexdigest()
        manifesto = {'url': URL, 'release': '20261015', 'sha256_zip': SHA256,
                     'bytes_zip': total, 'data_utc': datetime.now(timezone.utc).isoformat(),
                     'script': 'scripts/obter_carroceria.py', 'sha256_extraidos': hashes,
                     'codigo_externo_executado': False}
        (args.destino/'aquisicao.json').write_text(json.dumps(manifesto, indent=2))
    print(f'Ducato adquirido e verificado; fontes e licenças em {args.destino}')


if __name__ == '__main__':
    main()
