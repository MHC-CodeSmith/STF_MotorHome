"""Generate bounded CFD meshes ahead of GPU solves and publish verified hashes."""

import argparse
import hashlib
import json
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from executar_openfoam import ambiente


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--casos", type=Path, required=True)
    p.add_argument("--prefixo", type=Path, required=True)
    p.add_argument("--inicio", type=int, default=0)
    p.add_argument("--fim", type=int)
    p.add_argument("--apenas-verificar", action="store_true")
    p.add_argument("--workers", type=int, default=2, choices=[1, 2, 4])
    a = p.parse_args()
    env = ambiente(a.prefixo)
    cases = [
        c for c in sorted(a.casos.iterdir()) if (c / "entrada_comparacao.json").exists()
    ][a.inicio : a.fim]

    def prepare(case):
        result = {"case": case.name, "started_unix": time.time()}
        stages = (
            []
            if a.apenas_verificar
            else [("blockMesh", []), ("snappyHexMesh", ["-overwrite"])]
        )
        if (case / "resume_snapped.json").exists() and not a.apenas_verificar:
            stages = [
                ("checkMesh_snapped_resume", []),
                ("snappyHexMesh", ["-overwrite"]),
            ]
        stages.append(("checkMesh_prepared", []))
        for label, args in stages:
            tool = "checkMesh" if label.startswith("checkMesh") else label
            log = case / ("log." + label)
            if log.exists():
                raise FileExistsError(log)
            start = time.monotonic()
            with log.open("w") as stream:
                try:
                    proc = subprocess.run(
                        [tool, "-case", str(case.resolve()), *args],
                        env=env,
                        stdout=stream,
                        stderr=subprocess.STDOUT,
                        timeout=21600,
                        check=False,
                    )
                    code = proc.returncode
                except subprocess.TimeoutExpired:
                    code = -999
            result[label] = {
                "exit_code": code,
                "elapsed_s": time.monotonic() - start,
            }
            text = log.read_text(errors="replace")
            valid = code == 0 and bool(re.search(r"^End\s*$", text, re.MULTILINE))
            if label.startswith("checkMesh"):
                valid = valid and "Mesh OK." in text
            if label == "snappyHexMesh":
                valid = valid and "reached limit" not in text.lower()
            result["last_stage_passed"] = valid
            (case / "resultado_malha.json").write_text(
                json.dumps(result, indent=2) + "\n"
            )
            print(
                json.dumps(
                    {
                        "case": case.name,
                        "stage": label,
                        "passed": valid,
                        **result[label],
                    }
                ),
                flush=True,
            )
            if not valid:
                return False
        snappy = (case / "log.snappyHexMesh").read_text(errors="replace")
        if (
            not re.search(r"^End\s*$", snappy, re.MULTILINE)
            or "reached limit" in snappy.lower()
        ):
            return False
        marker = {
            "check_mesh_log": "log.checkMesh_prepared",
            "verified_unix": time.time(),
            "mesh_sha256": {
                f.name: hashlib.sha256(f.read_bytes()).hexdigest()
                for f in sorted((case / "constant/polyMesh").iterdir())
                if f.is_file()
            },
        }
        marker_path = case / "reuse_verified_mesh.json"
        pending = marker_path.with_suffix(".tmp")
        pending.write_text(json.dumps(marker, indent=2) + "\n")
        pending.replace(marker_path)
        return True

    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        results = list(pool.map(prepare, cases))
    if not all(results):
        raise SystemExit("Mesh preparation failed; preserve logs and inspect")


if __name__ == "__main__":
    main()
