
import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join("database", "mindvault.db")

def connect():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT,
            tags TEXT,
            source TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

def add_memory(title, content, category, tags, source="manual"):
    with connect() as conn:
        conn.execute("""
        INSERT INTO memories
        (title, content, category, tags, source)
        VALUES (?, ?, ?, ?, ?)
        """, (title, content, category, tags, source))

def get_memories():
    with connect() as conn:
        rows = conn.execute("""
        SELECT * FROM memories
        ORDER BY created_at DESC, id DESC
        """).fetchall()
    return [dict(row) for row in rows]

def update_memory(memory_id, title, content, category, tags):
    with connect() as conn:
        conn.execute("""
        UPDATE memories
        SET title=?, content=?, category=?, tags=?
        WHERE id=?
        """, (title, content, category, tags, memory_id))

def delete_memory(memory_id):
    with connect() as conn:
        conn.execute(
            "DELETE FROM memories WHERE id=?",
            (memory_id,)
        )

def get_stats():
    with connect() as conn:
        total = conn.execute(
            "SELECT COUNT(*) FROM memories"
        ).fetchone()[0]

        categories = conn.execute(
            "SELECT COUNT(DISTINCT category) FROM memories"
        ).fetchone()[0]

        documents = conn.execute(
            "SELECT COUNT(DISTINCT source) FROM memories WHERE source != 'manual'"
        ).fetchone()[0]

    return total, categories, documents

def get_timeline():
    with connect() as conn:
        rows = conn.execute("""
        SELECT DATE(created_at) AS day, COUNT(*) AS count
        FROM memories
        GROUP BY DATE(created_at)
        ORDER BY day
        """).fetchall()

    return pd.DataFrame([dict(row) for row in rows])
