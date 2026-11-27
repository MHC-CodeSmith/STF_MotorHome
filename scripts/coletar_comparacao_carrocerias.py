"""Collect completed CFD cases and compare Cd, CdA and drag without changing energy inputs."""

import argparse
import csv
import gzip
import hashlib
import json
import math
import re
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--casos", type=Path, required=True)
    p.add_argument("--destino", type=Path, required=True)
    a = p.parse_args()
    a.destino.mkdir(parents=True, exist_ok=True)
    cases = []
    fig, ax = plt.subplots(figsize=(9, 5), layout="constrained")
    for case in sorted(a.casos.iterdir()):
        config = case / "entrada_comparacao.json"
        if not config.exists():
            continue
        spec = json.loads(config.read_text())
        path = case / "resultado_execucao.json"
        r = json.loads(path.read_text()) if path.exists() else {}
        logpath = case / "log.simpleFoam"
        text = logpath.read_text(errors="replace") if logpath.exists() else ""
        history = []
        iteration = None
        for line in text.splitlines():
            t = re.match(r"Time = ([0-9.eE+-]+)", line)
            if t:
                iteration = float(t[1])
            cd = re.search(r"Cd:\s+([0-9.eE+-]+)", line)
            if cd and iteration is not None:
                history.append((iteration, float(cd[1])))
        cd = history[-1][1] if history else None
        components = re.findall(
            r"^\s*Cd:\s+([0-9.eE+-]+)\s+([0-9.eE+-]+)\s+([0-9.eE+-]+)\s+([0-9.eE+-]+)",
            text,
            re.MULTILINE,
        )
        lift = re.findall(r"^\s*Cl:\s+([0-9.eE+-]+)", text, re.MULTILINE)
        span = None
        if len(history) >= 50:
            last = [v for _, v in history[-50:]]
            span = (max(last) - min(last)) / max(abs(sum(last) / len(last)), 1e-12)
        area = spec["area_referencia_m2"]
        cda = cd * area if cd is not None else None
        rho = 1.1
        speed = spec["velocity_m_s"]
        mesh_ok = r.get("mesh_ok", False)
        solver_converged = "SIMPLE solution converged" in text
        finished = bool(re.search(r"^End\s*$", text, re.MULTILINE))
        completed = finished and r.get("simpleFoam", {}).get("exit_code") == 0
        iterative_check_passed = (
            mesh_ok
            and solver_converged
            and completed
            and cd is not None
            and math.isfinite(cd)
            and span is not None
            and span < 0.01
            and not r.get("refinement_truncated", False)
        )
        row = {
            "case": case.name,
            "panel_present": spec["panel_present"],
            "area_ref_m2": area,
            "cells": r.get("cells"),
            "cd_diagnostic": cd,
            "cd_pressure": float(components[-1][1]) if components else None,
            "cd_viscous": float(components[-1][2]) if components else None,
            "cl_diagnostic": float(lift[-1]) if lift else None,
            "cda_m2": cda,
            "drag_n": 0.5 * rho * speed**2 * cda if cda is not None else None,
            "aero_power_w": 0.5 * rho * speed**3 * cda if cda is not None else None,
            "iterations": history[-1][0] if history else None,
            "last50_cd_relative_span": span,
            "cd_mean_last50": sum(v for _, v in history[-50:]) / 50
            if len(history) >= 50
            else None,
            "mesh_ok": mesh_ok,
            "solver_converged": solver_converged,
            "completed": completed,
            "iterative_check_passed": iterative_check_passed,
            "grid_independence": False,
            "physical_validation": False,
            "validated_cd": None,
            "yplus": r.get("yplus", {}),
        }
        cases.append(row)
        if history:
            ax.plot(
                [x for x, _ in history],
                [y for _, y in history],
                label=case.name,
                linestyle="--" if spec["panel_present"] else "-",
            )
        d = a.destino / case.name
        d.mkdir(exist_ok=True)
        shutil.copy2(config, d / config.name)
        if path.exists():
            shutil.copy2(path, d / path.name)
        for name in [
            "recovery_protocol.json",
            "resultado_malha.json",
            "reuse_verified_mesh.json",
        ]:
            if (case / name).exists():
                shutil.copy2(case / name, d / name)
        for raw in sorted(case.glob("log.*")):
            with (
                raw.open("rb") as source,
                gzip.open(d / (raw.name + ".gz"), "wb") as target,
            ):
                shutil.copyfileobj(source, target)
        if (case / "system").is_dir():
            shutil.copytree(case / "system", d / "system", dirs_exist_ok=True)
        with (d / "historico_cd.csv").open("w") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["iteration", "cd"])
            w.writerows(history)
    fields = [k for k in cases[0] if k != "yplus"] if cases else []
    with (a.destino / "comparacao.csv").open("w") as f:
        w = csv.DictWriter(f, fields, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(cases)
    pairs = []
    for prefix in sorted(
        {r["case"][: r["case"].rfind("_a_")] for r in cases if "_a_" in r["case"]}
    ):
        bare = next((r for r in cases if r["case"] == prefix + "_a_sem_paineis"), None)
        panel = next((r for r in cases if r["case"] == prefix + "_b_com_paineis"), None)
        if (
            bare
            and panel
            and bare["cda_m2"] is not None
            and panel["cda_m2"] is not None
        ):
            pairs.append(
                {
                    "geometry": prefix,
                    "delta_cda_m2": panel["cda_m2"] - bare["cda_m2"],
                    "delta_drag_n": panel["drag_n"] - bare["drag_n"],
                    "delta_aero_power_w": panel["aero_power_w"] - bare["aero_power_w"],
                    "drag_change_percent": 100 * (panel["cda_m2"] / bare["cda_m2"] - 1),
                    "both_iteratively_converged": bare["iterative_check_passed"]
                    and panel["iterative_check_passed"],
                }
            )
    result = {
        "cases": cases,
        "panel_comparisons": pairs,
        "complete_six_cases": len(cases) == 6 and all(r["completed"] for r in cases),
        "all_iterative_checks_passed": len(cases) == 6
        and all(r["iterative_check_passed"] for r in cases),
        "validated_cd": None,
        "physical_validation": False,
        "grid_independence": False,
        "source_hashes": {
            str(p.relative_to(a.casos)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(a.casos.rglob("*"))
            if p.is_file()
            and (
                p.name.startswith("log.")
                or p.name.startswith("entrada_")
                or p.name == "resultado_execucao.json"
            )
        },
    }
    (a.destino / "resumo.json").write_text(json.dumps(result, indent=2) + "\n")
    ax.set(
        xlabel="SIMPLE iteration",
        ylabel="Cd diagnostic",
        title="Matched conditions — force coefficient histories",
    )
    ax.grid(alpha=0.2)
    if any(r["iterations"] is not None for r in cases):
        ax.legend(fontsize=7)
    fig.savefig(a.destino / "historicos_cd.png", dpi=160)
    ax.set_ylim(0, 1.5)
    ax.set_title("Cd histories — display limited to 0–1.5; full data in CSV")
    fig.savefig(a.destino / "historicos_cd_zoom.png", dpi=160)
    plt.close(fig)
    if len(cases) == 6 and all(r["iterative_check_passed"] for r in cases):
        import numpy as np

        labels = ["Original", "Modified", "OEM dimension fit"]
        fig, axes = plt.subplots(1, 2, figsize=(11, 4), layout="constrained")
        x = np.arange(3)
        for offset, panels, label in [
            (-0.18, False, "Without panels"),
            (0.18, True, "With panels"),
        ]:
            values = [r for r in cases if r["panel_present"] == panels]
            axes[0].bar(
                x + offset,
                [r["cd_diagnostic"] for r in values],
                width=0.36,
                label=label,
            )
            axes[1].bar(
                x + offset, [r["cda_m2"] for r in values], width=0.36, label=label
            )
        for chart, ylabel in zip(axes, ["Cd [-]", "CdA [m²]"]):
            chart.set_xticks(x, labels)
            chart.set_ylabel(ylabel)
            chart.grid(axis="y", alpha=0.2)
            chart.legend()
        fig.suptitle("Numerical comparison — physical validation pending")
        fig.savefig(a.destino / "comparacao_coeficientes.png", dpi=180)
        fig.savefig(a.destino / "comparacao_coeficientes.pdf")
        plt.close(fig)
    print(json.dumps({"cases": cases, "pairs": pairs}, indent=2))


if __name__ == "__main__":
    main()
