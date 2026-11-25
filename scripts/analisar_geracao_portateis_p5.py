"""I08 (revisão P5): geração horária por caso, candidatos de painel portátil e inclinação do teto.

Mesmo dia, clima e modelo do cenário vigente (pvlib + Faiman, 10 % de perdas) para isolar o efeito do
horário. Casos: só teto; parado o dia todo com os portáteis montados antes do amanhecer; condução
diurna 08-16 h; condução no fim da tarde/noite 18-02 h (horário do item 29). Portáteis só geram parados,
com 0,5 h de montagem depois da parada e 0,5 h de recolhimento antes da partida.

Os candidatos de portátil são comparados por ficha: kWh por parada (mesma inclinação ótima fixa),
massa, dimensões, envelope de guarda sob a cama (bolsas atuais: 1,10 x 0,26 x 0,98 m livres em x, y, z),
compatibilidade com o SmartSolar 150/60 em 2S2P e preço de referência. Nenhum candidato foi ensaiado.
"""
import copy
import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pvlib
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from motorhome.cenarios import carregar_configuracao, diretorio_entregas
from motorhome.solar import simular_dia

# Fichas consultadas em 25/11/2026. gamma None usa o coeficiente do portátil do cenário.
CANDIDATOS = [
    {"id": "ecoflow400_atual", "modelo": "EcoFlow 400 W (atual do projeto)", "wp": 400, "vmp_v": 41.0, "imp_a": 9.8,
     "voc_v": 48.0, "isc_a": 11.0, "beta_voc": None, "gamma": None, "massa_kg": 21.0, "massa_nota": "com bolsa",
     "aberto_m": [2.390, 1.068], "dobrado_m": [1.068, 0.600, 0.065], "preco": 5712.27, "moeda": "BRL",
     "fonte": "https://www.kabum.com.br/produto/1040075/painel-solar-portatil-de-400w-ecoflow"},
    {"id": "ecoflow400_lightweight", "modelo": "EcoFlow 400 W Lightweight (TOPCon)", "wp": 400, "vmp_v": 34.5,
     "imp_a": 11.7, "voc_v": 39.3, "isc_a": 12.2, "beta_voc": None, "gamma": None, "massa_kg": 10.2,
     "massa_nota": "painel", "aberto_m": [2.509, 0.967], "dobrado_m": [0.967, 0.659, 0.036], "preco": 649.0,
     "moeda": "EUR", "fonte": "https://solarkontor.de/en/products/ecoflow-400-w-lightweight-portable-solar-panel"},
    {"id": "zoupw450", "modelo": "ZOUPW 450 W N-Type 16BB", "wp": 450, "vmp_v": 38.3, "imp_a": 11.7, "voc_v": 45.9,
     "isc_a": 12.4, "beta_voc": None, "gamma": None, "massa_kg": 12.15, "massa_nota": "painel",
     "aberto_m": [3.095, 0.878], "dobrado_m": [0.878, 0.773, 0.090], "preco": 459.99, "moeda": "USD",
     "fonte": "https://zoupw.com/products/450-watt-portable-solar-panel"},
    {"id": "renogy400_rsp400lsc", "modelo": "Renogy 400 W RSP400LSC-G1 (anotado como E.FLEX 400; confirmar)",
     "wp": 400, "vmp_v": 40.0, "imp_a": 10.0, "voc_v": 47.2, "isc_a": 11.0, "beta_voc": -0.0028, "gamma": -0.0038,
     "massa_kg": 13.7, "massa_nota": "painel", "aberto_m": [2.838, 0.855], "dobrado_m": [0.855, 0.708, 0.080],
     "preco": None, "moeda": None, "fonte": "https://ca.renogy.com/cdn/shop/files/RSP400LSC-G1-datasheet.pdf"},
]
GUARDA_M = (1.10, 0.38, 0.98)   # x livre das bolsas; y de 0,27 m até o tanque (0,65 m); z piso-estrado
CASOS = {"so_teto": None, "parado_dia_todo": (0, 0), "conducao_08_16": (8, 16), "conducao_18_02": (18, 2)}


def base_solar(c):
    p = {k: v["value"] for k, v in c["parameters"].items()}
    base = yaml.safe_load((ROOT / "config/solar_proposta.yaml").read_text())
    base["scenario"].update(date=p["reference_day"], latitude_deg=p["latitude_deg"], longitude_deg=p["longitude_deg"],
                            altitude_m=p["altitude_m"], ambient_temperature_c=p["ambient_c"],
                            wind_speed_m_s=p["wind_m_s"], relative_humidity_percent=p["rh_percent"])
    base["array"].update(module_counts=[1], tilt_deg=0, azimuth_deg=0, albedo=p["pv_albedo"])
    base["assumptions"].update(converter_efficiency=1, other_losses_fraction=p["pv_other_loss"],
                               faiman_u0_w_m2k=p["pv_faiman_u0"], faiman_u1_w_s_m3k=p["pv_faiman_u1"])
    return p, base


def serie(base, wp, gamma, tilt, az, step):
    cand = copy.deepcopy(base)
    cand["module"].update(p_stc_w=wp, gamma_pdc_per_k=gamma)
    cand["array"].update(tilt_deg=tilt, azimuth_deg=az)
    data = simular_dia(cand, step)
    x = data.terminal_assumed_1_modules_w.to_numpy()
    return data.index, (x[:-1] + x[1:]) / 2000


def mascara_parado(hours, janela, setup, teardown):
    """Portáteis abertos: parado, depois da montagem e antes do recolhimento."""
    if janela is None:
        return np.zeros_like(hours, dtype=bool)
    ini, fim = janela
    if ini == fim:                      # parado o dia todo, montado antes do amanhecer
        return np.ones_like(hours, dtype=bool)
    dirigindo = ((hours - ini) % 24) < ((fim - ini) % 24)
    desde = (hours - fim) % 24          # horas desde o fim da condução
    ate = (ini - hours) % 24            # horas até a próxima partida
    return (~dirigindo) & (desde >= setup) & (ate >= teardown)


def main():
    c = carregar_configuracao(ROOT)
    if "_execution" not in c:
        raise ValueError("Selecionar MOTORHOME_SCENARIO registrado")
    p, base = base_solar(c)
    step = p["time_step_minutes"]
    dt = step / 60
    out = diretorio_entregas(ROOT) / "p5_geracao_portateis"
    out.mkdir(parents=True, exist_ok=True)
    idx, teto = serie(base, p["roof_power_48v_study_wp"], p["pv_gamma"], 0, 0, step)
    t = idx[:-1] + pd.Timedelta(minutes=step / 2)
    hours = np.asarray(t.hour + t.minute / 60)
    # Inclinação/azimute fixos dos portáteis: mesma grade do cenário (0-75 deg, N/L/S/O), escolhida pelo dia inteiro.
    grade = {(tilt, az): serie(base, p["portable_wp"], p["portable_gamma"], tilt, az, step)[1]
             for tilt, az in itertools.product(range(0, 76, 15), [0, 90, 180, 270])}
    linhas, resumo = [], {}
    for nome, janela in CASOS.items():
        usa = mascara_parado(hours, janela, p["pv_setup_h"], p["pv_teardown_h"])
        (tilt, az), port = max(grade.items(), key=lambda kv: float((kv[1] * usa).sum()))
        port = port * usa
        resumo[nome] = {"janela_conducao_h": janela, "teto_kwh": float(teto.sum() * dt),
                        "portateis_kwh": float(port.sum() * dt), "total_kwh": float((teto + port).sum() * dt),
                        "portateis_tilt_deg": tilt if usa.any() else None, "portateis_azimute_deg": az if usa.any() else None,
                        "horas_portateis_abertos": float(usa.sum() * dt)}
        linhas += [{"caso": nome, "hora": h, "teto_kw": a, "portateis_kw": b, "total_kw": a + b, "abertos": u}
                   for h, a, b, u in zip(hours, teto, port, usa)]
    pd.DataFrame(linhas).to_csv(out / "horario_casos.csv", index=False)

    # Candidatos de portátil: mesma inclinação ótima do caso parado o dia todo e do caso 18-02 h.
    tilt_ref, az_ref = resumo["parado_dia_todo"]["portateis_tilt_deg"], resumo["parado_dia_todo"]["portateis_azimute_deg"]
    s = c["development"]["pv_shared_study"]
    sol = pvlib.solarposition.get_solarposition(t, p["latitude_deg"], p["longitude_deg"], p["altitude_m"])
    elev_9h = float(np.interp(9.0, hours, sol["apparent_elevation"].to_numpy()))
    cand_rows = []
    for k in CANDIDATOS:
        gamma = k["gamma"] if k["gamma"] is not None else p["portable_gamma"]
        beta = k["beta_voc"] if k["beta_voc"] is not None else s["beta_voc_per_k"]
        _, x = serie(base, k["wp"], gamma, tilt_ref, az_ref, step)
        kwh = {nome: float((x * mascara_parado(hours, CASOS[nome], p["pv_setup_h"], p["pv_teardown_h"])).sum() * dt)
               for nome in ("parado_dia_todo", "conducao_18_02")}
        comp, larg = k["aberto_m"]
        dob = sorted(k["dobrado_m"], reverse=True)                     # maior, médio, espessura
        guarda = {"x_m": dob[0], "y_4un_m": 4 * dob[2], "z_m": dob[1]}
        cabe = guarda["x_m"] <= GUARDA_M[0] and guarda["y_4un_m"] <= GUARDA_M[1] and guarda["z_m"] <= GUARDA_M[2]
        voc_frio_2s = 2 * k["voc_v"] * (1 + beta * (s["cold_c"] - 25))
        isc_2p = 2 * k["isc_a"]
        cand_rows.append({
            "id": k["id"], "modelo": k["modelo"], "wp_unidade": k["wp"], "wp_4un": 4 * k["wp"],
            "kwh_parado_dia_todo_4un": 4 * kwh["parado_dia_todo"], "kwh_parada_18_02_4un": 4 * kwh["conducao_18_02"],
            "massa_4un_kg": 4 * k["massa_kg"],
            "massa_nota": k["massa_nota"], "kwh_por_kg_parado": kwh["parado_dia_todo"] / k["massa_kg"],
            "aberto_comp_m": comp, "aberto_larg_m": larg, "area_aberta_4un_m2": 4 * comp * larg,
            "fileira_4un_leste_oeste_m": 4 * larg + 3 * 0.10,
            "profundidade_n_s_m": comp * np.cos(np.radians(tilt_ref)),
            "sombra_9h_m": comp * np.sin(np.radians(tilt_ref)) / np.tan(np.radians(elev_9h)),
            "dobrado_m": "x".join(f"{d:.3f}" for d in k["dobrado_m"]), "guarda_4un_y_m": guarda["y_4un_m"],
            "cabe_na_guarda_atual": cabe, "voc_frio_2s_v": voc_frio_2s, "isc_2p_a": isc_2p,
            "mppt_150_60_2s2p_ok": voc_frio_2s < s["controller_voc_max_v"] and isc_2p <= s["controller_isc_max_a"],
            "vmp_2s_v": 2 * k["vmp_v"], "preco_unidade": k["preco"], "moeda": k["moeda"], "fonte": k["fonte"],
            "ensaiado": False})
    pd.DataFrame(cand_rows).to_csv(out / "candidatos_portateis.csv", index=False)

    # Sensibilidade: inclinação do teto pelo eixo longitudinal (rolagem do deck). Eixo leste-oeste do
    # veículo: face norte/sul; eixo norte-sul: face leste/oeste. Janela: dia inteiro, teto sempre exposto.
    incl = []
    for tilt, az in itertools.product([0, 5, 10, 15, 20], [0, 90, 180, 270]):
        _, x = serie(base, p["roof_power_48v_study_wp"], p["pv_gamma"], tilt, az, step)
        incl.append({"inclinacao_deg": tilt, "azimute_face_deg": az, "teto_kwh_dia": float(x.sum() * dt),
                     "ganho_vs_plano_kwh": float(x.sum() * dt - teto.sum() * dt)})
    pd.DataFrame(incl).to_csv(out / "inclinacao_teto.csv", index=False)

    result = {"execution": c["_execution"], "dia": p["reference_day"], "passo_min": step,
              "montagem_h": p["pv_setup_h"], "recolhimento_h": p["pv_teardown_h"], "casos": resumo,
              "candidatos": len(cand_rows), "elevacao_solar_9h_deg": elev_9h,
              "melhor_inclinacao_teto": max(incl, key=lambda r: r["teto_kwh_dia"]),
              "limites": ["Fichas de fabricante/revenda; nenhum portátil ensaiado; coeficiente térmico do cenário quando a ficha não publica.",
                          "Guarda conferida por envelope (dobrado x 4 unidades) contra o espaço das bolsas atuais, não por modelo CAD de cada produto.",
                          "Tempo de montagem igual para todos (0,5 h + 0,5 h), hipótese do cenário.",
                          "Inclinação do teto: rolagem rígida do deck, sem sombreamento próprio nem mudança de arrasto."]}
    (out / "resumo.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({k: round(v["total_kwh"], 3) for k, v in resumo.items()}))


if __name__ == "__main__":
    main()
