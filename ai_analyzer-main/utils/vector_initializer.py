from pathlib import Path

import streamlit as st

from config.config import settings


def _find_pdf_files(data_dir: Path) -> list[Path]:
    return sorted(data_dir.glob("*.pdf"))


def initialize_vector_db(pipeline) -> bool:
    """Build vector DB once per session from the first local PDF in data/.

    Returns True when retriever is ready, False otherwise.
    """
    if st.session_state.get("vector_db_ready", False):
        return True

    if st.session_state.get("vector_db_failed", False):
        return False

    pdf_files = _find_pdf_files(settings.DATA_DIR)
    if not pdf_files:
        st.session_state.vector_db_failed = True
        st.session_state.vector_db_error = (
            f"No PDF found in {settings.DATA_DIR}. Add one PDF file to start chat."
        )
        return False

    try:
        result = pipeline.build_from_file_path(pdf_files[0])
        st.session_state.vector_db_ready = True
        st.session_state.vector_db_meta = result
        return True
    except Exception as exc:
        st.session_state.vector_db_failed = True
        st.session_state.vector_db_error = str(exc)
        return False
