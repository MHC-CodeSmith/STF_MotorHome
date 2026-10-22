"""HTTP limitado e validação de contêiner; nunca executa fontes baixadas."""

import argparse
import ast
import csv
import hashlib
import io
import json
import re
import struct
import subprocess
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

STATUSES = {'pagina_verificada', 'arquivo_baixado_validado',
            'indexado_download_nao_validado', 'inacessivel', 'sem_licenca', 'nao_verificado'}
MAX_BYTES = 40 * 1024 * 1024


def fetch(url, opener=urllib.request.urlopen, timeout=25, limit=MAX_BYTES):
    """Uma tentativa, tempo/socket e tamanho limitados, erro não implica arquivo."""
    result = {'url': url, 'data_utc': datetime.now(timezone.utc).isoformat(),
              'url_final': '', 'http': None, 'erro': '', 'bytes': None}
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'MotorhomeAcademicAudit/0.1'})
        with opener(request, timeout=timeout) as response:
            result.update(url_final=response.geturl(), http=response.status)
            data = response.read(limit + 1)
            if len(data) > limit:
                raise ValueError('limite de bytes excedido')
            if not 200 <= response.status < 300:
                raise ValueError(f'HTTP {response.status}')
            result['bytes'] = data
    except (OSError, ValueError, urllib.error.URLError) as exc:
        if isinstance(exc, urllib.error.HTTPError):
            result.update(http=exc.code, url_final=exc.geturl())
        result['erro'] = str(exc)
    return result


def validate(data, extension, pdf_path=None):
    """Validação sintática/contêiner, sem garantia física ou rebuild CAD."""
    extension = extension.lower()
    head = data[:1024].lstrip().lower()
    if not data or re.match(br'(?:<!doctype\s+html[^>]*>\s*)?<html\b', head):
        raise ValueError('HTML/vazio em lugar de arquivo')
    if extension in {'.zip', '.fcstd'}:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            members = archive.infolist()
            if sum(x.file_size for x in members) > 250 * 1024 * 1024:
                raise ValueError('ZIP descompactado excede limite')
            bad = archive.testzip()
            if bad:
                raise ValueError(f'CRC inválido: {bad}')
            return {'nivel': 'container_zip_crc', 'membros': [x.filename for x in members]}
    if extension == '.pdf':
        if not data.startswith(b'%PDF-') or pdf_path is None:
            raise ValueError('assinatura PDF/caminho ausente')
        run = subprocess.run(['pdfinfo', str(pdf_path)], capture_output=True, text=True,
                             timeout=20, check=False)
        if run.returncode:
            raise ValueError('pdfinfo: ' + run.stderr)
        return {'nivel': 'container_pdfinfo', 'pdfinfo': run.stdout}
    if extension in {'.igs', '.iges'}:
        lines = data.decode('ascii').splitlines()
        sections = {line[72:73] for line in lines if len(line) >= 73}
        if not {'S', 'G', 'D', 'P', 'T'} <= sections:
            raise ValueError('seções IGES ausentes')
        return {'nivel': 'assinatura_iges', 'abertura_nativa': False, 'watertight': None}
    if extension in {'.step', '.stp'}:
        if b'ISO-10303-21;' not in data or b'END-ISO-10303-21;' not in data:
            raise ValueError('assinatura STEP ausente')
        return {'nivel': 'assinatura_step', 'abertura_nativa': False, 'watertight': None}
    if extension == '.stl':
        binary = len(data) >= 84 and len(data) == 84 + 50 * struct.unpack('<I', data[80:84])[0]
        ascii_stl = head.startswith(b'solid') and b'endsolid' in data and b'facet normal' in data
        if not binary and not ascii_stl:
            raise ValueError('assinatura STL ausente')
        return {'nivel': 'estrutura_stl', 'abertura_nativa': False, 'watertight': None}
    text = data.decode('utf-8')
    if '\x00' in text:
        raise ValueError('binário em lugar de texto')
    if extension == '.py':
        ast.parse(text)
        return {'nivel': 'sintaxe_python_sem_execucao'}
    if extension == '.ipynb' and 'cells' not in json.loads(text):
        raise ValueError('notebook sem células')
    if extension not in {'.py', '.txt', '.md', '.m', '.rs', '.ipynb', ''}:
        raise ValueError('formato sem validador: ' + extension)
    return {'nivel': 'texto_utf8_nao_html_sem_execucao'}


def check(url, cache, filename=None, opener=urllib.request.urlopen):
    result = fetch(url, opener=opener)
    data = result.pop('bytes')
    result.update(status='inacessivel', tamanho_bytes=None, sha256='', caminho_cache='',
                  extensao='', nivel_validacao='', validacao={})
    if data is None:
        return result
    if filename is None:
        if b'anubis_challenge' in data.lower() or b"making sure you&#39;re not a bot" in data.lower():
            result['erro'] = 'HTTP acessível; desafio anti-bot impede leitura da fonte'
            return result
        result['status'] = 'pagina_verificada'
        return result
    # Filename is caller supplied; refuse traversals and caches within this repository.
    cache = Path(cache).resolve()
    repo = Path(__file__).resolve().parents[1]
    if cache == repo or repo in cache.parents or Path(filename).name != filename:
        raise ValueError('cache deve estar fora do repositório; nome sem diretórios')
    cache.mkdir(parents=True, exist_ok=True)
    path = cache / filename
    path.write_bytes(data)
    result.update(tamanho_bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                  caminho_cache=str(path), extensao=path.suffix.lower(),
                  status='indexado_download_nao_validado')
    try:
        validation = validate(data, path.suffix, path)
        result.update(status='arquivo_baixado_validado', nivel_validacao=validation['nivel'],
                      validacao=validation)
    except (ValueError, SyntaxError, UnicodeError, zipfile.BadZipFile,
            OSError, subprocess.TimeoutExpired) as exc:
        result['erro'] = str(exc)
    return result


def check_catalog(catalog, cache, opener=urllib.request.urlopen):
    """Reverifica URLs registrados; não infere licença nem descobre URLs por adivinhação."""
    results = []
    with Path(catalog).open(encoding='utf-8', newline='') as stream:
        for number, row in enumerate(csv.DictReader(stream), 1):
            entry = {'titulo': row['titulo'], 'itens': row['itens'],
                     'pagina': check(row['url'], cache, opener=opener), 'arquivo': None,
                     'licenca_status_historico': row.get('licenca_status', 'nao_verificado')}
            if row.get('arquivo_url'):
                filename = f"{number:02}_arquivo{row.get('extensao', '')}"
                entry['arquivo'] = check(row['arquivo_url'], cache, filename, opener)
            results.append(entry)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('url', nargs='?')
    parser.add_argument('--catalogo', type=Path)
    parser.add_argument('--arquivo')
    parser.add_argument('--cache', type=Path, default=Path('/home/mhc/motorhome_referencias/downloads'))
    args = parser.parse_args()
    if bool(args.url) == bool(args.catalogo):
        parser.error('informe URL ou --catalogo, exclusivamente')
    if args.catalogo:
        results = check_catalog(args.catalogo, args.cache)
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return int(any(x['pagina']['status'] == 'inacessivel'
                       or (x['arquivo'] and x['arquivo']['status'] != 'arquivo_baixado_validado')
                       for x in results))
    result = check(args.url, args.cache, args.arquivo)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['status'] in {'pagina_verificada', 'arquivo_baixado_validado'} else 1


if __name__ == '__main__':
    raise SystemExit(main())
