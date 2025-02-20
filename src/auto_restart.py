import os
import time
import subprocess
from logging import log_event

def monitor_assistant():
    """Monitors the assistant process and restarts if it crashes."""
    while True:
        process = subprocess.Popen(["python3", "assistant.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            log_event(f"❌ Assistant crashed! Restarting...", "error")
            time.sleep(5)  # Wait before restarting
        else:
            log_event("✅ Assistant stopped normally.", "info")
            break  # Exit loop if assistant stops correctly

if __name__ == "__main__":
    log_event("Starting Assistant Monitor...", "info")
    monitor_assistant()