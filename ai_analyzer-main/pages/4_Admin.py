import streamlit as st

from auth.session import require_admin, get_current_user, logout
from admin.dashboard import render_dashboard

require_admin()

st.set_page_config(page_title="Admin Dashboard", page_icon="📊", layout="wide")

with st.sidebar:
    user = get_current_user()
    if user:
        st.write(f"Admin: **{user[1]}**")
        if st.button("Logout"):
            logout()
            st.switch_page("pages/1_Login.py")
        st.page_link("pages/3_Chat.py", label="Back to Chat")

render_dashboard()
