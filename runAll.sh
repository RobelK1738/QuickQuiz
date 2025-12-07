#!/bin/bash
# 🚀 QuickQuiz Full Stack Runner

echo "💻 Launching QuickQuiz Backend + Frontend..."

osascript -e 'tell app "Terminal" to do script "cd ~/Desktop/Fall/SWE-375-01/Final-Project/code/backend && source .venv/bin/activate && ./runBackend.sh"'
osascript -e 'tell app "Terminal" to do script "cd ~/Desktop/Fall/SWE-375-01/Final-Project/code/frontend && ./runFrontend.sh"'
