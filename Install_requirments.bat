@echo off
echo This mod requires the following Python packages:
echo   watchdog, lz4, pillow, numpy
set /p userinput="Do you want to install them now? [y/n]: "

if /i "%userinput%"=="y" (
    python -m pip install --upgrade pip
    pip install watchdog lz4 pillow numpy
    echo Done! All dependencies installed.
) else (
    echo Skipped installation.
)
pause
