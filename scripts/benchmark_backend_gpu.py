"""Compare CPU and CUDA linear backends on copies of one identical mesh."""

import argparse
import json
import math
import os
import re
import subprocess
import time
from pathlib import Path

from executar_openfoam import ambiente


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--caso", type=Path, required=True)
    p.add_argument("--prefixo", type=Path, required=True)
    p.add_argument("--gpu-lib", type=Path)
    p.add_argument("--device", type=int, default=0)
    p.add_argument("--mpi", type=int, default=1)
    a = p.parse_args()
    env = ambiente(a.prefixo)
    mpi_tmp = a.caso.resolve() / ".mpi-tmp"
    mpi_tmp.mkdir(exist_ok=True)
    env["OMPI_MCA_orte_tmpdir_base"] = str(mpi_tmp)
    if a.gpu_lib:
        env["LD_LIBRARY_PATH"] = os.pathsep.join(
            [str(a.gpu_lib), "/usr/local/cuda/lib64", env["LD_LIBRARY_PATH"]]
        )
        env["CUDA_VISIBLE_DEVICES"] = str(a.device)
    log = a.caso / "log.benchmark"
    if log.exists():
        raise FileExistsError(log)
    command = ["simpleFoam", "-case", str(a.caso.resolve())]
    if a.mpi > 1:
        (a.caso / "system/decomposeParDict").write_text(
            "FoamFile {version 2.0; format ascii; class dictionary; object decomposeParDict;}\n"
            f"numberOfSubdomains {a.mpi}; method simple; simpleCoeffs {{n ({a.mpi} 1 1); delta .001;}}\n"
            "distributed no; roots ();\n"
        )
        with (a.caso / "log.decomposePar").open("w") as stream:
            subprocess.run(
                ["decomposePar", "-case", str(a.caso.resolve())],
                env=env,
                stdout=stream,
                stderr=subprocess.STDOUT,
                check=True,
                timeout=300,
            )
        command = ["mpirun", "-np", str(a.mpi), *command, "-parallel"]
    start = time.monotonic()
    gpu_observations = []
    with log.open("w") as stream:
        proc = subprocess.Popen(
            command,
            env=env,
            stdout=stream,
            stderr=subprocess.STDOUT,
        )
        while proc.poll() is None:
            if time.monotonic() - start > 3600:
                proc.kill()
                proc.wait()
                break
            if a.gpu_lib:
                sample = subprocess.run(
                    [
                        "nvidia-smi",
                        "--query-compute-apps=pid,gpu_uuid,used_memory",
                        "--format=csv,noheader,nounits",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    check=False,
                )
                for line in sample.stdout.splitlines():
                    pid = line.split(",", 1)[0].strip()
                    try:
                        cmdline = (
                            Path(f"/proc/{pid}/cmdline")
                            .read_bytes()
                            .replace(b"\x00", b" ")
                            .decode()
                        )
                    except (OSError, UnicodeError):
                        continue
                    if "simpleFoam" in cmdline and str(a.caso.resolve()) in cmdline:
                        gpu_observations.append(
                            {"elapsed_s": time.monotonic() - start, "sample": line}
                        )
            time.sleep(2)
    elapsed = time.monotonic() - start
    text = log.read_text(errors="replace")
    history = [float(v) for v in re.findall(r"Cd:\s+([0-9.eE+-]+)", text)]
    result = {
        "exit_code": proc.returncode,
        "completed": proc.returncode == 0
        and bool(re.search(r"^End\s*$", text, re.MULTILINE)),
        "elapsed_s": elapsed,
        "backend": "CUDA" if a.gpu_lib else "CPU",
        "gpu_device": a.device if a.gpu_lib else None,
        "mpi_ranks": a.mpi,
        "cd_history": history,
        "finite": bool(history) and all(math.isfinite(v) for v in history),
        "validated_cd": None,
        "gpu_process_observations": gpu_observations,
    }
    (a.caso / "benchmark.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result), flush=True)
    if (
        not result["completed"]
        or not result["finite"]
        or (a.gpu_lib and not gpu_observations)
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
