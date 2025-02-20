import whisper

whisper_model = whisper.load_model("base")

def transcribe_audio(audio_path):
    """Converts speech to text."""
    result = whisper_model.transcribe(audio_path)
    return result["text"]