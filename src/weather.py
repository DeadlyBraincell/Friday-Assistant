import requests

API_KEY = "your-weather-api-key"
CITY = "New York"

def get_weather():
    """Fetches weather data."""
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric")
    return response.json()["weather"][0]["description"]