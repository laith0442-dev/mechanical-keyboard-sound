@echo off
setlocal
title Mechanical Keyboard Sound - Build Standalone EXE

echo ============================================================
echo   Mechanical Keyboard Sound - Standalone EXE Builder
echo ============================================================
echo.

echo [1/3] Checking dependencies...
py -3.13 -m pip install --only-binary=:all: -r requirements.txt pyinstaller
if errorlevel 1 (
    echo [ERROR] Failed to install required packages. Make sure Python 3.13 64-bit is installed.
    pause
    exit /b 1
)

echo.
echo [2/3] Compiling standalone executable with PyInstaller...
py -3.13 -m PyInstaller --clean --noconfirm --onefile --windowed --name MechanicalKeyboardSound keyboard_sound.py
if errorlevel 1 (
    echo [ERROR] PyInstaller build failed.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   BUILD SUCCESSFUL!
echo   Executable generated at: dist\MechanicalKeyboardSound.exe
echo ============================================================
echo.
pause
exit /b 0
