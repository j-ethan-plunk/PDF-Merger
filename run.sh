#!/bin/bash

# PDF Merger - Quick Start Script

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please create it first with: python -m venv .venv"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Check if dependencies are installed
if ! python -c "import flask" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Run the application
echo "Starting PDF Merger application..."
echo "Open your browser to: http://localhost:5010"
echo "Press Ctrl+C to stop the server"
python app.py
