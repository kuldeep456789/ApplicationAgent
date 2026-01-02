#!/bin/bash
cd "$(dirname "$0")/../.."
echo "========================================"
echo "Configuration Verification"
echo "========================================"
echo ""
if [ -f venv/bin/activate ]; then
    source venv/bin/activate
fi
echo "Running configuration checks..."
echo ""
python3 check_config.py
echo ""
