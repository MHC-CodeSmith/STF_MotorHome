"""Auditoria estrutural somente leitura; parâmetros pendentes não aprovam engenharia."""

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

import yaml

OWNERS = {
    "P1": {1, 2, 3, 14, 15, 18, 24, 33},
    "P2": {6, 7, 9, 23, 30},
    "P3": {16, 17, 19},
    "P4": {4, 5, 20, 21, 22, 28},
    "P5": {8, 25, 26, 27, 29},
    "P6": {11, 13, 31, 32},
    "P7": {10, 12, 34, 35},
}
PDFS = (
    "Projeto Sist. Térmicos e Fluídicos 2026.pdf",
    "Organizacao_Motorhome_P1_P7.pdf",
    "Projetos prontos, CADs e códigos reutilizáveis para o motorhome elétrico solar.pdf",
)
BOOKLET = Path('/home/mhc/Downloads/Apostila_SEM0571_Prof_Cristiano_2025.pdf')


def missing_values(value, prefix=""):
    """Retorna caminhos YAML null sem atribuir valores."""
    if isinstance(value, dict):
        return [p for k, v in value.items() for p in missing_values(v, f'{prefix}.{k}'.strip('.'))]
    if isinstance(value, list):
        return [p for k, v in enumerate(value) for p in missing_values(v, f'{prefix}[{k}]')]
    return [prefix] if value is None else []


def audit(root, booklet=BOOKLET):
    root = Path(root)
    errors, warnings, states = [], [], []
    with (root / 'metadata/itens.csv').open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream))
    ids = []
    graph = {}
    counts = Counter()
    for row in rows:
        try:
            number = int(row['numero'])
        except ValueError:
            errors.append(f"ID inválido: {row['numero']}")
            continue
        ids.append(number)
        owner = row['pessoa']
        counts[owner] += 1
        if number not in OWNERS.get(owner, set()):
            errors.append(f'I{number:02}: responsável CSV incorreto {owner}')
        deps = []
        for dep in filter(None, row['dependencias'].split(';')):
            try:
                deps.append(int(dep))
            except ValueError:
                errors.append(f'I{number:02}: dependência inválida {dep}')
        if len(deps) != len(set(deps)):
            errors.append(f'I{number:02}: dependência duplicada')
        graph[number] = deps
        folder = root / row['pasta']
        readme = folder / 'README.md'
        if not readme.is_file():
            errors.append(f'I{number:02}: README ausente')
            continue
        text = readme.read_text(encoding='utf-8')
        match = re.search(r'\*\*Responsável:\*\*\s*(P\d+)', text)
        if not match or match[1] != owner:
            errors.append(f'I{number:02}: responsável README/CSV divergente')
        if not re.search(rf'(^|/)({owner})_[^/]+/I{number:02}_', row['pasta']):
            errors.append(f'I{number:02}: pasta/responsável divergente')
        dep_line = re.search(r'\*\*Depende de:\*\*([^\n]*)', text)
        readme_deps = [int(x) for x in re.findall(r'\bI(\d+)\b', dep_line[1])] if dep_line else []
        if set(readme_deps) != set(deps):
            errors.append(f'I{number:02}: dependências README/CSV divergentes')
        theory = folder / 'teoria.md'
        template = theory.is_file() and 'A preencher com equações' in theory.read_text()
        validation = folder / 'validacao.md'
        pending = not validation.is_file() or 'PENDENTE' in validation.read_text()
        if row['status'] == 'aprovado' and (template or pending):
            errors.append(f'I{number:02}: aprovado com template/revisão pendente')
        states.append({'id': number, 'pessoa': owner, 'status': row['status'],
                       'teoria_template': template, 'revisao_pendente': pending})
    if set(ids) != set(range(1, 36)):
        errors.append(f'IDs devem ser exatamente 1..35: faltam {sorted(set(range(1, 36))-set(ids))}; '
                      f'extras {sorted(set(ids)-set(range(1, 36)))}')
    if len(ids) != len(set(ids)):
        errors.append('IDs duplicados')
    for owner, expected in OWNERS.items():
        if counts[owner] != len(expected):
            errors.append(f'{owner}: esperados {len(expected)}, encontrados {counts[owner]}')
    for number, deps in graph.items():
        for dep in deps:
            if dep not in graph:
                errors.append(f'I{number:02}: dependência inexistente I{dep:02}')
    visiting, done = set(), set()

    def visit(number, trail):
        if number in visiting:
            errors.append('Ciclo: ' + ' -> '.join(map(str, trail + [number])))
            return
        if number in done:
            return
        visiting.add(number)
        for dep in graph.get(number, []):
            if dep in graph:
                visit(dep, trail + [number])
        visiting.remove(number)
        done.add(number)

    for number in graph:
        visit(number, [])
    mermaid = root / 'docs/fluxograma_dependencias.mmd'
    expected_edges = {(dep, n) for n, deps in graph.items() for dep in deps}
    if mermaid.is_file():
        edges = {(int(a), int(b)) for a, b in re.findall(r'I(\d+)\s*-->\s*I(\d+)', mermaid.read_text())}
        if edges != expected_edges:
            errors.append('Grafo Mermaid/CSV divergente')
    else:
        errors.append('Grafo Mermaid ausente')
    parameters = yaml.safe_load((root / 'config/parametros_globais.yaml').read_text())
    missing = missing_values(parameters)
    if missing:
        warnings.append(f'{len(missing)} parâmetros null: engenharia bloqueada')
    if not parameters.get('project', {}).get('vehicle_baseline_approved'):
        warnings.append('Variante/configuração integrada sem aprovação final'
                        if parameters.get('canonical') else 'Veículo-base sem aprovação')
    contextual = []
    context_path = root / 'metadata/interfaces_contextuais.csv'
    if not context_path.is_file():
        errors.append('Arquivo metadata/interfaces_contextuais.csv ausente')
    else:
        contextual_pairs = set()
        with context_path.open(encoding='utf-8', newline='') as stream:
            for row in csv.DictReader(stream):
                try:
                    source, target = int(row['origem']), int(row['destino'])
                except (KeyError, ValueError):
                    errors.append('Interface contextual com ID inválido')
                    continue
                pair = (source, target)
                if pair in contextual_pairs:
                    errors.append(f'Interface contextual duplicada: I{source:02} -> I{target:02}')
                contextual_pairs.add(pair)
                if source == target:
                    errors.append(f'Interface contextual autorreferente: I{source:02}')
                if source not in graph or target not in graph:
                    errors.append(f'Interface contextual inexistente: I{source:02} -> I{target:02}')
                if pair in expected_edges:
                    errors.append(f'Interface contextual duplicada como dependência: I{source:02} -> I{target:02}')
                if row.get('tipo') != 'contextual_nao_bloqueante' or not row.get('descricao', '').strip():
                    errors.append(f'Interface contextual sem tipo/justificativa: I{source:02} -> I{target:02}')
                contextual.append({'origem': source, 'destino': target, 'tipo': row.get('tipo'),
                                   'descricao': row.get('descricao', '')})
    if 28 in graph.get(33, []):
        warnings.append('I28 -> I33 está marcado como dependência de dados; revisar classificação contextual')
    inventory = [{'path': str(root / 'docs/fontes_recebidas' / name),
                  'exists': (root / 'docs/fontes_recebidas' / name).is_file()} for name in PDFS]
    inventory.append({'path': str(booklet), 'exists': Path(booklet).is_file()})
    for doc in inventory:
        if not doc['exists']:
            warnings.append(f"Documento local ausente: {doc['path']}")
    return {'erros': errors, 'avisos': warnings, 'contagens': dict(sorted(counts.items())),
            'itens': sorted(states, key=lambda x: x['id']), 'parametros_null': missing,
            'documentos_locais': inventory, 'interfaces_contextuais': contextual,
            'aprovacao_engenharia': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--exigir-parametros', action='store_true')
    args = parser.parse_args()
    result = audit(args.root)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Auditoria: {len(result['itens'])} itens; responsáveis {result['contagens']}")
        print(f"Erros estruturais: {len(result['erros'])}; parâmetros null: {len(result['parametros_null'])}")
        for msg in result['erros'] + result['avisos']:
            print(msg)
        print('Estrutura auditada; aprovação de engenharia: NÃO.')
    return 1 if result['erros'] else (2 if args.exigir_parametros and result['parametros_null'] else 0)


if __name__ == '__main__':
    raise SystemExit(main())
