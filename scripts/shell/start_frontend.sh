#!/bin/bash
cd "$(dirname "$0")/../.."
echo "========================================"
echo "Starting Frontend UI"
echo "========================================"
echo ""
if [ -f venv/bin/activate ]; then
    source venv/bin/activate
fi
echo ""
echo "Starting Streamlit UI on http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""
python3 -m streamlit run frontend/app.py
