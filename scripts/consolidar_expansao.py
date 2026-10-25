"""Consolida artefatos já executados e orçamento parcial; não roda simulações."""

import csv
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import yaml


def main():
    root = Path(__file__).resolve().parents[1]
    cache = Path('/home/mhc/motorhome_referencias_tarefas')
    delivery = root/'entregas/parcial_2026-10-24'
    sources = {
        'instalacoes-04': ['interior_equipado.glb', 'interior_equipado.step',
                           'cobertura_fixa.glb', 'cobertura_fixa.step', 'cobertura_recolhida.glb',
                           'cobertura_recolhida.step', 'cobertura_aberta.glb', 'cobertura_aberta.step',
                           'manifesto_instalacoes.json'],
        'visualizador-08': ['visualizador.html', 'manifesto_visualizador.json'],
        'solar-calculo-03': ['resumo_solar.json', 'solar_proposta.png'],
        'expansao-solar-02': ['resumo_expansao_solar.json', 'expansao_solar.png', 'expansao_solar.csv'],
        'layout-03': ['layout_proposto.png', 'resumo_layout.json'],
        'triagem-banho-03': ['triagem_banheiro.json'],
    }
    for folder, names in sources.items():
        for name in names:
            path = cache/folder/name
            if not path.is_file():
                raise FileNotFoundError(path)
    for folder, names in sources.items():
        for name in names:
            shutil.copy2(cache/folder/name, delivery/name)
    for name in ['exterior', 'interior', 'solar_recolhido', 'solar_aberto', 'lava_seca']:
        shutil.copy2(cache/f'visualizador-08/qa/{name}.png', delivery/f'cad_{name}.png')
    shutil.copy2(cache/'visualizador-08/qa/qa.json', delivery/'qa_visualizador.json')
    shutil.copy2(cache/'expansao-fontes/manifesto.json', delivery/'fontes_expansao_consulta.json')
    cad = json.loads((delivery/'manifesto_instalacoes.json').read_text())
    equipment = yaml.safe_load((root/'config/equipamentos_interior.yaml').read_text())
    # O OEM já contém motor/pack/rodas. Só se acrescentam conversão e ocupação.
    known = sum(item['mass_kg'] for item in equipment['items'] if item['mass_kg'] is not None)
    unknown = [item['id'] for item in equipment['items'] if item['mass_kg'] is None]
    mass = {'status': 'ORCAMENTO_PARCIAL_NAO_MASSA_MONTADA', 'oem_without_driver_kg': 2790,
            'oem_limit_kg': 4250, 'known_equipment_kg': known,
            'assumed_two_occupants_kg': 150, 'assumed_total_water_kg': 100,
            'unknown_equipment_mass': unknown,
            'other_missing': ['mobiliário/acabamentos', 'baterias de serviços/BMS/inversor/conversores',
                              'chicotes/proteções/conexões/tubulações', 'ferragens/apoios/bagagens'],
            'roof_fixed_estimate_kg': cad['fixed_roof_mass_estimate_kg'],
            'roof_stacked_estimate_kg': cad['stacked_roof_mass_estimate_kg'],
            'roof_150kg_case': {'fixed_below_limit_before_missing_parts': cad['fixed_roof_mass_estimate_kg'] < 150,
                               'stacked_below_limit_before_missing_parts': cad['stacked_roof_mass_estimate_kg'] < 150},
            'exact_oem_roof_limit_confirmed': False, 'axle_loads_verified': False,
            'vehicle_total_mass_is_complete': False}
    for state in ['fixed', 'stacked']:
        total = 2790+known+150+100+mass[f'roof_{state}_estimate_kg']
        mass[f'sum_known_and_assumed_{state}_kg'] = total
        mass[f'remaining_before_missing_parts_{state}_kg'] = 4250-total
    (delivery/'orcamento_massa_parcial.json').write_text(json.dumps(mass, ensure_ascii=False, indent=2))
    p = root/'fontes_externas/catalogo.csv'
    with p.open() as f:
        rd = csv.DictReader(f)
        fields, rows = rd.fieldnames, list(rd)
    entries = [(i['label'], i['source'], '11;13;18;24;31;32', i.get('source_note', ''))
               for i in equipment['items'] if i['source'].startswith('https://')]
    entries += [('Victron BlueSolar190W modelos atuais',
                 'https://www.victronenergy.com/upload/documents/Datasheet-BlueSolar-Monocrystalline-Panels-current-models-EN-.pdf',
                 '8;9;17;18;25;29', 'SPM041903903190W/10.5kg; não confundir com175W descontinuado.'),
                ('Fiat Ducato UK limite de teto', 'https://www.fiat.co.uk/professional/models/ducato',
                 '15;17;18', 'Até200kg/50kg por barra, dependente de configuração; não aprova variante elétricaMY25. Download local403; consulta web.'),
                ('Fiamma Roof Rail Ducato', 'https://www.fiamma.it/en/product/roof-rail-ducato/',
                 '15;17;18', 'Limite do produto150kg; montagem empilhada171kg ultrapassa esta referência.'),
                ('Victron MPPT100/20 especificações', 'https://www.victronenergy.com/media/pg/Manual_SmartSolar_MPPT_75-10_up_to_100-20/en/technical-specifications.html',
                 '9;25;29', '190W em barramento12V;290W nominalPV/100VVoc/20AIsc;98%pico não eficiência constante.')]
    downloaded = json.loads((cache/'expansao-fontes/manifesto.json').read_text())
    for title, url, items, note in entries:
        if any(r['url'] == url for r in rows):
            continue
        row = dict.fromkeys(fields, '')
        row.update(titulo=title, url=url, itens=items, tipo='especificação primária de componente',
                   licenca='Documento protegido; referência factual, sem redistribuição de CAD OEM',
                   observacoes=note, data_utc=datetime.now(timezone.utc).isoformat(),
                   verificacao='pagina_verificada', nivel_validacao='consulta_fonte_primaria')
        for source in downloaded:
            if source['url'] == url and 'sha256' in source:
                row.update(arquivo_url=url, arquivo_http='200', extensao=Path(source['name']).suffix,
                           tamanho_bytes=source['bytes'], sha256=source['sha256'],
                           caminho_cache=str(cache/'expansao-fontes'/source['name']), verificacao='arquivo_baixado_validado')
        rows.append(row)
    with p.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    provenance = {'script': 'scripts/consolidar_expansao.py', 'created_utc': datetime.now(timezone.utc).isoformat(),
                  'generator_sha256': hashlib.sha256((root/'scripts/gerar_cad_instalacoes.py').read_bytes()).hexdigest(),
                  'source_cache_folders': sources, 'source_qa': 'visualizador-08/qa',
                  'cad_policy': equipment['model_policy'], 'not_final_engineering_approval': True}
    (delivery/'proveniencia_expansao.json').write_text(json.dumps(provenance, indent=2, ensure_ascii=False))
    print(json.dumps(mass, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
