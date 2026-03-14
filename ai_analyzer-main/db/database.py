"""Database connection and CRUD operations."""

import sqlite3
from datetime import datetime
from pathlib import Path

from config.config import settings
from db.models import USERS_TABLE, CHAT_HISTORY_TABLE, RESUMES_TABLE


def get_connection():
    path = settings.DB_PATH
    if isinstance(path, Path):
        path = str(path)
    return sqlite3.connect(path)


def init_db():
    conn = get_connection()
    conn.executescript(USERS_TABLE + CHAT_HISTORY_TABLE + RESUMES_TABLE)
    conn.commit()
    conn.close()


# ---------- Users ----------


def create_user(name: str, email: str, password: str) -> bool:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, 'client')",
            (name, email, password),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_user_by_email(email: str):
    conn = get_connection()
    row = conn.execute(
        "SELECT id, name, email, password, role, created_at, last_login, resume_uploaded FROM users WHERE email = ?",
        (email,),
    ).fetchone()
    conn.close()
    return row


def update_last_login(user_id: int):
    conn = get_connection()
    conn.execute(
        "UPDATE users SET last_login = ? WHERE id = ?",
        (datetime.utcnow().isoformat(), user_id),
    )
    conn.commit()
    conn.close()


def set_resume_uploaded(user_id: int, value: bool = True):
    conn = get_connection()
    conn.execute(
        "UPDATE users SET resume_uploaded = ? WHERE id = ?",
        (1 if value else 0, user_id),
    )
    conn.commit()
    conn.close()


def get_all_users():
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, name, email, role, created_at, last_login, resume_uploaded, country, age FROM users"
    ).fetchall()
    conn.close()
    return rows


# ---------- Chat history ----------


def save_chat_message(user_id: int, message: str, response: str):
    conn = get_connection()
    conn.execute(
        "INSERT INTO chat_history (user_id, message, response) VALUES (?, ?, ?)",
        (user_id, message, response),
    )
    conn.commit()
    conn.close()


def get_chat_count():
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) FROM chat_history").fetchone()[0]
    conn.close()
    return count


def get_all_chats():
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, user_id, message, response, timestamp FROM chat_history ORDER BY timestamp"
    ).fetchall()
    conn.close()
    return rows


# ---------- Resumes ----------


def save_resume(user_id: int, file_path: str, embedding_id: str):
    conn = get_connection()
    conn.execute(
        "INSERT INTO resumes (user_id, file_path, embedding_id) VALUES (?, ?, ?)",
        (user_id, file_path, embedding_id),
    )
    conn.commit()
    conn.close()


def get_resume_count():
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) FROM resumes").fetchone()[0]
    conn.close()
    return count


def get_all_resumes():
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, user_id, file_path, embedding_id, created_at FROM resumes"
    ).fetchall()
    conn.close()
    return rows
