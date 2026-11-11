"""FW3000: alimentação documentada por revisão, capacidade/solar/partidas separados."""
import itertools
import json
from pathlib import Path

import pandas as pd
import yaml

ROOT=Path(__file__).resolve().parents[1]


def main():
    c=yaml.safe_load((ROOT/'config/parametros_globais.yaml').read_text());g=c['development']['hvac_revision_study']
    p={k:v['value'] for k,v in c['parameters'].items()}
    out=ROOT/'entregas/desenvolvimento_2026-11-09/hvac_revisao';out.mkdir(parents=True,exist_ok=True)
    thermal=json.loads((ROOT/'entregas/etapa_pos_dec061/cabine_31_32_reexecutada.json').read_text())
    rows=[]
    for case,solar_factor,conduction_factor,capacity_factor in itertools.product(thermal['i32'],g['solar_gain_factor_sweep'],g['envelope_conduction_factor_sweep'],g['capacity_fraction_sweep']):
        # Existing I32 sum includes prescribed33/25°C and one occupant main.
        demand=case['cooling_required_w']+case['solar_w']*(solar_factor-1)+case['conduction_w']*(conduction_factor-1)
        capacity=g['nameplate_cooling_w']*capacity_factor
        rows.append({'occupants':case['occupants'],'solar_factor':solar_factor,'conduction_factor':conduction_factor,
            'capacity_fraction_assumed':capacity_factor,'cooling_required_w':demand,'cooling_available_assumed_w':capacity,
            'margin_w':capacity-demand,'passes_hypothetical_capacity':capacity>=demand,'oem_capacity_curve_validated':False})
    pd.DataFrame(rows).to_csv(out/'capacidade_72casos.csv',index=False)
    demands={int(case['occupants']):float(case['cooling_required_w']) for case in thermal['i32']}
    specs=[
        {'device':'FreshWell FW3000, manual 2018','capacity_claim_w':2700.0,'claim':'manual nominal; ISO 5151 per manual','source':'https://www.jacksonsleisure.com/content/pdf/dometic/dometic-freshwell-3000-manual.pdf'},
        {'device':'FreshWell FW3000 SKU 9105306675, official page headline','capacity_claim_w':2700.0,'claim':'headline 2700 W / 9200 BTU/h; conflicts with structured field','source':'https://www.dometic.com/en/product/dometic-freshwell-3000-9105306675'},
        {'device':'FreshWell FW3000 SKU 9105306675, official page ISO5151 field','capacity_claim_w':1758.0,'claim':'structured field 1758; adjacent display 5998.54 BTU/h; unit interpretation follows BTU/h conversion','source':'https://www.dometic.com/en/product/dometic-freshwell-3000-9105306675'},
        {'device':'FreshJet FJX7 3000 SKU 9600050994, comparator only','capacity_claim_w':3000.0,'claim':'official ISO 5151 capacity; rooftop package','source':'https://www.dometic.com/en/product/dometic-freshjet-fjx7-3000-75'},
    ]
    capacity_comparison=[]
    for occupants,demand in sorted(demands.items()):
        for spec in specs:
            capacity_comparison.append({
                'occupants':occupants,'cooling_demand_w_modelled':demand,**spec,
                'nominal_margin_w':spec['capacity_claim_w']-demand,
                'nominal_margin_fraction_of_demand':(spec['capacity_claim_w']-demand)/demand,
                'capacity_at_33c_outside_25c_inside_demonstrated':False,
                'physical_installation_demonstrated':False,
            })
    pd.DataFrame(capacity_comparison).to_csv(out/'comparacao_capacidade_documentada.csv',index=False)
    electrical=[]
    for pf,multiplier in itertools.product(g['electrical_pf_sweep'],g['starting_current_multiplier_sweep']):
        current=g['nominal_cooling_a_at_50_60hz'][1]*multiplier;apparent=p['ac_voltage_v']*current
        electrical.append({'power_factor_assumed':pf,'current_multiplier_assumed':multiplier,'current_a_assumed':current,
            'apparent_va_assumed':apparent,'active_w_assumed':apparent*pf,
            'within_inverter_continuous_w_va':apparent<=5000 and apparent*pf<=min(p['inverter_continuous_w']),
            'measured_start_current':False,'transient_compatibility_demonstrated':False})
    pd.DataFrame(electrical).to_csv(out/'potencia_partida_sensibilidade.csv',index=False)
    result={'thermal_cases':len(rows),'electrical_cases':len(electrical),
        'rated_ac_compatibility_for_document_revision':True,'actual_purchased_variant_confirmed':False,
        'source':c['sources']['freshwell_manual_2018'],'capacity_at_33outside_25inside_demonstrated':False,
        'base_1_2_occupants_required_w':[x['cooling_required_w'] for x in thermal['i32']],
        'base_1_2_occupants_nominal_margin_w':[g['nameplate_cooling_w']-x['cooling_required_w'] for x in thermal['i32']],
        'nominal_va_at220v60hz':p['ac_voltage_v']*g['nominal_cooling_a_at_50_60hz'][1],
        'manufacturer_capacity_comparison':capacity_comparison,
        'freshwell_document_conflict':{
            'sku':'9105306675','model':'FW3000','official_product_url':'https://www.dometic.com/en/product/dometic-freshwell-3000-9105306675',
            'page_headline_capacity_w':2700,'page_structured_iso5151_value':1758,'page_structured_companion_value':5998.54,
            'companion_value_unit_interpreted':'BTU/h','interpretation':'conflict unresolved; do not select one rating as verified performance',
            'accessed':'2026-11-11',
        },
        'freshjet_fjx7_comparator':{
            'sku':'9600050994','model':'FJX7337IHP','official_product_url':'https://www.dometic.com/en/product/dometic-freshjet-fjx7-3000-75',
            'cooling_capacity_iso5151_w':3000,'voltage_v':[220,240],'frequency_hz':[50,60],
            'max_cooling_current_a':6.77,'max_ac_protection_a':8,'mass_kg':36.8,
            'mass_delta_vs_freshwell_kg':36.8-21,
            'footprint_m2':1.09*0.70,'roof_panel_estimated_area_m2':4.294*1.690,
            'gross_unoccupied_area_in_roof_rectangle_m2':4.30*1.82-4.294*1.690,
            'status':'comparador; rooftop area conflicts with estimated roof PV envelope; mounting and capacity at design condition unverified',
            'accessed':'2026-11-11',
        },
        'fuse_conflict_open':g['fuse_in_manual_a']<g['nominal_cooling_a_at_50_60hz'][1],
        'daily_hvac_kwh_still_assumed':next(x['energy_ac_or_dc_kwh_day']['base'] for x in c['loads'] if x['id']=='ar_condicionado'),
        'larger_comparison':'WebastoCoolTopTrail35jácomparado/rejeitado50Hzteto;ColemanUB11/UB15primário115Vnãoaceito220Vsemadaptação/curva/layout. Não inferirBTUpelonome.',
        'notes':['Manual2018 foi renderizado/página29conferida;domíniofabricante76MBexcedeferramentaweb/download403. Espelho8MBhashado.',
            'FonteSKU9105306675nawebindica230V60HzmascapacidadeHTML1758/2700conflita;dados não misturados com manual2018.',
            '6.2A é corrente nominal da revisão, não corrente de partida nem potência ativa.',
            'Reserva de3kWh/diaDEC046 permanece hipótese independente;nenhuma curvaCOPoupartida inventada.']}
    (out/'resumo.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source'},ensure_ascii=False))


if __name__=='__main__':main()
