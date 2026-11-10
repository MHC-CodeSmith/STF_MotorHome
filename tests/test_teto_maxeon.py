import numpy as np
import pytest

from scripts.comparar_teto_maxeon import series_iv


def test_serie_identica_conserva_corrente_e_soma_tensao():
    model={'vmp_v':60.,'imp_a':6.,'voc_v':75.,'isc_a':7.}
    g={'alpha_isc_per_k':.00058,'beta_voc_per_k':-.00236,'beta_vmp_assumed_per_k':-.004}
    v=np.array([0.,120.,150.,160.])
    assert series_iv(v,[model,model],25,1,g)==pytest.approx([7,6,0,0])
    assert series_iv(np.array([120]),[model,model],25,.5,g)[0]==pytest.approx(3)


def test_tolerancia_termica_nao_e_curva_de_fabricante():
    model={'vmp_v':60.,'imp_a':6.,'voc_v':75.,'isc_a':7.}
    g={'alpha_isc_per_k':0.,'beta_voc_per_k':-.00236,'beta_vmp_assumed_per_k':-.004}
    v=np.linspace(0,180,20001)
    cold=series_iv(v,[model,model],-20,1,g)
    hot=series_iv(v,[model,model],85,1,g)
    assert v[cold>0].max()>150
    assert v[hot>0].max()<150
    assert np.max(v*hot)<np.max(v*cold)
