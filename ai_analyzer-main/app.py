import streamlit as st

from db.database import init_db
from auth.session import get_current_user

# Initialize database at startup
init_db()

st.set_page_config(page_title="Resume RAG Chatbot", page_icon="📄", layout="wide")

# Router: redirect based on auth
user = get_current_user()
if user is None:
    st.switch_page("pages/1_Login.py")
if user[2] == "admin":
    st.switch_page("pages/4_Admin.py")
st.switch_page("pages/3_Chat.py")
