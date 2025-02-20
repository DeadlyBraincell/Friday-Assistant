import os
import pvporcupine
import pyaudio
import struct
import requests
from logging import log_event

porcupine = pvporcupine.create(access_key="YOUR_PICOVOICE_ACCESS_KEY", keyword_paths=["friday_sleep.ppn"])

def listen_for_sleep():
    """Listens for 'Friday go to sleep' and shuts down AI."""
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=porcupine.sample_rate, input=True, frames_per_buffer=porcupine.frame_length)

    while True:
        pcm = stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        if porcupine.process(pcm) >= 0:
            log_event("Assistant is going to sleep.", "info")
            os.system("pkill -f assistant.py")
            break

    stream.close()
    pa.terminate()