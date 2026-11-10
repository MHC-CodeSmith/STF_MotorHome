"""BOM canônica: valores conhecidos por moeda, sem inventar câmbio/custo instalado."""
import json
import sys
from pathlib import Path

import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from motorhome.cenarios import carregar_configuracao, diretorio_entregas


def main():
    c=carregar_configuracao(ROOT);p={k:v['value'] for k,v in c['parameters'].items()}
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
    out=diretorio_entregas(ROOT)/'bom_atual';out.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(rows).to_csv(out/('bom_componentes.csv' if '_execution' in c else 'bom_26_linhas.csv'),index=False)
    result={'rows':rows,'known_subtotals_by_currency':totals,'installed_total_brl':None,
        'unpriced_line_ids':[x['id'] for x in rows if x['known_reference_line_total'] is None],
        'notes':['USD1486 refere-se apenas inversorGX+MPPT150/60,lista fabricante2026Q2 semVAT,não cotação vigente/importada.',
                 'EUR50990veículo da mesma varianteSK;BRL439cooktop é referência histórica não confirmada,sem somar moedas.',
                 'Todosinstalled_price_brl continuamnull;frete/tributos/conversão cambial/montagem não presumidos.',
                 'MassasMPPT já incluídas nas reservas;250/60 adicional465USD se presente no cenário,sem impostos/frete. SubtotalUSD varia por cenário.']}
    (out/'resumo.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},ensure_ascii=False))


if __name__=='__main__':main()
