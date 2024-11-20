@echo off
setlocal

if "%1"=="" (
    echo Usage: control.bat [command] [options]
    echo Commands:
    echo   setup   - Initial project setup
    echo   backup  - Create a backup
    echo   restore - Restore from backup
    echo   clean   - Clean project structure
    echo   reset   - Reset to initial state
    echo   list    - List available backups
    exit /b 1
)

python scripts/control.py %*
