import streamlit as st

from auth.session import require_auth, get_current_user, logout
from ui.chat_ui import render_chat_ui
from utils.rag_pipeline import ResumeRAGPipeline

require_auth()

st.set_page_config(page_title="Chat", page_icon="💬", layout="wide")
st.title("Resume RAG Chatbot")
st.caption("Chat with your resume context, tutorials, and roadmap guidance.")

# Sidebar: user info and logout
with st.sidebar:
    user = get_current_user()
    if user:
        st.write(f"Logged in as **{user[1]}**")
        st.write(f"Role: {user[2]}")
        if user[2] == "admin":
            st.page_link("pages/4_Admin.py", label="Admin Dashboard")
        if st.button("Logout"):
            logout()
            st.switch_page("pages/1_Login.py")

if "pipeline" not in st.session_state:
    try:
        st.session_state.pipeline = ResumeRAGPipeline()
    except Exception as exc:
        st.error(f"Pipeline initialization failed: {exc}")
        st.info("Set environment variables in your shell and restart Streamlit.")
        st.stop()

user_id = st.session_state.user_id if st.session_state.user_role != "admin" else None
render_chat_ui(st.session_state.pipeline, user_id=user_id)
