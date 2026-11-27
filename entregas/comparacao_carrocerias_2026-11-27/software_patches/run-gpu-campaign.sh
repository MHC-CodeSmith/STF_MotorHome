#!/bin/bash
set -eu
export XDG_RUNTIME_DIR=/run/user/1000
base=/home/hipolito/stf-aero-cache
cd /home/hipolito/stf-aero-review
out=/home/hipolito/stf-aero-review/entregas/comparacao_carrocerias_2026-11-27
while [ ! -f "$base/gpu_backend_benchmark/gpu0/benchmark.json" ] || [ ! -f "$base/gpu_backend_benchmark/gpu1/benchmark.json" ]; do
    state=$(systemctl --user show stf-aero-gpu-benchmarks-20261127 --property=ActiveState --value)
    if [ "$state" = failed ]; then
        echo 'GPU benchmark service failed. Campaign held.'
        exit 1
    fi
    sleep 15
done
"$base/venv/bin/python" scripts/comparar_backends_cfd.py --benchmark "$base/gpu_backend_benchmark" --gpu-lib "$base/software/ogl-install/lib" --destino "$out/backend_benchmark" --aprovacao "$base/gpu_backend_approved.json"
"$base/venv/bin/python" scripts/executar_comparacao_carrocerias.py --casos "$base/precision_v1" --prefixo "$base/software/openfoam2412" --gpu-lib "$base/software/ogl-install/lib" --workers 2 --mpi 2 --aguardar-malha --timeout-s 86400
"$base/venv/bin/python" scripts/coletar_comparacao_carrocerias.py --casos "$base/precision_v1" --destino "$out/v1"
"$base/venv/bin/python" scripts/preparar_malhas_campanha.py --casos "$base/precision_v2_refined" --prefixo "$base/software/openfoam2412" &
mesh_job=$!
"$base/venv/bin/python" scripts/executar_comparacao_carrocerias.py --casos "$base/precision_v2_refined" --prefixo "$base/software/openfoam2412" --gpu-lib "$base/software/ogl-install/lib" --workers 2 --mpi 2 --aguardar-malha --timeout-s 86400
wait "$mesh_job"
"$base/venv/bin/python" scripts/coletar_comparacao_carrocerias.py --casos "$base/precision_v2_refined" --destino "$out/v2_refined"
"$base/venv/bin/python" scripts/comparar_refinamentos_cfd.py --inicial "$out/v1/resumo.json" --refinada "$out/v2_refined/resumo.json" --destino "$out"
