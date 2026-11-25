"""I29 closure: wide speed/start search plus 1-minute refinement of the leaders.

Same model and inputs as ``refinar_resolucao_missao.py`` (scenario
maxeon1560_independente, hypothetical 0.38 kW DC floor (1 A x 380 V), 700 W traction
auxiliaries). Stage A scans 12-40 km/h and every start hour on a 5-minute grid,
which the earlier study showed agrees with 1 minute to 0.02 d. Stage B
re-evaluates a neighbourhood of each Stage A leader at 1 minute. The result is
the best point of a finite grid, not a proven global optimum, and it inherits
the conditional DC interface of the scenario.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from motorhome.cenarios import carregar_configuracao, diretorio_entregas
from motorhome.reconciliacao import consumo_plano, simular_missao
from motorhome.solar import simular_dia

RESERVES = [(0.1, 0.2), (0.2, 0.3)]
AUX_W = 700
_CTX: dict = {}


def preparar(step_min: int) -> dict:
    os.environ["MOTORHOME_SCENARIO"] = "maxeon1560_independente"
    config = carregar_configuracao(ROOT)
    params = {key: value["value"] for key, value in config["parameters"].items()}
    grid = config["development"]["mission_grid"]
    solar = yaml.safe_load((ROOT / "config/solar_proposta.yaml").read_text())
    solar["scenario"].update(
        date=params["reference_day"], latitude_deg=params["latitude_deg"],
        longitude_deg=params["longitude_deg"], altitude_m=params["altitude_m"],
        ambient_temperature_c=params["ambient_c"], wind_speed_m_s=params["wind_m_s"],
        relative_humidity_percent=params["rh_percent"],
    )
    solar["module"].update(p_stc_w=params["roof_power_48v_study_wp"], gamma_pdc_per_k=params["pv_gamma"])
    solar["array"].update(module_counts=[1], tilt_deg=0, azimuth_deg=0, albedo=params["pv_albedo"])
    solar["assumptions"].update(
        converter_efficiency=1, other_losses_fraction=params["pv_other_loss"],
        faiman_u0_w_m2k=params["pv_faiman_u0"], faiman_u1_w_s_m3k=params["pv_faiman_u1"],
    )
    roof_power = simular_dia(solar, step_min)["terminal_assumed_1_modules_w"].to_numpy()
    roof = (roof_power[:-1] + roof_power[1:]) / 2000
    portables = []
    for tilt, azimuth in itertools.product(range(0, 76, 15), (0, 90, 180, 270)):
        candidate = copy.deepcopy(solar)
        candidate["array"].update(tilt_deg=tilt, azimuth_deg=azimuth)
        candidate["module"].update(p_stc_w=params["portable_wp"], gamma_pdc_per_k=params["portable_gamma"])
        watts = simular_dia(candidate, step_min)["terminal_assumed_1_modules_w"].to_numpy()
        portables.append((tilt, azimuth, (watts[:-1] + watts[1:]) / 2000))
    ac = sum(load["energy_ac_or_dc_kwh_day"]["base"] for load in config["loads"] if load["side"] == "AC")
    dc = sum(load["energy_ac_or_dc_kwh_day"]["base"] for load in config["loads"] if load["side"] == "DC")
    service_day = ac / params["eta_inverter"] + dc / params["eta_lv"] + params["inverter_idle_w"] * 24 / 1000
    dt_h = step_min / 60
    return {"config": config, "params": params, "grid": grid, "roof": roof, "portables": portables,
            "service_day": service_day, "step_min": step_min,
            "slot_hours": np.arange(len(roof)) * dt_h + dt_h / 2}


def avaliar(args: tuple[float, float, tuple[float, float]], manter_traco: bool = False) -> dict:
    start_h, speed, reserve = args
    c, p = _CTX, _CTX["params"]
    slot = c["slot_hours"]
    driving = (slot - start_h) % 24 < 8.0
    since_park = (slot - (start_h + 8.0)) % 24
    usable = (~driving) & (since_park >= p["pv_setup_h"]) & (since_park < 16.0 - p["pv_teardown_h"])
    tilt, azimuth, curve = max(c["portables"], key=lambda item: float((item[2] * usable).sum()))
    consumption = consumo_plano(
        speed, p["assembled_typical_mass_kg"], p["cd_range"][1], p["area_m2"], p["crr_range"][1],
        p["rho_range"][1], p["eta_traction_range"][1], aux_traction_kw=AUX_W / 1000,
    )
    result = simular_missao(
        c["roof"].tolist(), (curve * usable).tolist(), driving.tolist(), speed_kmh=speed,
        kwh_km=consumption["kwh_km"], service_kwh_day=c["service_day"],
        traction_capacity_kwh=p["traction_usable_kwh"], service_capacity_kwh=14.4,
        reserve_traction=reserve[0], reserve_service=reserve[1], mode=c["grid"]["mode"],
        min_dc_kw=c["grid"]["hypothetical_min_dc_kw"], max_days=c["grid"]["max_days"],
        eta_dc=p["eta_dc"], primeira_partida_h=start_h,
    )
    if not manter_traco:
        result.pop("trace", None)
        result.pop("daily", None)
    return {"time_step_min": c["step_min"], "start_hour": start_h, "speed_kmh": speed,
            "reserve_traction": reserve[0], "reserve_service": reserve[1],
            "portable_tilt_deg": tilt, "portable_azimuth_deg": azimuth,
            "kwh_per_km": consumption["kwh_km"], **result}


def _init(step_min: int) -> None:
    _CTX.update(preparar(step_min))


def rodar(step_min: int, jobs: list, workers: int) -> list[dict]:
    with ProcessPoolExecutor(workers, initializer=_init, initargs=(step_min,)) as pool:
        return list(pool.map(avaliar, jobs, chunksize=4))


def lider(rows: list[dict], reserve: tuple[float, float]) -> dict | None:
    ok = [r for r in rows if (r["reserve_traction"], r["reserve_service"]) == reserve
          and r["status"] == "chegada_condicional"]
    return min(ok, key=lambda r: (r["elapsed_days"], r["start_hour"], r["speed_kmh"])) if ok else None


def main() -> None:
    # The parent process resolves the output directory, so the scenario is fixed here too.
    os.environ["MOTORHOME_SCENARIO"] = "maxeon1560_independente"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--teste", action="store_true", help="time one candidate per step and exit")
    parser.add_argument("--figura", action="store_true",
                        help="replay the 1-minute leader with its trace; write figure and report macros")
    args = parser.parse_args()
    if args.figura:
        figura()
        return
    if args.teste:
        import time
        for step in (5, 1):
            _init(step)
            t0 = time.perf_counter()
            row = avaliar((17.75, 20.8, RESERVES[0]))
            print(step, round(time.perf_counter() - t0, 2), "s", round(row["elapsed_days"], 4), row["status"])
        return

    speeds_a = [float(v) for v in range(12, 41)]
    starts_a = [h / 2 for h in range(48)]
    stage_a = rodar(5, list(itertools.product(starts_a, speeds_a, RESERVES)), args.workers)
    jobs_b = set()
    for reserve in RESERVES:
        best = lider(stage_a, reserve)
        if best is None:
            continue
        for ds, dh in itertools.product(np.arange(-1.0, 1.01, 0.1), np.arange(-0.75, 0.76, 0.25)):
            speed = round(best["speed_kmh"] + ds, 1)
            if speed > 0:
                jobs_b.add(((best["start_hour"] + dh) % 24, speed, reserve))
    stage_b = rodar(1, sorted(jobs_b), args.workers)

    out = diretorio_entregas(ROOT) / "i29_fechamento"
    out.mkdir(parents=True, exist_ok=True)
    for name, rows in (("etapa_a_5min.json", stage_a), ("etapa_b_1min.json", stage_b)):
        (out / name).write_text(json.dumps(rows, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    summary = {
        "scenario": "maxeon1560_independente",
        "script": "scripts/fechar_i29_velocidade.py",
        "method": "etapa A: 5 min, 12–40 km/h (1 km/h), início 0–23,5 h (0,5 h); etapa B: 1 min, ±1 km/h (0,1) e ±0,75 h (0,25) em torno do líder de A",
        "candidates_stage_a": len(stage_a), "candidates_stage_b": len(stage_b),
        "leaders_stage_a_5min": [lider(stage_a, r) for r in RESERVES],
        "leaders_stage_b_1min": [lider(stage_b, r) for r in RESERVES],
        "leader_on_grid_edge_b": [
            None if (b := lider(stage_b, r)) is None else
            bool(abs(b["speed_kmh"] - max(s for _, s, rr in jobs_b if rr == r)) < 1e-9
                 or abs(b["speed_kmh"] - min(s for _, s, rr in jobs_b if rr == r)) < 1e-9)
            for r in RESERVES
        ],
        "auxiliary_traction_w_assumed": AUX_W,
        "hypothetical_dc_interface": True,
        "global_optimum_claimed": False,
        "configuration_file_sha256": hashlib.sha256((ROOT / "config/parametros_globais.yaml").read_bytes()).hexdigest(),
    }
    (out / "resumo.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("candidates_stage_a", "candidates_stage_b", "leader_on_grid_edge_b")}))
    for row in summary["leaders_stage_b_1min"]:
        if row:
            print({k: row[k] for k in ("start_hour", "speed_kmh", "reserve_traction", "elapsed_days", "kwh_per_km")})


def primeira_reserva(resultado: dict, reserva: float) -> dict | None:
    """Primeiro intervalo que atinge a reserva, mesmo se houver recarga no mesmo dia."""
    row = next((x for x in resultado["trace"] if x["soc_traction"] <= reserva + 1e-9), None)
    if row is None:
        return None
    return {**row, "elapsed_days": row["day"] - 1 + row["hour_end"] / 24}


def figura() -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    out = diretorio_entregas(ROOT) / "i29_fechamento"
    resumo = json.loads((out / "resumo.json").read_text())
    lideres = [r for r in resumo["leaders_stage_b_1min"] if r]
    lider = min(lideres, key=lambda r: r["reserve_traction"])
    _init(1)
    r = avaliar((lider["start_hour"], lider["speed_kmh"], (lider["reserve_traction"], lider["reserve_service"])), True)
    daily, trace = r["daily"], r["trace"]
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.4))
    d = np.array([x["day"] for x in daily]); km = np.array([x["distance_km"] for x in daily])
    axs[0].plot(d, km, color="#1f5fbf", lw=2)
    axs[0].set(xlabel="dia de viagem", ylabel="distância acumulada [km]", title=f"Chegada em {r['elapsed_days']:.1f} dias", ylim=(0, 7300))
    ax2 = axs[0].twinx()
    ax2.plot(d, 100 * np.array([x["soc_traction"] for x in daily]), color="#e8590c", lw=1)
    ax2.set_ylabel("SOC tração ao fim do dia [%]", color="#e8590c"); ax2.set_ylim(0, 105); ax2.grid(False)
    meio = int(len(daily) / 2)
    dia = [x for x in trace if x["day"] == meio]
    hora = np.array([x["hour_end"] for x in dia]); dt = hora[1] - hora[0]
    vel = np.array([x["driving_h_interval"] for x in dia]) / dt * lider["speed_kmh"]
    pv = np.array([x["pv_kwh_interval"] for x in dia]) / dt
    axs[1].fill_between(hora, pv, color="#e8590c", alpha=0.3, step="pre", label="potência FV [kW]")
    axs[1].set(xlabel="hora do dia", ylabel="potência FV [kW]", xlim=(0, 24), title=f"Dia típico ({meio}º dia)")
    ax3 = axs[1].twinx()
    ax3.plot(hora, vel, color="#1f5fbf", drawstyle="steps-pre", label="velocidade [km/h]")
    ax3.set_ylabel("velocidade [km/h]", color="#1f5fbf"); ax3.set_ylim(0, 30); ax3.grid(False)
    fig.tight_layout(); fig.savefig(out / "missao_lider.png", dpi=180)
    km_dia = 7000 / r["elapsed_days"]
    # fase 1: a tração desce até a reserva; fase 2: cada dia roda o que o sol repôs
    fim1 = primeira_reserva(r, lider["reserve_traction"])
    if fim1 is None:
        raise ValueError("O líder não atingiu a reserva; não atribuir ritmo pós-reserva.")
    km_regime = (7000 - fim1["distance_km"]) / (r["elapsed_days"] - fim1["elapsed_days"])
    h_regime = km_regime / lider["speed_kmh"]
    alt = next((x for x in lideres if x is not lider), None)
    virg = lambda x, n=1: f"{x:.{n}f}".replace(".", ",")
    borda = any(x is True for x in resumo["leader_on_grid_edge_b"])
    borda_texto = "há líder na borda da grade, portanto o refino local não encerra a busca" if borda else "os líderes não estão na borda da grade local"
    h0 = lider["start_hour"]; hh = f"{int(h0):02d}h{round((h0 % 1) * 60):02d}"
    h1 = (h0 + 8) % 24; hf = f"{int(h1):02d}h{round((h1 % 1) * 60):02d}"
    tex = f"\\newcommand{{\\PartidaMissao}}{{{hh}}}\n" + (
        f"\\newcommand{{\\IbResposta}}{{Melhor combinação encontrada: velocidade \\textbf{{constante de \\SI{{{virg(lider['speed_kmh'])}}}{{km/h}}}}, "
        f"com partida às {hh} (janela de 8\\,h até {hf}); a viagem de \\SI{{7000}}{{km}} termina em "
        f"\\textbf{{{virg(r['elapsed_days'])} dias}} (\\SI{{{virg(km_dia)}}}{{km/dia}} em média) com reservas de "
        f"{int(100 * lider['reserve_traction'])}\\,\\% na tração e {int(100 * lider['reserve_service'])}\\,\\% nos serviços"
        + (f", ou {virg(alt['elapsed_days'])} dias com reservas de {int(100 * alt['reserve_traction'])}/{int(100 * alt['reserve_service'])}\\,\\%" if alt else "")
        + ".}\n"
        f"\\newcommand{{\\IbResumo}}{{{virg(lider['speed_kmh'])} km/h constantes; {virg(r['elapsed_days'])} dias "
        f"({virg(km_regime, 0)} km/dia em regime)}}\n"
        "\\newcommand{\\IbTexto}{%\n"
        "A viagem parte com a tração cheia (\\SI{98}{kWh} úteis) e o banco de serviços "
        "nominalmente cheio (\\SI{14,4}{kWh} nominais) e só recebe energia solar. "
        f"O tempo é contado a partir de 0h do primeiro dia, e a primeira partida é às {hh}: antes dela o "
        f"veículo não roda, embora a janela diária de condução ({hh} a {hf}) cruze a meia-noite. "
        f"A primeira chegada à reserva ocorre em {virg(fim1['elapsed_days'], 2)} dias, após percorrer "
        f"\\SI{{{virg(fim1['distance_km'], 0)}}}{{km}}; daí em diante cada dia roda o que o sol repôs, "
        f"\\SI{{{virg(km_regime)}}}{{km}} em cerca de \\SI{{{virg(h_regime, 1)}}}{{h}} de condução, "
        "bem abaixo do limite de 8\\,h. "
        f"Ao longo da viagem, os painéis geram \\SI{{{virg(r['totals']['pv_kwh'], 0)}}}{{kWh}}: "
        f"\\SI{{{virg(r['totals']['traction_solar_kwh'], 0)}}}{{kWh}} chegam à tração e "
        f"\\SI{{{virg(r['totals']['service_solar_kwh'], 0)}}}{{kWh}} abastecem a habitação "
        f"(\\SI{{{virg(r['totals']['service_used_kwh'] / r['elapsed_days'], 2)}}}{{kWh/dia}}). "
        f"A tração consome \\SI{{{virg(r['totals']['traction_used_kwh'], 0)}}}{{kWh}} "
        f"(\\SI{{{virg(lider['kwh_per_km'], 3)}}}{{kWh/km}}), em "
        f"\\SI{{{virg(r['totals']['driving_h'], 0)}}}{{h}} de condução.\n\n"
        "Como a energia solar diária é fixa, o tempo total é dominado pelos dias de espera para acumular "
        "energia, e não apenas pelas horas ao volante. O mínimo de consumo específico $v^{*}$ do item 27 "
        "é uma referência analítica para a busca; a agenda e as reservas ainda precisam ser verificadas. "
        "Nos casos comparados, rodar mais rápido aumenta o consumo e os dias de espera. Partir no fim da tarde deixa todo o período de "
        "sol com o veículo parado e os portáteis abertos. A Tabela~\\ref{tab:i29comparacao} compara a "
        "melhor velocidade com 40 e \\SI{80}{km/h} sob a mesma partida, as mesmas reservas e a mesma "
        "geração. A distância até a primeira vez que a tração atinge a reserva mede a autonomia com a "
        "bateria inicialmente cheia; o ritmo depois disso é o que a geração diária sustenta.\n"
        "\\IbComparacao\n\n"
        "Em pista plana, o mínimo de consumo específico pode ser calculado diretamente (item 27), mas o "
        "tempo total também depende da agenda solar, da abertura dos portáteis, das reservas e da energia "
        "disponível em cada horário, interações que o simulador resolve intervalo a intervalo e que não têm "
        "forma fechada. Por isso a velocidade e o horário foram buscados numa grade; a velocidade publicada "
        "é a melhor combinação encontrada nas condições testadas, não um ótimo global demonstrado.\n\n"
        f"A melhor política foi localizada em duas etapas: varredura de \\num{{{resumo['candidates_stage_a']}}} combinações "
        "(\\SIrange{12}{40}{km/h} a cada \\SI{1}{km/h}, partida a cada \\SI{0,5}{h}, duas reservas) com passo de "
        f"\\SI{{5}}{{min}}, e refino de \\num{{{resumo['candidates_stage_b']}}} casos (passo de \\SI{{0,1}}{{km/h}} e "
        f"\\SI{{0,25}}{{h}}) com passo de \\SI{{1}}{{min}}; {borda_texto}. Para o líder, entre "
        f"passos de 5 e \\SI{{1}}{{min}} a duração muda \\SI{{{virg(abs(resumo['leaders_stage_a_5min'][0]['elapsed_days'] - resumo['leaders_stage_b_1min'][0]['elapsed_days']), 2)}}}{{dias}}. "
        "A chegada é discretizada pela janela diária: se o último trecho não cabe antes do fim da janela, o "
        "veículo espera até a noite seguinte, de modo que uma pequena mudança de velocidade pode antecipar ou "
        "atrasar a chegada em quase um dia, como ocorre com as reservas de 20/30\\,\\%.\n\n"
        "\\textbf{Cenário opcional: acumular por mais de um dia.} Em vez de rodar todo dia o que o sol "
        "repôs, o veículo pode esperar alguns dias e percorrer um trecho maior depois, até 8\\,h por dia. "
        "Essa política pode reduzir montagens, mas também altera o SOC, o espaço disponível nos bancos "
        "e o corte por capacidade; não se atribui a ela uma duração sem simulação específica. Devem ser "
        "mantidos o teto de 1560 Wp, o mínimo de 0,38 kW, as reservas e a ausência de energia da rede. A hipótese de dias claros repetidos, a "
        "recarga só pela interface CC e a operação diária dos portáteis continuam valendo; esse cenário não "
        "foi simulado.\n"
        "\\begin{figure}[H]\\centering\\includegraphics[width=\\linewidth]{i29_missao.png}\n"
        "\\caption{Item 29 — distância acumulada e SOC da tração ao longo da viagem, e um dia típico.}\\end{figure}}\n"
    )
    # Mesma partida e mesmas reservas do líder, só a velocidade muda: isola o efeito da velocidade.
    comp = []
    for v in (lider["speed_kmh"], 40.0, 80.0):
        x = r if v == lider["speed_kmh"] else avaliar(
            (h0, v, (lider["reserve_traction"], lider["reserve_service"])), True)
        f1 = primeira_reserva(x, lider["reserve_traction"])
        if f1 is None:
            f1 = {"elapsed_days": x["elapsed_days"], "distance_km": x["distance_km"]}
        resto = x["elapsed_days"] - f1["elapsed_days"]
        comp.append({"speed_kmh": v, "elapsed_days": x["elapsed_days"], "driving_h": x["totals"]["driving_h"],
                     "kwh_per_km": x["totals"]["traction_used_kwh"] / 7000,
                     "dias_ate_reserva": f1["elapsed_days"], "km_bateria_cheia": f1["distance_km"],
                     "km_dia_regime": (7000 - f1["distance_km"]) / resto if resto > 0 else None,
                     "h_dia_regime": ((7000 - f1["distance_km"]) / resto / v) if resto > 0 else None})
    (out / "comparacao_velocidades.json").write_text(json.dumps(comp, indent=1, ensure_ascii=False) + "\n")
    linhas = " \\\\\n".join(
        f"{virg(c['speed_kmh'])} & {virg(c['elapsed_days'])} & {virg(c['driving_h'], 0)} & "
        f"{virg(c['kwh_per_km'], 3)} & {virg(c['km_bateria_cheia'], 0)} & {virg(c['km_dia_regime'])} & "
        f"{virg(c['h_dia_regime'], 2)}" for c in comp)
    tex += (
        "\\newcommand{\\IbComparacao}{%\n"
        "\\begin{table}[H]\\centering\\small\\setlength{\\tabcolsep}{4pt}\n"
        f"\\caption{{Item 29 — mesma partida ({hh}), mesmas reservas e mesma geração; só a velocidade muda.}}\n"
        "\\label{tab:i29comparacao}\n\\begin{tabular}{rrrrrrr}\n\\toprule\n"
        "$v$ & Viagem & Ao volante & Consumo & Até a reserva & \\multicolumn{2}{c}{Depois da reserva} \\\\\n"
        "{}[km/h] & [dias] & [h] & [kWh/km] & [km] & [km/dia] & [h/dia] \\\\\n\\midrule\n"
        + linhas + " \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}}\n")
    (ROOT / "relatorio/valores_i29.tex").write_text(tex, encoding="utf-8")
    print(json.dumps({"elapsed_days": r["elapsed_days"], "km_dia": km_dia, "totals": r["totals"]}, indent=1))


if __name__ == "__main__":
    main()
