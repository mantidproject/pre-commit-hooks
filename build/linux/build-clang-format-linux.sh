#!/bin/bash
# Compiles a statically-linked clang-format exe for 64-bit linux
set -ex

# functions
function download_and_extract_xz {
  _url=$1
  wget --quiet ${_url}
  tar --extract --xz --strip-components=1 --file $(basename ${_url})
}

# tarballs
LLVM_SRC_TXZ=https://github.com/llvm/llvm-project/releases/download/llvmorg-9.0.1/llvm-9.0.1.src.tar.xz
CLANG_SRC_TGZ=https://github.com/llvm/llvm-project/releases/download/llvmorg-9.0.1/clang-9.0.1.src.tar.xz

# extract source
mkdir -p llvm/tools/clang
mkdir llvm-build
pushd llvm
download_and_extract_xz ${LLVM_SRC_TXZ}
cd tools/clang
download_and_extract_xz ${CLANG_SRC_TGZ}
# patch CMakeLists.txt to statically link to libgcc and libstdc++ to clang-format exe
sed -i -e 's@${CLANG_FORMAT_LIB_DEPS}@${CLANG_FORMAT_LIB_DEPS} -static-libgcc -static-libstdc++@' tools/clang-format/CMakeLists.txt
popd

# build
cd llvm-build
CC=clang CXX=clang++ cmake \
  -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DLLVM_ENABLE_ASSERTIONS=OFF \
  -DLLVM_ENABLE_THREADS=OFF \
  -DLLVM_ENABLE_TERMINFO=OFF \
  -DLIBCLANG_BUILD_STATIC=ON \
  -DCLANG_ENABLE_STATIC_ANALYZER=OFF \
  -DCLANG_ENABLE_ARCMT=OFF \
  ../llvm/
cmake --build . --target clang-format
strip bin/clang-format
