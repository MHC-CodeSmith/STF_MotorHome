import json
from pathlib import Path

import pytest
import yaml

from motorhome.cenarios import carregar_configuracao, diretorio_entregas

ROOT=Path(__file__).resolve().parents[1]


def test_base_nao_alterado(monkeypatch):
    monkeypatch.delenv('MOTORHOME_SCENARIO',raising=False)
    c=carregar_configuracao(ROOT)
    assert c['parameters']['roof_power_48v_study_wp']['value']==1350
    assert '_execution' not in c


def test_cenario_isolado_e_resolvido(tmp_path,monkeypatch):
    (tmp_path/'config').mkdir()
    original=(ROOT/'config/parametros_globais.yaml').read_text()
    (tmp_path/'config/parametros_globais.yaml').write_text(original)
    monkeypatch.setenv('MOTORHOME_SCENARIO','maxeon1540_independente')
    c=carregar_configuracao(tmp_path);p=c['parameters']
    assert p['roof_power_48v_study_wp']['value']==1540
    assert p['assembled_typical_mass_kg']['source']=='hyp'
    assert p['ac_voltage_v']['value']==220 and p['ac_frequency_hz']['value']==60
    assert not p['stored_transfer_allowed']['value'] and not p['dc_interface_demonstrated']['value']
    assert sum(x['mass_kg'] for x in c['development']['selected_roof_inventory'])==76
    assert not any(x['id'] in ['pv_teto','pv_cabine'] for x in c['bom_components'])
    snap=json.loads((diretorio_entregas(tmp_path)/'parametros_resolvidos.json').read_text())
    assert snap['_execution']['scenario']=='maxeon1540_independente'
    assert (tmp_path/'config/parametros_globais.yaml').read_text()==original


def test_nome_e_saida_nao_registrados_recusados(tmp_path,monkeypatch):
    (tmp_path/'config').mkdir();c=yaml.safe_load((ROOT/'config/parametros_globais.yaml').read_text())
    c['development']['integrated_scenarios']['maxeon1540_independente']['output_directory']='../invasao'
    (tmp_path/'config/parametros_globais.yaml').write_text(yaml.safe_dump(c))
    monkeypatch.setenv('MOTORHOME_SCENARIO','../../fora')
    with pytest.raises(ValueError):carregar_configuracao(tmp_path)
    monkeypatch.setenv('MOTORHOME_SCENARIO','maxeon1540_independente')
    with pytest.raises(ValueError):carregar_configuracao(tmp_path)
