import os
import json
import threading
from src.wake_word import wake_word_listener
from src.listener import listen_for_command
from src.auto_restart import monitor_assistant
from src.auto_sleep import monitor_activity
from logging import log_event

# Load configuration
CONFIG_FILE = "config.json"
with open(CONFIG_FILE, "r") as file:
    config = json.load(file)

ASSISTANT_NAME = config["assistant"]["name"]

def start_wake_word_detection():
    """Starts the wake word listener in a separate thread."""
    log_event(f"🚀 Starting wake word detection for {ASSISTANT_NAME}.", "info")
    wake_word_listener()

def start_command_listener():
    """Starts the voice command listener in a separate thread."""
    log_event(f"🎤 Listening for '{config['assistant']['wake_word']}' command.", "info")
    listen_for_command()

def start_auto_sleep_monitor():
    """Monitors system activity and triggers sleep mode if idle."""
    log_event("⌛ Monitoring inactivity for auto-sleep...", "info")
    monitor_activity()

def start_auto_restart_monitor():
    """Monitors the AI assistant and restarts it if it crashes."""
    if config["system"]["auto_restart"]:
        log_event("🔄 Auto-restart enabled. Monitoring for crashes...", "info")
        monitor_assistant()

if __name__ == "__main__":
    log_event(f"✅ {ASSISTANT_NAME} AI starting up...", "info")

    # Start wake word detection
    wake_thread = threading.Thread(target=start_wake_word_detection, daemon=True)
    wake_thread.start()

    # Start command listener
    listener_thread = threading.Thread(target=start_command_listener, daemon=True)
    listener_thread.start()

    # Start auto-sleep monitoring
    sleep_thread = threading.Thread(target=start_auto_sleep_monitor, daemon=True)
    sleep_thread.start()

    # Start auto-restart monitoring
    restart_thread = threading.Thread(target=start_auto_restart_monitor, daemon=True)
    restart_thread.start()

    # Keep main thread running
    wake_thread.join()
    listener_thread.join()
    sleep_thread.join()
    restart_thread.join()
