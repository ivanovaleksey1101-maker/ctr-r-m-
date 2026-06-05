@echo off
REM This Source Code Form is subject to the terms of the Mozilla Public
REM License, v. 2.0. If a copy of the MPL was not distributed with this
REM file, You can obtain one at https://mozilla.org/MPL/2.0/.

echo Installing required packages for Windows...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed!
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Check if pip is available
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo pip is not available!
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install required packages
echo Installing Python packages...
pip install pygame python-vlc

REM Install VLC media player if not installed
echo Checking for VLC media player...
vlc --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo VLC media player is not installed!
    echo Please download and install VLC from: https://www.videolan.org/vlc/
    echo VLC is required for video playback.
    echo.
    pause
)

echo.
echo Installation complete!
echo To launch the game: run launch_game.bat
echo.
pause
