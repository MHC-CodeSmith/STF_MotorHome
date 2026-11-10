import numpy as np
import pytest

from motorhome.protecoes import (
    GerenciadorCargas,
    alocar_picos,
    circuito_dc,
    falta_prospectiva,
    grupo_parafusos,
)


def test_carga_potencia_constante_conserva_e_raiz_fisica():
    r=circuito_dc(4000,48,.9,4,70,90)
    assert r['load_voltage_v']*r['current_a']==pytest.approx(4000/.9)
    assert abs(r['energy_residual_w'])<1e-9
    assert r['current_a']>4000/(48*.9)
    assert circuito_dc(1e9,48,.9,4,70,90)['status']=='sem_equilibrio_potencia_constante'


def test_paralelo_aumenta_falta_nao_confundir_com_limite_bms():
    assert falta_prospectiva(48,.03,3,.001)==pytest.approx(48/.011)
    assert falta_prospectiva(48,.03,3,0)==3*falta_prospectiva(48,.03,1,0)


def test_grupo_simetrico_estatica_e_torcao():
    xy=[[-1,-1],[1,-1],[1,1],[-1,1]]
    r=grupo_parafusos([400,0],0,xy)
    assert r['bolt_shear_n']==pytest.approx([100]*4)
    r=grupo_parafusos([0,0],800,xy)
    assert r['bolt_shear_n']==pytest.approx([100*2**.5]*4)
    assert np.max(np.abs(r['force_residual_n']))<1e-9 and abs(r['moment_residual_nm'])<1e-9


def test_gerencia_falha_travada_recuperacao_e_reset():
    m=GerenciadorCargas(30)
    assert m.step(0,10)['stage']==3
    assert m.step(0,20)['stage']==0
    assert m.step(2,1)['stage']==2
    assert m.step(0,10)['stage']==2
    assert m.step(1,20)['stage']==2  # changed request restarts hold time
    assert m.step(1,10)['stage']==1
    assert m.step(0,1,bms_allow=False)['fault_latched']
    assert m.step(0,100)['stage']==3
    assert m.step(0,30,reset=True)['stage']==0


@pytest.mark.parametrize('flag',['bms_allow','telemetry_valid','actuator_ok'])
def test_falha_sempre_supera_reset(flag):
    m=GerenciadorCargas(0)
    assert m.step(0,1,reset=True,**{flag:False})['stage']==3


def test_picos_recusam_desconhecidos_e_intertravam_grandes():
    loads=[{'id':'fridge','priority':0,'w':None,'va':None,'shed_at_stage':3},
           {'id':'boiler','priority':1,'w':500,'va':500,'large':True,'shed_at_stage':1},
           {'id':'hob','priority':2,'w':2000,'va':2200,'large':True,'shed_at_stage':1}]
    r=alocar_picos(loads,0,3700,5000)
    assert r['accepted']==['boiler']
    assert [x['reason'] for x in r['rejected']]==['pico_nao_documentado','intertravamento_grandes_cargas']
