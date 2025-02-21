import os
import json
import time
from tts import speak
from stt import transcribe_audio
from memory import save_memory, fetch_memory
from internet_search import google_search
from weather import get_weather
from calendar import get_calendar_events
from music_control import play_music
from smart_home import turn_on_light, turn_off_light
from volume_control import set_volume
from call_system import make_call
from timer import set_timer
from logging import log_event, log_execution_time

# Load configuration
CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)

config = load_config()

def notify_disabled_feature(feature_name):
    """Notifies the user that a requested feature is disabled."""
    message = f"Sorry, the {feature_name} feature is currently disabled."
    log_event(message, "warning")
    if config["tts"]["enabled"]:
        speak(message)

def process_command(user_input):
    """Processes user commands and executes the corresponding function."""
    user_input = user_input.lower()
    log_event(f"User command received: {user_input}")

    start_time = time.time()
    config = load_config()  # Reload the config dynamically

    try:
        if "weather" in user_input:
            if config["weather"]["enabled"]:
                response = get_weather()
            else:
                notify_disabled_feature("weather")
                return
        elif "calendar" in user_input:
            if config["calendar"]["enabled"]:
                response = get_calendar_events()
            else:
                notify_disabled_feature("calendar")
                return
        elif "play music" in user_input:
            if config["music"]["enabled"]:
                play_music("Imagine Dragons - Believer")
                response = "Playing music."
            else:
                notify_disabled_feature("music")
                return
        elif "turn on the light" in user_input:
            if config["smart_home"]["enabled"]:
                turn_on_light("light.living_room")
                response = "Turning on the light."
            else:
                notify_disabled_feature("smart home")
                return
        elif "turn off the light" in user_input:
            if config["smart_home"]["enabled"]:
                turn_off_light("light.living_room")
                response = "Turning off the light."
            else:
                notify_disabled_feature("smart home")
                return
        elif "set timer for" in user_input:
            if config["system"]["auto_sleep_timeout"]:
                duration = int(user_input.split("for")[1].strip().split(" ")[0])
                set_timer(duration)
                response = f"Timer set for {duration} seconds."
            else:
                notify_disabled_feature("timer")
                return
        elif "call" in user_input:
            if config["communication"]["enabled"]:
                make_call("+123456789")
                response = "Making a call."
            else:
                notify_disabled_feature("communication")
                return
        elif "search" in user_input:
            if config["internet_search"]["enabled"]:
                query = user_input.replace("search", "").strip()
                results = google_search(query)
                response = f"Here are some search results: {results}"
            else:
                notify_disabled_feature("internet search")
                return
        elif "show logs" in user_input:
            if config["logging"]["enabled"]:
                os.system("python3 server.py &")
                response = "Opening logs on the TV."
            else:
                notify_disabled_feature("logging")
                return
        else:
            response = "I don't understand that command."

        log_execution_time(user_input, start_time)

        if config["memory"]["enabled"]:
            save_memory(user_input, response)

        if config["tts"]["enabled"]:
            speak(response)

    except Exception as e:
        log_event(f"Error executing command: {user_input} - {str(e)}", "error")
        response = "There was an error processing your request."
        if config["tts"]["enabled"]:
            speak(response)

if __name__ == "__main__":
    while True:
        if config["stt"]["enabled"]:
            user_input = transcribe_audio()
            if user_input:
                process_command(user_input)
