#!/bin/bash

# ---------------------------------------
# 🚀 QuickQuiz Backend Runner Script
# ---------------------------------------

echo "🔹 Starting QuickQuiz Backend Setup..."

# Move to script directory (backend)
cd "$(dirname "$0")"

# Check if Python 3 is installed
if ! command -v python3 &>/dev/null; then
    echo "❌ Python3 is not installed. Please install it first."
    exit 1
fi

# Create virtual environment if missing
if [ ! -d ".venv" ]; then
    echo "🧱 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies if not already installed
if [ -f "requirements.txt" ]; then
    echo "📚 Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "⚠️ No requirements.txt found. Skipping dependency installation."
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️ No .env file found. Please create one with your Firebase credentials and DB URL."
fi

# Run FastAPI server
echo "🚀 Starting FastAPI server..."
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
