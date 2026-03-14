"""Signup logic: create client user only."""

from db.database import create_user


def signup(name: str, email: str, password: str) -> tuple[bool, str]:
    """
    Create a new client user. Returns (success, message).
    """
    name = (name or "").strip()
    email = (email or "").strip()
    password = password or ""

    if not name:
        return False, "Name is required."
    if not email:
        return False, "Email is required."
    if not password:
        return False, "Password is required."

    if create_user(name, email, password):
        return True, "Account created. Please log in."
    return False, "Email already registered."
