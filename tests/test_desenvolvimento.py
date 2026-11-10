"""Referências independentes: flexão, momentos, balanço hídrico e empuxo."""
import numpy as np
import pytest

from motorhome.desenvolvimento import (
    caixa_intersecao,
    centro_massa,
    consumir_agua,
    vazao_chamine,
    viga_fem,
)


@pytest.mark.parametrize('n',[4,8,16,32])
def test_viga_flexao_analitica_e_reacoes(n):
    # Closed form EI*wmax=5*q*L^4/384, independently dimensioned SI.
    length,E,I,q=2.,200e9,1e-6,1000.
    r=viga_fem(length,E,I,q,n)
    assert r['max_displacement_m']==pytest.approx(5*q*length**4/(384*E*I),rel=1e-8)
    assert r['reactions_n']==pytest.approx([q*length/2,q*length/2])
    assert abs(r['force_residual_n'])<1e-5
    assert r['displacement_m'][0]==r['displacement_m'][-1]==0


def test_viga_linearidade_e_simetrias():
    a=viga_fem(1.,100e9,1e-6,1000.,8)
    b=viga_fem(1.,100e9,1e-6,2000.,8)
    assert b['max_displacement_m']==pytest.approx(2*a['max_displacement_m'])
    assert a['displacement_m']==pytest.approx(a['displacement_m'][::-1])
    assert a['rotation_rad']==pytest.approx(-np.array(a['rotation_rad'][::-1]))


def test_conservacao_agua_na_transferencia_e_evaporacao():
    r=consumir_agua({'clean_l':100,'grey_l':0,'black_l':0},30,.2,5)
    assert r==pytest.approx({'clean_l':70,'grey_l':20,'black_l':5,'residual_l':0})


@pytest.mark.parametrize('state,draw',[({'clean_l':10,'grey_l':0,'black_l':0},20),
                                    ({'clean_l':100,'grey_l':69,'black_l':0},2)])
def test_nao_inventa_agua_ou_capacidade(state,draw):
    with pytest.raises(ValueError): consumir_agua(state,draw)


def test_chamine_nula_sem_gradiente_e_simetria_das_aberturas():
    assert vazao_chamine(.1,.2,1,25,25)==0
    assert vazao_chamine(.1,.2,1,30,25)==vazao_chamine(.2,.1,1,30,25)
    # Doubling BOTH opening areas doubles Q; not sqrt(2), not wind-driven.
    assert vazao_chamine(.2,.4,1,30,25)==pytest.approx(2*vazao_chamine(.1,.2,1,30,25))


def test_massas_momentos_independentes_e_caixa_tocante():
    total,cg=centro_massa([{'mass_kg':100,'cg_m':[0,0,0]}, {'mass_kg':300,'cg_m':[4,0,2]}])
    assert total==400 and cg==[3,0,1.5]
    a={'position_m':[0,0,0],'dimensions_m':[1,1,1]}
    b={'position_m':[1,0,0],'dimensions_m':[1,1,1]}
    assert caixa_intersecao(a,b)==0
    b['position_m']=[.5,0,0]
    assert caixa_intersecao(a,b)==pytest.approx(.5)
