"""I13/I17: verificação estrutural da cama fixa do layout A (estrado, quadro e postes).

Geometria do CAD (relatorio/montagem_cad.py): estrado de compensado naval de 18 mm (geometria anterior) com 1,95 x 1,35 m
a 1,66 m do solo, sobre quatro postes de 45 mm com 0,98 m de altura; vãos entre eixos de postes de
1,90 m (longitudinal) e 1,30 m (transversal). O estrado apoia num quadro de tubos de aço quadrados
50 x 50 x 3 mm: duas longarinas laterais e uma central de 1,90 m e duas travessas de 1,30 m nas
cabeceiras, que levam a reação da longarina central aos postes.

Casos de carga (coeficiente 1,5 sobre a carga variável, verificação no estado-limite último; flechas
com cargas de serviço, limite L/300):
  A) parado, uso: 2 pessoas (2 x 80 kg) e colchão distribuídos, mais o peso próprio;
  B) parado, carga concentrada: uma pessoa ajoelhada (80 kg com fator dinâmico 2) no meio do vão;
  C) em movimento: colchão, roupa de cama e peso próprio a 3 g vertical (1 g + 2 g de solavanco);
  D) em movimento: estrado, quadro, postes, colchão e roupa de cama a 5 g lateral nos quatro postes em balanço
     (sem contar a fixação do quadro à parede, caso conservador) e, na solução adotada, pelo quadro
     parafusado ao trilho da parede direita com quatro parafusos M8 classe 8.8.
O estrado de 18 mm do CAD não passa no caso B e os postes em balanço não passam no caso D; a solução
adotada usa compensado de 30 mm, quadro de 50 x 50 x 3 mm e postes de 45 x 45 x 4 mm.
A fixação lateral é complementar; o caso de postes em balanço também deve atender.
Propriedades: aço S235 (fy = 235 MPa, E = 210 GPa); compensado naval com f_m,k = 23 MPa,
k_mod = 0,8, gamma_M = 1,2 e E = 8 GPa (valores típicos, não ensaiados).
"""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
G = 9.80665

VAO_X, VAO_Y = 1.90, 1.30          # entre eixos dos postes [m]
ESTRADO_CAD = (1.95, 1.35, 0.018)  # [m] estrado do CAD
ESTRADO = (1.95, 1.35, 0.030)      # [m] estrado adotado após a verificação (compensado de 30 mm)
H_POSTE = 0.98                     # [m]
RHO_COMP_CAD = 550.0                 # densidade do inventário anterior [kg/m3]
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
    a_t, i_t, w_t = tubo_quadrado(0.050, 0.003)
    a_poste, i_poste, w_poste = tubo_quadrado(0.045, 0.004)
    m_postes = 4 * H_POSTE * 7850 * a_poste
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
                                      "flecha_mm": 1e3 * ((2 * 80 * G) * vao_p ** 3 / (48 * E_COMP * 0.40 * i_p) +
                                                       5 * g_k * vao_p ** 4 / (384 * E_COMP * i_p)),
                                      "limite_flecha_mm": 1e3 * vao_p / 300}

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
    i_min = i_poste
    p_cr = math.pi ** 2 * E_ACO * i_min / (2 * H_POSTE) ** 2
    casos["A_poste"] = {"compressao_kn": n_poste / 1e3, "flambagem_euler_kn": p_cr / 1e3,
                        "utilizacao_flambagem": n_poste / p_cr, "utilizacao_compressao": n_poste / (a_poste * FY)}

    # C) em movimento, 3 g vertical sem pessoas.
    q3 = 3 * g_k
    m3 = 3 * (g_k * larg + m_tubo * G) * VAO_X ** 2 / 8
    casos["C_longarina_3g"] = {"utilizacao": m3 / w_t / FY, "sigma_mpa": m3 / w_t / 1e6}
    casos["C_estrado_3g"] = {"utilizacao": q3 * vao_p ** 2 / 8 / w_p / fmd}

    # D) 5 g lateral, cama sem pessoas, só os postes em balanço.
    m_cama = m_estrado + M_COLCHAO + M_ROUPA + m_quadro + m_postes
    f_lat = 5 * m_cama * G / 4
    m_base = f_lat * H_POSTE
    casos["D_poste_5g_lateral"] = {"forca_por_poste_n": f_lat, "momento_base_nm": m_base,
                                   "sigma_mpa": m_base / w_poste / 1e6, "utilizacao": m_base / w_poste / FY}

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
    # Verificar também a carga concentrada transferida integralmente à longarina central.
    q_perm = g_k * larg + m_tubo * G
    m_knee = p_d * VAO_X / 4 + q_perm * VAO_X ** 2 / 8
    casos["B_longarina_concentrada"] = {
        "sigma_mpa": m_knee / w_t / 1e6, "utilizacao": m_knee / w_t / FY,
        "flecha_mm": 1e3 * ((2 * 80 * G) * VAO_X ** 3 / (48 * E_ACO * i_t) +
                            5 * q_perm * VAO_X ** 4 / (384 * E_ACO * i_t)),
        "limite_flecha_mm": 1e3 * VAO_X / 300}
    # Cada poste é fixado por quatro M8 8.8: verificar aço dos parafusos,
    # com braço de alavanca entre fileiras de 60 mm. Não verifica a chapa OEM.
    shear_bolt = f_total / 16
    tension_bolt = (f_total / 4 * H_POSTE) / (2 * 0.060)
    tensile_capacity = 0.9 * fub * a_s / gamma_m2
    casos["D3_parafusos_bases_5g"] = {
        "cisalhamento_por_parafuso_n": shear_bolt,
        "tracao_por_parafuso_n": tension_bolt,
        "resistencia_cisalhamento_n": cap_parafuso,
        "resistencia_tracao_n": tensile_capacity,
        "utilizacao": shear_bolt / cap_parafuso + tension_bolt / (1.4 * tensile_capacity)}
    # Registro original: 18 mm, quadro/poste de 40x40x2 sem contraventamento.
    a_old, _, w_old = tubo_quadrado(0.040, 0.002)
    old_frame = 7850 * a_old * comp_tubos
    old_mass = RHO_COMP_CAD * ESTRADO_CAD[0] * ESTRADO_CAD[1] * ESTRADO_CAD[2] + M_COLCHAO + M_ROUPA + old_frame
    reprovados_cad["D_poste_5g_lateral_sem_fixacao"] = (5 * old_mass * G / 4 * H_POSTE) / w_old / FY
    casos_solucao = casos
    util = {k: max(v.get("utilizacao", 0), v.get("utilizacao_flambagem", 0)) for k, v in casos_solucao.items()}
    flechas_ok = all(v["flecha_mm"] <= v["limite_flecha_mm"] for v in casos_solucao.values() if "limite_flecha_mm" in v)
    out = ROOT / "entregas/integrado_maxeon1560/cama_estrutura"
    out.mkdir(parents=True, exist_ok=True)
    result = {"script": "scripts/verificar_estrutura_cama.py",
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "config_sha256": hashlib.sha256((ROOT / "config/parametros_globais.yaml").read_bytes()).hexdigest() if (ROOT / "config/parametros_globais.yaml").exists() else None,
              "geometria": {"vao_x_m": VAO_X, "vao_y_m": VAO_Y, "estrado_m": ESTRADO, "altura_poste_m": H_POSTE,
                            "tubo_mm": [50, 50, 3], "poste_mm": [45, 45, 4]},
              "massas_kg": {"estrado": m_estrado, "quadro_aco": m_quadro, "postes_aco": m_postes, "colchao": M_COLCHAO, "roupa": M_ROUPA,
                            "pessoas": M_PESSOAS},
              "casos": casos, "reprovados_no_cad_original": reprovados_cad,
              "acrescimo_massa_kg": m_quadro + m_postes - 12.0 + m_estrado - RHO_COMP_CAD * ESTRADO_CAD[0] * ESTRADO_CAD[1] * ESTRADO_CAD[2],
              "utilizacao_maxima": max(util.values()),
              "caso_governante": max(util, key=util.get), "flechas_dentro_do_limite": flechas_ok,
              "aprovado": max(util.values()) <= 1 and flechas_ok,
              "aprovacao_fisica": False, "ancoragem_carroceria_verificada": False,
              "massa_reserva_substituida_kg": 12.0,
              "cenario": "maxeon1560_independente", "data": "2026-11-25",
              "limites": ["Propriedades do compensado são hipóteses de cálculo; EN 636 não determina sozinha a resistência desta chapa ou direção de fibras.",
                          "Parafusos M8 verificados no aço; soldas, chapas de base, arrancamento e pontos de ancoragem OEM requerem detalhamento.",
                          "Caso D ignora a fixação do quadro à parede; aprovação refere-se apenas aos elementos idealizados, sem ensaio ou homologação."]}
    (out / "resumo.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"utilizacao_maxima": result["utilizacao_maxima"], "governante": result["caso_governante"],
                      "aprovado": result["aprovado"], "massa_quadro": m_quadro, "estrado": m_estrado}, ensure_ascii=False))


if __name__ == "__main__":
    main()
