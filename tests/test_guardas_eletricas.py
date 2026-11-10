import subprocess
import sys
from pathlib import Path

import pytest

ROOT=Path(__file__).parents[1]


@pytest.mark.parametrize('script,flags',[
    ('gerar_cad_eletrico.py',['--destino']),
    ('calcular_integracao_eletrica.py',['--destino']),
    ('consolidar_eletrica.py',['--cad','--viewer','--calculo','--fontes','--interior','--solar']),
])
def test_execucao_eletrica_antiga_requer_modo_historico(tmp_path,script,flags):
    destination=tmp_path/'nao_criar'
    args=[sys.executable,str(ROOT/'scripts'/script)]
    for flag in flags:args.extend([flag,str(destination)])
    result=subprocess.run(args,cwd=ROOT,capture_output=True,text=True,check=False)
    assert result.returncode==2
    assert 'Configuração elétrica histórica' in result.stderr
    assert not destination.exists()
