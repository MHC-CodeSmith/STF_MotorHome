"""Copy verified meshes into fresh cases with bounded steady-state numerics."""

import argparse
import hashlib
import json
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--origem", type=Path, required=True)
    parser.add_argument("--destino", type=Path, required=True)
    args = parser.parse_args()
    args.destino.mkdir(exist_ok=False, parents=True)
    for source in sorted(args.origem.iterdir()):
        if not (source / "entrada_comparacao.json").exists():
            continue
        marker = json.loads((source / "reuse_verified_mesh.json").read_text())
        for name, digest in marker["mesh_sha256"].items():
            if (
                hashlib.sha256(
                    (source / "constant/polyMesh" / name).read_bytes()
                ).hexdigest()
                != digest
            ):
                raise RuntimeError(f"Mesh hash changed: {source}/{name}")
        case = args.destino / source.name
        case.mkdir()
        shutil.copytree(source / "constant", case / "constant")
        shutil.copytree(source / "system", case / "system")
        (case / "0").mkdir()
        for name in ["U", "p", "k", "omega", "nut"]:
            shutil.copy2(source / "0" / name, case / "0" / name)
        for name in [
            "entrada_comparacao.json",
            "reuse_verified_mesh.json",
            "log.snappyHexMesh",
            "resultado_malha.json",
        ]:
            shutil.copy2(source / name, case / name)
        original = source / "system/fvSolution.cpu"
        text = (
            original if original.exists() else source / "system/fvSolution"
        ).read_text()
        text = text.replace("p .3;", "p .2;").replace(
            "U .7; k .7; omega .7;", "U .3; k .3; omega .3;"
        )
        text = text.replace(
            "solvers {",
            "solvers {\n Phi {solver GAMG; tolerance 1e-8; relTol 0; smoother GaussSeidel;}",
        )
        text += "\npotentialFlow {nNonOrthogonalCorrectors 10;}\n"
        (case / "system/fvSolution").write_text(text)
        path = case / "system/fvSchemes"
        path.write_text(
            path.read_text().replace(
                "default Gauss linear;", "default cellLimited Gauss linear 1;"
            )
        )
        path = case / "system/controlDict"
        path.write_text(
            path.read_text()
            .replace('libs ("libOGL.so");', "")
            .replace("endTime 2000;", "endTime 4000;")
            .replace("writeInterval 200;", "writeInterval 100;")
        )
        path = case / "system/controlDict"
        path.write_text(
            path.read_text().replace(
                "functions {",
                'functions { fieldExtrema {type fieldMinMax; libs ("libfieldFunctionObjects.so"); fields (U p k omega nut); mode magnitude; log yes; writeToFile true; executeControl timeStep; executeInterval 25; writeControl timeStep; writeInterval 25;} ',
                1,
            )
        )
        (case / "recovery_protocol.json").write_text(
            json.dumps(
                {
                    "source": str(source.resolve()),
                    "mesh_changed": False,
                    "geometry_changed": False,
                    "physical_conditions_changed": False,
                    "pressure_relaxation": 0.2,
                    "equation_relaxation": {"U": 0.3, "k": 0.3, "omega": 0.3},
                    "gradient_default": "cellLimited Gauss linear 1",
                    "initialisation": "potentialFoam -initialiseUBCs",
                    "validated_cd": None,
                },
                indent=2,
            )
            + "\n"
        )


if __name__ == "__main__":
    main()
