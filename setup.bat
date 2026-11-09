@echo off
setlocal
title Mechanical Keyboard Sound - Setup & Build

echo ============================================================
echo   Mechanical Keyboard Sound - Windows Setup
echo ============================================================
echo.

echo [1/3] Upgrading pip...
py -3.13 -m pip install --upgrade pip
if errorlevel 1 goto fail

echo.
echo [2/3] Installing dependencies from requirements.txt...
py -3.13 -m pip install --only-binary=:all: -r requirements.txt pyinstaller
if errorlevel 1 goto fail

echo.
echo [3/3] Building standalone executable...
py -3.13 -m PyInstaller --clean --noconfirm --onefile --windowed --name MechanicalKeyboardSound keyboard_sound.py
if errorlevel 1 goto fail

echo.
echo ============================================================
echo   Setup and Build Complete!
echo   Executable created at: dist\MechanicalKeyboardSound.exe
echo ============================================================
echo.
pause
exit /b 0

:fail
echo.
echo [ERROR] Setup or build failed.
echo Please verify that Python 3.13 (64-bit) is installed and accessible via 'py -3.13'.
pause
exit /b 1
