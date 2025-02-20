import sounddevice as sd
import numpy as np
from TTS.api import TTS

def speak(text):
    """Converts text to speech."""
    tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")
    audio = tts.tts(text)
    sd.play(np.array(audio), samplerate=22050)
    sd.wait()