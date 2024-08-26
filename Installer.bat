@echo off

:: Initialization
set "ScriptDirectoryWt=%~dp0"
set "ScriptDirectoryWt=%ScriptDirectoryWt:~0,-1%"
pushd "%ScriptDirectoryWt%"
set "PYTHON_VERSION_TEXT=Python_3.9"
set "PYTHON_VERSION_FOLDER=Python39"
set "downloadUrl=https://github.com/ggerganov/llama.cpp/releases/download/b3620/llama-b3620-bin-win-vulkan-x64.zip"

:: Check for administrative privileges
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo Error: Admin Required!
    echo Right Click, then Run As Administrator.
    timeout /t 3 >nul
    goto :eof
)

:: Find Python and pip
set "PIP_EXE_TO_USE="
set "PYTHON_EXE_TO_USE="
set "PYTHON_FOLDER_TO_USE="
for %%I in (
    "C:\Program Files\%PYTHON_VERSION_FOLDER%\"
    "%LocalAppData%\Programs\Python\%PYTHON_VERSION_FOLDER%\"
) do (
    if exist "%%~I" (
        set "PYTHON_FOLDER_TO_USE=%%~I"
        set "PYTHON_EXE_TO_USE=%%~dpI\python.exe"
        set "PIP_EXE_TO_USE=%%~dpI\Scripts\pip.exe"
        goto :found_python_location
    )
)
:found_python_location
if not defined PYTHON_EXE_TO_USE (
    echo Error: %PYTHON_VERSION_TEXT% not found. Please install it before running this script.
    timeout /t 3 >nul
    goto :eof
)
echo Python Found: %PYTHON_EXE_TO_USE%
echo Pip Found: %PIP_EXE_TO_USE%
timeout /t 1 >nul
echo.

:: BaNNer
echo *******************************************************************************************************************
echo                                                     AutoCPP-Lite
echo *******************************************************************************************************************
echo.
echo Working Dir: %ScriptDirectoryWt%

:: Install Libraries
echo Maintenance Tasks...
echo Checking: .\data\libraries
if not exist ".\data\libraries" (
    mkdir ".\data\libraries"
    echo Created: .\data\libraries.
) else (
    echo Emptying .\data\libraries
    del /s /q ".\data\libraries\*.*"
    echo Emptied: .\data\libraries
)
echo Checking: .\cache
if not exist ".\cache" (
    echo ".\cache" not found.
    mkdir ".\cache"
    echo ".\
