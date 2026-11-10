import importlib.util
from itertools import pairwise
from pathlib import Path

import pytest

spec=importlib.util.spec_from_file_location('hydric',Path(__file__).parents[1]/'scripts/detalhar_paradas_hidricas.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)


def test_logistica_antes_de_uso_sem_sobrepor_intervalos():
    state={'clean_l':10.,'grey_l':65.,'black_l':15.}
    events,final=mod.agendar_eventos([False,True,True,True],[('banho',20.,0.),('pia',10.,0.)],state)
    assert [e['event'] for e in events]==['reabastecer_descartar','banho','pia']
    assert all(a['end_h']<=b['start_h'] for a,b in pairwise(events))
    assert final=={'clean_l':70.,'grey_l':30.,'black_l':0.}
    assert events[0]['refill_l']==90 and events[0]['disposal_l']==80


def test_nao_desloca_viagem_para_esconder_falta_de_parada():
    with pytest.raises(ValueError,match='insuficiente'):
        mod.agendar_eventos([False,True],[('uso',20.,0.)],{'clean_l':0.,'grey_l':0.,'black_l':0.})
