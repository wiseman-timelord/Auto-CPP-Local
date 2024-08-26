@echo off

:: Initialization
set "ScriptDirectoryWt=%~dp0"
set "ScriptDirectoryWt=%ScriptDirectoryWt:~0,-1%"
pushd "%ScriptDirectoryWt%"
set "PYTHON_VERSION_TEXT=Python_3.9"
set "PYTHON_VERSION_FOLDER=Python39"

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
        set "PYTHON_EXE_TO_USE=%%~Ipython.exe"
        set "PIP_EXE_TO_USE=%%~IScripts\pip.exe"
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

:: BaNNer
echo *******************************************************************************************************************
echo                                                     AutoCPP-Lite
echo *******************************************************************************************************************
echo.
echo Working Dir: %ScriptDirectoryWt%

:: Run Program
echo Executing Main Script...
"%PYTHON_EXE_TO_USE%" main.py
echo AutoLLM Has Exited.

:: End Of Script
popd
pause
