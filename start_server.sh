#!/bin/bash

echo "🌿 EIA Pro Platform - Starting Server..."
echo "============================================"

# Try different Python commands
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python not found. Please install Python 3."
    exit 1
fi

echo "✅ Using Python: $PYTHON_CMD"

# Check if Flask is available
if $PYTHON_CMD -c "import flask" 2>/dev/null; then
    echo "✅ Flask available - Starting advanced server..."
    $PYTHON_CMD integrated_backend.py
else
    echo "⚠️  Flask not found - Starting simple server..."
    echo "   (For advanced features, install: pip install flask flask-cors)"
    $PYTHON_CMD simple_server.py
fi