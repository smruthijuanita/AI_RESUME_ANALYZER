import streamlit as st


def persist_chat_exchange(user_id: int, message: str, response: str):
    """Save user message and assistant response to DB (when user is logged in)."""
    try:
        from db.database import save_chat_message
        save_chat_message(user_id, message, response)
    except Exception:
        pass


GREETING = """Hello 👋 I am your AI Career Guide.
I can help you with career advice, job roles, skills, resume tips, and interview preparation.
Please upload your resume so I can guide you better."""



def _debug_log(msg: str, data: dict):
    try:
        with open("/home/elvis/ai_resume_skill_analyzer/.cursor/debug-3261c7.log", "a") as f:
            import json, time
            f.write(json.dumps({"sessionId": "3261c7", "timestamp": int(time.time() * 1000), "message": msg, "data": data}) + "\n")
    except Exception:
        pass

def init_memory():
    # #region agent log
    _debug_log("init_memory entry", {"resume_uploaded_in_state": st.session_state.get("resume_uploaded"), "has_key": "resume_uploaded" in st.session_state})
    # #endregion
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "resume_uploaded" not in st.session_state:
        st.session_state.resume_uploaded = False
        # #region agent log
        _debug_log("init_memory set resume_uploaded=False", {"reason": "key_missing"})
        # #endregion

    if "resume_meta" not in st.session_state:
        st.session_state.resume_meta = None

    if "active_resume_hash" not in st.session_state:
        st.session_state.active_resume_hash = None

    if "messages" in st.session_state and not st.session_state.messages:
        st.session_state.messages.append({"role": "assistant", "content": GREETING})



def get_messages() -> list[dict[str, str]]:
    return st.session_state.get("messages", [])



def append_message(role: str, content: str):
    st.session_state.messages.append({"role": role, "content": content})
