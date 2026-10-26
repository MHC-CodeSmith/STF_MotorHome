"""BOM rastreável sem preços fictícios e comparação deCr por rótulo de outro pneu."""

import argparse
import csv
import hashlib
import json
from pathlib import Path

import yaml


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destino', type=Path, required=True)
    args = parser.parse_args()
    paths = [Path('config')/name for name in ['mecanica_comparativa_proposta.yaml', 'custos_proposta.yaml',
             'equipamentos_interior.yaml', 'instalacoes_eletricas_proposta.yaml', 'solar_portatil_proposta.yaml']]
    mechanical, costs, interior, electrical, portable = [yaml.safe_load(f.read_text()) for f in paths]
    quotes = {q['id']: q for q in costs['quotes']}
    bom = []
    all_items = [dict(i) for i in interior['items']]+[dict(i) for i in electrical['items']]
    all_items += [{'id': 'pv_portatil', 'label': portable['module']['model'], 'quantity': 4,
                   'mass_kg': portable['module']['mass_with_case_kg'], 'optional_extension': True}]
    all_items += [{'id': 'chassi_bev', 'label': 'E-DucatoMY25L3H24250kg', 'quantity': 1, 'mass_kg': 2790},
                  {'id': 'solar_fixo_ja', 'label': 'JA450', 'quantity': 3, 'mass_kg': 22},
                  {'id': 'solar_fixo_victron', 'label': 'Victron190', 'quantity': 1, 'mass_kg': 10.5}]
    for item in all_items:
        q = quotes.get(item['id'], {})
        qty = item.get('quantity', 1)
        included = item.get('mass_in_oem_curb', False)
        value = q.get('unit_price_brl')
        bom.append({'id': item['id'], 'description': item['label'], 'quantity': qty,
                    'unit_known_mass_kg': item.get('mass_kg'),
                    'oem_included_do_not_duplicate': included,
                    'optional': item.get('optional_extension', False),
                    'public_unit_reference_brl': value,
                    'public_line_reference_brl': qty*value if value is not None and not included else None,
                    'exact_variant_price_confirmed': q.get('exact_220v_price_confirmed', False),
                    'tax_breakdown_verified': q.get('tax_breakdown_verified', False),
                    'quote_url': q.get('url'), 'quote_date': costs['quote_date'] if q else None})
    tyre = mechanical['tyre_comparison']
    lo, hi = tyre['rolling_coefficient_label_interval']
    comparison = [{'cr': cr, 'mass_assumed_kg': 4250, 'rolling_force_n': cr*4250*9.80665,
                   'rolling_power_at40_w': cr*4250*9.80665*40/3.6,
                   'rolling_power_at80_w': cr*4250*9.80665*80/3.6}
                  for cr in [lo, tyre['midpoint_for_comparison'], hi]]
    args.destino.mkdir(parents=True, exist_ok=False)
    for name, rows in [('bom_parcial.csv', bom), ('rolamento_comparativo.csv', comparison)]:
        with (args.destino/name).open('w') as f:
            w = csv.DictWriter(f, list(rows[0]), lineterminator='\n'); w.writeheader(); w.writerows(rows)
    summary = {'status': costs['status'], 'bom_lines': len(bom),
               'lines_with_no_public_quote': sum(row['public_unit_reference_brl'] is None and not row['oem_included_do_not_duplicate'] for row in bom),
               'public_reference_subtotal_brl': sum(row['public_line_reference_brl'] or 0 for row in bom),
               'final_total_including_tax_shipping_brl': None,
               'missing_scopes': costs['missing_scopes'], 'rolling_comparison_not_main_tyre': comparison,
               'tyre_reference': tyre, 'lubrication': mechanical['lubrication'],
               'inputs_sha256': {str(f): hashlib.sha256(f.read_bytes()).hexdigest() for f in [*paths, Path(__file__)]}}
    (args.destino/'resumo_bom_rolamento.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps({key: value for key, value in summary.items() if key not in ['inputs_sha256','tyre_reference','lubrication']}, indent=2))


if __name__ == '__main__':
    main()
