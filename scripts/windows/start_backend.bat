@echo off
cd /d "%~dp0..\.."
echo Starting Backend Server
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)
echo Initializing database...
python -c "import asyncio; from backend.models.database import init_db; asyncio.run(init_db())"
echo Starting FastAPI server on http://localhost:8000
echo Press Ctrl+C to stop the server
python -m backend.main
