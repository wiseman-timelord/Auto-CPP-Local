@echo off
setlocal enabledelayedexpansion
cls

:: Set the filename to download
set "llamaVulkanVersion=llama-b3617-bin-win-vulkan-x64"
set "downloadUrl=https://github.com/ggerganov/llama.cpp/releases/download/b3617/%llamaVulkanVersion%"

:: Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script requires administrative privileges.
    echo Please run this script as an administrator.
    timeout /t 5 >nul
    goto :error
)
echo Running with Admin rights.

:: Working Fodler Fix After Admin
set "ScriptDirectory=%~dp0"
set "ScriptDirectory=%ScriptDirectory:~0,-1%"
pushd "%ScriptDirectory%"

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

:: Custom Banner
echo *******************************************************************************************************************
echo                                          Chat-LlamaVulkan - Installer
echo *******************************************************************************************************************
echo.
echo Working Dir: %ScriptDirectory%
echo.

:: Create Directories
timeout /t 1 >nul
echo Checking ".\data\libraries"...
if not exist ".\data\libraries" (
    echo ".\data\libraries" not found.
    mkdir ".\data\libraries"
    echo ".\data\libraries" created.
) else (
    echo ".\data\libraries" exists.
)
echo Checking for ".\data\cache"...
if not exist ".\data\cache" (
    echo ".\data\cache" not found.
    mkdir ".\data\cache"
    echo ".\data\cache" created.
) else (
    echo ".\data\cache" exists.
)
echo Checking ".\models"...
if not exist ".\models" (
    echo ".\models" not found.
    mkdir ".\models"
    echo ".\models" created.
) else (
    echo ".\models" exists.
)
timeout /t 1 >nul
echo.

:: Folder Maintenance
if exist ".\data\libraries\*.*" (
    echo Emptying .\data\libraries
    del /s /q ".\data\libraries\*.*"
	echo Emptied: .\data\libraries
) 
timeout /t 1 <nul

:: Install Requirements
echo Installing Pip Requirements...
"%PIP_EXE_TO_USE%" install -r ./data/requirements.txt
echo Requirements install finished.
timeout /t 2 >nul

:: Check if the file exists in the cache
set "cachedFilePath=.\data\cache\%llamaVulkanVersion%.zip"
if exist "%cachedFilePath%" (
    echo Cached file found. Continuing.
) else (
    echo Downloading Llama Vulkan Binary...
    powershell -Command "Invoke-WebRequest -Uri \"%downloadUrl%.zip\" -OutFile \"%cachedFilePath%\""
)
timeout /t 2 >nul
if %errorlevel% neq 0 (
    echo Failed to download Llama Vulkan Binary.
    goto :error
)
timeout /t 1 >nul

:: Locate 7-Zip
echo Locating 7-Zip...
set "sevenZipPath="
if exist "C:\Program Files\7-Zip\7z.exe" (
    set "sevenZipPath=C:\Program Files\7-Zip\7z.exe"
) else if exist "C:\Program Files (x86)\7-Zip\7z.exe" (
    set "sevenZipPath=C:\Program Files (x86)\7z.exe"
)
if not defined sevenZipPath (
    echo 7-Zip not found in default locations. Please install 7-Zip.
    goto :error
) else (
    echo 7-Zip found at "%sevenZipPath%".
)
timeout /t 2 >nul

:: Extract Llama Vulkan Binary
echo Extracting Llama Vulkan Binary to ".\data\libraries\LlamaCpp_Binaries"...
"%sevenZipPath%" x "%cachedFilePath%" -o".\data\libraries\LlamaCpp_Binaries" -mmt4 -y
if %errorlevel% neq 0 (
    echo Failed to extract Llama Vulkan Binary.
    goto :error
)
timeout /t 2 >nul

:: Installer Complete
goto :end

:error
echo An Error Occurred, Analyze Output For Clues.
pause
exit /b 1

:end
echo.
echo Installation Processes Completed Normally.
pause
exit /b 0
