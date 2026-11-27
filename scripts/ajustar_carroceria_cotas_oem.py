"""Prepare three van geometries for the requested comparison; fitted mesh is approximate."""

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import trimesh
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from motorhome.adaptacao_geometrica import mapa_linear_trechos
from motorhome.geometria_malha import area_frontal


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--entrada", type=Path, required=True)
    p.add_argument("--destino", type=Path, required=True)
    a = p.parse_args()
    c = yaml.safe_load(
        (ROOT / "config/arquitetura_eletrica_proposta.yaml").read_text()
    )["chassis"]
    raw = yaml.safe_load((ROOT / "config/parametros_globais.yaml").read_text())
    radius = raw["development"]["performance_envelope"]["wheel_radius_m"]
    s = trimesh.load(a.entrada, force="scene")
    parts = []
    for node in s.graph.nodes_geometry:
        transform, key = s.graph[node]
        mesh = s.geometry[key].copy()
        mesh.apply_transform(transform)
        parts.append((node, mesh))
    tyres = [(n, m) for n, m in parts if n.startswith("Wheel_") and m.extents[0] > 0.65]
    front = np.mean([m.bounds.mean(0)[0] for _, m in tyres if m.bounds.mean(0)[0] > 0])
    rear = np.mean([m.bounds.mean(0)[0] for _, m in tyres if m.bounds.mean(0)[0] < 0])
    allmesh = s.to_mesh()
    # Mirror indicator meshes are named Light_Indicator_* and must also be
    # excluded from a measurement explicitly defined as width without mirrors.
    bodyparts = [
        m
        for n, m in parts
        if not n.startswith(("Wheel_", "Mirror_", "Brake_Caliper_"))
        and np.max(np.abs(m.bounds[:, 1])) < 1.1
    ]
    body = trimesh.util.concatenate(bodyparts)
    xmax = allmesh.bounds[1, 0]
    xf = xmax - 0.948
    xr = xf - c["wheelbase_m"]
    xmin = xmax - c["length_m"]
    # Keep the wheel-arch regions rigid in X. Stretching directly between axle
    # centres distorts half of each arch along with the cargo compartment.
    source_x = [
        allmesh.bounds[0, 0],
        rear - 0.45,
        rear + 0.45,
        front - 0.6,
        front + 0.6,
        xmax,
    ]
    target_x = [xmin, xr - 0.45, xr + 0.45, xf - 0.6, xf + 0.6, xmax]
    width_scale = c["body_width_without_mirrors_m"] / body.extents[1]
    mirror_shift = (c["width_open_mirrors_m"] - allmesh.extents[1]) / 2
    # Nominal free tyre radius is a project assumption, not loaded ride height.
    source_radius = np.mean([m.extents[2] / 2 for _, m in tyres])
    dz = radius - source_radius
    # Approximate the upper side profile from the manufacturer's illustration,
    # normalised by the published length and selected height. A single Z scale
    # stretches the windshield along with the cargo roof and is insufficient.
    profile_path = ROOT / "config/perfil_educato_ilustracao_2026-11-27.json"
    profile = json.loads(profile_path.read_text())
    pixels = np.array(profile["profile_pixels"], dtype=float)
    profile_x = xmin + (
        (pixels[:, 0] - profile["rear_datum_x_px"])
        / (profile["front_datum_x_px"] - profile["rear_datum_x_px"])
        * c["length_m"]
    )
    profile_z = (
        (profile["ground_y_px"] - pixels[:, 1])
        / (profile["ground_y_px"] - profile["roof_y_px"])
        * max(c["height_range_m"])
    )
    source_profile_x = np.linspace(
        body.bounds[0, 0] + 1e-5, body.bounds[1, 0] - 1e-5, 300
    )
    source_profile_z = []
    for x in source_profile_x:
        segments = trimesh.intersections.mesh_plane(
            body, plane_normal=[1, 0, 0], plane_origin=[x, 0, 0]
        )
        source_profile_z.append(
            float(segments[:, :, 2].max()) if len(segments) else 0.0
        )
    z_anchor = 1.35
    fitted = trimesh.Scene()
    checks = []
    for node, mesh in parts:
        v = mesh.vertices.copy()
        if node.startswith(("Wheel_", "Brake_Caliper_")):
            center = mesh.bounds.mean(0)
            is_front = center[0] > 0
            axle_source = front if is_front else rear
            axle_target = xf if is_front else xr
            track_target = c["front_track_m"] if is_front else c["rear_track_m"]
            side = 1 if center[1] > 0 else -1
            # Keep wheel circular; use rigid lateral placement, radial scale.
            sy = side * 0.8981
            v[:, 0] = (v[:, 0] - axle_source) * radius / source_radius + axle_target
            v[:, 2] = (v[:, 2] - source_radius) * radius / source_radius + radius
            v[:, 1] = v[:, 1] - sy + side * track_target / 2
            if node.startswith("Wheel_") and mesh.extents[0] > 0.65:
                checks.append(
                    {
                        "node": node,
                        "center_target_m": [
                            axle_target,
                            side * track_target / 2,
                            radius,
                        ],
                        "radius_m": radius,
                    }
                )
        else:
            source_vx = v[:, 0].copy()
            v[:, 0] = mapa_linear_trechos(v[:, 0], source_x, target_x)
            source_roof = np.interp(source_vx, source_profile_x, source_profile_z)
            target_roof = np.interp(v[:, 0], profile_x, profile_z)
            weight = np.clip(
                (v[:, 2] - z_anchor) / np.maximum(source_roof - z_anchor, 0.1), 0.0, 1.0
            )
            weight[source_roof < z_anchor + 0.1] = 0.0
            v[:, 2] += dz + weight * (target_roof - source_roof - dz)
            v[:, 2] = np.minimum(v[:, 2], max(c["height_range_m"]))
            # Keep housing shape, translate each assembly to match the open
            # mirror width. This fits width only, not the detailed OEM pose.
            if np.max(np.abs(mesh.bounds[:, 1])) < 1.1:
                v[:, 1] *= width_scale
            else:
                v[:, 2] = mesh.vertices[:, 2] + dz
                v[:, 1] += np.sign(mesh.bounds.mean(0)[1]) * mirror_shift
        mesh.vertices = v
        fitted.add_geometry(mesh, node_name=node, geom_name=node)
    a.destino.mkdir(parents=True, exist_ok=False)
    fitted.export(a.destino / "ducato_L3H2_ajuste_cotas.glb")
    m = fitted.to_mesh()
    m.export(a.destino / "ducato_L3H2_ajuste_cotas.stl")
    report = {
        "status": "AJUSTE_DIMENSIONAL_APROXIMADO_NAO_OEM",
        "source_sha256": hashlib.sha256(a.entrada.read_bytes()).hexdigest(),
        "oem_source": "https://www.fiat.sk/content/dam/fiat2023/sk/cenniky/2026/03/e_Ducato_pricelist_dodavka_200326.pdf",
        "source_page": 5,
        "x_source_landmarks_m": source_x,
        "x_target_landmarks_m": target_x,
        "upper_profile_source_x_m": source_profile_x.tolist(),
        "upper_profile_source_z_m": source_profile_z,
        "upper_profile_anchor_z_m": z_anchor,
        "body_vertical_offset_m": float(dz),
        "upper_profile_method": "manually digitised illustration, normalised to official overall dimensions",
        "upper_profile_config_sha256": hashlib.sha256(
            profile_path.read_bytes()
        ).hexdigest(),
        "upper_profile_target_x_m": profile_x.tolist(),
        "upper_profile_target_z_m": profile_z.tolist(),
        "body_width_scale": float(width_scale),
        "open_mirror_width_target_m": c["width_open_mirrors_m"],
        "mirror_lateral_shift_each_side_m": float(mirror_shift),
        "tyres": checks,
        "extents_m": m.extents.tolist(),
        "area_open_m2": area_frontal(m),
        "nominal_body_width_m": c["body_width_without_mirrors_m"],
        "front_overhang_m": 0.948,
        "rear_overhang_m": 1.015,
        "limits": [
            "Manufacturer overall dimensions constrain the mesh; detailed OEM surface sections are unavailable.",
            "Upper side profile follows a manually digitised illustration; transverse sections and detailed windshield, mirrors and underside remain approximate.",
            "Mirror assemblies translated laterally to match 2.690 m width; detailed factory housing, stalk and angular pose are not reconstructed.",
            "Free tyre radius 0.37211 m is the existing project assumption; no loaded tyre model.",
            "No aerodynamic result has been fitted to a target Cd.",
        ],
    }
    (a.destino / "ajuste.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
