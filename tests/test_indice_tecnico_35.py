import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def test_35_itens_ligam_metodos_a_evidencia_real_sem_aprovacao():
    index=json.loads((ROOT/'entregas/indice_execucao_35.json').read_text())
    assert {x['item'] for x in index['items']}==set(range(1,36))
    assert index['human_approvals']==0 and not index['physical_validation']
    for row in index['items']:
        item=json.loads((ROOT/row['path']).read_text());evidence=ROOT/item['evidence']
        assert hashlib.sha256(evidence.read_bytes()).hexdigest()==row['evidence_sha256']==item['evidence_sha256']
        assert item['owner']==row['owner'] and item['requirement'] and item['model_equations'] and item['remaining_limit']
        assert not item['human_approval'] and not item['physical_validation']
        theory=(ROOT/row['path']).parents[1]/'teoria.md'
        assert 'A preencher com equações' not in theory.read_text()


def test_parametros_locais_sao_derivados_da_fonte_unica_com_unidades():
    index=json.loads((ROOT/'entregas/indice_execucao_35.json').read_text())
    for row in index['items']:
        folder=(ROOT/row['path']).parents[1]
        data=json.loads((folder/'dados/parametros_execucao_integrada.json').read_text())
        source=ROOT/data['derived_snapshot']
        assert hashlib.sha256(source.read_bytes()).hexdigest()==data['snapshot_sha256']
        assert data['values'] and not data['editable_source'] and data['canonical_source']=='config/parametros_globais.yaml'
        resolved=json.loads(source.read_text())
        for key,value in data['values'].items():
            assert value==resolved['parameters'][key]
            assert all(x in value for x in ['unit','source','status','confidence','version','owner'])
