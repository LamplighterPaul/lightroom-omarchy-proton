#!/bin/bash
set -euo pipefail
# Run inside the pinned Steam Runtime SDK after GE's preparation and our patches.
source_root=${1:?source root required}
build_root=${2:?build directory required}
cd "$source_root/wine"
if [[ ! -f include/wine/vulkan.h ]]; then
  XDG_CACHE_HOME="$build_root" dlls/winevulkan/make_vulkan
  tools/make_specfiles
fi
mkdir -p "$build_root"
cd "$build_root"
if [[ ! -f Makefile ]]; then
  "$source_root/wine/configure" --enable-win64 --enable-archs=x86_64,i386 \
    --disable-tests --without-ffmpeg --without-gstreamer --without-opencl \
    --without-vkd3d --without-oss --without-sane --without-v4l2
fi
make -j8 __tooldeps__
make -j8 dlls/advapi32/x86_64-windows/advapi32.dll \
  dlls/advapi32/i386-windows/advapi32.dll \
  dlls/shcore/x86_64-windows/shcore.dll \
  dlls/shcore/i386-windows/shcore.dll \
  dlls/d2d1/x86_64-windows/d2d1.dll \
  dlls/d2d1/i386-windows/d2d1.dll \
  dlls/hnetcfg/x86_64-windows/hnetcfg.dll \
  dlls/hnetcfg/i386-windows/hnetcfg.dll \
  dlls/win32u/win32u.so
