#!/bin/bash
cd "$(dirname "$0")/../.."
echo "========================================"
echo "Starting Backend Server"
echo "========================================"
echo ""
if [ -f venv/bin/activate ]; then
    source venv/bin/activate
fi
echo "Initializing database..."
python3 -c "import asyncio; from backend.models.database import init_db; asyncio.run(init_db())"
echo ""
echo "Starting FastAPI server on http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""
python3 -m backend.main
