import os
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

def process_command(user_input):
    """Processes user commands and executes the corresponding function."""
    user_input = user_input.lower()
    log_event(f"User command received: {user_input}")

    start_time = time.time()  # Track execution time

    try:
        if "weather" in user_input:
            response = get_weather()
        elif "calendar" in user_input:
            response = get_calendar_events()
        elif "play music" in user_input:
            play_music("Imagine Dragons - Believer")
            response = "Playing music."
        elif "turn on the light" in user_input:
            turn_on_light("light.living_room")
            response = "Turning on the light."
        elif "turn off the light" in user_input:
            turn_off_light("light.living_room")
            response = "Turning off the light."
        elif "set timer for" in user_input:
            duration = int(user_input.split("for")[1].strip().split(" ")[0])
            set_timer(duration)
            response = f"Timer set for {duration} seconds."
        elif "call" in user_input:
            make_call("+123456789")
            response = "Making a call."
        elif "search" in user_input:
            query = user_input.replace("search", "").strip()
            results = google_search(query)
            response = f"Here are some search results: {results}"
        elif "show logs" in user_input:
            os.system("python3 server.py &")  # Start the web server
            response = "Opening logs on the TV."
        else:
            response = "I don't understand that command."
            log_event(f"Command failed: {user_input}", "error")
            speak(response)
            return response

        log_execution_time(user_input, start_time)  # Log execution time

        # Save conversation memory
        save_memory(user_input, response)

        # Speak response
        speak(response)

    except Exception as e:
        log_event(f"Error executing command: {user_input} - {str(e)}", "error")
        response = "There was an error processing your request."
        speak(response)

    return response

if __name__ == "__main__":
    while True:
        user_input = transcribe_audio()
        if user_input:
            process_command(user_input)
