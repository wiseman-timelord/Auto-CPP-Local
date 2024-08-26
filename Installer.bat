@echo off

:: Initialization
set "ScriptDirectoryWt=%~dp0"
set "ScriptDirectoryWt=%ScriptDirectoryWt:~0,-1%"
pushd "%ScriptDirectoryWt%"
set "PYTHON_VERSION_TEXT=Python_3.9"
set "PYTHON_VERSION_FOLDER=Python39"'
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
echo Checking: .\Libraries
if not exist ".\libraries" (
    mkdir ".\libraries"
    echo Created: .\libraries.
) else (
    echo Emptying .\libraries
    del /s /q ".\libraries\*.*"
	echo Emptied: .\libraries
)
echo Checking: .\cache
if not exist ".\cache" (
    echo ".\cache" not found.
    mkdir ".\cache"
    echo ".\cache" created.
)
echo Checking: .\models
if not exist ".\models" (
    echo ".\models" not found.
    mkdir ".\models"
    echo ".\models" created.
)
echo Checking: .\working
if not exist ".\working" (
    echo ".\working" not found.
    mkdir ".\working"
    echo ".\working" created.
)

:: Install Requirements
echo Installing requirements.txt...
"%PIP_EXE_TO_USE%" install -r requirements.txt
echo requirements.txt Installed.
echo.

:: Install Libraries
:: Download llama binaries
set "cachedFilePath=.\cache\llama_cpp_binaries.zip"
if exist "%cachedFilePath%" (
    echo Cached file found. Continuing.
) else (
    echo Downloading Llama Vulkan Binary...
    powershell -Command "Invoke-WebRequest -Uri "%downloadUrl%" -OutFile "%cachedFilePath%""
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
echo Extracting Llama Vulkan Binary to ".\libraries\LlamaCpp_Binaries"...
"%sevenZipPath%" x "%cachedFilePath%" -o".\libraries\LlamaCpp_Binaries" -mmt4 -y
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