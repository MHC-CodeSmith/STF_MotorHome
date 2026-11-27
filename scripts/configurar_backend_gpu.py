"""Configure the isolated CUDA linear backend while retaining physical settings."""

from pathlib import Path


def configure(case: Path, tolerance: float = 1e-9, relative: float = 0.001):
    solution = case / "system/fvSolution"
    text = solution.read_text()
    if "solver GKOCG;" in text:
        return
    original = case / "system/fvSolution.cpu"
    original.write_text(text)
    text = text.replace(
        "p {solver GAMG; tolerance 1e-7; relTol .1; smoother GaussSeidel;}",
        "p {solver GKOCG; executor cuda; verbose 0; "
        f"tolerance {tolerance}; relTol {relative}; maxIter 1000; "
        "updateRHS true; updateInitGuess true; adaptMinIter false; forceHostBuffer true; "
        "scaling 1; preconditioner {preconditioner Multigrid; "
        "caching 0; maxLevels 9; minCoarseRows 20;}}",
    ).replace(
        '"(U|k|omega)" {solver smoothSolver; smoother symGaussSeidel; tolerance 1e-7; relTol .1;}',
        '"(U|k|omega)" {solver GKOBiCGStab; executor cuda; verbose 0; '
        f"tolerance {tolerance}; relTol {relative}; maxIter 1000; "
        "updateRHS true; updateInitGuess true; adaptMinIter false; forceHostBuffer true; "
        "preconditioner {preconditioner BJ; maxBlockSize 1; caching 0;}}",
    )
    if "solver GKOCG;" not in text or "solver GKOBiCGStab;" not in text:
        raise RuntimeError(
            "Unexpected CPU dictionaries; refuse incomplete GPU conversion"
        )
    solution.write_text(text)
    control = case / "system/controlDict"
    if 'libs ("libOGL.so");' not in control.read_text():
        control.write_text(control.read_text() + '\nlibs ("libOGL.so");\n')
