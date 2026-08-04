import sqlite3
import os

# Use DATABASE_PATH env var if set (configured in render.yaml for production).
# Falls back to the local project root for development.
_DEFAULT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database.db')
DATABASE_PATH = os.environ.get('DATABASE_PATH', _DEFAULT_PATH)

def get_db_connection():
    """Establish a connection to the SQLite database with Row factory."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create the contacts table if it does not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized successfully.")
