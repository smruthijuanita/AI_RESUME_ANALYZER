import sqlite3
from config.config import DB_PATH


def init_db():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    # RESUME ANALYSIS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume_analysis(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        role TEXT,
        extracted_skills TEXT,
        missing_skills TEXT,
        roadmap TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()