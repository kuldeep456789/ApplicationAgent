@echo off
cd /d "%~dp0..\.."
echo Starting Frontend UI
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)
echo Starting Streamlit UI on http://localhost:8501
echo Press Ctrl+C to stop the server
python -m streamlit run frontend/app.py
