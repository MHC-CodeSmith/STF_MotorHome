"""Prepare matched bare-body CFD cases from explicit supplied surfaces."""

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import trimesh
from configurar_camadas_cfd import configure as configure_layers

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--geometrias",
        type=Path,
        required=True,
        help="JSON mapping names to STL paths and their frontal areas",
    )
    p.add_argument("--destino", type=Path, required=True)
    p.add_argument("--com-e-sem-paineis", action="store_true")
    p.add_argument("--divisoes", type=int, nargs=3, default=[55, 20, 10])
    p.add_argument("--max-celulas", type=int, default=3000000)
    a = p.parse_args()
    inputs = json.loads(a.geometrias.read_text())
    a.destino.mkdir(parents=True, exist_ok=False)
    expanded = {}
    for name, spec in inputs.items():
        expanded[name + "_a_sem_paineis"] = {**spec, "panels": False}
        if a.com_e_sem_paineis:
            expanded[name + "_b_com_paineis"] = {**spec, "panels": True}
    for name, spec in expanded.items():
        case = a.destino / name
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/preparar_cfd_piloto.py"),
                "--superficie",
                spec["stl"],
                "--area-m2",
                str(spec["area_m2"]),
                "--destino",
                str(case),
                "--nivel",
                "4",
            ],
            check=True,
        )
        snappy = case / "system/snappyHexMeshDict"
        block = case / "system/blockMeshDict"
        block.write_text(
            block.read_text().replace(
                "(55 20 10)", "(" + " ".join(map(str, a.divisoes)) + ")"
            )
        )
        text = snappy.read_text()
        text = text.replace(
            "maxLocalCells 400000; maxGlobalCells 400000;",
            f"maxLocalCells {a.max_celulas}; maxGlobalCells {a.max_celulas};",
        )
        text = text.replace("level (4 5)", "level (5 6)")
        text = text.replace("levels ((1E15 1))", "levels ((1E15 3))")
        text = text.replace("addLayers false;", "addLayers true;")
        text = text.replace(
            "relativeSizes true; layers {};",
            'relativeSizes false; layers {"aurora.*" {nSurfaceLayers 8;} ground {nSurfaceLayers 8;}}',
        )
        text = text.replace("finalLayerThickness .3;", "firstLayerThickness .001;")
        text = text.replace("minThickness .1;", "minThickness .0001;")
        body = trimesh.load(spec["stl"], force="mesh")
        lo = [float(body.bounds[0, 0]) + 0.025, -0.845, float(body.bounds[1, 2]) + 0.04]
        boxes = []
        gap_geometry, gap_refinement = [], []
        for i in range(4):
            panel = trimesh.creation.box(extents=[1.046, 1.690, 0.040])
            panel.apply_translation(np.asarray(lo) + [i * 1.066 + 0.523, 0.845, 0.020])
            boxes.append(panel)
            if i < 3:
                x = lo[0] + i * 1.066 + 1.046
                gap_geometry.append(
                    f"moduleGap{i} {{type searchableBox; min ({x - 0.02} -.9 {lo[2] - 0.02}); "
                    f"max ({x + 0.04} .9 {lo[2] + 0.06});}}"
                )
                gap_refinement.append(
                    f"moduleGap{i} {{mode inside; levels ((1E15 8));}}"
                )
        # Retain these regions in the bare-body case too, so removing the panels
        # does not also remove all local refinement around their gaps.
        text = text.replace("geometry {", "geometry {" + "\n".join(gap_geometry), 1)
        text = text.replace(
            "refinementRegions {", "refinementRegions {" + "\n".join(gap_refinement), 1
        )
        if spec["panels"]:
            trimesh.util.concatenate(boxes).export(case / "constant/triSurface/pv.stl")
            text = text.replace(
                "geometry {", "geometry {pv.stl {type triSurfaceMesh; name pv;}", 1
            )
            text = text.replace(
                "refinementSurfaces {",
                "refinementSurfaces {pv {level (5 6); patchInfo {type wall;}}",
                1,
            )
            text = text.replace(
                '"aurora.*" {nSurfaceLayers 8;}', '"(aurora|pv).*" {nSurfaceLayers 8;}'
            )
            for field in (case / "0").iterdir():
                field.write_text(
                    field.read_text().replace('"aurora.*"', '"(aurora|pv).*"')
                )
        snappy.write_text(text)
        schemes = case / "system/fvSchemes"
        schemes.write_text(
            schemes.read_text().replace(
                "div(phi,U) bounded Gauss upwind;",
                "div(phi,U) bounded Gauss linearUpwind grad(U);",
            )
        )
        control = case / "system/controlDict"
        control.write_text(control.read_text().replace("endTime 600;", "endTime 2000;"))
        if spec["panels"]:
            control.write_text(
                control.read_text().replace('"aurora.*"', '"(aurora|pv).*"')
            )
        solution = case / "system/fvSolution"
        solution.write_text(
            solution.read_text().replace(
                'residualControl {p 1e-4; U 1e-5; "(k|omega)" 1e-5;}',
                'residualControl {p 1e-5; U 1e-6; "(k|omega)" 1e-6;}',
            )
        )
        configure_layers(case)
        manifest = json.loads((case / "entrada_piloto.json").read_text())
        manifest.update(
            status="COMPARACAO_PREPARADA_NAO_EXECUTADA",
            geometry_name=name,
            input_geometry=spec,
            surface_levels=[5, 6],
            requested_layers=5,
            first_layer_m=None,
            final_layer_relative=0.3,
            expansion_ratio=1.2,
            velocity_convection="bounded Gauss linearUpwind grad(U)",
            wheel_rotation=False,
            panel_present=spec["panels"],
            panel_dimensions_m=[1.046, 1.690, 0.040],
            panel_count=4,
            panel_gaps_m=0.020,
            roof_clearance_m=0.040,
            panel_minimum_corner_m=lo,
            panel_supports_modelled=False,
            panel_fit_to_original_short_body_verified=False,
            matched_settings=True,
            validated_cd=None,
            background_divisions=a.divisoes,
            maximum_cells=a.max_celulas,
            mesh_shrinker="displacementMotionSolver/displacementLaplacian",
            minimum_layer_stack_relative=0.1,
        )
        (case / "entrada_comparacao.json").write_text(
            json.dumps(manifest, indent=2) + "\n"
        )


if __name__ == "__main__":
    main()
