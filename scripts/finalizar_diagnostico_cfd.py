"""Record a running diagnostic case after its existing solver process finishes."""

import argparse
import json
import re
import time
from pathlib import Path

from executar_openfoam import ambiente
from processo_cfd_monitorado import run


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--caso", type=Path, required=True)
    p.add_argument("--driver-log", type=Path, required=True)
    p.add_argument("--prefixo", type=Path, required=True)
    p.add_argument("--gpu-lib", type=Path, required=True)
    args = p.parse_args()
    case = args.caso.resolve()
    started = time.monotonic()
    guard_requested = False
    while True:
        driver = args.driver_log.read_text(errors="replace")
        records = re.findall(
            r"^gpu simpleFoam (-?\d+) ([0-9.]+)$", driver, re.MULTILINE
        )
        if records:
            break
        logpath = case / "log.simpleFoam"
        if logpath.exists() and not guard_requested:
            with logpath.open("rb") as source:
                source.seek(max(0, logpath.stat().st_size - 300000))
                tail = source.read().decode(errors="replace")
            times = re.findall(r"^Time = ([0-9.eE+-]+)", tail, re.MULTILINE)
            cds = re.findall(r"^\s*Cd:\s+(\S+)", tail, re.MULTILINE)
            if times and cds and float(times[-1]) > 100 and abs(float(cds[-1])) > 10:
                control = case / "system/controlDict"
                control.write_text(
                    control.read_text().replace("stopAt endTime;", "stopAt writeNow;")
                )
                guard_requested = True
        if time.monotonic() - started > 86400:
            raise TimeoutError("Diagnostic solver completion record missing")
        time.sleep(15)
    code, elapsed = int(records[-1][0]), float(records[-1][1])
    text = (case / "log.simpleFoam").read_text(errors="replace")
    cd = [float(v) for v in re.findall(r"^\s*Cd:\s+(\S+)", text, re.MULTILINE)]
    env = ambiente(args.prefixo)
    env["LD_LIBRARY_PATH"] = (
        str(args.gpu_lib) + ":/usr/local/cuda/lib64:" + env["LD_LIBRARY_PATH"]
    )
    env["CUDA_VISIBLE_DEVICES"] = "0"
    env["OMPI_MCA_orte_tmpdir_base"] = str(case / ".mpi-tmp")
    mesh_result = run(
        ["checkMesh", "-case", str(case)], env, case / "log.checkMesh", 300
    )
    mesh_text = (case / "log.checkMesh").read_text()
    cells = re.search(r"cells:\s+(\d+)", mesh_text)
    result = {
        "case": args.caso.name,
        "backend": "OGL CUDA",
        "cuda_visible_devices": "0",
        "validated_cd": None,
        "simpleFoam": {"exit_code": code, "elapsed_s": elapsed},
        "checkMesh": mesh_result,
        "mesh_ok": mesh_result["exit_code"] == 0 and "Mesh OK." in mesh_text,
        "cells": int(cells[1]) if cells else None,
        "solver_converged": "SIMPLE solution converged" in text,
        "divergence_guard_requested": guard_requested,
        "last_cd_diagnostic": cd[-1] if cd else None,
        "cd_span_last50": (max(cd[-50:]) - min(cd[-50:]))
        / max(abs(sum(cd[-50:]) / 50), 1e-12)
        if len(cd) >= 50
        else None,
        "reused_mesh": json.loads((case / "reuse_verified_mesh.json").read_text()),
    }
    if code == 0 and result["solver_converged"]:
        y = run(
            [
                "mpirun",
                "-np",
                "2",
                "simpleFoam",
                "-case",
                str(case),
                "-postProcess",
                "-func",
                "yPlus",
                "-latestTime",
                "-parallel",
            ],
            env,
            case / "log.yPlus",
            300,
        )
        result["yplus_exit_code"] = y["exit_code"]
        ytext = (case / "log.yPlus").read_text(errors="replace")
        result["yplus"] = {
            r[0]: [float(v) for v in r[1:]]
            for r in re.findall(
                r"patch (\w+) y\+ : min = ([\deE.+-]+), max = ([\deE.+-]+), average = ([\deE.+-]+)",
                ytext,
            )
        }
    (case / "resultado_execucao.json").write_text(json.dumps(result, indent=2) + "\n")
    if code or not result["solver_converged"]:
        raise SystemExit(
            "Diagnostic did not converge; do not accept or launch dependent runs"
        )


if __name__ == "__main__":
    main()
