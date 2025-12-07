#!/bin/bash

# ---------------------------------------
# 🚀 QuickQuiz Frontend Runner Script
# ---------------------------------------

echo "🔹 Starting QuickQuiz Frontend Setup..."

# Move to script directory (frontend)
cd "$(dirname "$0")"

# Check if Node.js is installed
if ! command -v node &>/dev/null; then
    echo "❌ Node.js is not installed. Please install it first (https://nodejs.org/)."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &>/dev/null; then
    echo "❌ npm is not installed. Please install it first."
    exit 1
fi

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing npm dependencies..."
    npm install
else
    echo "✅ Dependencies already installed."
fi

# Ensure environment variables exist
if [ ! -f ".env" ]; then
    echo "⚠️ No .env file found. Please create one with your Firebase web config."
fi

# Start React development server
echo "🚀 Starting React development server..."
npm start
