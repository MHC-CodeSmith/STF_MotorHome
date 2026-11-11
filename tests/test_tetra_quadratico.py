import numpy as np
import pytest

from scripts.verificar_chapas_3d import shape_gradients, strain_operator

NODES=np.array([[0,0,0],[1,0,0],[0,1,0],[0,0,1],[.5,0,0],[.5,.5,0],[0,.5,0],[0,0,.5],[0,.5,.5],[.5,0,.5]])
GRAD=np.array([[-1,1,0,0],[-1,0,1,0],[-1,0,0,1]])


@pytest.mark.parametrize('point',[[.25]*4,[.7,.1,.1,.1],[.1,.2,.3,.4]])
def test_particao_reproducao_linear_e_modos_rigidos(point):
    grad=shape_gradients(point,GRAD,2);b=strain_operator(grad)
    assert grad.sum(axis=1)==pytest.approx(np.zeros(3),abs=1e-14)
    assert NODES.T@grad.T==pytest.approx(np.eye(3),abs=1e-14)
    # All translations/rotations have zero strain; arbitrary affine
    # displacement recovers exact engineering strains at everyGauss point.
    for translation in np.eye(3):assert b@np.tile(translation,10)==pytest.approx(np.zeros(6),abs=1e-14)
    for rotation in np.eye(3):assert b@np.cross(rotation,NODES).ravel()==pytest.approx(np.zeros(6),abs=1e-14)
    displacement=NODES@np.diag([.01,.02,.03])
    assert b@displacement.ravel()==pytest.approx([.01,.02,.03,0,0,0],abs=1e-14)
