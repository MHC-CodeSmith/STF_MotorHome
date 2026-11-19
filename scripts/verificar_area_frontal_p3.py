"""Área frontal do casco e do conjunto equipado. Executar com o extra de CAD do projeto.

Da raiz: PYTHONPATH=src python scripts/verificar_area_frontal_p3.py
O cálculo de Cd reutiliza a última força adimensional da malha fina publicada.
"""
import hashlib
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AERO = ROOT / "entregas/aero_equipado1540"
GEOMETRIA = AERO / "malha_adicional_1/case/constant/triSurface"
CASO_FINO = AERO / "familia_gci/bg_55x20x10/case"
CORPO = GEOMETRIA / "aurora.stl"
DECK = GEOMETRIA / "pvdeck.stl"
CONTROLE = CASO_FINO / "system/controlDict"
FORCAS = CASO_FINO / "postProcessing/forces1/0/coefficient.dat"
SAIDA = AERO / "areas_frontais_p3.json"


def salvar_resultado(area_corpo, area_deck, area_equipada):
    with FORCAS.open(encoding="utf-8") as stream:
        for linha in stream:
            if linha.startswith("# Time"):
                if linha.lstrip("# ").split()[:2] != ["Time", "Cd"]:
                    raise ValueError("Colunas de força diferentes de Time e Cd")
                break
        else:
            raise ValueError("Cabeçalho de forças ausente")
        dados = [linha.split() for linha in stream if linha.strip() and not linha.startswith("#")]
    if not dados:
        raise ValueError("Histórico de forças vazio")
    iteracao, cd_referencia = int(dados[-1][0]), float(dados[-1][1])
    area_ref = float(re.search(r"\bAref\s+([\d.eE+\-]+)\s*;", CONTROLE.read_text())[1])
    if not math.isclose(area_ref, area_corpo, rel_tol=1e-7):
        raise ValueError("A referência do CFD difere da área do casco reparado")
    cda = cd_referencia * area_ref
    resultado = {
        "script": "scripts/verificar_area_frontal_p3.py",
        "revisao_do_calculo": "2026-11-19",
        "commit_de_origem": "5144702c6fe460329e138d985bfdb9f430d76249",
        "revisao_configuracao_do_caso": "1.1.1-execucao1540",
        "cenario": "maxeon1540_independente",
        "metodo_area": "União geométrica das projeções triangulares em YZ, observação ao longo de X",
        "superficies_com_forca": ["aurora", "pvdeck"],
        "ultima_iteracao_malha_fina": iteracao,
        "area_frontal_casco_m2": area_corpo,
        "area_frontal_deck_m2": area_deck,
        "area_frontal_equipada_m2": area_equipada,
        "area_de_referencia_openfoam_m2": area_ref,
        "cd_malha_fina_referencia_openfoam": cd_referencia,
        "cd_malha_fina_referencia_equipada": cda / area_equipada,
        "cd_vezes_area_m2": cda,
        "arquivos_de_entrada_sha256": {
            arq.relative_to(ROOT).as_posix(): hashlib.sha256(arq.read_bytes()).hexdigest()
            for arq in (CORPO, DECK, CONTROLE, FORCAS)
        },
    }
    SAIDA.write_text(json.dumps(resultado, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    import trimesh
    from motorhome.geometria_malha import area_frontal

    corpo = trimesh.load_mesh(CORPO, process=False)
    deck = trimesh.load_mesh(DECK, process=False)
    conjunto = trimesh.util.concatenate([corpo, deck])
    salvar_resultado(area_frontal(corpo), area_frontal(deck), area_frontal(conjunto))


if __name__ == "__main__":
    main()
