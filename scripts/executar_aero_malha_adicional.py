"""One additional equipped-CFD grid with finer background and surfaces.

The result extends the numerical trend only. The wake refinement remains
locally fixed, so this case alone cannot establish a formal GCI/grid family.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

import numpy as np
import trimesh
import yaml
from executar_openfoam import ambiente

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path("/home/mhc/motorhome_referencias_tarefas")
SOURCE_NAME = "cfd-aurora-refino-semcamadas-02"


def run(command: list[str], case: Path, env: dict[str, str], timeout_s: int, log: str) -> int:
    try:
        with (case / log).open("w") as stream:
            return subprocess.run(command + ["-case", str(case)], env=env,
                                  stdout=stream, stderr=subprocess.STDOUT,
                                  timeout=timeout_s, check=False).returncode
    except subprocess.TimeoutExpired:
        return -999


def main() -> None:
    raw = yaml.safe_load((ROOT / "config/parametros_globais.yaml").read_text())
    verification = raw["development"]["equipped_aero_verification"]
    roof = raw["development"]["roof_maxeon_comparison"]
    source = CACHE / SOURCE_NAME
    out = ROOT / "entregas/aero_equipado1540/malha_adicional_1"
    out.mkdir(parents=True, exist_ok=False)
    case = out / "case"
    case.mkdir()
    for folder in ("0", "constant", "system"):
        shutil.copytree(source / folder, case / folder)
    shutil.rmtree(case / "constant/polyMesh")
    for name in ("cellLevel", "pointLevel"):
        for path in (case / "0").glob(name + "*"):
            path.unlink()

    # Refine all background dimensions by 20%, and both the body/deck surface
    # levels. The wake-region level is left as the documented source setting.
    block = case / "system/blockMeshDict"
    block_text = block.read_text()
    if "(55 20 10)" not in block_text:
        raise ValueError("Base block mesh differs from the source audited for this refinement")
    block.write_text(block_text.replace("(55 20 10)", "(66 24 12)"))
    snappy = case / "system/snappyHexMeshDict"
    text = snappy.read_text()
    text = text.replace("maxLocalCells 400000; maxGlobalCells 400000;",
                        "maxLocalCells 650000; maxGlobalCells 650000;")
    text = text.replace("level (4 5);", "level (5 6);")
    if "level (5 6);" not in text:
        raise ValueError("Could not set the intended finer surface refinement")
    text = text.replace("geometry {", "geometry {pvdeck.stl {type triSurfaceMesh; name pvdeck;}")
    text = text.replace("refinementSurfaces {", "refinementSurfaces {pvdeck {level (5 6); patchInfo {type wall;}}")
    snappy.write_text(text)

    body = trimesh.load(case / "constant/triSurface/aurora.stl")
    dims = [4 * roof["module_dimensions_m"][0] + 3 * roof["gap_m"],
            roof["module_dimensions_m"][1], roof["module_dimensions_m"][2]]
    low = [body.bounds[0, 0] + roof["end_margin_m"], -dims[1] / 2,
           body.bounds[1, 2] + verification["panel_gap_above_body_m"]]
    panel = trimesh.creation.box(extents=dims)
    panel.apply_translation(np.asarray(low) + np.asarray(dims) / 2)
    panel.export(case / "constant/triSurface/pvdeck.stl")

    # Add the deck as a no-slip wall to all fields and force coefficient data.
    for field in (case / "0").iterdir():
        if field.is_file():
            field.write_text(field.read_text().replace('"aurora.*"', '"(aurora|pvdeck).*"'))
    control = case / "system/controlDict"
    control.write_text(control.read_text().replace(
        'patches ("aurora.*")', 'patches ("(aurora|pvdeck).*")'
    ).replace("endTime 1200;", f"endTime {verification['max_iterations']};"))

    env = ambiente(CACHE / "software/openfoam2412-local/usr/lib/openfoam/openfoam2412")
    mesh_timeout = max(verification["mesh_timeout_s"], 600)
    solver_timeout = max(verification["solver_timeout_s"], 600)
    result: dict[str, object] = {
        "source_case": SOURCE_NAME,
        "source_snappy_sha256": hashlib.sha256((source / "system/snappyHexMeshDict").read_bytes()).hexdigest(),
        "block_mesh_dimensions": [66, 24, 12],
        "surface_levels_body_deck": [5, 6],
        "wake_refinement_changed": False,
        "grid_independence_claimed": False,
        "validated_cd": None,
        "physical_validation": False,
        "block_mesh_exit": run(["blockMesh"], case, env, 120, "log.blockMesh"),
    }
    if result["block_mesh_exit"] == 0:
        result["snappy_exit"] = run(["snappyHexMesh", "-overwrite"], case, env,
                                    mesh_timeout, "log.snappyHexMesh")
    else:
        result["snappy_exit"] = None
    if result["snappy_exit"] == 0:
        result["check_mesh_exit"] = run(["checkMesh"], case, env, 120, "log.checkMesh")
        mesh_log = (case / "log.checkMesh").read_text(errors="replace")
        match = re.search(r"cells:\s+(\d+)", mesh_log)
        result["cell_count"] = int(match.group(1)) if match else None
        result["mesh_ok"] = "Mesh OK." in mesh_log
        if result["mesh_ok"]:
            result["solver_exit"] = run(["simpleFoam"], case, env, solver_timeout,
                                         "log.simpleFoam")
            log = (case / "log.simpleFoam").read_text(errors="replace")
            coefficients = [float(x) for x in re.findall(r"Cd:\s+([\deE.+-]+)", log)]
            result["solver_converged"] = "SIMPLE solution converged" in log
            result["last_cd_diagnostic"] = coefficients[-1] if coefficients else None
            result["last50_cd_relative_span"] = (
                (max(coefficients[-50:]) - min(coefficients[-50:])) /
                max(abs(float(np.mean(coefficients[-50:]))), 1e-12)
                if len(coefficients) >= 50 else None
            )
            result["finite_coefficients"] = bool(coefficients and np.isfinite(coefficients).all())
            if result["solver_exit"] == 0:
                result["yplus_exit"] = run(
                    ["simpleFoam", "-postProcess", "-func", "yPlus", "-latestTime"],
                    case, env, 120, "log.yPlus"
                )
                ylog = (case / "log.yPlus").read_text(errors="replace")
                result["yplus_summary"] = {
                    row[0]: [float(value) for value in row[1:]]
                    for row in re.findall(
                        r"patch (\w+) y\+ : min = ([\deE.+-]+), max = ([\deE.+-]+), average = ([\deE.+-]+)", ylog
                    )
                }

    (out / "resumo.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
