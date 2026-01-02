#!/bin/bash
cd "$(dirname "$0")/../.."
echo "========================================"
echo "Job Application Assistant Setup"
echo "========================================"
echo ""
echo "1. Creating virtual environment..."
python3 -m venv venv
echo ""
echo "2. Activating virtual environment..."
source venv/bin/activate
echo ""
echo "3. Installing dependencies..."
python3 -m pip install --upgrade pip
pip install fastapi uvicorn[standard] pydantic pydantic-settings python-multipart playwright beautifulsoup4 lxml anthropic openai google-generativeai tiktoken sqlalchemy alembic aiosqlite asyncpg httpx aiohttp python-dotenv loguru tenacity streamlit plotly
echo ""
echo "4. Installing Playwright browsers..."
python3 -m playwright install chromium
echo ""
echo "5. Creating .env file from .env.example..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file. Please edit it with your API keys."
else
    echo ".env file already exists."
fi
echo ""
echo "6. Creating logs directory..."
mkdir -p logs
echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit the .env file with your API keys"
echo "2. Run scripts/shell/start_backend.sh"
echo "3. Run scripts/shell/start_frontend.sh"
echo ""
