"""Extrai cortes de campos realmente calculados; não calcula Cd ou os valida."""

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np
import vtk
from vtk.util.numpy_support import vtk_to_numpy


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--caso', type=Path, required=True)
    p.add_argument('--tempo', type=float, required=True)
    p.add_argument('--destino', type=Path, required=True)
    args = p.parse_args()
    reader = vtk.vtkOpenFOAMReader()
    marker = args.caso/'aurora.foam'
    marker.touch(exist_ok=True)
    reader.SetFileName(str(marker))
    reader.UpdateInformation()
    times = reader.GetTimeValues()
    valid_times = [times.GetValue(i) for i in range(times.GetNumberOfValues())]
    if args.tempo not in valid_times:
        raise ValueError(f'Tempo não disponível: {valid_times}')
    reader.EnableAllCellArrays()
    reader.SetTimeValue(args.tempo)
    reader.Update()
    mesh = reader.GetOutput().GetBlock(0)
    plane = vtk.vtkPlane()
    plane.SetOrigin(0, 0, 0)
    plane.SetNormal(0, 1, 0)
    cutter = vtk.vtkCutter()
    cutter.SetCutFunction(plane)
    cutter.SetInputData(mesh)
    triangle = vtk.vtkTriangleFilter()
    triangle.SetInputConnection(cutter.GetOutputPort())
    triangle.Update()
    cut = triangle.GetOutput()
    points = vtk_to_numpy(cut.GetPoints().GetData())
    faces = vtk_to_numpy(cut.GetPolys().GetData()).reshape(-1, 4)[:, 1:]
    pressure = vtk_to_numpy(cut.GetCellData().GetArray('p'))
    speed = np.linalg.norm(vtk_to_numpy(cut.GetCellData().GetArray('U')), axis=1)
    if not all(np.isfinite(x).all() for x in (pressure, speed)):
        raise ValueError('Campos não finitos')
    inputs = json.loads((args.caso/'entrada_piloto.json').read_text())
    ref = inputs['velocity_m_s']
    cp = pressure/(.5*ref**2)
    args.destino.mkdir(parents=True, exist_ok=False)
    fig, axes = plt.subplots(2, 1, figsize=(11, 8), layout='constrained')
    triangulation = mtri.Triangulation(points[:, 0], points[:, 2], faces)
    for ax, values, label, cmap in zip(axes, [speed, cp], ['Velocidade [m/s]', 'Cp = p/(0,5 Uref²)'], ['viridis', 'coolwarm']):
        im = ax.tripcolor(triangulation, facecolors=values, cmap=cmap, shading='flat')
        fig.colorbar(im, ax=ax, label=label)
        ax.set(xlim=(-8, 6), ylim=(0, 4.5), aspect='equal', xlabel='X [m]', ylabel='Z [m]')
    fig.suptitle('CFD piloto Aurora — corte central Y=0\nCampos calculados, sem validação de malha/parede para Cd')
    fig.savefig(args.destino/'campos_piloto.png', dpi=160)
    plt.close(fig)
    result = {'status': 'PILOTO_NAO_VALIDADO', 'caso': str(args.caso), 'iteracao': args.tempo,
              'cells': mesh.GetNumberOfCells(), 'u_max_m_s': float(speed.max()),
              'cp_min_slice': float(cp.min()), 'cp_max_slice': float(cp.max()),
              'cd': None, 'pressure_is_kinematic_m2_s2': True,
              'vtk_version': vtk.vtkVersion.GetVTKVersion(),
              'script': 'scripts/visualizar_cfd_piloto.py',
              'solver_log_sha256': hashlib.sha256((args.caso/'log.simpleFoam.fields').read_bytes()).hexdigest()}
    (args.destino/'resumo_cfd_piloto.json').write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
