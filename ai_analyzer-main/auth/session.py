"""Session management and route protection."""

import streamlit as st


def get_current_user():
    """Return (user_id, email, role) or None if not logged in."""
    if "user_id" not in st.session_state or st.session_state.user_id is None:
        return None
    return (
        st.session_state.user_id,
        st.session_state.user_email,
        st.session_state.user_role,
    )


def set_user(user_id: int, email: str, role: str):
    st.session_state.user_id = user_id
    st.session_state.user_email = email
    st.session_state.user_role = role


def logout():
    for key in ("user_id", "user_email", "user_role"):
        if key in st.session_state:
            del st.session_state[key]


def require_auth():
    """Redirect to Login if not authenticated."""
    if get_current_user() is None:
        st.switch_page("pages/1_Login.py")


def require_admin():
    """Redirect to Login if not authenticated, or to Chat if not admin."""
    user = get_current_user()
    if user is None:
        st.switch_page("pages/1_Login.py")
    if user[2] != "admin":
        st.switch_page("pages/3_Chat.py")
