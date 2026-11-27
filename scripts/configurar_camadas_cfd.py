"""Configure smooth Laplacian mesh shrinking and prevent collapsed layer stacks."""

from pathlib import Path


def configure(case: Path):
    path = case / "system/snappyHexMeshDict"
    text = path.read_text()
    if "meshShrinker displacementMotionSolver;" not in text:
        text = text.replace(
            "addLayersControls {",
            """addLayersControls {
 meshShrinker displacementMotionSolver;
 solver displacementLaplacian;
 displacementLaplacianCoeffs {diffusivity quadratic inverseDistance (ground "(aurora|pv).*");}
""",
        )
    text = text.replace("minThickness .0001;", "minThickness .003;")
    text = text.replace("relativeSizes false;", "relativeSizes true;")
    text = text.replace("firstLayerThickness .001;", "finalLayerThickness .3;")
    text = text.replace("nSurfaceLayers 8;", "nSurfaceLayers 5;")
    text = text.replace("minThickness .003;", "minThickness .1;")
    text = text.replace("nGrow 1;", "nGrow 0;")
    text = text.replace("nRelaxIter 3;", "nRelaxIter 10;")
    text = text.replace("nSmoothSurfaceNormals 1;", "nSmoothSurfaceNormals 3;")
    text = text.replace("nSmoothNormals 3;", "nSmoothNormals 5;")
    text = text.replace("nSmoothThickness 10;", "nSmoothThickness 20;")
    text = text.replace("nBufferCellsNoExtrude 0;", "nBufferCellsNoExtrude 1;")
    text = text.replace("nLayerIter 50;", "nLayerIter 30; nRelaxedIter 30;")
    text = text.replace("relaxed {maxNonOrtho 75;}", "relaxed {maxNonOrtho 65;}")
    text = text.replace(
        "writeFlags (scalarLevels);", "writeFlags (scalarLevels layerSets layerFields);"
    )
    path.write_text(text)
    path = case / "system/fvSolution"
    text = path.read_text()
    if "cellDisplacement {" not in text:
        text = text.replace(
            "solvers {",
            "solvers {\n cellDisplacement {solver GAMG; smoother GaussSeidel; tolerance 1e-8; relTol .01; minIter 5; maxIter 200;}\n",
            1,
        )
    path.write_text(text)
    path = case / "system/fvSchemes"
    text = path.read_text()
    if "laplacian(diffusivity,cellDisplacement)" not in text:
        text = text.replace(
            "laplacianSchemes {",
            "laplacianSchemes {laplacian(diffusivity,cellDisplacement) Gauss linear corrected; ",
            1,
        )
    path.write_text(text)
