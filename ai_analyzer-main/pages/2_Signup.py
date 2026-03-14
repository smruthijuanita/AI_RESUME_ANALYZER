import streamlit as st

from auth.signup import signup
from auth.session import get_current_user

st.set_page_config(page_title="Sign up", page_icon="📝", layout="centered")
st.title("Create Account")

# If already logged in, redirect to chat
if get_current_user():
    st.switch_page("pages/3_Chat.py")

with st.form("signup_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Sign up")

if submitted:
    ok, msg = signup(name, email, password)
    if ok:
        st.success(msg)
    else:
        st.error(msg)

st.page_link("pages/1_Login.py", label="Already have an account? Log in")
