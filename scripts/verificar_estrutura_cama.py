"""I13/I17: verificação estrutural da cama fixa do layout A (estrado, quadro e postes).

Geometria do CAD (relatorio/montagem_cad.py): estrado de compensado naval de 18 mm com 1,95 x 1,35 m
a 1,66 m do solo, sobre quatro postes de 45 mm com 0,98 m de altura; vãos entre eixos de postes de
1,90 m (longitudinal) e 1,30 m (transversal). O estrado apoia num quadro de tubos de aço quadrados
40 x 40 x 2 mm: duas longarinas laterais e uma central de 1,90 m e duas travessas de 1,30 m nas
cabeceiras, que levam a reação da longarina central aos postes.

Casos de carga (coeficiente 1,5 sobre a carga variável, verificação no estado-limite último; flechas
com cargas de serviço, limite L/300):
  A) parado, uso: 2 pessoas (2 x 80 kg) e colchão distribuídos, mais o peso próprio;
  B) parado, carga concentrada: uma pessoa ajoelhada (80 kg com fator dinâmico 2) no meio do vão;
  C) em movimento: colchão, roupa de cama e peso próprio a 3 g vertical (1 g + 2 g de solavanco);
  D) em movimento: os mesmos 50 kg da cama a 5 g lateral resistidos só pelos quatro postes em balanço
     (sem contar a fixação do quadro à parede, caso conservador) e, na solução adotada, pelo quadro
     parafusado ao trilho da parede direita com quatro parafusos M8 classe 8.8.
O estrado de 18 mm do CAD não passa no caso B e os postes em balanço não passam no caso D; a solução
adotada usa compensado de 25 mm e a fixação lateral do quadro à parede.
Propriedades: aço S235 (fy = 235 MPa, E = 210 GPa); compensado naval EN 636 com f_m,k = 23 MPa,
k_mod = 0,8, gamma_M = 1,2 e E = 8 GPa (valores típicos, não ensaiados).
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
G = 9.80665

VAO_X, VAO_Y = 1.90, 1.30          # entre eixos dos postes [m]
ESTRADO_CAD = (1.95, 1.35, 0.018)  # [m] estrado do CAD
ESTRADO = (1.95, 1.35, 0.025)      # [m] estrado adotado após a verificação (compensado de 25 mm)
H_POSTE = 0.98                     # [m]
RHO_COMP = 600.0                   # compensado naval [kg/m3]
M_PESSOAS, M_COLCHAO, M_ROUPA = 160.0, 20.0, 10.0
GAMMA_Q = 1.5
FY, E_ACO = 235e6, 210e9
FMK, KMOD, GAMMA_M, E_COMP = 23e6, 0.8, 1.2, 8e9


def tubo_quadrado(b, t):
    """Área, inércia e módulo resistente de tubo quadrado de lado b e parede t [m]."""
    a = b * b - (b - 2 * t) ** 2
    i = (b ** 4 - (b - 2 * t) ** 4) / 12
    return a, i, i / (b / 2)


def main():
    a_t, i_t, w_t = tubo_quadrado(0.040, 0.002)
    m_tubo = 7850 * a_t
    comp_tubos = 3 * VAO_X + 2 * VAO_Y
    m_estrado = RHO_COMP * ESTRADO[0] * ESTRADO[1] * ESTRADO[2]
    m_quadro = m_tubo * comp_tubos
    area = ESTRADO[0] * ESTRADO[1]
    fmd = KMOD * FMK / GAMMA_M
    casos = {}

    # Estrado: faixa de 1 m entre longarinas (vão 0,65 m), biapoiada.
    vao_p = VAO_Y / 2
    t = ESTRADO[2]
    w_p, i_p = t * t / 6, t ** 3 / 12
    g_k = (m_estrado + M_COLCHAO + M_ROUPA) * G / area          # permanente [Pa]
    q_k = M_PESSOAS * G / area                                  # variável [Pa]
    q_d = g_k + GAMMA_Q * q_k
    m_d = q_d * vao_p ** 2 / 8
    flecha = 5 * (g_k + q_k) * vao_p ** 4 / (384 * E_COMP * i_p)
    casos["A_estrado"] = {"sigma_mpa": m_d / w_p / 1e6, "resistencia_mpa": fmd / 1e6,
                          "utilizacao": m_d / w_p / fmd, "flecha_mm": 1e3 * flecha,
                          "limite_flecha_mm": 1e3 * vao_p / 300}
    # Carga concentrada (pessoa ajoelhada): largura efetiva de 0,40 m.
    p_d = GAMMA_Q * 2 * 80 * G
    m_p = p_d * vao_p / 4 + g_k * 0.40 * vao_p ** 2 / 8
    sigma_p = m_p / (0.40 * w_p)
    casos["B_estrado_concentrada"] = {"sigma_mpa": sigma_p / 1e6, "utilizacao": sigma_p / fmd,
                                      "flecha_mm": 1e3 * (2 * 80 * G) * vao_p ** 3 / (48 * E_COMP * 0.40 * i_p)}

    # Longarina central: faixa de 0,65 m, vão 1,90 m, mais peso próprio do tubo.
    def viga(q_serv, q_ult, vao):
        m = q_ult * vao ** 2 / 8
        return {"sigma_mpa": m / w_t / 1e6, "utilizacao": m / w_t / FY,
                "flecha_mm": 1e3 * 5 * q_serv * vao ** 4 / (384 * E_ACO * i_t),
                "limite_flecha_mm": 1e3 * vao / 300}
    larg = VAO_Y / 2
    q_serv = (g_k + q_k) * larg + m_tubo * G
    q_ult = (g_k + GAMMA_Q * q_k) * larg + m_tubo * G
    casos["A_longarina_central"] = viga(q_serv, q_ult, VAO_X)
    casos["A_longarina_lateral"] = viga(q_serv / 2, q_ult / 2, VAO_X)
    # Travessa de cabeceira: reação da longarina central no meio do vão de 1,30 m.
    r_ult = q_ult * VAO_X / 2
    r_serv = q_serv * VAO_X / 2
    m_tr = r_ult * VAO_Y / 4
    casos["A_travessa"] = {"sigma_mpa": m_tr / w_t / 1e6, "utilizacao": m_tr / w_t / FY,
                           "flecha_mm": 1e3 * r_serv * VAO_Y ** 3 / (48 * E_ACO * i_t),
                           "limite_flecha_mm": 1e3 * VAO_Y / 300}

    # Postes: compressão com flambagem (Euler, engastado-livre K = 2, caso conservador).
    total_ult = (g_k + GAMMA_Q * q_k) * area + m_quadro * G
    n_poste = total_ult / 4
    i_min = i_t
    p_cr = math.pi ** 2 * E_ACO * i_min / (2 * H_POSTE) ** 2
    casos["A_poste"] = {"compressao_kn": n_poste / 1e3, "flambagem_euler_kn": p_cr / 1e3,
                        "utilizacao_flambagem": n_poste / p_cr, "utilizacao_compressao": n_poste / (a_t * FY)}

    # C) em movimento, 3 g vertical sem pessoas.
    q3 = 3 * g_k
    m3 = 3 * (g_k * larg + m_tubo * G) * VAO_X ** 2 / 8
    casos["C_longarina_3g"] = {"utilizacao": m3 / w_t / FY, "sigma_mpa": m3 / w_t / 1e6}
    casos["C_estrado_3g"] = {"utilizacao": q3 * vao_p ** 2 / 8 / w_p / fmd}

    # D) 5 g lateral, cama sem pessoas, só os postes em balanço.
    m_cama = m_estrado + M_COLCHAO + M_ROUPA + m_quadro
    f_lat = 5 * m_cama * G / 4
    m_base = f_lat * H_POSTE
    casos["D_poste_5g_lateral"] = {"forca_por_poste_n": f_lat, "momento_base_nm": m_base,
                                   "sigma_mpa": m_base / w_t / 1e6, "utilizacao": m_base / w_t / FY}

    # D2) solução adotada: o quadro parafusado ao trilho da parede leva toda a força lateral.
    f_total = 5 * m_cama * G
    a_s, fub, gamma_m2 = 36.6e-6, 800e6, 1.25          # M8 8.8: área resistente e resistência
    cap_parafuso = 0.6 * fub * a_s / gamma_m2
    casos["D2_parafusos_parede_5g"] = {"forca_total_n": f_total, "capacidade_4xM8_n": 4 * cap_parafuso,
                                       "utilizacao": f_total / (4 * cap_parafuso)}
    # Verificação do estrado do CAD (18 mm), mantida para registro.
    w18 = ESTRADO_CAD[2] ** 2 / 6
    m18 = GAMMA_Q * 2 * 80 * G * vao_p / 4 + ((RHO_COMP * ESTRADO_CAD[2] * G) + (M_COLCHAO + M_ROUPA) * G / area) * 0.40 * vao_p ** 2 / 8
    reprovados_cad = {"B_estrado_18mm_concentrada": m18 / (0.40 * w18) / fmd,
                      "D_poste_5g_lateral_sem_fixacao": casos["D_poste_5g_lateral"]["utilizacao"]}
    casos_solucao = {k: v for k, v in casos.items() if k != "D_poste_5g_lateral"}
    util = {k: max(v.get("utilizacao", 0), v.get("utilizacao_flambagem", 0)) for k, v in casos_solucao.items()}
    flechas_ok = all(v["flecha_mm"] <= v["limite_flecha_mm"] for v in casos_solucao.values() if "limite_flecha_mm" in v)
    out = ROOT / "entregas/integrado_maxeon1560/cama_estrutura"
    out.mkdir(parents=True, exist_ok=True)
    result = {"script": "scripts/verificar_estrutura_cama.py",
              "geometria": {"vao_x_m": VAO_X, "vao_y_m": VAO_Y, "estrado_m": ESTRADO, "altura_poste_m": H_POSTE,
                            "tubo_mm": [40, 40, 2]},
              "massas_kg": {"estrado": m_estrado, "quadro_aco": m_quadro, "colchao": M_COLCHAO, "roupa": M_ROUPA,
                            "pessoas": M_PESSOAS},
              "casos": casos, "reprovados_no_cad_original": reprovados_cad,
              "acrescimo_massa_kg": m_quadro + m_estrado - RHO_COMP * ESTRADO_CAD[0] * ESTRADO_CAD[1] * ESTRADO_CAD[2],
              "utilizacao_maxima": max(util.values()),
              "caso_governante": max(util, key=util.get), "flechas_dentro_do_limite": flechas_ok,
              "aprovado": max(util.values()) <= 1 and flechas_ok,
              "limites": ["Propriedades do compensado são valores típicos de EN 636, sem ensaio.",
                          "Ligações (parafusos dos postes às chapas do item 15 e do quadro à parede) não dimensionadas aqui.",
                          "Caso D ignora a fixação do quadro à parede e é conservador."]}
    (out / "resumo.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"utilizacao_maxima": result["utilizacao_maxima"], "governante": result["caso_governante"],
                      "aprovado": result["aprovado"], "massa_quadro": m_quadro, "estrado": m_estrado}, ensure_ascii=False))


if __name__ == "__main__":
    main()
