"""Fixtures originais em memória; testes nunca acessam a rede."""

import importlib.util
import io
import subprocess
import urllib.error
import zipfile
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    'sources', Path(__file__).resolve().parents[1] / 'scripts/verificar_fontes.py')
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def opener(data, status=200):
    class Response(io.BytesIO):
        def geturl(self):
            return 'https://fixture.invalid/final'

    def open_fixture(request, timeout):
        assert timeout == 25
        response = Response(data)
        response.status = status
        return response
    return open_fixture


def archive_bytes():
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_STORED) as archive:
        archive.writestr('original.txt', b'conteudo sintetico original')
    return stream.getvalue()


def test_page_and_independent_file(tmp_path):
    page = module.check('https://fixture.invalid/', tmp_path, opener=opener(b'<html>page</html>'))
    assert page['status'] == 'pagina_verificada'
    assert page['tamanho_bytes'] is None
    data = archive_bytes()
    result = module.check('https://fixture.invalid/z', tmp_path, 'fixture.zip', opener(data))
    assert result['status'] == 'arquivo_baixado_validado'
    assert result['tamanho_bytes'] == len(data)
    assert len(result['sha256']) == 64
    assert result['url_final'].endswith('/final')
    assert result['validacao']['membros'] == ['original.txt']


@pytest.mark.parametrize('data', [b'<html>login</html>', b'<!DOCTYPE html>blocked', b'not a zip'])
def test_fake_zip(tmp_path, data):
    result = module.check('https://fixture.invalid/z', tmp_path, 'bad.zip', opener(data))
    assert result['status'] == 'indexado_download_nao_validado'
    assert result['erro']
    assert result['nivel_validacao'] == ''


def test_crc_failure():
    data = archive_bytes().replace(b'conteudo sintetico original', b'CONTEUDO sintetico original')
    with pytest.raises((ValueError, zipfile.BadZipFile), match='CRC'):
        module.validate(data, '.zip')


def test_inaccessible(tmp_path):
    def fail(request, timeout):
        raise urllib.error.HTTPError(request.full_url, 403, 'Forbidden', {}, None)
    result = module.check('https://fixture.invalid/z', tmp_path, 'z.zip', fail)
    assert result['status'] == 'inacessivel'
    assert result['http'] == 403
    assert result['tamanho_bytes'] is None and result['sha256'] == ''
    assert not list(tmp_path.iterdir())


def test_timeout_and_size_limit():
    def fail(request, timeout):
        raise TimeoutError('synthetic timeout')
    assert module.fetch('https://fixture.invalid', fail)['erro'] == 'synthetic timeout'
    result = module.fetch('https://fixture.invalid', opener(b'12345'), limit=4)
    assert result['bytes'] is None and 'limite' in result['erro']


def test_python_is_parsed_not_executed(tmp_path):
    result = module.check('https://fixture.invalid/a', tmp_path, 'a.py',
                          opener(b'raise RuntimeError("must never execute")\n'))
    assert result['status'] == 'arquivo_baixado_validado'
    bad = module.check('https://fixture.invalid/a', tmp_path, 'bad.py', opener(b'def bad('))
    assert bad['status'] == 'indexado_download_nao_validado'


def test_cad_signature_is_not_native_validation():
    data = b'ISO-10303-21;\nEND-ISO-10303-21;'
    result = module.validate(data, '.step')
    assert result['abertura_nativa'] is False and result['watertight'] is None
    with pytest.raises(ValueError, match='IGES'):
        module.validate(b'fake CAD', '.igs')


def test_source_with_html_literal_is_text():
    result = module.validate(b'html = "<html>example</html>"\n', '.py')
    assert result['nivel'] == 'sintaxe_python_sem_execucao'


def test_challenge_is_not_verified_page(tmp_path):
    result = module.check('https://fixture.invalid', tmp_path,
                          opener=opener(b'<html>Making sure you&#39;re not a bot</html>'))
    assert result['http'] == 200 and result['status'] == 'inacessivel'


def test_stl_structure_only():
    result = module.validate(b'\0' * 84, '.stl')
    assert result['watertight'] is None
    with pytest.raises(ValueError, match='STL'):
        module.validate(b'fake', '.stl')


def test_pdfinfo_is_required(tmp_path, monkeypatch):
    def run(command, **kwargs):
        assert command == ['pdfinfo', str(tmp_path / 'tiny.pdf')]
        assert kwargs['timeout'] == 20 and kwargs['check'] is False
        return subprocess.CompletedProcess(command, 0, stdout='Pages: 1\n', stderr='')
    monkeypatch.setattr(module.subprocess, 'run', run)
    result = module.check('https://fixture.invalid', tmp_path, 'tiny.pdf',
                          opener(b'%PDF-1.4\n%%EOF'))
    assert result['nivel_validacao'] == 'container_pdfinfo'
    monkeypatch.setattr(module.subprocess, 'run', lambda *a, **k:
                        subprocess.CompletedProcess(a, 1, stdout='', stderr='invalid PDF'))
    result = module.check('https://fixture.invalid', tmp_path, 'tiny.pdf',
                          opener(b'%PDF-1.4\n%%EOF'))
    assert result['status'] == 'indexado_download_nao_validado'


def test_catalog_uses_separate_page_and_pinned_file(tmp_path):
    catalog = tmp_path / 'catalog.csv'
    catalog.write_text('titulo,url,itens,arquivo_url,extensao,licenca_status\n'
                       'synthetic,https://fixture.invalid/page,17,'
                       'https://fixture.invalid/commit/a.py,.py,sem_licenca\n')
    calls = []

    def open_fixture(request, timeout):
        calls.append(request.full_url)
        data = b'x=1' if request.full_url.endswith('.py') else b'<html>page</html>'
        return opener(data)(request, timeout)

    results = module.check_catalog(catalog, tmp_path / 'cache', open_fixture)
    assert len(calls) == 2
    assert results[0]['pagina']['status'] == 'pagina_verificada'
    assert results[0]['arquivo']['status'] == 'arquivo_baixado_validado'
    assert results[0]['licenca_status_historico'] == 'sem_licenca'


def test_reject_repo_cache_and_path_traversal(tmp_path):
    with pytest.raises(ValueError, match='cache'):
        module.check('https://fixture.invalid', tmp_path, '../escape.py', opener(b'x=1'))
    with pytest.raises(ValueError, match='cache'):
        module.check('https://fixture.invalid', Path(__file__).parents[1], 'a.py', opener(b'x=1'))
