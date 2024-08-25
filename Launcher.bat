@echo off
mode 45,22
title Chat-LlamaVulkan-Launcher

:: Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script requires administrative privileges.
    echo Please run this script as an administrator.
    pause
    exit /b 1
)
echo Running with Admin rights.


:: Find Python 3.X and pip
set "PIP_EXE_TO_USE="
set "PYTHON_EXE_TO_USE="
set "PYTHON_FOLDER_TO_USE="
for %%I in (
    "C:\Program Files\Python39\"
    "C:\Program Files (x86)\Python39\"
    "%LocalAppData%\Programs\Python\Python39\"
) do (
    if exist "%%~I" (
        set "PYTHON_FOLDER_TO_USE=%%~I"
        set "PYTHON_EXE_TO_USE=%%~dpI\python.exe"
        set "PIP_EXE_TO_USE=%%~dpI\Scripts\pip.exe"
        goto :found_python3X
    )
)
:found_python3X
if not defined PYTHON_EXE_TO_USE (
    echo Error: Python 3.X not found. Please ensure it is installed.
    timeout /t 5 >nul
    goto :error
)

:: Intro
echo *********************************************
echo         Chat-LlamaVulkan - Launcher
echo *********************************************
echo.
set "ScriptDirectoryWt=%~dp0"
set "ScriptDirectoryWt=%ScriptDirectoryWt:~0,-1%"
pushd "%ScriptDirectoryWt%"
echo Working Dir: %ScriptDirectoryWt%
echo.

:: Run both windows for Chat-LlamaVulkan
echo Launching 2 Windows...
echo.
timeout /t 1 /nobreak >nul
echo Options for window1: --logs
echo Options for window2: --tts --sound
echo.
timeout /t 2 /nobreak >nul

start "" cmd /c "%PYTHON_EXE_TO_USE% window_1.py --logs || pause"
if errorlevel 1 (
    echo Error launching window 1.
    pause
    exit /b 1
)

start "" cmd /c "%PYTHON_EXE_TO_USE% window_2.py --tts --sound || pause"
if errorlevel 1 (
    echo Error launching window 2.
    pause
    exit /b 1
)

echo.
echo Windows launched, closing in 3 seconds...
echo.
timeout /t 3 /nobreak >nul
exit /b 0