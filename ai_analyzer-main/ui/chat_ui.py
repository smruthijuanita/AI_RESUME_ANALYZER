import streamlit as st

from agent import generate_career_response
from memory import append_message, get_messages, init_memory, persist_chat_exchange
from vector_db import build_vector_db_from_upload


CHAT_HEIGHT = 520


def _render_messages():
    with st.container(height=CHAT_HEIGHT):
        for message in get_messages():
            with st.chat_message(message["role"]):
                st.write(message["content"])


def _inject_layout_css():
    st.markdown(
        """
        <style>
        div[data-testid="stFileUploader"] {
            position: fixed;
            bottom: 1.15rem;
            right: 1.5rem;
            z-index: 9999;
            width: 6.25rem;
        }
        div[data-testid="stFileUploader"] section {
            min-height: 2.5rem;
            border-radius: 0.75rem;
        }
        div[data-testid="stChatInput"] {
            padding-right: 8.25rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _debug_log(msg: str, data: dict):
    try:
        with open("/home/elvis/ai_resume_skill_analyzer/.cursor/debug-3261c7.log", "a") as f:
            import json, time
            f.write(json.dumps({"sessionId": "3261c7", "timestamp": int(time.time() * 1000), "message": msg, "data": data}) + "\n")
    except Exception:
        pass

def _handle_resume_upload(pipeline, user_id=None):
    uploaded_file = st.file_uploader(
        "Upload resume",
        type=["pdf", "docx", "txt"],
        key="resume_upload",
        label_visibility="collapsed",
        help="📎 Upload resume",
    )

    if not uploaded_file:
        # #region agent log
        _debug_log("_handle_resume_upload early return", {"reason": "no_file", "resume_uploaded": st.session_state.get("resume_uploaded")})
        # #endregion
        return

    new_hash = hash(uploaded_file.getvalue())
    if st.session_state.active_resume_hash == new_hash:
        # #region agent log
        _debug_log("_handle_resume_upload skip duplicate", {"hash_match": True, "resume_uploaded": st.session_state.get("resume_uploaded")})
        # #endregion
        return

    with st.spinner("Processing resume and building vector DB..."):
        try:
            meta = build_vector_db_from_upload(pipeline, uploaded_file, user_id=user_id)
            st.session_state.resume_uploaded = True
            # #region agent log
            _debug_log("_handle_resume_upload SUCCESS", {"resume_uploaded_set": True, "retriever_set": pipeline.retriever is not None})
            # #endregion
            st.session_state.resume_meta = meta
            st.session_state.active_resume_hash = new_hash
            append_message(
                "assistant",
                "Resume uploaded and indexed. I can now provide personalized career guidance.",
            )
        except Exception as exc:
            st.session_state.resume_uploaded = False
            st.session_state.resume_meta = None
            # #region agent log
            _debug_log("_handle_resume_upload EXCEPTION", {"error": str(exc), "resume_uploaded_set": False})
            # #endregion
            append_message("assistant", f"I could not process that file: {exc}")


def render_chat_ui(pipeline, user_id=None):
    init_memory()

    _inject_layout_css()
    _handle_resume_upload(pipeline, user_id=user_id)

    _render_messages()

    prompt = st.chat_input("Ask career questions")

    if prompt:
        # #region agent log
        _debug_log("generate_career_response call", {"resume_uploaded": st.session_state.get("resume_uploaded"), "retriever": pipeline.retriever is not None})
        # #endregion
        append_message("user", prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Use pipeline.retriever as source of truth (persists in session); resume_uploaded can be lost on reruns
                has_resume = pipeline.retriever is not None
                answer = generate_career_response(
                    pipeline,
                    prompt,
                    resume_uploaded=has_resume,
                )
                st.write(answer)
        append_message("assistant", answer)
        if user_id is not None:
            persist_chat_exchange(user_id, prompt, answer)

    st.markdown(
        """
        <script>
          window.scrollTo(0, document.body.scrollHeight);
        </script>
        """,
        unsafe_allow_html=True,
    )
