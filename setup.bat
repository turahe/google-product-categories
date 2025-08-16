@echo off
echo Google Product Categories Setup
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Run setup
echo.
echo Running setup script...
python setup.py

echo.
echo Setup completed! Press any key to exit.
pause >nul
