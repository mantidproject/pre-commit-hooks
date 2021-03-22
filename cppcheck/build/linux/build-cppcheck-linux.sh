#!/bin/bash
# Compiles Cppcheck
set -ex

# tarballs
CPPCHECK=https://github.com/danmar/cppcheck/archive/2.3.tar.gz
TAR_FILE=$(basename ${CPPCHECK})

# extract source
mkdir cppcheck
cd cppcheck
wget --quiet ${CPPCHECK}
tar --extract --gz --strip-components=1 --file ${TAR_FILE}
# patch CMakeLists.txt to statically link to libgcc and libstdc++ to clang-format exe
sed -i -e 's@${CLANG_FORMAT_LIB_DEPS}@${CLANG_FORMAT_LIB_DEPS} -static-libgcc -static-libstdc++@' CMakeLists.txt

# build
cd ..
mkdir cppcheck-build
cd cppcheck-build
cmake ../cppcheck \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_GUI=OFF \
    -DHAVE_RULES=OFF \
    -DUSE_MATCHCOMPILER=ON
cmake --build .

# Move binary
mv bin/cppcheck ../../../bin/cppcheck-linux-64
cd ..

# Cleanup
rm -rf cppcheck
rm -rf ${TAR_FILE}
rm -rf cppcheck-build