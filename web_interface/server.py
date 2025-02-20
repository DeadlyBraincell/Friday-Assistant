from flask import Flask, render_template, send_file, jsonify
import os
import requests

app = Flask(__name__)
LOG_FILE = "error.log"

HOME_ASSISTANT_URL = "http://192.168.1.200:8123/api/services/media_player/play_media"
HA_HEADERS = {"Authorization": "Bearer YOUR_LONG_LIVED_ACCESS_TOKEN", "Content-Type": "application/json"}
TV_ENTITY_ID = "media_player.living_room_tv"

def get_latest_logs(n=50):
    """Fetch the latest n lines from the log file."""
    if not os.path.exists(LOG_FILE):
        return ["No logs available."]
    
    with open(LOG_FILE, "r") as file:
        lines = file.readlines()
    
    return lines[-n:]  # Return last n lines

@app.route("/")
def home():
    """Main dashboard page."""
    return render_template("dashboard.html")

@app.route("/logs")
def view_logs():
    """Log viewer page."""
    logs = get_latest_logs()
    return render_template("logs.html", logs=logs)

@app.route("/logs/download")
def download_logs():
    """Allow users to download the log file."""
    return send_file(LOG_FILE, as_attachment=True)

@app.route("/logs/latest")
def latest_logs():
    """Fetch latest logs dynamically for AJAX updates."""
    logs = get_latest_logs()
    return jsonify(logs)

@app.route("/logs/show_on_tv")
def show_logs_on_tv():
    """Display logs on a smart TV."""
    url = "http://your-server-ip:5000/logs"
    payload = {
        "entity_id": TV_ENTITY_ID,
        "media_content_id": url,
        "media_content_type": "browser"
    }
    response = requests.post(HOME_ASSISTANT_URL, headers=HA_HEADERS, json=payload)
    return "Logs are now displayed on the TV!" if response.status_code == 200 else "Failed to display logs."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
