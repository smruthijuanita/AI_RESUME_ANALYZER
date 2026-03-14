"""Login logic: admin check first, then DB lookup."""

from config.config import settings
from db.database import get_user_by_email, update_last_login
from auth.session import set_user


def login(email: str, password: str):
    """
    Attempt login. Returns (user_id, email, role) on success, None on failure.
    Admin is checked via ADMIN_EMAIL and ADMIN_PASSWORD from config.
    """
    email = (email or "").strip()
    password = password or ""

    if not email or not password:
        return None

    # Admin check first
    if settings.ADMIN_EMAIL and settings.ADMIN_PASSWORD:
        if email == settings.ADMIN_EMAIL and password == settings.ADMIN_PASSWORD:
            # Admin has no DB row; use synthetic id 0 and update last_login is N/A
            set_user(0, email, "admin")
            return (0, email, "admin")

    # Regular user from DB
    row = get_user_by_email(email)
    if row is None:
        return None
    user_id, name, db_email, db_password, role, created_at, last_login, resume_uploaded = row
    if password != db_password:
        return None

    update_last_login(user_id)
    set_user(user_id, db_email, role)
    return (user_id, db_email, role)
