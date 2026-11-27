"""Save live campaign status and evidence of the actual CFD GPU processes."""

import argparse
import json
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


def tail(path, limit=200000):
    if not path.exists():
        return ""
    with path.open("rb") as stream:
        stream.seek(max(0, path.stat().st_size - limit))
        return stream.read().decode(errors="replace")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--destino", type=Path, required=True)
    parser.add_argument("--intervalo", type=int, default=30)
    args = parser.parse_args()
    args.destino.mkdir(parents=True, exist_ok=True)
    while True:
        now = datetime.now(timezone.utc).isoformat()
        state = {"updated_utc": now, "validated_cd": None, "phases": {}}
        for phase in ["precision_v1", "precision_v2_refined"]:
            cases = []
            for case in sorted((args.cache / phase).iterdir()):
                if not (case / "entrada_comparacao.json").exists():
                    continue
                row = {"case": case.name, "mesh_verified": False}
                row["mesh_verified"] = (case / "reuse_verified_mesh.json").exists()
                for filename in ["resultado_malha.json", "resultado_execucao.json"]:
                    try:
                        row[filename] = json.loads((case / filename).read_text())
                    except (FileNotFoundError, json.JSONDecodeError):
                        pass
                for logfile, pattern, key in [
                    (
                        "log.snappyHexMesh",
                        r"Layer addition iteration (\d+)",
                        "layer_iteration",
                    ),
                    ("log.simpleFoam", r"^Time = ([0-9.eE+-]+)", "solver_iteration"),
                ]:
                    values = re.findall(pattern, tail(case / logfile), re.MULTILINE)
                    row[key] = float(values[-1]) if values else None
                cases.append(row)
            state["phases"][phase] = cases
        sample = subprocess.run(
            [
                "nvidia-smi",
                "--query-compute-apps=pid,gpu_uuid,used_memory",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        observed = []
        for line in sample.stdout.splitlines():
            pid = line.split(",", 1)[0].strip()
            try:
                command = (
                    Path(f"/proc/{pid}/cmdline")
                    .read_bytes()
                    .replace(b"\0", b" ")
                    .decode()
                )
            except (OSError, UnicodeError):
                continue
            if "simpleFoam" in command and str(args.cache / "precision_") in command:
                observed.append({"sample": line, "command": command})
        state["gpu_processes"] = observed
        if observed:
            with (args.destino / "gpu_process_observations.jsonl").open("a") as stream:
                stream.write(json.dumps({"utc": now, "processes": observed}) + "\n")
        unit = subprocess.run(
            [
                "systemctl",
                "--user",
                "show",
                "stf-aero-gpu-campaign-20261127",
                "--property=ActiveState",
                "--value",
            ],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        state["campaign_service"] = unit.stdout.strip()
        pending = args.destino / "estado_campanha.tmp"
        pending.write_text(json.dumps(state, indent=2) + "\n")
        pending.replace(args.destino / "estado_campanha.json")
        if unit.returncode or state["campaign_service"] not in ["active", "activating"]:
            break
        time.sleep(args.intervalo)


if __name__ == "__main__":
    main()
