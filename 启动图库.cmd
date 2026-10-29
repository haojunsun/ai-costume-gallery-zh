@echo off
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0"
python scripts\serve.py --open
if errorlevel 1 pause
