from pathlib import Path
import json,sys,time,re,subprocess,os
base=Path('/home/hipolito/stf-aero-cache')
repo=Path('/home/hipolito/stf-aero-review')
out=repo/'entregas/comparacao_carrocerias_2026-11-27'
python=base/'venv/bin/python'
coarse=base/'precision_v1_recovery'
fine=base/'precision_v2_refined_recovery'
def invoke(script,*args):
 subprocess.run([str(python),str(repo/'scripts'/script),*map(str,args)],check=True,cwd=repo)
def accepted(path):
 try:r=json.loads(path.read_text())
 except (FileNotFoundError,json.JSONDecodeError):return None
 if 'finished_unix' not in r and 'last_cd_diagnostic' not in r:return None
 return r.get('simpleFoam',{}).get('exit_code')==0 and r.get('solver_converged',False) and r.get('cd_span_last50',99)<.01
invoke('finalizar_diagnostico_cfd.py','--caso',coarse/'01_original_a_sem_paineis','--driver-log',base/'stability-diagnostic.log','--prefixo',base/'software/openfoam2412','--gpu-lib',base/'software/ogl-install/lib')
panel=coarse/'01_original_b_com_paineis/resultado_execucao.json'
started=time.monotonic()
while accepted(panel) is None:
 if time.monotonic()-started>86400:raise TimeoutError('Panel recovery not complete')
 time.sleep(30)
if not accepted(panel):raise RuntimeError('Original panel recovery did not converge; remaining production held')
history={}
for label in ['cpu','gpu']:
 s=(base/'stability_diagnostic'/label/'log.simpleFoam').read_text()
 history[label]=[float(v) for v in re.findall(r'^\s*Cd:\s+(\S+)',s,re.M)]
n=min(map(len,history.values()))
if n<500:raise RuntimeError('Long CPU/GPU reference check incomplete')
diff=max(abs(a-b)/max(abs(a),1e-12) for a,b in zip(history['cpu'][n-100:n],history['gpu'][n-100:n]))
check={'common_iterations':n,'max_relative_cd_difference_last100':diff,'passed':diff<.005,'physical_validation':False,'validated_cd':None}
(out/'recovery_backend_check.json').write_text(json.dumps(check,indent=2)+'\n')
if not check['passed']:raise RuntimeError('Long CPU/GPU backend comparison failed; production held')
invoke('executar_comparacao_carrocerias.py','--casos',coarse,'--prefixo',base/'software/openfoam2412','--gpu-lib',base/'software/ogl-install/lib','--workers',2,'--mpi',2,'--inicio',2,'--potential','--timeout-s',86400)
invoke('coletar_comparacao_carrocerias.py','--casos',coarse,'--destino',out/'v1')
for case in sorted((base/'precision_v2_refined').iterdir()):
 if not (case/'entrada_comparacao.json').exists():continue
 while not (case/'reuse_verified_mesh.json').exists():
  p=case/'resultado_malha.json'
  if p.exists() and not json.loads(p.read_text()).get('last_stage_passed',True):raise RuntimeError('Refined meshing failed: '+str(case))
  time.sleep(30)
invoke('preparar_recuperacao_cfd.py','--origem',base/'precision_v2_refined','--destino',fine)
invoke('executar_comparacao_carrocerias.py','--casos',fine,'--prefixo',base/'software/openfoam2412','--gpu-lib',base/'software/ogl-install/lib','--workers',2,'--mpi',2,'--potential','--timeout-s',86400)
invoke('coletar_comparacao_carrocerias.py','--casos',fine,'--destino',out/'v2_refined')
invoke('comparar_refinamentos_cfd.py','--inicial',out/'v1/resumo.json','--refinada',out/'v2_refined/resumo.json','--destino',out)
