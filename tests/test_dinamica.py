import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from motorhome.dinamica import (
    forca_aerodinamica,
    forca_rolamento,
    potencia_eletrica_tracao_w,
)


class TestModeloLongitudinal(unittest.TestCase):
    def test_drag_cresce_com_quadrado_da_velocidade(self):
        # Dados SINTÉTICOS para testar a fórmula, NÃO dados do motorhome.
        f = forca_aerodinamica(1.2, 0.4, 3.0, 10.0)
        self.assertAlmostEqual(forca_aerodinamica(1.2,0.4,3.0,20.0),4*f)
    def test_drag_zero_parado(self):
        self.assertEqual(forca_aerodinamica(1.2, 0.4, 3.0, 0.),0.)
    def test_rolamento(self):
        self.assertGreater(forca_rolamento(.01,1000),0)
    def test_eletrica_gte_rodas(self):
        self.assertGreaterEqual(potencia_eletrica_tracao_w(1000,.9),1000)
    def test_invalid_efficiency(self):
        with self.assertRaises(ValueError): potencia_eletrica_tracao_w(1000,0)
if __name__=='__main__': unittest.main()
