@setlocal enableextensions
:: build statically linked executable

:: enable VC environment. activates cmake, ninja
call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvarsall.bat" amd64 || call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Enterprise\VC\Auxiliary\Build\vcvarsall.bat" amd64
:: assume 7z is installed in standard path
set PATH=C:\Program Files\7-Zip;%PATH%
set SCRIPTDIR=%~dp0
set CPPCHECK_URL=https://github.com/danmar/cppcheck/archive/2.3.tar.gz
set CPPCHECK_TGZ=cppcheck.tar.gz

:: sources
mkdir cppcheck
cd cppcheck
curl -L %CPPCHECK_URL% -o %CPPCHECK_TGZ%
call:extract-tgz %CPPCHECK_TGZ%
cd ..

:: Choose python directory
if exist "C:\Program Files\Python38\python.exe" (
  set PYTHONEXE="C:\Program Files\Python38\python.exe"
) else (
  set PYTHONEXE="C:\Program Files\Python37\python.exe"
)

:: build
mkdir cppcheck-build
cd cppcheck-build
cmake ^
    -DCMAKE_BUILD_TYPE=Release ^
    -DBUILD_GUI=OFF ^
    -DHAVE_RULES=OFF ^
    -DUSE_MATCHCOMPILER=ON ^
  ../cppcheck/
cmake --build . --config Release
copy /Y Release/bin/cppcheck ../../../bin/cppcheck.exe

goto:eof


:extract-tgz
:: Using the -J filter on tar directly seems to hang...
set _tgzfile=%~1
set _tarfile=%_tgzfile:~0,-3%
del /Q %_tarfile%
7z -bb0 x %_tgzfile%
7z -bb0 x %_tarfile%
goto:eof