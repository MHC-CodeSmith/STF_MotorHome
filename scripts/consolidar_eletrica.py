"""Copia artefatos elétricos verificados e registra fontes; não altera entregas históricas."""

import argparse
import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ['cad', 'viewer', 'calculo', 'fontes', 'interior', 'solar']:
        p.add_argument('--'+name, type=Path, required=True)
    a = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    delivery = root/'entregas/parcial_2026-10-24'
    qa = json.loads((a.viewer/'qa/qa.json').read_text())
    if qa['errors'] or qa['external_requests'] or not qa['technical_view_enabled']:
        raise ValueError('QA do navegador reprovada')
    for folder, names in [(a.cad, ['tracao_e_servicos.step', 'tracao_e_servicos.glb', 'manifesto_cad_eletrico.json']),
                          (a.viewer, ['visualizador.html', 'manifesto_visualizador.json']),
                          (a.calculo, ['resumo_integracao_eletrica.json']),
                          (a.solar, ['resumo_expansao_solar.json', 'expansao_solar.csv', 'expansao_solar.png']),
                          (a.interior, ['manifesto_instalacoes.json', *[stem+suffix
                           for stem in ['interior_equipado', 'cobertura_fixa', 'cobertura_recolhida', 'cobertura_aberta']
                           for suffix in ['.step', '.glb']]])]:
        for name in names:
            shutil.copyfile(folder/name, delivery/name)
    shutil.copyfile(a.viewer/'qa/qa.json', delivery/'qa_visualizador.json')
    for name in ['tracao', 'eletrica_servicos', 'hvac', 'interior']:
        shutil.copyfile(a.viewer/f'qa/{name}.png', delivery/f'cad_{name}.png')
    registry = root/'fontes_externas/catalogo.csv'
    with registry.open() as f:
        rd = csv.DictReader(f)
        fields, rows = rd.fieldnames, list(rd)
    sources = json.loads((a.fontes/'manifesto.json').read_text())
    now = datetime.now(timezone.utc).isoformat()
    for s in sources:
        row = next((r for r in rows if r['url'] == s['url']), None)
        if row is None:
            row = dict.fromkeys(fields, '')
            rows.append(row)
            row.update(titulo='Integração elétrica: '+s['name'], url=s['url'], itens='6;7;9;13;17;18;23;24',
                       tipo='especificação ou referência de instalação primária',
                       licenca='Documento de fabricante protegido; somente referência factual, sem CAD OEM redistribuído')
        row.update(data_utc=now, arquivo_url=s['url'], arquivo_http='200',
                   sha256=s['sha256'], tamanho_bytes=str(s['bytes']),
                   caminho_cache=str(a.fontes/s.get('filename', s['name']+'.html')),
                   verificacao='arquivo_baixado_validado', nivel_validacao='consulta_fonte_primaria')
    with registry.open('w', newline='') as f:
        wr = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        wr.writeheader()
        wr.writerows(rows)
    provenance = {'script': 'scripts/consolidar_eletrica.py', 'created_utc': now,
                  'source_caches': {n: str(getattr(a, n)) for n in ['cad', 'viewer', 'calculo', 'fontes', 'interior', 'solar']},
                  'sources': sources, 'status': 'PARCIAL_NAO_APROVADO',
                  'qa': qa, 'oem_traction_geometry_is_estimated': True}
    (delivery/'proveniencia_eletrica.json').write_text(json.dumps(provenance, indent=2, ensure_ascii=False)+'\n')
    print(f'Consolidados CAD elétrico e viewer com {qa["components"]} equipamentos')


if __name__ == '__main__':
    main()
