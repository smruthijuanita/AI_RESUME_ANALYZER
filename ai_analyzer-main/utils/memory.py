import streamlit as st


def init_memory():

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "skills" not in st.session_state:
        st.session_state.skills = []

    if "missing_skills" not in st.session_state:
        st.session_state.missing_skills = []

    if "messages" not in st.session_state:
        st.session_state.messages = []


def get_messages() -> list[dict[str, str]]:
    return st.session_state.get("messages", [])


def append_message(role: str, content: str):
    st.session_state.messages.append({"role": role, "content": content})