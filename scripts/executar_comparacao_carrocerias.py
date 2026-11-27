"""Run matched cases with bounded workers/MPI; retain failures and raw logs."""

import argparse
import hashlib
import json
import os
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from queue import SimpleQueue
from threading import local

from executar_openfoam import ambiente


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--casos", type=Path, required=True)
    p.add_argument("--prefixo", type=Path, required=True)
    p.add_argument("--workers", type=int, default=1)
    p.add_argument("--mpi", type=int, default=1)
    p.add_argument("--gpu-lib", type=Path)
    p.add_argument("--aguardar-malha", action="store_true")
    p.add_argument("--timeout-s", type=int, default=21600)
    a = p.parse_args()
    env = ambiente(a.prefixo)
    if a.gpu_lib:
        if a.mpi < 2:
            raise ValueError(
                "This OGL release requires an MPI communicator: use --mpi 2"
            )
        if not (a.gpu_lib / "libOGL.so").is_file():
            raise FileNotFoundError(a.gpu_lib / "libOGL.so")
        env["LD_LIBRARY_PATH"] = os.pathsep.join(
            [str(a.gpu_lib), "/usr/local/cuda/lib64", env["LD_LIBRARY_PATH"]]
        )
    if not 1 <= a.workers <= 2 or not 1 <= a.mpi <= 4:
        raise ValueError("Supported limits: workers 1–2; MPI 1–4")
    worker_state = local()
    devices = SimpleQueue()
    for device in range(a.workers):
        devices.put(device)

    def init_worker():
        worker_state.device = devices.get()

    def run_case(case):
        wait_start = time.monotonic()
        while a.aguardar_malha and not (case / "reuse_verified_mesh.json").exists():
            mesh_status = case / "resultado_malha.json"
            if mesh_status.exists():
                try:
                    passed = json.loads(mesh_status.read_text()).get(
                        "last_stage_passed", True
                    )
                except json.JSONDecodeError:
                    passed = True
                if not passed:
                    raise RuntimeError(f"Mesh generation failed: {case}")
            if time.monotonic() - wait_start > a.timeout_s:
                raise TimeoutError(f"Waiting for verified mesh: {case}")
            time.sleep(15)
        case_env = env.copy()
        mpi_tmp = case.resolve() / ".mpi-tmp"
        mpi_tmp.mkdir(exist_ok=True)
        case_env["OMPI_MCA_orte_tmpdir_base"] = str(mpi_tmp)
        if a.gpu_lib:
            case_env["CUDA_VISIBLE_DEVICES"] = str(worker_state.device)
            from configurar_backend_gpu import configure

            configure(case)
        result = {"case": case.name, "started_unix": time.time(), "validated_cd": None}
        result["backend"] = "OGL CUDA" if a.gpu_lib else "OpenFOAM CPU"
        result["cuda_visible_devices"] = case_env.get("CUDA_VISIBLE_DEVICES")
        stages = [
            ("blockMesh", []),
            ("snappyHexMesh", ["-overwrite"]),
            ("checkMesh", []),
        ]
        if (case / "reuse_verified_mesh.json").exists():
            if not (case / "constant/polyMesh/faces").exists():
                raise RuntimeError("Requested reuse without saved mesh")
            result["reused_mesh"] = json.loads(
                (case / "reuse_verified_mesh.json").read_text()
            )
            for name, digest in result["reused_mesh"]["mesh_sha256"].items():
                if (
                    hashlib.sha256(
                        (case / "constant/polyMesh" / name).read_bytes()
                    ).hexdigest()
                    != digest
                ):
                    raise RuntimeError("Saved mesh changed after verification")
            if (
                "reached limit"
                in (case / "log.snappyHexMesh").read_text(errors="replace").lower()
            ):
                raise RuntimeError("Refinement cap reached in saved mesh")
            stages = [("checkMesh", [])]
        elif (case / "resume_snapped.json").exists():
            if not (case / "constant/polyMesh/faces").exists():
                raise RuntimeError("Requested layer resume without saved mesh")
            result["resume_snapped"] = json.loads(
                (case / "resume_snapped.json").read_text()
            )
            stages = [("checkMesh_snapped", []), *stages[1:]]
        if a.mpi > 1:
            (case / "system/decomposeParDict").write_text(
                "FoamFile {version 2.0; format ascii; class dictionary; object decomposeParDict;}\n"
                f"numberOfSubdomains {a.mpi}; method simple; simpleCoeffs {{n ({a.mpi} 1 1); delta 0.001;}}\n"
                "distributed no; roots ();\n"
            )
            stages.append(("decomposePar", []))
        stages.append(("simpleFoam", []))
        for tool, args in stages:
            binary = "checkMesh" if tool == "checkMesh_snapped" else tool
            command = [binary, "-case", str(case.resolve()), *args]
            if tool == "simpleFoam" and a.mpi > 1:
                command = ["mpirun", "-np", str(a.mpi), *command, "-parallel"]
            log = case / ("log." + tool)
            if log.exists():
                raise FileExistsError(log)
            start = time.time()
            with log.open("w") as stream:
                try:
                    proc = subprocess.run(
                        command,
                        env=case_env,
                        stdout=stream,
                        stderr=subprocess.STDOUT,
                        timeout=a.timeout_s,
                        check=False,
                    )
                    code = proc.returncode
                except subprocess.TimeoutExpired:
                    code = -999
            text = log.read_text(errors="replace")
            result[tool] = {"exit_code": code, "elapsed_s": time.time() - start}
            if tool.startswith("checkMesh"):
                result["mesh_ok"] = "Mesh OK." in text
                m = re.search(r"cells:\s+(\d+)", text)
                result["cells"] = int(m[1]) if m else None
            if tool == "snappyHexMesh":
                result["refinement_truncated"] = "reached limit" in text.lower()
            if tool == "simpleFoam":
                result["solver_converged"] = "SIMPLE solution converged" in text
                cd = [float(x) for x in re.findall(r"Cd:\s+([\deE.+-]+)", text)]
                result["last_cd_diagnostic"] = cd[-1] if cd else None
                if len(cd) >= 50:
                    tail = cd[-50:]
                    result["cd_span_last50"] = (max(tail) - min(tail)) / max(
                        abs(sum(tail) / len(tail)), 1e-12
                    )
                cfg = json.loads((case / "entrada_comparacao.json").read_text())
                area = cfg["area_referencia_m2"]
                result["area_m2"] = area
                result["cda_m2"] = cd[-1] * area if cd else None
                result["drag_n"] = (
                    0.5 * 1.1 * 22.222222**2 * result["cda_m2"] if cd else None
                )
                with (case / "log.yPlus").open("w") as stream:
                    ycommand = [
                        "simpleFoam",
                        "-case",
                        str(case.resolve()),
                        "-postProcess",
                        "-func",
                        "yPlus",
                        "-latestTime",
                    ]
                    if a.mpi > 1:
                        ycommand = ["mpirun", "-np", str(a.mpi), *ycommand, "-parallel"]
                    yproc = subprocess.run(
                        ycommand,
                        env=case_env,
                        stdout=stream,
                        stderr=subprocess.STDOUT,
                        timeout=120,
                        check=False,
                    )
                result["yplus_exit_code"] = yproc.returncode
                y = (case / "log.yPlus").read_text(errors="replace")
                result["yplus"] = {
                    r[0]: [float(v) for v in r[1:]]
                    for r in re.findall(
                        r"patch (\w+) y\+ : min = ([\deE.+-]+), max = ([\deE.+-]+), average = ([\deE.+-]+)",
                        y,
                    )
                }
            (case / "resultado_execucao.json").write_text(
                json.dumps(result, indent=2) + "\n"
            )
            print(
                json.dumps({"case": case.name, "tool": tool, **result[tool]}),
                flush=True,
            )
            if (
                code
                or (tool.startswith("checkMesh") and not result["mesh_ok"])
                or result.get("refinement_truncated")
            ):
                break
        result["finished_unix"] = time.time()
        (case / "resultado_execucao.json").write_text(
            json.dumps(result, indent=2) + "\n"
        )
        return result

    cases = [
        c for c in sorted(a.casos.iterdir()) if (c / "entrada_comparacao.json").exists()
    ]
    with ThreadPoolExecutor(max_workers=a.workers, initializer=init_worker) as pool:
        results = list(pool.map(run_case, cases))
    if any(r.get("simpleFoam", {}).get("exit_code") != 0 for r in results):
        raise SystemExit("One or more cases failed; inspect retained logs")


if __name__ == "__main__":
    main()
