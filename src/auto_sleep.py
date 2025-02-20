import time
import os
from logging import log_event

INACTIVITY_TIMEOUT = 1800  # 30 minutes

def monitor_activity():
    last_interaction = time.time()

    while True:
        time.sleep(60)  # Check every minute
        if time.time() - last_interaction > INACTIVITY_TIMEOUT:
            log_event("No interaction for 30 minutes. Going to sleep.")
            os.system("python3 sleep_command.py")
            break

monitor_activity()
