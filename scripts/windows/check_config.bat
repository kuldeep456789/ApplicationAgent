@echo off
cd /d "%~dp0..\.."
echo Configuration Verification
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)
echo Running configuration checks...
python check_config.py
pause
