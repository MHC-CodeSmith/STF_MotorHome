"""Dados sintéticos locais; nenhum parâmetro do veículo é preenchido."""

import csv
import importlib.util
from pathlib import Path

import pytest
import yaml

SPEC = importlib.util.spec_from_file_location(
    'audit', Path(__file__).resolve().parents[1] / 'scripts/auditar_projeto.py')
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


@pytest.fixture
def project(tmp_path):
    rows = []
    for owner, ids in module.OWNERS.items():
        for number in sorted(ids):
            folder = f'equipe/{owner}_sintetico/I{number:02}_sintetico'
            p = tmp_path / folder
            p.mkdir(parents=True)
            (p / 'README.md').write_text(f'**Responsável:** {owner}\n**Depende de:** nenhum\n')
            (p / 'teoria.md').write_text('A preencher com equações')
            (p / 'validacao.md').write_text('PENDENTE')
            rows.append({'numero': str(number), 'pessoa': owner, 'dependencias': '',
                         'pasta': folder, 'status': 'nao_iniciado'})
    (tmp_path / 'metadata').mkdir()
    (tmp_path / 'config').mkdir()
    (tmp_path / 'docs/fontes_recebidas').mkdir(parents=True)
    (tmp_path / 'docs/fluxograma_dependencias.mmd').write_text('flowchart TD\n')
    (tmp_path / 'config/parametros_globais.yaml').write_text(
        yaml.safe_dump({'vehicle': {'mass': None}, 'project': {'vehicle_baseline_approved': False}}))
    for name in module.PDFS:
        (tmp_path / 'docs/fontes_recebidas' / name).write_bytes(b'fixture original')
    save(tmp_path, rows)
    return tmp_path, rows


def save(root, rows):
    with (root / 'metadata/itens.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def test_positive_coverage_and_pending_parameters(project):
    root, _ = project
    before = (root / 'config/parametros_globais.yaml').read_bytes()
    result = module.audit(root, booklet=root / 'apostila-ausente.pdf')
    assert result['erros'] == []
    assert result['contagens'] == {'P1': 8, 'P2': 5, 'P3': 3, 'P4': 6, 'P5': 5, 'P6': 4, 'P7': 4}
    assert [x['id'] for x in result['itens']] == list(range(1, 36))
    assert all(x['teoria_template'] and x['revisao_pendente'] for x in result['itens'])
    assert result['parametros_null'] == ['vehicle.mass']
    assert result['aprovacao_engenharia'] is False
    assert len(result['documentos_locais']) == 4
    assert 'Documento local ausente' in '\n'.join(result['avisos'])
    assert before == (root / 'config/parametros_globais.yaml').read_bytes()


@pytest.mark.parametrize(('mutation', 'diagnostic'), [
    ('duplicate', 'IDs duplicados'), ('range', 'exatamente 1..35'),
    ('bad_id', 'ID inválido'), ('owner', 'responsável CSV incorreto'),
    ('readme', 'responsável README/CSV divergente'),
    ('unknown_dep', 'dependência inexistente'), ('bad_dep', 'dependência inválida'),
    ('duplicate_dep', 'dependência duplicada'), ('cycle', 'Ciclo:'),
    ('graph', 'Grafo Mermaid/CSV divergente'),
    ('missing_readme', 'README ausente'), ('approval', 'aprovado com template'),
])
def test_diagnoses_defects(project, mutation, diagnostic):
    root, rows = project
    if mutation == 'duplicate':
        rows.append(rows[0].copy())
    elif mutation == 'range':
        rows[0]['numero'] = '36'
    elif mutation == 'bad_id':
        rows[0]['numero'] = 'x'
    elif mutation == 'owner':
        rows[0]['pessoa'] = 'P2'
    elif mutation == 'readme':
        (root / rows[0]['pasta'] / 'README.md').write_text('**Responsável:** P7')
    elif mutation == 'unknown_dep':
        rows[0]['dependencias'] = '99'
    elif mutation == 'bad_dep':
        rows[0]['dependencias'] = 'x'
    elif mutation == 'duplicate_dep':
        rows[0]['dependencias'] = '2;2'
    elif mutation == 'cycle':
        rows[0]['dependencias'] = rows[1]['numero']
        rows[1]['dependencias'] = rows[0]['numero']
    elif mutation == 'graph':
        (root / 'docs/fluxograma_dependencias.mmd').write_text('I01 --> I02')
    elif mutation == 'missing_readme':
        (root / rows[0]['pasta'] / 'README.md').unlink()
    elif mutation == 'approval':
        rows[0]['status'] = 'aprovado'
    save(root, rows)
    assert diagnostic in '\n'.join(module.audit(root)['erros'])


def test_nested_nulls():
    assert module.missing_values({'a': [None, {'b': None}], 'c': 0}) == ['a[0]', 'a[1].b']
