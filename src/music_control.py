import requests

AMAZON_MUSIC_API = "https://api.amazonmusic.com/v1"
ACCESS_TOKEN = "your-access-token"

def play_music(song_name):
    """Plays music via Amazon API."""
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    data = {"command": f"play {song_name}"}
    response = requests.post(f"{AMAZON_MUSIC_API}/playback", json=data, headers=headers)
    return response.json()