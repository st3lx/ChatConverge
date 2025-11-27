import sqlite3
import os

class FTSDatabase:
    """
    Builds and queries a local SQLite FTS5 database for chat messages.
    """

    def __init__(self, db_path="chatconverge.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True) if os.path.dirname(db_path) else None
        self.conn = sqlite3.connect(self.db_path)
        self.create_schema()

    def create_schema(self):
        c = self.conn.cursor()
        c.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS messages
        USING fts5(timestamp, sender, text);
        """)
        self.conn.commit()

    def insert_messages(self, messages):
        c = self.conn.cursor()
        c.executemany(
            "INSERT INTO messages (timestamp, sender, text) VALUES (?, ?, ?)",
            [(m["timestamp"], m["sender"], m["text"]) for m in messages]
        )
        self.conn.commit()

    def search(self, query, limit=10):
        c = self.conn.cursor()
        c.execute("SELECT timestamp, sender, text FROM messages WHERE messages MATCH ? LIMIT ?;", (query, limit))
        return c.fetchall()
