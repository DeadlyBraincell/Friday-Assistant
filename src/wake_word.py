import pvporcupine
import pyaudio
import struct
import os
import time
from tts import speak
from led_control import pulse_leds
from system_check import check_system_status

porcupine = pvporcupine.create(
    access_key="YOUR_PICOVOICE_ACCESS_KEY",
    keyword_paths=["friday_wake_up.ppn"]
)

def wake_word_listener():
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=porcupine.sample_rate,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("Listening for 'Friday wake up'...")

    while True:
        pcm = stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            print("Wake word detected! Starting assistant...")

            # Pulse LEDs while booting
            pulse_leds()

            # Check system status
            issues = check_system_status()
            if issues:
                issue_text = "However, I detected the following issues: " + ", ".join(issues)
            else:
                issue_text = "All systems are running smoothly."

            speak(f"Welcome home. {issue_text}")

            # Start the assistant process
            os.system("python3 listener.py")
            break

    stream.close()
    pa.terminate()

if __name__ == "__main__":
    wake_word_listener()
