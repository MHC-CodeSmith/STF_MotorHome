"""Compare backend timings and coefficient trajectories; do not validate vehicle Cd."""

import argparse
import gzip
import hashlib
import json
import shutil
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--benchmark", type=Path, required=True)
    p.add_argument("--gpu-lib", type=Path, required=True)
    p.add_argument("--destino", type=Path, required=True)
    p.add_argument("--aprovacao", type=Path, required=True)
    a = p.parse_args()
    cpu = json.loads((a.benchmark / "cpu_mpi2/benchmark.json").read_text())
    rows = []
    histories = {"CPU MPI2": cpu["cd_history"]}
    for label in ["gpu0", "gpu1"]:
        gpu = json.loads((a.benchmark / label / "benchmark.json").read_text())
        histories[label] = gpu["cd_history"]
        same_count = len(cpu["cd_history"]) == len(gpu["cd_history"]) == 40
        deviation = (
            max(
                abs(x - y) / max(abs(x), 1e-12)
                for x, y in zip(cpu["cd_history"][-10:], gpu["cd_history"][-10:])
            )
            if same_count
            else None
        )
        passed = (
            cpu["completed"]
            and gpu["completed"]
            and cpu["finite"]
            and gpu["finite"]
            and same_count
            and deviation < 0.005
            and bool(gpu["gpu_process_observations"])
        )
        rows.append(
            {
                "device": label,
                "cpu_mpi2_s": cpu["elapsed_s"],
                "gpu_mpi2_s": gpu["elapsed_s"],
                "observed_speedup": cpu["elapsed_s"] / gpu["elapsed_s"],
                "max_relative_cd_difference_last10": deviation,
                "check_passed": passed,
            }
        )
    result = {
        "backend_checks": rows,
        "all_passed": all(r["check_passed"] for r in rows),
        "physical_validation": False,
        "validated_cd": None,
        "scope": "40-iteration same-mesh backend comparison on a shared workstation; these coefficients are not production CFD results.",
        "libogl_sha256": hashlib.sha256(
            (a.gpu_lib / "libOGL.so").read_bytes()
        ).hexdigest(),
        "libginkgo_sha256": hashlib.sha256(
            (a.gpu_lib / "libginkgo.so").read_bytes()
        ).hexdigest(),
    }
    a.destino.mkdir(parents=True, exist_ok=True)
    for label in ["cpu", "cpu_mpi2", "gpu0", "gpu1"]:
        source = a.benchmark / label
        target = a.destino / label
        target.mkdir(exist_ok=True)
        shutil.copy2(source / "benchmark.json", target / "benchmark.json")
        for name in ["log.benchmark", "log.decomposePar"]:
            if (source / name).exists():
                with (
                    (source / name).open("rb") as src,
                    gzip.open(target / (name + ".gz"), "wb") as dst,
                ):
                    shutil.copyfileobj(src, dst)
        shutil.copytree(source / "system", target / "system", dirs_exist_ok=True)
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")
    for label, values in histories.items():
        axes[0].plot(range(31, 41), values[-10:], marker=".", label=label)
    axes[0].set(xlabel="Iteration", ylabel="Diagnostic Cd", title="Backend agreement")
    axes[0].legend()
    axes[0].grid(alpha=0.2)
    axes[1].bar(
        ["CPU MPI2", "GPU 0", "GPU 1"],
        [cpu["elapsed_s"], *[r["gpu_mpi2_s"] for r in rows]],
    )
    axes[1].set(ylabel="Elapsed time [s]", title="40 iterations, shared workstation")
    fig.suptitle("Backend check: not a production Cd or vehicle validation")
    fig.savefig(a.destino / "comparacao_backends.png", dpi=160)
    fig.savefig(a.destino / "comparacao_backends.pdf")
    plt.close(fig)
    (a.destino / "resumo.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if not result["all_passed"]:
        raise SystemExit("CUDA backend checks failed; do not start campaign")
    a.aprovacao.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
