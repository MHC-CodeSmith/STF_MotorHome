#!/bin/bash
set -eu
base=/home/hipolito/stf-aero-cache/software
export WM_PROJECT_DIR="$base/openfoam2412"
export FOAM_SRC="$base/openfoam-source-extract/usr/lib/openfoam/openfoam2412/src"
export FOAM_LIBBIN="$WM_PROJECT_DIR/platforms/linux64GccDPInt32Opt/lib"
export FOAM_USER_LIBBIN="$base/ogl-install/lib"
export FOAM_MPI=sys-openmpi WM_LABEL_SIZE=32 WM_PRECISION_OPTION=DP
export PATH="/usr/local/cuda/bin:$PATH"
export LD_LIBRARY_PATH="$FOAM_LIBBIN/sys-openmpi:$FOAM_LIBBIN/dummy:$FOAM_LIBBIN:/usr/local/cuda/lib64:${LD_LIBRARY_PATH:-}"
export CMAKE_BUILD_PARALLEL_LEVEL=2
mkdir -p "$FOAM_USER_LIBBIN"
cmake -S "$base/ginkgo-fc86d48b78cebd2b2c5833a2dcf0fe40f615cf19" -B "$base/Ginkgo-build" -DCMAKE_BUILD_TYPE=Release -DGINKGO_BUILD_CUDA=ON -DGINKGO_BUILD_OMP=OFF -DGINKGO_BUILD_MPI=ON -DGINKGO_BUILD_TESTS=OFF -DGINKGO_BUILD_EXAMPLES=OFF -DGINKGO_BUILD_BENCHMARKS=OFF -DGINKGO_BUILD_HWLOC=OFF -DGINKGO_ENABLE_HALF=OFF -DGINKGO_FORCE_GPU_AWARE_MPI=OFF -DCMAKE_CUDA_ARCHITECTURES=86 -DCMAKE_CUDA_COMPILER=/usr/local/cuda/bin/nvcc -DCMAKE_INSTALL_PREFIX="$base/ogl-install" -DBUILD_SHARED_LIBS=ON -DCMAKE_CXX_STANDARD=17
cmake --build "$base/Ginkgo-build" --parallel 2
cmake --install "$base/Ginkgo-build"
cmake -S "$base/OGL" -B "$base/OGL-build-local" -DCMAKE_BUILD_TYPE=Release -DOGL_USE_EXTERNAL_GINKGO=ON -DGinkgo_DIR="$base/ogl-install/lib/cmake/Ginkgo" -DGINKGO_BUILD_CUDA=ON -DGINKGO_BUILD_OMP=OFF -DGINKGO_FORCE_GPU_AWARE_MPI=OFF -DOGL_CUDA_ARCHITECTURES=86 -DCMAKE_INSTALL_PREFIX="$base/ogl-install"
cmake --build "$base/OGL-build-local" --parallel 2
cmake --install "$base/OGL-build-local"
