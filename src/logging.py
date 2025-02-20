import logging
import requests
import time

LOG_FILE = "error.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

HOME_ASSISTANT_URL = "http://192.168.1.200:8123/api/services/notify/mobile_app"
HA_HEADERS = {"Authorization": "Bearer YOUR_LONG_LIVED_ACCESS_TOKEN", "Content-Type": "application/json"}

SLOW_THRESHOLD = 3  # Seconds before a command is considered slow

def log_event(message, level="info"):
    """Logs system events and sends notifications if an error occurs."""
    if level == "info":
        logging.info(f"✅ SUCCESS: {message}")
    elif level == "error":
        logging.error(f"❌ FAILURE: {message}")
        send_notification(f"Friday AI Error: {message}")
    elif level == "warning":
        logging.warning(f"⚠ WARNING: {message}")

def log_execution_time(command, start_time):
    """Logs execution time for each command."""
    execution_time = time.time() - start_time
    if execution_time > SLOW_THRESHOLD:
        log_event(f"⚠ WARNING: Slow execution ({execution_time:.2f}s) for: {command}", "warning")
    else:
        log_event(f"✅ Command executed in {execution_time:.2f}s: {command}", "info")

def send_notification(message):
    """Send an error notification to a mobile device via Home Assistant."""
    payload = {"message": message}
    requests.post(f"{HOME_ASSISTANT_URL}", headers=HA_HEADERS, json=payload)