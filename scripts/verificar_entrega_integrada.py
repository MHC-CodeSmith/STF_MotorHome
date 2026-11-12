"""Auditoria35itens: integridade, proveniência e interfaces; não aprova engenharia."""

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from auditar_projeto import audit


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--destino', type=Path, default=Path('output/verificacao_integrada_35.json'))
    args = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    delivery = root/'entregas/parcial_2026-10-24'
    structural = audit(root)
    errors = list(structural['erros'])
    manifest = json.loads((delivery/'manifesto_entrega.json').read_text())
    for name, expected in manifest['artefatos'].items():
        path = delivery/name
        if not path.is_file() or sha(path) != expected:
            errors.append(f'Hash entrega divergente: {name}')
    pdf = manifest['memorial']
    if sha(root/pdf['path_relative_to_repo']) != pdf['sha256']:
        errors.append('Hash do memorial divergente')
    # This delivery is an immutable 2026-10-24 snapshot. Its input hashes are
    # expected to diverge from today's evolving sources; current outputs are
    # covered by the integrated/development manifests, not retrofitted here.
    fresh = set()
    for missing in sorted(fresh-{path.name for path in delivery.glob('*.json')}):
        errors.append(f'Resultado atual ausente: {missing}')
    provenance = []
    for path in sorted(delivery.glob('*.json')):
        r = json.loads(path.read_text())
        if not isinstance(r, dict):
            provenance.append({'file': path.name, 'status': 'lista_sem_mapa_inputs_sha256', 'changed_inputs': []})
            continue
        inputs = r.get('inputs_sha256', {})
        changed = []
        for name, expected in inputs.items():
            source = Path(name)
            if not source.is_absolute():
                source = root/source
            if not source.is_file() or sha(source) != expected:
                changed.append(name)
        status = 'entradas_conferidas' if inputs and not changed else ('historico_ou_desatualizado' if changed else 'sem_mapa_inputs_sha256')
        provenance.append({'file': path.name, 'status': status, 'changed_inputs': changed})
        if path.name in fresh and (changed or not inputs):
            errors.append(f'Proveniência atual divergente: {path.name}: {changed}')
    def read(name):
        return json.loads((delivery/name).read_text())
    battery = read('resumo_bateria_carga.json')
    for case in battery['nominal']:
        if abs(case['thermal_residual_j']) > .1 or abs(case['electrical_residual_j']) > .1:
            errors.append('Balanço de bateria falhou')
        if case['stop'] != 'target_soc' or abs(case['final_soc']-.8) > 1e-7:
            errors.append('Protocolo nominal da bateria não atingiuSOC alvo')
    hydraulics = read('resumo_hidraulica.json')['operating_point']
    if abs(hydraulics['pressure_residual_pa']) > .01 or not 0 < hydraulics['pump_electrohydraulic_efficiency'] <= 1:
        errors.append('Ponto hidráulico inconsistente')
    portable = read('resumo_solar_portatil.json')
    if portable['equipment_clashes_aabb'] or portable['cold_voc_design_v'] >= 150 or portable['input_isc_stc_a'] >= 40:
        errors.append('Triagem de solar portátil falhou')
    viewer = read('qa_visualizador.json')
    if viewer.get('errors') or viewer.get('external_requests') or viewer.get('portable_meshes') != 324:
        errors.append('QA visualizador divergente ou não atualizada')
    with (root/'metadata/itens.csv').open() as f:
        rows = sorted(csv.DictReader(f), key=lambda row: int(row['numero']))
    final_gaps = []
    for row in rows:
        item = root/row['pasta']
        for required in ['README.md', 'teoria.md', 'fontes.md', 'validacao.md']:
            if not (item/required).is_file():
                errors.append(f'I{int(row["numero"]):02}: ausente{required}')
        final_gaps.append({'item': int(row['numero']), 'owner': row['pessoa'], 'title': row['titulo'],
                           'status': row['status'], 'folder': row['pasta'],
                           'human_review_pending': 'PENDENTE' in (item/'validacao.md').read_text()})
    out = {'status': 'AUDITORIA_TECNICA_PARCIAL_NAO_APROVACAO_FISICA',
           'delivery_snapshot_date': '2026-10-24',
           'active_validation': 'scripts/verificar_cenario_integrado.py and scripts/verificar_desenvolvimento.py',
           'generated_utc': datetime.now(timezone.utc).isoformat(), 'errors': errors,
           'items_checked': len(rows), 'delivery_hashes_checked': len(manifest['artefatos']),
           'provenance': provenance, 'items': final_gaps,
           'all_35_finished': False,
           'final_blockers': ['Dados físicos e revisões humanas pendentes descritos na matriz docs/REVISAO_35_ITENS.md.',
                              'CFD sem independência de malha; mapas motor/R(SOC,T)/UA/curvas de perdas reais ausentes.',
                              'Massa/eixos/fixação/custos emR$ não fechados; transmissão numérica/lubrificante/rolamento ainda sem dados.',
                              'MissõesI27/I29 ainda sem agenda atual integrada à alternativa portátil e interfaceHV demonstrada.',
                              'Relatório é parcial; seminário/vídeo com integrantes não produzidos.'],
           'warning': 'Zero erros nesta auditoria significa integridade dos controles implementados, não validação física de todos os cálculos.'}
    args.destino.parent.mkdir(parents=True, exist_ok=True)
    args.destino.write_text(json.dumps(out, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps({'items_checked': len(rows), 'errors': errors, 'all_35_finished': False,
                      'historical_or_changed_provenance': [r['file'] for r in provenance if r['changed_inputs']]}, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
