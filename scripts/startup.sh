#!/bin/bash

echo "🚀 Starting Friday AI..."

# Navigate to the AI assistant folder
cd /home/user/home-assistant-ai

# Start the assistant monitoring (auto-restarts on crash)
nohup python3 scripts/auto_restart.py > logs/startup.log 2>&1 &

# Start the background cleanup service (runs daily at 2 AM via cron)
nohup python3 scripts/cleanup.py > logs/cleanup.log 2>&1 &

# Start the wake word listener so AI can be activated
nohup python3 src/wake_word.py > logs/wake_word.log 2>&1 &

echo "✅ Friday AI is now running."

exit 0
