import os
import json
import threading
from src.wake_word import wake_word_listener
from src.listener import listen_for_command
from src.auto_restart import monitor_assistant
from src.auto_sleep import monitor_activity
from tts import speak
from logging import log_event

CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

config = load_config()

def list_features():
    """Generates a list of enabled and disabled features."""
    enabled_features = [key.replace("_", " ").title() for key, value in config.items() if "enabled" in value and value["enabled"]]
    disabled_features = [key.replace("_", " ").title() for key, value in config.items() if "enabled" in value and not value["enabled"]]

    enabled_text = f"Enabled Features: {', '.join(enabled_features)}" if enabled_features else "No features are enabled."
    disabled_text = f"Disabled Features: {', '.join(disabled_features)}" if disabled_features else "No features are disabled."

    log_event("📜 Feature List on Startup:\n" + enabled_text + "\n" + disabled_text, "info")

    if config["tts"]["enabled"]:
        speak(f"Hello! Here is your current feature list. {enabled_text}. {disabled_text}.")

    return enabled_text, disabled_text

def start_wake_word_detection():
    if config["assistant"]["enabled"]:
        log_event("🚀 Starting wake word detection.", "info")
        wake_word_listener()

def start_command_listener():
    if config["assistant"]["enabled"]:
        log_event(f"🎤 Listening for '{config['assistant']['wake_word']}' command.", "info")
        listen_for_command()

def start_auto_sleep_monitor():
    if config["system"]["auto_sleep_timeout"]:
        log_event("⌛ Monitoring inactivity for auto-sleep...", "info")
        monitor_activity()

def start_auto_restart_monitor():
    if config["system"]["auto_restart"]:
        log_event("🔄 Auto-restart enabled. Monitoring for crashes...", "info")
        monitor_assistant()

if __name__ == "__main__":
    log_event("✅ Friday AI is starting up...", "info")

    # Display and announce feature status
    list_features()

    threads = []

    if config["assistant"]["enabled"]:
        wake_thread = threading.Thread(target=start_wake_word_detection, daemon=True)
        threads.append(wake_thread)
        wake_thread.start()

        listener_thread = threading.Thread(target=start_command_listener, daemon=True)
        threads.append(listener_thread)
        listener_thread.start()

    if config["system"]["auto_sleep_timeout"]:
        sleep_thread = threading.Thread(target=start_auto_sleep_monitor, daemon=True)
        threads.append(sleep_thread)
        sleep_thread.start()

    if config["system"]["auto_restart"]:
        restart_thread = threading.Thread(target=start_auto_restart_monitor, daemon=True)
        threads.append(restart_thread)
        restart_thread.start()

    for thread in threads:
        thread.join()
