import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent.parent / "clinic.db"


def get_connection():
    """
    Create and return SQLite connection.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def execute_query(query: str):
    """
    Execute SQL query and return results.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]