import sqlite3
import os
import time
from logging import log_event

DB_FILE = "../db/assistant_memory.db"
LOG_FILE = "../error.log"
EXPIRATION_DAYS = 60  # Keep logs and memory for 60 days

def cleanup_memory():
    """Deletes old AI memory from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM memory WHERE timestamp < datetime('now', '-60 days')")
    
    deleted_rows = cursor.rowcount
    conn.commit()
    conn.close()

    log_event(f"🧹 Deleted {deleted_rows} old memory records.", "info")

def cleanup_logs():
    """Trims the log file to only keep recent entries."""
    if not os.path.exists(LOG_FILE):
        return
    
    with open(LOG_FILE, "r") as file:
        lines = file.readlines()

    # Keep only logs from the last 60 days
    timestamp_cutoff = time.time() - (EXPIRATION_DAYS * 86400)  # 60 days in seconds
    filtered_logs = [line for line in lines if is_recent_log(line, timestamp_cutoff)]

    with open(LOG_FILE, "w") as file:
        file.writelines(filtered_logs)

    log_event("🧹 Cleaned up old log entries.", "info")

def is_recent_log(log_line, cutoff):
    """Checks if a log entry is recent."""
    try:
        timestamp_str = log_line.split(" - ")[0]  # Extract timestamp
        log_timestamp = time.mktime(time.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S"))
        return log_timestamp >= cutoff
    except Exception:
        return True  # If parsing fails, keep the log

def run_cleanup():
    """Runs cleanup tasks for memory and logs."""
    log_event("🧹 Running cleanup process...", "info")
    cleanup_memory()
    cleanup_logs()
    log_event("✅ Cleanup complete!", "info")

if __name__ == "__main__":
    run_cleanup()
