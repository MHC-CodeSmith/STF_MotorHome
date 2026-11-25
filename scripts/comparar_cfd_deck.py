"""I19-I20: arrasto com e sem o deck fixo do teto, mesma malha de fundo e mesmas condições de contorno.

Casos: familia_gci/bg_55x20x10 (casco + deck) e sem_deck_bg_55x20x10 (só casco), ambos com
blockMesh 55x20x10, refinamento 5-6 nas superfícies, rodas paradas, solo móvel a 22,22 m/s e a mesma
área de referência (casco com espelhos, 4,82784 m2). A diferença de C_d A é levada ao consumo do item 26
(mesmo modelo, rendimento 0,90 e 700 W de auxiliares) a 40 e 80 km/h e comparada com a geração do teto.
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from motorhome.cenarios import carregar_configuracao, diretorio_entregas
from motorhome.reconciliacao import consumo_plano

AERO = ROOT / "entregas/aero_equipado1540"


def main():
    os.environ.setdefault("MOTORHOME_SCENARIO", "maxeon1560_independente")
    c = carregar_configuracao(ROOT)
    p = {k: v["value"] for k, v in c["parameters"].items()}
    casos = {nome: json.loads((AERO / pasta / "resumo.json").read_text())
             for nome, pasta in (("com_deck", "familia_gci/bg_55x20x10"), ("sem_deck", "sem_deck_bg_55x20x10"))}
    for nome, r in casos.items():
        if not (r["solver_converged"] and r["mesh_ok"]):
            raise RuntimeError(f"Caso {nome} não convergiu")
    if casos["com_deck"]["block_mesh_dimensions"] != casos["sem_deck"]["block_mesh_dimensions"]:
        raise RuntimeError("Malhas de fundo diferentes")
    area = p["area_m2"]
    cd = {k: r["last_cd_diagnostic"] for k, r in casos.items()}
    massa = json.loads((diretorio_entregas(ROOT) / "integracao/layouts_massas.json").read_text())["layouts"]["A_fixa"]["nominal"]["mass_kg"]
    aux = c["parameters"]["traction_aux_assumed_w"]["value"] / 1000
    # Os modelos de energia usam Cd = 0,625 (com deck); sem deck aplica-se a mesma razão do CFD.
    cd_energia = {"com_deck": p["cd_range"][1], "sem_deck": p["cd_range"][1] * cd["sem_deck"] / cd["com_deck"]}
    velocidades = {}
    for v in (40, 80):
        linha = {}
        for k in cd:
            r = consumo_plano(v, massa, cd_energia[k], area, p["crr_range"][1], p["rho_range"][1],
                              p["eta_traction_range"][1], aux_traction_kw=aux)
            linha[k] = {"forca_aero_n": r["aerodinamica_n"], "potencia_rodas_kw": r["rodas_kw"],
                        "potencia_bateria_kw": r["bateria_kw"], "kwh_km": r["kwh_km"], "km_kwh": r["km_kwh"]}
        dk = linha["com_deck"]["kwh_km"] - linha["sem_deck"]["kwh_km"]
        linha["diferenca_kwh_km"] = dk
        linha["diferenca_percentual"] = 100 * dk / linha["sem_deck"]["kwh_km"]
        velocidades[str(v)] = linha
    teto = json.loads((diretorio_entregas(ROOT) / "solar/resumo.json").read_text())["policies"][0]["roof_kwh_day"]
    out = AERO / "comparacao_deck"
    out.mkdir(exist_ok=True)
    result = {"area_referencia_m2": area, "cd_cfd": cd, "cda_m2": {k: v * area for k, v in cd.items()},
              "delta_cda_m2": (cd["com_deck"] - cd["sem_deck"]) * area,
              "aumento_arrasto_percentual": 100 * (cd["com_deck"] / cd["sem_deck"] - 1),
              "celulas": {k: r["cell_count"] for k, r in casos.items()},
              "iteracoes_convergencia_simple": {k: r.get("last_completed_iteration") for k, r in casos.items()},
              "cd_energia": cd_energia, "massa_kg": massa, "por_velocidade_kmh": velocidades,
              "geracao_teto_kwh_dia": teto,
              "km_dia_para_empatar": {v: teto / velocidades[v]["diferenca_kwh_km"] for v in velocidades},
              "limites": ["Rodas paradas e solo móvel: a rotação das rodas não é resolvida nos dois casos.",
                          "A malha sem deck tem menos células porque o refinamento 5-6 do deck não existe; a malha do casco é a mesma.",
                          "Três malhas não estabelecem independência de malha (item 19); a diferença é entre casos com o mesmo tratamento numérico.",
                          "Massa dos módulos e suportes mantida nos dois casos; a comparação isola só o arrasto."]}
    (out / "resumo.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"cd": cd, "delta_cda": result["delta_cda_m2"], "km_empate": result["km_dia_para_empatar"]}))


if __name__ == "__main__":
    main()
