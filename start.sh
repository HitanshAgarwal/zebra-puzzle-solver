#!/bin/bash

# Zebra Puzzle Solver - Startup Script

echo "========================================================================"
echo "🧩 Zebra Puzzle Solver"
echo "========================================================================"
echo ""

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Error: Flask is not installed."
    echo "Please install it with: pip install Flask"
    echo ""
    exit 1
fi

# Kill any existing processes on common ports
for port in 5000 5001 8080; do
    if lsof -ti:$port >/dev/null 2>&1; then
        echo "Killing existing process on port $port..."
        lsof -ti:$port | xargs kill -9 2>/dev/null
    fi
done

echo ""
echo "Starting server on port 5001..."
echo ""

# Start the server
python3 web_app.py

echo ""
echo "Server stopped."
