import openai
import whisper
import sqlite3

whisper_model = whisper.load_model("base")
openai.api_key = "your-api-key"

conn = sqlite3.connect("notes.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)''')
conn.commit()

def take_note(audio_file):
    """Converts speech to text and stores it as a note."""
    result = whisper_model.transcribe(audio_file)
    text = result["text"]
    cursor.execute("INSERT INTO notes (content) VALUES (?)", (text,))
    conn.commit()
    return text

def summarize_notes():
    """Summarizes saved notes using OpenAI."""
    cursor.execute("SELECT content FROM notes")
    notes = [note[0] for note in cursor.fetchall()]
    full_text = " ".join(notes)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Summarize the following notes:"}, {"role": "user", "content": full_text}]
    )
    return response["choices"][0]["message"]["content"]