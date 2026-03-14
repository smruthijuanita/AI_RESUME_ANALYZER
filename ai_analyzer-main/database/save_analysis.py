import sqlite3
import json
from config.config import DB_PATH


def save_analysis(email, role, skills, missing, roadmap):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO resume_analysis
    (user_email, role, extracted_skills, missing_skills, roadmap)
    VALUES (?, ?, ?, ?, ?)
    """, (
        email,
        role,
        json.dumps(skills),
        json.dumps(missing),
        json.dumps(roadmap)
    ))

    conn.commit()
    conn.close()