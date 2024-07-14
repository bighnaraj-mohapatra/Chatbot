import streamlit as st
import sqlite3
import bcrypt

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.switch_page("pages/Path.py")

# Function to check user credentials
def check_user(email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE email=?', (email,))
    user = cursor.fetchone()
    conn.close()
    if user and bcrypt.checkpw(password.encode('utf-8'), user[0]):
        return True
    return False

# Login form
st.subheader("Login Section")
username = st.text_input("Username",key = 'user_input')
password = st.text_input("Password", type='password',key='password_input')
if st.button("Login", key = 'login_button'):
    
    user = check_user(username, password)
    if user:
        st.session_state.logged_in = True
        st.success(f"Logged In as {username}")
        st.info("Click the Home button to get the career path")
    else:
        st.error("Invalid credentials")

if st.session_state.logged_in and st.button("Home",key = 'home_button'):
    st.switch_page("pages/Path.py")

st.markdown("Don't have an account?")
if st.button("Sign up",key = 'signup_button'):
    st.switch_page("Signup.py")
