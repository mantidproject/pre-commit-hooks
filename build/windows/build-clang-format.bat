@setlocal enableextensions
:: build statically linked executable

:: enable VC environment. activates cmake, ninja
call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvarsall.bat" amd64
:: assume 7z is installed in standard path
set PATH=C:\Program Files\7-Zip;%PATH%
set SCRIPTDIR=%~dp0
set LLVM_RELEASES_URL=https://github.com/llvm/llvm-project/releases/download/llvmorg-9.0.1
set LLVM_TGZ=llvm-9.0.1.src.tar.xz
set CLANG_TGZ=clang-9.0.1.src.tar.xz

:: sources
del /Q %LLVM_TGZ%
rmdir /S /Q llvm
rmdir /S /Q llvm-build
mkdir llvm-build
curl -L %LLVM_RELEASES_URL%/%LLVM_TGZ% -o %LLVM_TGZ%
call:extract-tgz %LLVM_TGZ%
move %LLVM_TGZ:~0,-7% llvm
cd llvm\tools
curl -L %LLVM_RELEASES_URL%/%CLANG_TGZ% -o %CLANG_TGZ%
call:extract-tgz %CLANG_TGZ%
move %CLANG_TGZ:~0,-7% clang

:: build
cd ..\..\llvm-build
set CC=cl
set CXX=cl
cmake ^
  -G Ninja ^
  -DCMAKE_BUILD_TYPE=Release ^
  -DLLVM_USE_CRT_RELEASE=MT ^
  -DLLVM_ENABLE_ASSERTIONS=OFF ^
  -DLLVM_ENABLE_THREADS=OFF ^
  -DLLVM_ENABLE_TERMINFO=OFF ^
  -DLIBCLANG_BUILD_STATIC=ON ^
  -DCLANG_ENABLE_STATIC_ANALYZER=OFF ^
  -DCLANG_ENABLE_ARCMT=OFF ^
  -DPYTHON_EXECUTABLE="C:\Program Files\Python38\python.exe" ^
  ../llvm/
ninja clang-format
copy /Y bin\clang-format.exe %SCRIPTDIR%..\..\bin

goto:eof


:extract-tgz
:: Using the -J filter on tar directly seems to hang...
set _tgzfile=%~1
set _tarfile=%_tgzfile:~0,-3%
del /Q %_tarfile%
7z -bb0 x %_tgzfile%
7z -bb0 x %_tarfile%
goto:eof