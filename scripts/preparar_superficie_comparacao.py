"""Prepare CFD surfaces by part, retaining source CAD, tyres and bounding boxes.

Only the body uses a finite raster reconstruction. Tyres and mirror assemblies
are repaired separately so a body repair cannot silently remove the wheels.
"""

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import pymeshfix
import trimesh

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from motorhome.geometria_malha import area_frontal


def close(mesh):
    mesh = mesh.copy()
    mesh.merge_vertices(digits_vertex=7)
    mesh.update_faces(mesh.unique_faces())
    mesh.update_faces(mesh.nondegenerate_faces())
    mesh.remove_unreferenced_vertices()
    if mesh.is_watertight:
        return mesh
    v, f = pymeshfix.clean_from_arrays(
        np.array(mesh.vertices, dtype=np.float64),
        np.array(mesh.faces, dtype=np.int32),
        verbose=False,
        joincomp=False,
        remove_smallest_components=False,
    )
    result = trimesh.Trimesh(v, f, process=False)
    if not result.is_watertight:
        raise ValueError("Local surface repair did not close a component")
    return result


def projections(mesh):
    values = []
    for axes in [(0, 1, 2), (2, 0, 1), (1, 0, 2)]:
        other = mesh.copy()
        other.vertices = other.vertices[:, axes]
        values.append(area_frontal(other))
    return values


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--entrada", type=Path, required=True)
    p.add_argument("--destino", type=Path, required=True)
    p.add_argument("--passo-m", type=float, default=0.015)
    p.add_argument("--faces", type=int, default=60000)
    a = p.parse_args()
    if not 0.005 <= a.passo_m <= 0.025:
        p.error("Require 0.005–0.025 m raster pitch")
    a.destino.mkdir(parents=True, exist_ok=False)
    s = trimesh.load(a.entrada, force="scene")
    m = s.to_mesh()
    groups = {"body": []}
    for node in s.graph.nodes_geometry:
        transform, key = s.graph[node]
        g = s.geometry[key].copy()
        g.apply_transform(transform)
        if node.startswith("Wheel_"):
            if g.extents[0] > 0.65:
                groups[node] = [g]
        elif node.startswith("Brake_Caliper_"):
            continue
        elif np.max(np.abs(g.bounds[:, 1])) > 1.1:
            side = "left" if g.bounds.mean(0)[1] > 0 else "right"
            groups.setdefault("mirror_" + side, []).append(g)
        else:
            groups["body"].append(g)
    if sum(n.startswith("Wheel_") for n in groups) != 4:
        raise ValueError("Four outer tyres are required")
    start = time.time()
    prepared = []
    stats = []
    for name, parts in groups.items():
        original = trimesh.util.concatenate(parts)
        if name == "body":
            voxels = original.voxelized(a.passo_m)
            voxels.fill()
            candidate = voxels.marching_cubes
            candidate.apply_transform(voxels.transform)
            trimesh.smoothing.filter_taubin(candidate, lamb=0.5, nu=0.53, iterations=8)
            if len(candidate.faces) > a.faces:
                candidate = candidate.simplify_quadric_decimation(face_count=a.faces)
            candidate = close(candidate)
        else:
            candidate = close(original)
        bounds_before_mapping = candidate.bounds.copy()
        if np.max(np.abs(bounds_before_mapping - original.bounds)) > 2 * a.passo_m:
            raise ValueError(
                f"Repair changed {name} bounds by more than two raster cells"
            )
        lo, hi = candidate.bounds.copy()
        if np.any(hi <= lo):
            raise ValueError("Degenerate repaired component")
        candidate.vertices = (candidate.vertices - lo) / (
            hi - lo
        ) * original.extents + original.bounds[0]
        candidate.fix_normals()
        if not candidate.is_watertight:
            raise ValueError("Open surface after bounds mapping")
        candidate.export(a.destino / (name + ".stl"))
        prepared.append(candidate)
        stats.append(
            {
                "part": name,
                "source_bounds_m": original.bounds.tolist(),
                "repair_bounds_before_mapping_m": bounds_before_mapping.tolist(),
                "final_bounds_m": candidate.bounds.tolist(),
                "faces": len(candidate.faces),
                "closed": bool(candidate.is_watertight),
            }
        )
    r = trimesh.util.concatenate(prepared)
    source_areas = projections(m)
    final_areas = projections(r)
    changes = [abs(x - y) / x for x, y in zip(source_areas, final_areas)]
    report = {
        "status": "SUPERFICIE_CFD_DISCRETIZADA_NAO_VALIDADA",
        "source_sha256": hashlib.sha256(a.entrada.read_bytes()).hexdigest(),
        "pitch_m": a.passo_m,
        "cad_bounds_m": m.bounds.tolist(),
        "cfd_bounds_m": r.bounds.tolist(),
        "area_before_m2": source_areas[0],
        "area_after_m2": final_areas[0],
        "relative_area_change": changes[0],
        "projection_order": ["front_YZ", "top_XY", "side_XZ"],
        "source_projection_areas_m2": source_areas,
        "cfd_projection_areas_m2": final_areas,
        "relative_projection_changes": changes,
        "parts": stats,
        "triangles": len(r.faces),
        "watertight": bool(r.is_watertight),
        "elapsed_s": time.time() - start,
        "validated_cd": None,
        "libraries": {
            "trimesh": trimesh.__version__,
            "numpy": np.__version__,
            "pymeshfix": pymeshfix.__version__,
        },
        "limits": [
            "Body details below the raster pitch are not resolved; compare pitch sensitivity.",
            "Small body gaps may be sealed; inspect underside, windows and mirrors.",
            "Bounding-box mapping removes raster inflation but does not prove local surface fidelity.",
            "Tyres and mirrors repaired separately; original CAD retained unchanged.",
        ],
    }
    (a.destino / "manifesto_superficie.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    if not r.is_watertight or not np.allclose(r.bounds, m.bounds, atol=1e-7):
        raise ValueError("Surface rejected: closure or overall bounds")
    if max(changes) > 0.03:
        raise ValueError("Surface rejected: projected silhouette changed by >3%")
    r.export(a.destino / "aurora_cfd_m.stl")
    print(json.dumps(report, indent=2), flush=True)


if __name__ == "__main__":
    main()
