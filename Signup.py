import streamlit as st
import sqlite3
import re
import bcrypt
from Database_init import init_db
import os

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.switch_page("pages/Path.py")


# Check if the database exists
if not os.path.exists('users.db'):
    print("Database not found. Initializing database...")
    init_db()
    print("Database initialized successfully.")

# Function to add a new user to the database
def add_user(email, contact_number, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (email, contact_number, password) VALUES (?, ?, ?)
    ''', (email, contact_number, hashed_password))
    conn.commit()
    conn.close()

# Function to validate email and phone number
def is_valid_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

def is_valid_phone(phone):
    return re.match(r'^\d{10}$', phone)

# Sign-up form
st.subheader("Create New Account")
new_user = st.text_input("Email")
contact_number = st.text_input("Phone number")
new_password = st.text_input("Password", type='password')


if st.button("Signup"):
    if not is_valid_email(new_user):
        st.error("Invalid email address.")
    elif not is_valid_phone(contact_number):
        st.error("Invalid contact number. It should consist of exactly 10 digits.")
        
    else:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email=?', (new_user,))
        if cursor.fetchone():
            st.error("User already exists. Please log in.")
        else:
            add_user(new_user, contact_number, new_password)
            st.session_state.logged_in = True
            st.success(f"Signed up as {new_user}")
            st.info("Click the Home button to get the career path")
        conn.close()
        
if st.session_state.logged_in and st.button("Home"):
    st.switch_page("pages/Path.py")

st.markdown("Already have an account?")
if st.button("Login"):
    st.switch_page("pages/Login.py")
