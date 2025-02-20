import pvporcupine
import pyaudio
import struct
import os

porcupine = pvporcupine.create(
    access_key="YOUR_PICOVOICE_ACCESS_KEY",
    keyword_paths=["friday.ppn"]
)

def listen_for_command():
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=porcupine.sample_rate,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("Waiting for 'Friday' command...")

    while True:
        pcm = stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            print("Wake word detected! Listening for command...")
            os.system("python3 assistant.py")

    stream.close()
    pa.terminate()

if __name__ == "__main__":
    listen_for_command()