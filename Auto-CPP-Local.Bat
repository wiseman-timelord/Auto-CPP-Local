:: Script: `.\Auto-CPP-Local.Bat`

:: Initialization
@echo off
setlocal enabledelayedexpansion

:: Globals
set "PYTHON_VERSION_USED=39"
set "AUTO_CCP_LOCAL_VERSION=009"
set "downloadUrl=https://github.com/ggerganov/llama.cpp/releases/download/b3620/llama-b3620-bin-win-vulkan-x64.zip"
set "zipFileName=llama_cpp.zip"
set "zipFilePath=.\cache\downloads\%zipFileName%"
set "PYTHON_EXE_TO_USE="
set "PERSISTENCE_FILE=.\data\persistence_batch.txt"

:: Dp0
set "ScriptDirectory=%~dp0"
set "ScriptDirectory=%ScriptDirectory:~0,-1%"
cd /d "%ScriptDirectory%"

:: Initial Banner
call :display_banner

:: Check for administrative privileges
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo Error: Admin Required!
    echo Right Click, then Run As Administrator.
    timeout /t 3 >nul
    goto :end_of_script
)

:: Print Working DIR
echo Working Dir: %ScriptDirectory%

:: Check for persistence file
if exist "%PERSISTENCE_FILE%" (
    echo Persistence file found.
    for /f "tokens=1,* delims==" %%A in ('type "%PERSISTENCE_FILE%"') do (
        if "%%A"=="python_exe" (
            set "PYTHON_EXE_TO_USE=%%B"
            if exist "!PYTHON_EXE_TO_USE!" (
                echo Found: .\data\persistence_batch.txt
                goto :found_python_location
            ) else (
                echo Corrupt: .\data\persistence_batch.txt
                set "PYTHON_EXE_TO_USE="
            )
        )
    )
) else (
    echo Missing: .\Data\persistence_batch.txt
)
timeout /t 1 >nul
if not defined PYTHON_EXE_TO_USE (
    for %%I in (
        "C:\Program Files\Python%PYTHON_VERSION_USED%\"
        "%LocalAppData%\Programs\Python\Python%PYTHON_VERSION_USED%\"
    ) do (
        if exist "%%~I\python.exe" (
            set "PYTHON_EXE_TO_USE=%%~I\python.exe"
            echo python_exe=!PYTHON_EXE_TO_USE! > "%PERSISTENCE_FILE%"
            echo Created: .\data\persistence_batch.txt
			timeout /t 1 >nul
            goto :found_python_location
        )
    )
)
timeout /t 1 >nul
if not defined PYTHON_EXE_TO_USE (
    echo Missing: Python%PYTHON_VERSION_USED%
    timeout /t 3 >nul
    goto :end_of_script
)
:found_python_location
echo Python Found: !PYTHON_EXE_TO_USE!
timeout /t 1 >nul

:: Initialization Completed.
echo Start-up Complete, Loading Menu...
timeout /t 2 >nul
goto :menu

:: Banner
:display_banner
cls
echo =======================================================================================================================
echo     Auto-CPP-Local v%AUTO_CCP_LOCAL_VERSION%
echo =======================================================================================================================
echo.
timeout /t 1 >nul
goto :eof

:: Separator
:display_separator
echo.
echo -----------------------------------------------------------------------------------------------------------------------
goto :eof

:: Menu
:menu
call :display_banner
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo     1. Run Auto-CPP-Local v%AUTO_CCP_LOCAL_VERSION% on Python v%PYTHON_VERSION_USED%
echo.
echo     2. Check Folders and Install Libraries
echo.
echo     3. Upgrade Pip Version to Current
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
echo.
call :display_separator
set /p choice="Selection; Menu Options = 1-3, Exit Menu = X: "

if /i "%choice%"=="1" goto :run_main_program
if /i "%choice%"=="2" goto :check_folders_install_libraries
if /i "%choice%"=="3" goto :upgrade_pip_version
if /i "%choice%"=="x" goto :end_of_script
echo Invalid choice. Please enter a number between 1 and 3.
timeout /t 3 >nul
goto :menu

:: Option 1: Check Folders & Install Libraries
:check_folders_install_libraries
:: Checking/Creating Folders...
call :display_banner
echo Maintenance Tasks...
timeout /t 1 >nul
for %%F in (data\libraries cache Input Output) do (
    if not exist ".\%%F" (
        mkdir ".\%%F"
        echo Created: .\%%F
    ) else (
        if "%%F" == "data\libraries" (
            echo Emptying .\data\libraries\llama_cpp
            if exist ".\data\libraries\llama_cpp" (
                rmdir /s /q ".\data\libraries\llama_cpp"
            )
            mkdir ".\data\libraries\llama_cpp"
            echo Emptied and recreated: .\data\libraries\llama_cpp
        ) else (
            echo Found: .\%%F
        )
    )
)
echo Folder Setup Complete.
timeout /t 2 >nul

:: Installing Libraries...
echo Installing `requirements.txt`...
if not exist ".\data\requirements.txt" (
    echo Error: requirements.txt not found!
    timeout /t 3 >nul
    goto :menu
)
"%PYTHON_EXE_TO_USE%" -m pip install -r .\data\requirements.txt
if %errorLevel% NEQ 0 (
    echo Error: Pip installation failed!
    timeout /t 3 >nul
    goto :menu
)
echo ...`requirements.txt` Installed.
timeout /t 2 >nul

echo Installing Exta-Libraries...
timeout /t 1 >nul

:: Download and extract llama.cpp
echo Downloading llama.cpp...
powershell -Command "Invoke-WebRequest -Uri '%downloadUrl%' -OutFile '%zipFilePath%'"
if %errorLevel% NEQ 0 (
    echo Error: Download failed!
    timeout /t 3 >nul
    goto :menu
)

echo Extracting llama.cpp...
powershell -Command "Expand-Archive -Path '%zipFilePath%' -DestinationPath '.\data\libraries\llama_cpp' -Force"
if %errorLevel% NEQ 0 (
    echo Error: Extraction failed!
    timeout /t 3 >nul
    goto :menu
)

echo ...Extra-Libraries Installed.
timeout /t 2 >nul

:: All Libraries Installed
echo Check Printout for Issues.
pause
goto :menu

:: Option 2: Upgrade Pip Version to Current
:upgrade_pip_version
call :display_banner
echo Installing Pip Upgrade...
timeout /t 1 >nul
"%PYTHON_EXE_TO_USE%" -m pip install --upgrade pip
if %errorLevel% NEQ 0 (
    echo Error: Pip upgrade failed!
    timeout /t 3 >nul
    goto :menu
)
echo ...Pip has been Upgraded.
timeout /t 2 >nul
echo Check Printout for Issues.
pause
goto :menu

:: Option 1: Run Main Program
:run_main_program
call :display_banner
echo Launching Auto-CPP-Local...
"%PYTHON_EXE_TO_USE%" .\launch_main.py
echo Auto-CPP-Local Exited.
timeout /t 3 >nul
goto :end_of_script

:: End Of Script
:end_of_script
call :display_banner
echo All Processes Finished.
echo Exiting Script in 3s...
timeout /t 3 >nul
endlocal
exit /b 0