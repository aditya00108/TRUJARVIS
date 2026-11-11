
"""
TRUJARVIS - Database Manager
Handles persistent chat and message storage.
"""

import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "trujarvis.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():

    with get_connection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id)
                REFERENCES conversations(id)
                ON DELETE CASCADE
            )
        """)


def create_conversation(title="New Chat"):

    with get_connection() as connection:

        cursor = connection.execute(
            "INSERT INTO conversations (title) VALUES (?)",
            (title,)
        )

        return cursor.lastrowid


def get_conversations():

    with get_connection() as connection:

        return connection.execute("""
            SELECT * FROM conversations
            ORDER BY created_at DESC, id DESC
        """).fetchall()


def save_message(conversation_id, role, content):

    with get_connection() as connection:

        connection.execute("""
            INSERT INTO messages
            (conversation_id, role, content)
            VALUES (?, ?, ?)
        """, (conversation_id, role, content))


def get_messages(conversation_id):

    with get_connection() as connection:

        return connection.execute("""
            SELECT role, content
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id ASC
        """, (conversation_id,)).fetchall()


def delete_conversation(conversation_id):

    with get_connection() as connection:

        connection.execute(
            "DELETE FROM messages WHERE conversation_id = ?",
            (conversation_id,)
        )

        connection.execute(
            "DELETE FROM conversations WHERE id = ?",
            (conversation_id,)
        )

def update_conversation_title(conversation_id, title):

    with get_connection() as connection:

        connection.execute(
            """
            UPDATE conversations
            SET title = ?
            WHERE id = ?
            """,
            (title, conversation_id)
        )

def rename_conversation(conversation_id, new_title):

    with get_connection() as connection:

        connection.execute(
            """
            UPDATE conversations
            SET title = ?
            WHERE id = ?
            """,
            (new_title, conversation_id)
        )


def delete_all_conversations():

    with get_connection() as connection:

        connection.execute("DELETE FROM messages")
        connection.execute("DELETE FROM conversations")
