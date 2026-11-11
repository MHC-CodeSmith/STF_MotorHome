"""Cenários derivados exclusivamente do YAML canônico, com saídas isoladas.

MOTORHOME_SCENARIO seleciona uma entrada documentada; nunca interpreta caminho
arbitrário como configuração, nem promove estudo a aprovação física.
"""
import copy
import hashlib
import json
import os
import sys
from pathlib import Path

import yaml


def carregar_configuracao(root):
    root=Path(root);path=root/'config/parametros_globais.yaml'
    c=yaml.safe_load(path.read_text());name=os.environ.get('MOTORHOME_SCENARIO','base')
    if name=='base':return c
    scenarios=c['development'].get('integrated_scenarios',{})
    if name not in scenarios:raise ValueError(f'Cenário não registrado: {name}')
    spec=scenarios[name]
    for key,value in spec.get('parameter_values',{}).items():
        if key not in c['parameters']:raise ValueError(f'Parâmetro desconhecido: {key}')
        c['parameters'][key].update(value=copy.deepcopy(value),status='provisorio_cenario',version=spec.get('version',c['revision']),reference_date=spec.get('reference_date',c['updated']),source=spec.get('parameter_sources',{}).get(key,spec['source']),note=f'Cenário {name};{spec["note"]}')
    for entry in c['development']['mass_allowances']:
        if entry['id'] in spec.get('allowance_overrides',{}):entry.update(spec['allowance_overrides'][entry['id']])
    c['development']['selected_roof_inventory']=spec['roof_inventory']
    remove=spec.get('bom_remove_ids',[])
    c['bom_components']=[x for x in c['bom_components'] if x['id'] not in remove]+copy.deepcopy(spec.get('bom_add',[]))
    output=(root/spec['output_directory']).resolve()
    if not output.is_relative_to((root/'entregas').resolve()):raise ValueError('Saída fora das entregas')
    c['_execution']={'scenario':name,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'output_directory':spec['output_directory'],'physical_validation':False,'note':spec['note']}
    resolved=json.dumps(c,sort_keys=True,ensure_ascii=False,allow_nan=False).encode()
    c['_execution']['resolved_sha256']=hashlib.sha256(resolved).hexdigest()
    output.mkdir(parents=True,exist_ok=True)
    text=json.dumps(c,indent=2,ensure_ascii=False)+'\n'
    (output/'parametros_resolvidos.json').write_text(text)
    archive=output/'configuracoes_executadas';archive.mkdir(exist_ok=True)
    (archive/(c['_execution']['resolved_sha256']+'.json')).write_text(text)
    executions=output/'entradas_por_executor';executions.mkdir(exist_ok=True)
    (executions/(Path(sys.argv[0]).stem+'.json')).write_text(json.dumps(c['_execution'],indent=2,ensure_ascii=False)+'\n')
    return c


def diretorio_entregas(root):
    c=carregar_configuracao(root)
    return Path(root)/(c.get('_execution',{}).get('output_directory','entregas/desenvolvimento_2026-11-09'))
