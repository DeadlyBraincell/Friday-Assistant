#!/bin/bash

echo "🚀 Starting installation of Friday AI dependencies..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install core dependencies
echo "📦 Installing required system packages..."
sudo apt install -y python3 python3-pip python3-venv portaudio19-dev libssl-dev libffi-dev libasound2-dev build-essential ffmpeg sox libsox-fmt-mp3 curl git unzip jq

# Create and activate Python virtual environment
echo "🐍 Setting up a virtual environment..."
python3 -m venv friday-ai-env
source friday-ai-env/bin/activate

# Install Python dependencies
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install openai whisper google-auth google-auth-oauthlib google-auth-httplib2 googleapiclient \
            pvporcupine pyaudio sounddevice numpy coqui-tts \
            twilio requests flask paho-mqtt sqlite3 \
            beautifulsoup4 googlesearch-python schedule

# Install Home Assistant
echo "🏡 Installing Home Assistant..."
pip install homeassistant

# Install and configure MQTT broker (Mosquitto)
echo "📡 Installing Mosquitto MQTT broker..."
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto

# Install and configure Wake Word Engine (Porcupine)
echo "🎤 Setting up Porcupine Wake Word Engine..."
mkdir -p ~/friday-ai/models
cd ~/friday-ai/models
curl -O https://github.com/Picovoice/porcupine/raw/master/resources/keyword_files/raspberry-pi/friday.ppn
curl -O https://github.com/Picovoice/porcupine/raw/master/resources/keyword_files/raspberry-pi/friday_wake_up.ppn
curl -O https://github.com/Picovoice/porcupine/raw/master/resources/keyword_files/raspberry-pi/friday_sleep.ppn
cd ~

# Install and configure Whisper AI (Speech-to-Text)
echo "🗣️ Setting up Whisper AI..."
mkdir -p ~/friday-ai/models/whisper_model
cd ~/friday-ai/models/whisper_model
curl -O https://huggingface.co/openai/whisper/resolve/main/whisper-base.pt
cd ~

# Configure permissions
echo "🔧 Setting up permissions..."
sudo usermod -aG audio $(whoami)

# Ensure startup scripts are executable
echo "🔧 Configuring startup scripts..."
chmod +x ~/friday-ai/scripts/startup.sh
chmod +x ~/friday-ai/scripts/cleanup.py

# Add startup script to crontab for auto-boot
echo "🔧 Adding startup script to crontab..."
(crontab -l 2>/dev/null; echo "@reboot /home/$(whoami)/friday-ai/scripts/startup.sh") | crontab -

echo "✅ Installation complete! Reboot your system to apply changes."
