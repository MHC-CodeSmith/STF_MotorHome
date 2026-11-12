"""Parallel SIMPLE solve and trend extraction for the additional CFD mesh."""

from __future__ import annotations

import argparse
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
            timeout_s: int, append: bool = False) -> tuple[int, float]:
    started = time.monotonic()
    try:
        with log.open("a" if append else "w") as stream:
            result = subprocess.run(command, cwd=CASE, env=env, stdout=stream,
                                    stderr=subprocess.STDOUT, timeout=timeout_s, check=False)
        return result.returncode, time.monotonic() - started
    except subprocess.TimeoutExpired:
        return -999, time.monotonic() - started


def main() -> None:
    global CASE, SUMMARY
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-dir", default="entregas/aero_equipado1540/malha_adicional_1/case",
                        help="case path relative to the project root")
    parser.add_argument("--resume", action="store_true", help="continue from the latest saved processor field")
    parser.add_argument("--timeout-s", type=int, default=900)
    parser.add_argument("--end-time", type=int, default=1200)
    args = parser.parse_args()
    CASE = ROOT / args.case_dir
    SUMMARY = CASE.parent / "resumo.json"

    sys.path.insert(0, str(ROOT / "scripts"))
    from executar_openfoam import ambiente

    env = ambiente(FOAM)
    summary = json.loads(SUMMARY.read_text())
    if not summary.get("mesh_ok") or not (CASE / "constant/polyMesh/faces").exists():
        raise RuntimeError("Refuse solver: verified mesh is unavailable")
    control = CASE / "system/controlDict"
    control_text = control.read_text()
    control_text = re.sub(r"startFrom\s+\w+;", f"startFrom {'latestTime' if args.resume else 'startTime'};", control_text)
    control_text = re.sub(r"endTime\s+[\d.eE+-]+;", f"endTime {args.end_time};", control_text)
    control_text = re.sub(r"writeInterval\s+[\d.eE+-]+;", "writeInterval 50;", control_text)
    control.write_text(control_text)
    fv_solution_text = (CASE / "system/fvSolution").read_text()
    consistent_match = re.search(r"consistent\s+(yes|no);", fv_solution_text)
    residual_control_block = re.search(r"residualControl\s*\{([^}]*)\}", fv_solution_text, re.DOTALL)
    relaxation_block = re.search(r"relaxationFactors\s*\{\s*fields\s*\{([^}]*)\}\s*equations\s*\{([^}]*)\}", fv_solution_text, re.DOTALL)
    def parse_factors(text: str) -> dict[str, str]:
        return {
            key.strip('"'): value
            for key, value in re.findall(r'("?[A-Za-z][A-Za-z|()]*"?)\s+([0-9.eE+-]+);', text)
        }
    solver_configuration = {
        "consistent": consistent_match.group(1) if consistent_match else "unspecified",
        "residual_control": parse_factors(residual_control_block.group(1)) if residual_control_block else {},
        "relaxation_factors": {
            "fields": parse_factors(relaxation_block.group(1)),
            "equations": parse_factors(relaxation_block.group(2)),
        } if relaxation_block else {},
    }
    for processor_system in CASE.glob("processor*/system/controlDict"):
        processor_text = processor_system.read_text()
        processor_text = re.sub(r"startFrom\s+\w+;", f"startFrom {'latestTime' if args.resume else 'startTime'};", processor_text)
        processor_text = re.sub(r"endTime\s+[\d.eE+-]+;", f"endTime {args.end_time};", processor_text)
        processor_text = re.sub(r"writeInterval\s+[\d.eE+-]+;", "writeInterval 50;", processor_text)
        processor_system.write_text(processor_text)
    decomp = CASE / "system/decomposeParDict"
    decomp.write_text("""FoamFile {version 2.0; format ascii; class dictionary; object decomposeParDict;}
numberOfSubdomains 4;
method simple;
simpleCoeffs {n (4 1 1); delta 0.001;}
distributed no;
roots ();
""")
    decomp_bin = shutil.which("decomposePar", path=env["PATH"])
    if not decomp_bin:
        raise FileNotFoundError("decomposePar absent from the selected OpenFOAM environment")
    processor_dirs = list(CASE.glob("processor[0-9]*"))
    if args.resume:
        if len(processor_dirs) != 4 or not all(any(path.iterdir()) for path in processor_dirs):
            raise RuntimeError("--resume requires the four retained processor directories")
        decomp_exit, decomp_seconds = 0, 0.0
    else:
        for path in processor_dirs:
            if path.is_dir():
                shutil.rmtree(path)
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
        CASE / "log.simpleFoam.parallel", args.timeout_s, append=args.resume,
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
        "parallel_solver_seconds": float(summary.get("parallel_solver_seconds", 0.0)) + solver_seconds,
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
        "parallel_timeout_reached": solver_exit == -999,
        "parallel_last_completed_iteration": history[-1]["iteration"] if history else None,
        "parallel_residual_control_met": "SIMPLE solution converged" in log,
        "processor_checkpoint_retained": True,
    })
    settings_history = summary.setdefault("parallel_solver_configuration_history", [])
    if not settings_history or settings_history[-1] != solver_configuration:
        settings_history.append(solver_configuration)
    completed = []
    for block in re.split(r"(?=^Time = )", log, flags=re.MULTILINE):
        match = re.match(r"Time = ([0-9.eE+-]+)", block)
        if not match or "ExecutionTime =" not in block:
            continue
        residuals = {}
        for field in ("Ux", "Uy", "Uz", "p", "omega", "k"):
            residual = re.search(
                rf"Solving for {field}, Initial residual = ([0-9.eE+-]+), Final residual = ([0-9.eE+-]+)",
                block,
            )
            if residual:
                residuals[field] = {"initial": float(residual.group(1)),
                                    "final": float(residual.group(2))}
        continuity = re.search(r"global = ([0-9.eE+-]+), cumulative =", block)
        completed.append({
            "iteration": int(float(match.group(1))),
            "residuals": residuals,
            "global_continuity_error": float(continuity.group(1)) if continuity else None,
        })
    if completed:
        last = completed[-1]
        summary["parallel_last_completed_iteration"] = last["iteration"]
        summary["parallel_last_completed_initial_residuals"] = {
            key: value["initial"] for key, value in last["residuals"].items()
        }
        summary["parallel_last_completed_final_residuals"] = {
            key: value["final"] for key, value in last["residuals"].items()
        }
        summary["parallel_last_completed_global_continuity_error"] = last["global_continuity_error"]
    summary["parallel_nonconvergence_reason"] = (
        f"{args.timeout_s} s execution timeout; residualControl thresholds unmet; "
        f"last50 Cd relative span={summary['last50_cd_relative_span']:.6g}"
    ) if solver_exit == -999 else (
        "Solver exited without reporting SIMPLE solution converged" if not summary["parallel_solver_converged"] else None
    )
    processor_times = []
    for processor in sorted(CASE.glob("processor[0-9]*")):
        processor_times.append({
            int(path.name) for path in processor.iterdir()
            if path.is_dir() and path.name.replace(".", "", 1).isdigit()
        })
    common_times = set.intersection(*processor_times) if processor_times else set()
    saved_time = max(common_times) if common_times else None
    summary["parallel_latest_common_saved_time"] = saved_time
    if solver_exit in (0, -999) and saved_time is not None:
        yplus_exit, _ = execute(
            [mpi, "-np", "4", solver, "-parallel", "-postProcess", "-func", "yPlus", "-latestTime", "-case", str(CASE)],
            env, CASE / "log.yPlus.parallel", 300,
        )
        summary["parallel_yplus_exit"] = yplus_exit
        summary["parallel_yplus_diagnostic_only"] = True
        summary["parallel_yplus_convergence_claim"] = False
        summary["parallel_yplus_at_saved_iteration"] = saved_time
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
