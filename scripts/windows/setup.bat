@echo off
cd /d "%~dp0..\.."
echo Job Application Assistant Setup
echo 1. Creating virtual environment...
python -m venv venv
echo 2. Activating virtual environment...
call venv\Scripts\activate.bat
echo 3. Installing dependencies...
python -m pip install --upgrade pip
pip install fastapi uvicorn[standard] pydantic pydantic-settings python-multipart playwright beautifulsoup4 lxml anthropic openai google-generativeai tiktoken sqlalchemy alembic aiosqlite asyncpg httpx aiohttp python-dotenv loguru tenacity streamlit plotly
echo 4. Installing Playwright browsers...
python -m playwright install chromium
echo 5. Creating .env file from .env.example...
if not exist .env (
    copy .env.example .env
    echo Created .env file. Please edit it with your API keys.
) else (
    echo .env file already exists.
)
echo 6. Creating logs directory...
if not exist logs mkdir logs
echo Setup Complete!
echo Next steps:
echo 1. Edit the .env file with your API keys
echo 2. Run scripts\windows\start_backend.bat
echo 3. Run scripts\windows\start_frontend.bat
pause
