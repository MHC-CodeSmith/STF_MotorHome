import numpy as np
import pytest

from motorhome.protecoes import grupo_parafusos, grupo_parafusos_espacial

XY=[[-1,-1],[1,-1],[1,1],[-1,1]]
XYZ=[[*p,0] for p in XY]


def test_tracao_uniforme_e_momento_analitico():
    r=grupo_parafusos_espacial([0,0,400],[800,0,0],XYZ)
    assert [p[2] for p in r['components_n']]==pytest.approx([-100,-100,300,300])
    assert r['bolt_tension_n']==pytest.approx([0,0,300,300])
    assert r['support_compression_n']==pytest.approx([100,100,0,0])


def test_reduz_ao_grupo_plano_e_conserva_seis_componentes():
    planar=grupo_parafusos([400,20],800,XY)
    r=grupo_parafusos_espacial([400,20,0],[0,0,800],XYZ)
    assert np.array(r['components_n'])[:,:2]==pytest.approx(np.array(planar['components_n']))
    r=grupo_parafusos_espacial([400,-20,70],[35,-23,800],XYZ)
    assert np.max(np.abs(r['force_residual_n']))<1e-10
    assert np.max(np.abs(r['moment_residual_nm']))<1e-10


def test_invariancia_translacao_e_interface_degenerada():
    a=grupo_parafusos_espacial([1,2,3],[4,5,6],XYZ)
    b=grupo_parafusos_espacial([1,2,3],[4,5,6],np.array(XYZ)+[30,15,8])
    assert np.array(a['components_n'])==pytest.approx(np.array(b['components_n']))
    with pytest.raises(ValueError):grupo_parafusos_espacial([0,0,0],[0,0,0],[[0,0,0],[1,0,0],[2,0,0]])
