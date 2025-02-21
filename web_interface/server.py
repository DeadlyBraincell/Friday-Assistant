from flask import Flask, render_template, request, jsonify
import json

CONFIG_FILE = "config.json"

app = Flask(__name__)

def load_config():
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)

@app.route("/")
def home():
    """Main dashboard page."""
    config = load_config()
    enabled_features = [key.replace("_", " ").title() for key, value in config.items() if "enabled" in value and value["enabled"]]
    disabled_features = [key.replace("_", " ").title() for key, value in config.items() if "enabled" in value and not value["enabled"]]
    return render_template("dashboard.html", enabled_features=enabled_features, disabled_features=disabled_features)

@app.route("/toggle_feature", methods=["POST"])
def toggle_feature():
    """Toggles a feature on or off."""
    data = request.get_json()
    feature = data.get("feature")
    state = data.get("state")

    config = load_config()

    if feature in config:
        config[feature]["enabled"] = state
        save_config(config)
        return jsonify({"message": f"{feature} has been {'enabled' if state else 'disabled'}."})
    else:
        return jsonify({"error": "Feature not found."}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)