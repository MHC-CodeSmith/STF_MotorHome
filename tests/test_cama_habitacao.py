"""Verificações de engenharia para a cama e o perfil entregue à P5."""
import json
from pathlib import Path

import pytest
import yaml

from scripts import verificar_estrutura_cama as cama
from scripts.gerar_perfil_habitacao_p5 import gerar_perfil

ROOT = Path(__file__).resolve().parents[1]


def resultado_cama(monkeypatch, tmp_path):
    monkeypatch.setattr(cama, 'ROOT', tmp_path)
    cama.main()
    return json.loads((tmp_path/'entregas/integrado_maxeon1560/cama_estrutura/resumo.json').read_text())


def test_cama_atende_resistencia_e_flecha_sem_aprovacao_fisica(monkeypatch, tmp_path):
    r = resultado_cama(monkeypatch, tmp_path)
    assert r['aprovado'] and r['flechas_dentro_do_limite']
    assert r['casos']['D_poste_5g_lateral']['utilizacao'] < 1
    assert r['casos']['B_longarina_concentrada']['flecha_mm'] < r['casos']['B_longarina_concentrada']['limite_flecha_mm']
    assert not r['aprovacao_fisica'] and not r['ancoragem_carroceria_verificada']


def test_estrado_fino_falha_na_carga_concentrada(monkeypatch, tmp_path):
    monkeypatch.setattr(cama, 'ESTRADO', (1.95, 1.35, .018))
    r = resultado_cama(monkeypatch, tmp_path)
    assert not r['aprovado']
    assert r['casos']['B_estrado_concentrada']['utilizacao'] > 1


def test_massa_cama_substitui_reserva_sem_duplicacao(monkeypatch, tmp_path):
    r = resultado_cama(monkeypatch, tmp_path)
    m = r['massas_kg']
    volume_antigo = 1.95*1.35*.018
    esperado = m['estrado'] + m['quadro_aco'] + m['postes_aco'] - volume_antigo*550 - 12
    assert r['acrescimo_massa_kg'] == pytest.approx(esperado)
    c = yaml.safe_load((ROOT/'config/parametros_globais.yaml').read_text())
    masses = c['development']['integrated_scenarios']
    old = masses['maxeon1540_independente']['parameter_values']['assembled_typical_mass_kg']
    new = masses['maxeon1560_independente']['parameter_values']['assembled_typical_mass_kg']
    assert new-old == pytest.approx(esperado)


def test_perfil_horario_conserva_energia_e_separa_perdas():
    config = yaml.safe_load((ROOT/'config/parametros_globais.yaml').read_text())
    rows, _ = gerar_perfil(config)
    p = {k:v['value'] for k,v in config['parameters'].items()}
    expected = sum(x['energy_ac_or_dc_kwh_day']['base'] /
                   (p['eta_inverter'] if x['side']=='AC' else p['eta_lv']) for x in config['loads'])
    expected += 24*p['inverter_idle_w']/1000
    assert sum(x['potencia_retirada_banco_kw'] for x in rows) == pytest.approx(expected)
    for row in rows:
        assert row['potencia_retirada_banco_kw'] == pytest.approx(row['potencia_media_aparelho_kw']+row['perdas_conversao_kw'])
    cooktop = [x for x in rows if x['id']=='inducao' and x['potencia_retirada_banco_kw']>0]
    assert [x['hora_inicio'] for x in cooktop] == [8, 12, 19]
