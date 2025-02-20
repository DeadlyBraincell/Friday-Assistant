import sqlite3

DB_FILE = "assistant_memory.db"

def init_db():
    """Initialize memory database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS memory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        user_input TEXT,
                        assistant_response TEXT
                     )''')
    conn.commit()
    conn.close()

def save_memory(user_input, assistant_response):
    """Saves conversation history."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO memory (user_input, assistant_response) VALUES (?, ?)", (user_input, assistant_response))
    conn.commit()
    conn.close()

def fetch_memory(limit=5):
    """Fetches the last n stored interactions."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT user_input, assistant_response FROM memory ORDER BY timestamp DESC LIMIT ?", (limit,))
    memories = cursor.fetchall()
    conn.close()
    return memories

init_db()