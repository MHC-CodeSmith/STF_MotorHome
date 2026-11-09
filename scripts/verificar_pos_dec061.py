"""QA da execução reconciliada; não aprova nem certifica os35itens."""
import csv
import hashlib
import json
from pathlib import Path

import yaml

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'entregas/etapa_pos_dec061'


def main():
    errors=[]
    cfg=yaml.safe_load((ROOT/'config/parametros_globais.yaml').read_text())
    manifest=json.loads((OUT/'manifesto.json').read_text())
    def check(condition,message):
        if not condition:
            errors.append(message)
    for name,expected in manifest['inputs_sha256'].items():
        path=ROOT/name
        check(path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==expected,f'Entrada alterada:{name}')
    for name,expected in manifest['outputs_sha256'].items():
        path=OUT/name
        check(path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==expected,f'Saída alterada:{name}')
    supplement=json.loads((OUT/'manifesto_pacote.json').read_text())
    check(supplement['canonical_sha256']==hashlib.sha256((ROOT/'config/parametros_globais.yaml').read_bytes()).hexdigest(),
          'BOM/documentos com fonte canônica desatualizada')
    check(supplement['generator_sha256']==hashlib.sha256((ROOT/supplement['generator']).read_bytes()).hexdigest(),
          'Gerador da consolidação alterado')
    check(supplement['inputs_numerical_manifest_sha256']==hashlib.sha256((OUT/'manifesto.json').read_bytes()).hexdigest(),
          'Reexecute a consolidação após a execução numérica')
    for name,expected in supplement['files_sha256'].items():
        check(hashlib.sha256((OUT/name).read_bytes()).hexdigest()==expected,'BOM alterada:'+name)
    for name,expected in supplement['documents_sha256'].items():
        check(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,'Documento alterado:'+name)
    decisions=json.loads((OUT/'matriz_decisoes_61.json').read_text())
    check([x['decision'] for x in decisions]==[f'DEC-{n:03}' for n in range(1,62)],'Cobertura61decisões')
    for x in decisions:
        check(bool(x['parameter_keys']) and all(k in cfg['parameters'] for k in x['parameter_keys']),x['decision']+' parâmetros')
        check((ROOT/x['evidence']).is_file(),x['decision']+' evidência ausente')
    for key,record in cfg['parameters'].items():
        check(all(name in record for name in ['unit','source','owner','status','confidence','version','reference_date']),key+' metadados')
        check(record['source'] in cfg['sources'],key+' fonte desconhecida')
    items=json.loads((OUT/'matriz_itens_35.json').read_text())
    check(sorted(x['item'] for x in items['items'])==list(range(1,36)),'Cobertura35itens')
    check(items['final_human_approved']==0 and not any(x['human_approval_recorded'] for x in items['items']),'Aprovação humana indevida')
    missions=json.loads((OUT/'missoes_7000km.json').read_text())
    for m in missions:
        check(abs(m['energy_residual_kwh'])<1e-6,m['case']+' balanço')
        check(m['max_driving_h_day']<=8+1e-8,m['case']+' direção')
        check(m['external_electric_energy_kwh']==0,m['case']+' carga externa')
        check(m['soc_initial_service']==1 and m['soc_initial_traction']==1,m['case']+' SOC inicial')
        check(m['soc_final_service']>=m['reserve_service']-1e-8,m['case']+' reserva serviços')
        check(m['soc_final_traction']>=m['reserve_traction']-1e-8,m['case']+' reserva tração')
        check(not m['physical_mission_demonstrated'],m['case']+' viabilidade física indevida')
        if m['mode']=='sem_interface':
            check(m['totals']['traction_solar_kwh']==0,m['case']+' créditoHV indevido')
        if m['status']=='chegada_condicional':
            check(abs(m['distance_km']-7000)<1e-6,m['case']+' distância principal')
    for name,key,tolerance in [('dc_direta_vs_buffer_hipoteses.csv','residual_kwh',1e-9),
            ('cabos_servicos_convergencia.csv','residual_w_m',1e-6),
            ('freios_2d_atrito_regeneracao.csv','thermal_residual_j',1e-4),
            ('freios_2d_atrito_regeneracao.csv','mechanical_residual_j',1e-4),
            ('hidraulica_potavel_trecho_critico.csv','pressure_residual_pa',1e-4)]:
        with (OUT/name).open() as f:
            for row in csv.DictReader(f):
                check(abs(float(row[key]))<tolerance,name+' '+key)
    for name in ['solar_fixo_08_16.csv','solar_alternativo_00_08.csv']:
        with (OUT/name).open() as f:
            for row in csv.DictReader(f):
                check(row['planned_driving']!='True' or float(row['portable_kw'])==0,name+' portátil em movimento')
    result={'status':'PASSOU' if not errors else 'FALHOU','errors':errors,'decisions':len(decisions),
            'items':len(items['items']),'mission_cases':len(missions),
            'input_hashes_checked':len(manifest['inputs_sha256']),
            'output_hashes_checked':len(manifest['outputs_sha256']),
            'supplemental_files_checked':len(supplement['files_sha256'])+len(supplement['documents_sha256']),
            'engineering_approval':False,'physical_dc_demonstrated':False}
    path=ROOT/'output/qa_pos_dec061.json'
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 1 if errors else 0


if __name__=='__main__':
    raise SystemExit(main())
