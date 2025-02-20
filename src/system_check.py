import os
import subprocess
from logging import log_event

def check_system_status():
    """Checks if key services are running"""
    issues = []

    # Check Home Assistant
    ha_status = subprocess.run(["systemctl", "is-active", "home-assistant"], capture_output=True, text=True)
    if "inactive" in ha_status.stdout:
        issues.append("Home Assistant is not running.")
        log_event("Home Assistant inactive.", "error")

    return issues