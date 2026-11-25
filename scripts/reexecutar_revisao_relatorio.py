"""Reproduz a revisão de massa/cama e as saídas usadas no relatório (cenário1560).

Usar --executar conscientemente: a grade densa e o fechamento da viagem levam
vários minutos. Não roda CFD nem comanda equipamentos. Registra cada comando,
seu código de saída e o SHA da configuração; interrompe se a entrada mudar.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEPS = [
    ('verificar_estrutura_cama',), ('gerar_solar_cenario',), ('desenvolver_integracao',),
    ('desenvolver_mecanica_termica',), ('sensibilizar_raio_i28',), ('integrar_freios_massa',),
    ('desenvolver_protecoes_fixacoes',), ('detalhar_rotas_cad',), ('desenvolver_energia_sistemas',),
    ('desenvolver_despacho_i25',), ('otimizar_grade_missao',), ('detalhar_paradas_hidricas',),
    ('consolidar_bom_atual',), ('sensibilizar_cenario_integrado',), ('comparar_buffer_comercial',),
    ('simular_prioridades_servicos',), ('comparar_bancos_servicos_cad',),
    ('conferir_protecao_pylon_documentada',), ('sensibilizar_resistencias_rota',),
    ('sensibilizar_ventilacao_mecanica',), ('modelar_envelope_subida_condicional',),
    ('calcular_envelope_frenagem_eixos',), ('resumir_envelope_eixos',),
    ('calcular_limite_aderencia_dianteira',), ('otimizar_janela_missao',),
    ('otimizar_janela_missao', '--densa'), ('otimizar_janela_missao', '--refino-extra'),
    ('refinar_velocidade_missao',), ('refinar_resolucao_missao',), ('analisar_aliasing_limiar_dc',),
    ('fechar_i29_velocidade', '--workers', '2'), ('fechar_i29_velocidade', '--figura'),
    ('calcular_custo_brl_i24',), ('comparar_cfd_deck',), ('analisar_geracao_portateis_p5',),
    ('fechar_i30_corrente_maxima',), ('calcular_i32_protecao_parabrisa',),
    ('gerar_perfil_habitacao_p5',),
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--executar', action='store_true')
    args = parser.parse_args()
    if not args.executar:
        for step in STEPS:
            print(' '.join([sys.executable, f'scripts/{step[0]}.py', *step[1:]]))
        return
    cfg = ROOT/'config/parametros_globais.yaml'
    initial = digest(cfg)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out = ROOT/'entregas/integrado_maxeon1560/revisao_relatorio'
    logs = out/'logs'/stamp;logs.mkdir(parents=True)
    env = os.environ | {'PYTHONPATH': 'src:scripts', 'MOTORHOME_SCENARIO': 'maxeon1560_independente',
                        'OMP_NUM_THREADS': '2', 'OPENBLAS_NUM_THREADS': '2', 'MKL_NUM_THREADS': '2'}
    receipt = {'script': 'scripts/reexecutar_revisao_relatorio.py', 'config_sha256': initial,
               'scenario': 'maxeon1560_independente', 'started_utc': stamp,
               'commands': [], 'complete': False, 'physical_validation': False}
    for i, step in enumerate(STEPS):
        if digest(cfg) != initial:
            raise RuntimeError('A configuração mudou durante a execução; preservar logs e reiniciar.')
        command = [sys.executable, f'scripts/{step[0]}.py', *step[1:]]
        log = logs/f'{i:02}_{step[0]}.log'
        start = time.monotonic()
        with log.open('w') as f:
            result = subprocess.run(command, cwd=ROOT, env=env, stdout=f, stderr=subprocess.STDOUT, check=False)
        receipt['commands'].append({'command': command, 'returncode': result.returncode,
                                    'seconds': time.monotonic()-start,
                                    'log': str(log.relative_to(ROOT)), 'log_sha256': digest(log)})
        (out/'execucao.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n')
        print(json.dumps({'step': step, 'returncode': result.returncode}), flush=True)
        if result.returncode:
            raise SystemExit(result.returncode)
    receipt['complete'] = True
    (out/'execucao.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    main()
