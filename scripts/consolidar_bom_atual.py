"""BOM canônica: valores conhecidos por moeda, sem inventar câmbio/custo instalado."""
import json
from pathlib import Path

import pandas as pd
import yaml

ROOT=Path(__file__).resolve().parents[1]


def main():
    c=yaml.safe_load((ROOT/'config/parametros_globais.yaml').read_text());p={k:v['value'] for k,v in c['parameters'].items()}
    rows=[];totals={}
    for original in c['bom_components']:
        row=original.copy()
        for field in ['model','quantity']:
            if field+'_parameter' in row:row[field]=p[row[field+'_parameter']]
        if 'mass_parameter' in row:row['unit_mass_kg']=p[row['mass_parameter']]
        if 'price_parameter' in row:row['unit_reference_price']=p[row['price_parameter']]
        value=row.get('unit_reference_price');qty=row.get('quantity')
        row['known_reference_line_total']=None if value is None or qty is None else value*qty
        src=c['sources'].get(row.get('price_source',row.get('source')),{})
        row['reference_url']=src.get('url');row['is_installed_quote']=False
        if row['known_reference_line_total'] is not None:
            currency=row['price_currency'];totals[currency]=totals.get(currency,0)+row['known_reference_line_total']
        rows.append(row)
    out=ROOT/'entregas/desenvolvimento_2026-11-09/bom_atual';out.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(rows).to_csv(out/'bom_26_linhas.csv',index=False)
    result={'rows':rows,'known_subtotals_by_currency':totals,'installed_total_brl':None,
        'unpriced_line_ids':[x['id'] for x in rows if x['known_reference_line_total'] is None],
        'notes':['USD1486 refere-se apenas inversorGX+MPPT150/60,lista fabricante2026Q2 semVAT,não cotação vigente/importada.',
                 'EUR50990veículo da mesma varianteSK;BRL439cooktop é referência histórica não confirmada,sem somar moedas.',
                 'Todosinstalled_price_brl continuamnull;frete/tributos/conversão cambial/montagem não presumidos.',
                 'MPPT3kg já incluído reserva15kg;estaBOM não substitui inventárioCAD ou soma massas duas vezes.']}
    (out/'resumo.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},ensure_ascii=False))


if __name__=='__main__':main()
