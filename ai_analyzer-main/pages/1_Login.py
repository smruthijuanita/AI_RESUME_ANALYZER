import streamlit as st

from auth.login import login
from auth.session import get_current_user

st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")
st.title("Login")

# If already logged in, redirect
if get_current_user():
    if st.session_state.user_role == "admin":
        st.switch_page("pages/4_Admin.py")
    st.switch_page("pages/3_Chat.py")

with st.form("login_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

if submitted:
    result = login(email, password)
    if result:
        st.success("Login successful!")
        if result[2] == "admin":
            st.switch_page("pages/4_Admin.py")
        st.switch_page("pages/3_Chat.py")
    else:
        st.error("Invalid email or password.")

st.page_link("pages/2_Signup.py", label="Don't have an account? Sign up")
