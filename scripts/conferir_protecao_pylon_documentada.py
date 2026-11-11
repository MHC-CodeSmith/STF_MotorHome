"""Distingue limite de saída declarado do módulo de curto prospectivo e fusível."""
import json
import sys
from pathlib import Path

import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from motorhome.cenarios import carregar_configuracao, diretorio_entregas


def main():
    c=carregar_configuracao(ROOT);g=c['development']['pylon_short_circuit_documented_screen'];e=c['development']['electrical_detail']
    out=diretorio_entregas(ROOT)/'protecao_pylon_documentada';out.mkdir(exist_ok=True);rows=[]
    for count in g['module_counts']:
        upper=count*g['module_short_current_upper_a']
        rows.append({'modules_parallel':count,'source_current_upper_a_if_each_module_conforms':upper,
            'stated_duration_s':g['stated_duration_s'],'rectangular_i2t_budget_over_stated_interval_only_a2s':upper**2*g['stated_duration_s'],
            'main_fuse_dc_breaking_a':e['fuse_main']['dc_breaking_a'],'current_upper_below_fuse_breaking':upper<e['fuse_main']['dc_breaking_a'],
            'waveform_and_restart_behavior_known':False,'prospective_pre_bms_fault_known':False,'fuse_total_clearing_i2t_a2s':None,'coordination_demonstrated':False})
    pd.DataFrame(rows).to_csv(out/'limites_declarados.csv',index=False)
    result={'cases':len(rows),'source':c['sources']['pylon_us_series2024'],'historical_parametric_144_faults_retained':True,
        'prospective_fault_model_replaced':False,'fuse_coordination_demonstrated':False,
        'interpretation':'Portfólio declara<2000A/1ms porUS5000. Se cada módulo respeitar esse teto,3paralelos<6000A no intervalo declarado,abaixo20kA. Não é prova de corrente prospectiva pré-limitação ou integralI²t de interrupção.',
        'open_evidence':['Revisão exata/firmware do produto instalado e condições de ensaio do fabricante.',
            'Forma de onda,tempo de reação,reinícios e falhaBMS;topologia/corrente em faltas de barramento.',
            'Curvas/I²t total doJLLN200 e coordenação de módulo/cabo/terminais no circuito real.']}
    (out/'resumo.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
