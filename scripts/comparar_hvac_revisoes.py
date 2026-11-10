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
