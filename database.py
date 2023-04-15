from datetime import datetime
from sqlite3 import connect
from dataclasses import dataclass


@dataclass
class Message:
    id: int
    content: str
    created_at: str


class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = connect(db_name, check_same_thread=False)

    def create_tables(self):
        cursor = self.conn.cursor()

        # CURRENT_TIMESTAMP in local timezone

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

        cursor.close()

    def add_message(self, content: str) -> Message:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO messages (content, created_at) VALUES (?, ?)
            """,
            (content, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        self.conn.commit()
        cursor.execute(
            """
            SELECT * FROM messages WHERE id = ?
            """,
            (cursor.lastrowid,),
        )
        message = Message(*cursor.fetchone())
        cursor.close()
        return message

    def get_messages(self) -> list[Message]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT * FROM messages ORDER BY id ASC
            """
        )
        messages = [Message(*row) for row in cursor.fetchall()]
        cursor.close()
        return messages


db = Database("database.db")
db.create_tables()
