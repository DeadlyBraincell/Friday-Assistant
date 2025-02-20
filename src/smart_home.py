import requests

HOME_ASSISTANT_URL = "http://192.168.1.200:8123/api/services"
HA_HEADERS = {"Authorization": "Bearer YOUR_LONG_LIVED_ACCESS_TOKEN", "Content-Type": "application/json"}

def turn_on_light(entity_id):
    """Turns on a smart light."""
    requests.post(f"{HOME_ASSISTANT_URL}/light/turn_on", headers=HA_HEADERS, json={"entity_id": entity_id})

def turn_off_light(entity_id):
    """Turns off a smart light."""
    requests.post(f"{HOME_ASSISTANT_URL}/light/turn_off", headers=HA_HEADERS, json={"entity_id": entity_id})