"""Reproduz a cadeia integrada,recusando alteração de configuração durante a execução."""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from motorhome.cenarios import carregar_configuracao, diretorio_entregas

STEPS=['gerar_solar_cenario','desenvolver_integracao','desenvolver_mecanica_termica','integrar_freios_massa',
       'desenvolver_protecoes_fixacoes','detalhar_rotas_cad','desenvolver_energia_sistemas','desenvolver_despacho_i25',
       'otimizar_grade_missao','detalhar_paradas_hidricas','consolidar_bom_atual','sensibilizar_cenario_integrado','comparar_buffer_comercial','simular_prioridades_servicos','comparar_bancos_servicos_cad','conferir_protecao_pylon_documentada']


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--cenario',default='maxeon1540_independente');parser.add_argument('--reexecutar',action='store_true');args=parser.parse_args()
    os.environ['MOTORHOME_SCENARIO']=args.cenario;c=carregar_configuracao(ROOT);out=diretorio_entregas(ROOT)
    if (out/'execucao_pipeline.json').exists() and not args.reexecutar:raise FileExistsError('Usar--reexecutar para cadeia já registrada')
    config=ROOT/'config/parametros_globais.yaml';initial=hashlib.sha256(config.read_bytes()).hexdigest()
    run=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');logs=out/'logs'/run;logs.mkdir(parents=True)
    report={'execution':c['_execution'],'commands':[],'complete':False,'physical_validation':False};env=os.environ.copy();env['PYTHONPATH']=str(ROOT/'src')
    for step in [*STEPS,'verificar_cenario_integrado']:
        if hashlib.sha256(config.read_bytes()).hexdigest()!=initial:raise RuntimeError('Configuração alterada durante cadeia;preservar logs e reexecutar')
        command=[sys.executable,str(ROOT/f'scripts/{step}.py')]+(['--registrar'] if step=='verificar_cenario_integrado' else [])
        with (logs/f'{step}.log').open('w') as stream:r=subprocess.run(command,cwd=ROOT,env=env,stdout=stream,stderr=subprocess.STDOUT,check=False)
        report['commands'].append({'command':command,'returncode':r.returncode,'log':str((logs/f'{step}.log').relative_to(ROOT))})
        (out/'execucao_pipeline.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
        print(json.dumps({'step':step,'returncode':r.returncode}),flush=True)
        if r.returncode:raise SystemExit(r.returncode)
    report['complete']=True;(out/'execucao_pipeline.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')


if __name__=='__main__':main()
