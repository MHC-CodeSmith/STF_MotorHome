"""Parallel SIMPLE solve and trend extraction for the additional CFD mesh."""

from __future__ import annotations

import csv
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path("/home/mhc/motorhome_referencias_tarefas")
FOAM = CACHE / "software/openfoam2412-local/usr/lib/openfoam/openfoam2412"
CASE = ROOT / "entregas/aero_equipado1540/malha_adicional_1/case"
SUMMARY = CASE.parent / "resumo.json"


def execute(command: list[str], env: dict[str, str], log: Path,
            timeout_s: int) -> tuple[int, float]:
    started = time.monotonic()
    try:
        with log.open("w") as stream:
            result = subprocess.run(command, cwd=CASE, env=env, stdout=stream,
                                    stderr=subprocess.STDOUT, timeout=timeout_s, check=False)
        return result.returncode, time.monotonic() - started
    except subprocess.TimeoutExpired:
        return -999, time.monotonic() - started


def main() -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    from executar_openfoam import ambiente

    env = ambiente(FOAM)
    summary = json.loads(SUMMARY.read_text())
    if not summary.get("mesh_ok") or not (CASE / "constant/polyMesh/faces").exists():
        raise RuntimeError("Refuse solver: verified mesh is unavailable")
    decomp = CASE / "system/decomposeParDict"
    decomp.write_text("""FoamFile {version 2.0; format ascii; class dictionary; object decomposeParDict;}
numberOfSubdomains 4;
method simple;
simpleCoeffs {n (4 1 1); delta 0.001;}
distributed no;
roots ();
""")
    for path in CASE.glob("processor*"):
        if path.is_dir():
            shutil.rmtree(path)
    decomp_bin = shutil.which("decomposePar", path=env["PATH"])
    if not decomp_bin:
        raise FileNotFoundError("decomposePar absent from the selected OpenFOAM environment")
    decomp_exit, decomp_seconds = execute(
        [decomp_bin, "-force", "-case", str(CASE)], env, CASE / "log.decomposePar", 300
    )
    if decomp_exit != 0:
        summary["parallel_decompose_exit"] = decomp_exit
        summary["parallel_solver_exit"] = None
        SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
        raise SystemExit(1)

    mpi = shutil.which("mpirun", path=env["PATH"])
    solver = shutil.which("simpleFoam", path=env["PATH"])
    if not mpi or not solver:
        raise FileNotFoundError("MPI runtime or simpleFoam absent")
    solver_exit, solver_seconds = execute(
        [mpi, "-np", "4", solver, "-parallel", "-case", str(CASE)], env,
        CASE / "log.simpleFoam.parallel", 900,
    )
    log = (CASE / "log.simpleFoam.parallel").read_text(errors="replace")
    time_value = 0
    history = []
    for line in log.splitlines():
        time_match = re.match(r"Time = ([0-9.eE+-]+)", line)
        if time_match:
            time_value = int(float(time_match.group(1)))
        cd_match = re.match(r"\s*Cd:\s+([0-9.eE+-]+)", line)
        if cd_match:
            history.append({"iteration": time_value, "cd": float(cd_match.group(1))})
    with (CASE.parent / "historico_cd.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, ["iteration", "cd"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(history)
    cd = [row["cd"] for row in history]
    summary.update({
        "parallel_decompose_exit": decomp_exit,
        "parallel_decompose_seconds": decomp_seconds,
        "parallel_subdomains": 4,
        "parallel_decomposition": "simple (4,1,1)",
        "parallel_solver_exit": solver_exit,
        "parallel_solver_seconds": solver_seconds,
        "parallel_solver_converged": "SIMPLE solution converged" in log,
        "parallel_iterations_with_cd": len(cd),
        "last_cd_diagnostic": cd[-1] if cd else summary.get("last_cd_diagnostic"),
        "last50_cd_relative_span": ((max(cd[-50:]) - min(cd[-50:])) /
                                     max(abs(float(np.mean(cd[-50:]))), 1e-12)
                                     if len(cd) >= 50 else None),
        "finite_coefficients": bool(cd and np.isfinite(cd).all()),
        "grid_independence_claimed": False,
        "validated_cd": None,
        "physical_validation": False,
    })
    if solver_exit == 0:
        yplus_exit, _ = execute(
            [mpi, "-np", "4", solver, "-parallel", "-postProcess", "-func", "yPlus", "-latestTime", "-case", str(CASE)],
            env, CASE / "log.yPlus.parallel", 300,
        )
        summary["parallel_yplus_exit"] = yplus_exit
        ylog = (CASE / "log.yPlus.parallel").read_text(errors="replace")
        summary["yplus_summary"] = {
            row[0]: [float(value) for value in row[1:]]
            for row in re.findall(
                r"patch (\w+) y\+ : min = ([\deE.+-]+), max = ([\deE.+-]+), average = ([\deE.+-]+)", ylog
            )
        }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({key: summary.get(key) for key in (
        "cell_count", "mesh_ok", "parallel_solver_exit", "parallel_solver_converged",
        "parallel_iterations_with_cd", "last_cd_diagnostic", "last50_cd_relative_span",
        "parallel_solver_seconds", "parallel_yplus_exit"
    )}, ensure_ascii=False))


if __name__ == "__main__":
    main()
