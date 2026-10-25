"""Verificações de interface dos equipamentos efetivamente posicionados no CAD."""

from pathlib import Path

import yaml

from motorhome.integracao_eletrica import analisar

ROOT = Path(__file__).resolve().parents[1]


def configs():
    return [yaml.safe_load((ROOT/'config'/p).read_text()) for p in
            ['instalacoes_eletricas_proposta.yaml', 'equipamentos_interior.yaml']]


def test_equipamentos_instalados_nao_sobrepoem_envelopes():
    result = analisar(*configs())
    assert result['equipment_pair_overlaps'] == []
    assert not result['full_vehicle_interference_free_verified']


def test_triagem_detecta_colisao_introduzida():
    e, i = configs()
    e['items'][7]['position_xyz_m'] = e['items'][6]['position_xyz_m'][:]
    result = analisar(e, i)
    assert any(set(c['ids']) == {'bateria_servicos_1', 'bateria_servicos_2'}
               for c in result['equipment_pair_overlaps'])


def test_massa_incremental_nao_soma_pack_oem():
    e, i = configs()
    before = analisar(e, i)['known_added_service_mass_kg']
    e['items'][0]['mass_kg'] = 700
    assert analisar(e, i)['known_added_service_mass_kg'] == before
    assert analisar(e, i)['unknown_added_mass_ids'] == ['quadro_ac_dc']


def test_banco_atende_capacidade_recomendada_inversor():
    result = analisar(*configs())
    assert result['bank_recommended_min_200ah_met']
    assert result['main_bank_energy_kwh'] == 10.24
    assert result['bank_continuous_current_a'] == 200


def test_inducao_220v_usa_potencia_da_versao_correta():
    _, i = configs()
    item = next(e for e in i['items'] if e['id'] == 'fogao')
    assert item['electrical'] == {'voltage_v': 220, 'frequency_hz': 60, 'rated_power_w': 2000}
    assert item['position_xyz_m'][2] >= .92  # portátil acima do tampo, sem embutir
