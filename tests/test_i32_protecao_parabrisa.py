"""O estudo da cortina do para-brisa reproduz o I32 sem proteção e fica dentro dos 2,7 kW."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_cortina_reproduz_base_e_cobre_deficit(tmp_path):
    subprocess.run([sys.executable, str(ROOT / "scripts/calcular_i32_protecao_parabrisa.py"),
                    "--destino", str(tmp_path)], check=True, capture_output=True)
    resumo = json.loads((tmp_path / "resumo.json").read_text())
    assert resumo["design_case_unshaded_w"] == pytest.approx(2867.34, abs=0.01)
    assert resumo["design_case_nominal_iac_w"] == pytest.approx(
        2867.34 - 0.5 * resumo["windshield_gain_unshaded_w"], abs=0.01)
    assert resumo["all_shaded_cases_within_capacity_claim"]
