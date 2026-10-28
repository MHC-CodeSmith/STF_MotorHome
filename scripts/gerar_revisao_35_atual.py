"""Revisão legível dos35itens após a simulação geográfica, com fontes e lacunas."""

import argparse
import hashlib
import html
import json
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rota', required=True, type=Path)
    p.add_argument('--qa', required=True, type=Path)
    p.add_argument('--destino', required=True, type=Path)
    args = p.parse_args()
    args.destino.mkdir(parents=True, exist_ok=True)
    source = Path('docs/REVISAO_35_ITENS.md')
    route = json.loads(args.rota.read_text())
    qa = json.loads(args.qa.read_text())
    if not qa['passed']:
        raise ValueError('Revisão exige replay concluído')
    rows = []
    for line in source.read_text().splitlines():
        if not line.startswith('| ') or not line[2:4].isdigit():
            continue
        fields = [x.strip() for x in line.strip('|').split('|')]
        item, owner = fields[0].split(' / ')
        rows.append({'item': int(item), 'owner': owner, 'requirement': fields[1],
                     'evidence': fields[2], 'method': fields[3], 'missing': fields[4],
                     'status': 'em_desenvolvimento', 'human_approval_recorded': False})
    if sorted(row['item'] for row in rows) != list(range(1, 36)):
        raise ValueError('Matriz deve conter35itens únicos')
    # Atualização desta frente sem promover os componentes a parâmetros aprovados.
    for row in rows:
        if row['item'] == 8:
            row['evidence'] = 'Teto1540W e portátil1600W documentados/modelados; solar12/48V separado; geração agora calculada ao longo da rota/data.'
        elif row['item'] == 18:
            row['evidence'] = 'Subtotal conhecido com portátil3458,605kg; taraOEM inclui tração. Ainda não massa completa/eixos.'
        elif row['item'] == 29:
            row['evidence'] = f'Rota costeiraOSRM de{route["actual_route_km"]:.1f}km,21pontos,DEM5km,ERA5 em14nós; comparação60/80/90km/h e marco7000km; replay de velocidades/energia.'
            row['missing'] = 'Fechar interfaceOEM, mapas/Cd/Cr e cargas reais; melhorar despacho para dias nublados, validar paradas e obter mínimo global de tempo. Resultados condicionados.'
        elif row['item'] in [21, 22, 26]:
            row['evidence'] += ' Novo estudo integra consumo por trecho com velocidade aproximada e relevoDEM.'
    case_rows = []
    for name, result in route['cases'].items():
        milestones = result['milestones']
        distance = result['distance_km']
        case_rows.append({'case': name, 'weather': result['scenario'], 'cruise_cap_km_h': result['cruise_cap_km_h'],
                          'distance_km': distance, 'status': result['status'],
                          '7000km_elapsed_days': milestones.get('7000km', {}).get('elapsed_days'),
                          'route_elapsed_days': milestones.get('route_finish', {}).get('elapsed_days'),
                          'failure': result['failure']})
    notes = ['Os35itens possuem trabalho iniciado; nenhum tem aprovação humana final registrada.',
             'Testes e replay verificam implementação, conservação e rastreabilidade; não medem o veículo físico.',
             'Estado de carga é a fração de energia restante: I27 parte100% e termina30% da janela útil98kWh nesta hipótese.',
             'I29 parte100%, reserva10% na tração e20% nos serviços; não impõe30% ao fim da viagem.',
             'Rota aproximada por vias reaisOSM; limites por classe/perfilOSRM não substituem placas.',
             '21jun2025 é a partida histórica escolhida; calendário/local mudam a geração em cada parada.',
             'DadosERA5 são reanálise horária em14nós espaciais; céu limpo é outro cenário. Falha de política não prova inviabilidade global.',
             'Sem recargas externas; transferência48V→OBCOEM continua hipótese e requer comprovação.',
             'Faltam integração dos suplementos ao memorial final, revisão cruzada, seminário e vídeo com os integrantes.']
    report = {'date': '2026-10-28', 'items_reviewed': len(rows), 'items': rows, 'route_cases': case_rows,
              'all_35_finished': False, 'notes': notes,
              'inputs_sha256': {str(path): sha(path) for path in [source, args.rota, args.qa, Path(__file__)]}}
    (args.destino/'revisao_35_itens.json').write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n')
    md = ['# Revisão dos35itens após avanço na rota —28/10/2026', '',
          f'Rota rodoviária costeira:{route["actual_route_km"]:.1f}km. FontesOSRM/OSM, relevoCopernicus eERA5. Dados/modelos rastreados no suplemento.', '',
          '## Novos resultados de viagem', '', '| Cenário | Progresso(km) | Dia7000km | DiaChuí | Estado |', '|---|---:|---:|---:|---|']
    def number(value):
        return '—' if value is None else f'{value:.2f}'
    for case in case_rows:
        md.append(f'| {case["case"]} | {case["distance_km"]:.2f} | {number(case["7000km_elapsed_days"])} | {number(case["route_elapsed_days"])} | {case["status"]} |')
    md += ['', 'Os dias são tempo decorrido desde21/06/2025. Uma política que interrompe por reserva indica a primeira falha daquela gestão; não estabelece inviabilidade de toda arquitetura.', '',
           '## Evidências e falta concreta por item', '', '| Item | Requisito | O que já existe | O que ainda falta |', '|---|---|---|---|']
    for row in rows:
        md.append(f'| {row["item"]:02d}/{row["owner"]} | {row["requirement"]} | {row["evidence"]} | {row["missing"]} |')
    md += ['', '## Limites e fechamento da entrega', '']+['- '+note for note in notes]
    md += ['', 'Ver[estudo da rota](../../docs/ROTA_REAL_2026-10-28.md) e[matriz técnica](../../docs/REVISAO_35_ITENS.md).', '']
    (args.destino/'REVISAO_35_ITENS.md').write_text('\n'.join(md))
    table = ''.join('<tr>'+''.join('<td>'+html.escape(str(value))+'</td>' for value in [f'{r["item"]:02d}/{r["owner"]}', r['requirement'], r['evidence'], r['missing']])+'</tr>' for r in rows)
    cases_html = ''.join('<tr>'+''.join('<td>'+html.escape(str(value))+'</td>' for value in [r['case'], number(r['distance_km']), number(r['7000km_elapsed_days']), number(r['route_elapsed_days']), r['status']])+'</tr>' for r in case_rows)
    document = f'''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>AuroraSolar — revisão35itens</title>
<style>body{{font:16px/1.5 system-ui,sans-serif;margin:0;color:#173044;background:#f0f4f7}}main{{max-width:1500px;margin:auto;padding:30px}}h1{{font-size:30px}}.card{{background:white;border-radius:10px;padding:22px;margin:20px 0}}table{{border-collapse:collapse;width:100%;font-size:14px}}th,td{{text-align:left;padding:12px;border-bottom:1px solid #d5e0e8;vertical-align:top}}th{{background:#173044;color:white}}tr:nth-child(even){{background:#f1f7fa}}img{{width:100%;max-width:1200px}}.scroll{{overflow-x:auto}}@media print{{body{{background:white}}main{{padding:0}}.card{{padding:0}}th{{color:black;background:white}}}}</style>
<main><h1>AuroraSolar: progresso e revisão dos35itens</h1><p>28/10/2026 · trabalho em desenvolvimento · aprovação final pendente</p>
<section class="card"><h2>Viagem pelo litoral</h2><p>RotaOSM/OSRM:{route['actual_route_km']:.1f}km;21pontos intermediários e extremidades. Comparação entre céu limpo e reanálise históricaERA5. Reservas e até8h de condução por dia de calendário.</p>
<img src="rota_e_progresso.png" alt="Mapa da rota e curvas de progresso dos cenários"><div class="scroll"><table><thead><tr><th>Cenário</th><th>Progresso(km)</th><th>Dias até7000km</th><th>Dias atéChuí</th><th>Estado</th></tr></thead><tbody>{cases_html}</tbody></table></div></section>
<section class="card"><h2>O que já existe e o que falta</h2><p>Os35itens têm evidências parciais. A coluna de pendências descreve o fechamento de cada um; nenhum item foi promovido a aprovado.</p><div class="scroll"><table><thead><tr><th>Item/equipe</th><th>Requisito</th><th>Evidência existente</th><th>Falta concreta</th></tr></thead><tbody>{table}</tbody></table></div></section>
<section class="card"><h2>Hipóteses e próximos fechamentos</h2><ul>{''.join('<li>'+html.escape(x)+'</li>' for x in notes)}</ul><p>Fontes:©OpenStreetMap contributors/OSRM; Open-Meteo/ERA5; CopernicusDEM2021GLO90 DOI10.5270/ESA-c5d3d65. Fontes completas, scripts e hashes no repositório.</p></section></main></html>'''
    (args.destino/'revisao_35_itens.html').write_text(document)
    print(json.dumps({'items': len(rows), 'route_cases': len(case_rows), 'output': str(args.destino)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
