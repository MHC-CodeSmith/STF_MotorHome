"""Render the three open CADs and their actual prepared CFD surfaces."""

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import trimesh
from matplotlib.collections import PolyCollection


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cache", type=Path, required=True)
    p.add_argument("--destino", type=Path, required=True)
    p.add_argument("--casos", type=Path)
    a = p.parse_args()
    specs = [
        (
            "Original downloaded CAD",
            "exterior_original/ducato_exterior_m.glb",
            "original_prepared_parts",
        ),
        (
            "Current modified CAD",
            "modified_reproduced/aurora_L3H2_proposta_m.glb",
            "modified_prepared_parts",
        ),
        (
            "OEM dimension fit (approximate)",
            "revised_oem_v6/ducato_L3H2_ajuste_cotas.glb",
            "revised_open_mirrors_prepared",
        ),
    ]
    a.destino.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(3, 2, figsize=(12, 11), layout="constrained")
    rows = []
    for row, (label, source, closed) in enumerate(specs):
        scene = trimesh.load(a.cache / source, force="scene")
        m = scene.to_mesh()
        r = trimesh.load(a.cache / closed / "aurora_cfd_m.stl", force="mesh")
        manifest = json.loads(
            (a.cache / closed / "manifesto_superficie.json").read_text()
        )
        rows.append(
            {
                "geometry": label,
                "cad_extents_m": m.extents.tolist(),
                "cfd_extents_m": r.extents.tolist(),
                "area_before_m2": manifest["area_before_m2"],
                "area_after_m2": manifest["area_after_m2"],
                "repair_relative_area_change": manifest["relative_area_change"],
            }
        )
        for col, (i, j, title) in enumerate(
            [(0, 2, "Side view"), (1, 2, "Front view")]
        ):
            ax = axes[row, col]
            triangles = m.triangles[:, :, [i, j]]
            ax.add_collection(
                PolyCollection(
                    triangles, facecolor="#4b779d", edgecolor="none", alpha=0.8
                )
            )
            ax.set_aspect("equal")
            ax.set_xlim((-3.8, 2.8) if col == 0 else (-1.5, 1.5))
            ax.set_ylim(-0.05, 2.85)
            ax.set_xlabel("X [m]" if col == 0 else "Y [m]")
            ax.set_ylabel("Z [m]")
            ax.grid(alpha=0.15)
            ax.set_title(label + " — " + title, fontsize=10)
        axes[row, 0].text(
            0.02,
            0.84,
            f"L={m.extents[0]:.3f} m | H={m.extents[2]:.3f} m",
            transform=axes[row, 0].transAxes,
            va="top",
            fontsize=9,
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.85},
        )
        axes[row, 1].text(
            0.02,
            0.84,
            f"CFD frontal area={manifest['area_after_m2']:.3f} m²",
            transform=axes[row, 1].transAxes,
            va="top",
            fontsize=9,
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.85},
        )
    fig.suptitle("Three CAD geometries — identical plotting scale", fontsize=14)
    fig.supxlabel(
        "Derived razor24 / Dogan Ulus, OpenX Assets 20261015 — MPL-2.0 AND CC-BY-4.0. Dimension fit is not OEM CAD.",
        fontsize=8,
    )
    fig.savefig(a.destino / "comparacao_cad.png", dpi=160)
    fig.savefig(a.destino / "comparacao_cad.pdf")
    if a.casos:
        for row in range(3):
            candidates = sorted(
                a.casos.glob(
                    f"{row + 1:02d}_*_b_com_paineis/constant/triSurface/pv.stl"
                )
            )
            if len(candidates) != 1:
                raise RuntimeError("Expected one panel configuration per body")
            pv = trimesh.load(candidates[0], force="mesh")
            for col, (i, j) in enumerate([(0, 2), (1, 2)]):
                axes[row, col].add_collection(
                    PolyCollection(
                        pv.triangles[:, :, [i, j]],
                        facecolor="#e99a28",
                        edgecolor="#754200",
                        linewidth=0.2,
                        alpha=0.9,
                    )
                )
        fig.suptitle(
            "Panel configurations used for CFD — mounting hypothesis", fontsize=14
        )
        fig.savefig(a.destino / "comparacao_cad_paineis.png", dpi=160)
        fig.savefig(a.destino / "comparacao_cad_paineis.pdf")
    plt.close(fig)
    (a.destino / "geometrias_medidas.json").write_text(
        json.dumps(rows, indent=2) + "\n"
    )
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
