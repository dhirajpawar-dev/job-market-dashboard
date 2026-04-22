import sqlite3
import bcrypt
import streamlit as st
import random

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def signup_user(name, email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                  (name, email, hashed))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT name, password FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()
    if user and bcrypt.checkpw(password.encode(), user[1]):
        return user[0]
    return None

def show_auth():
    # Center the form like Google
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/3281/3281289.png", width=60)
        st.title("Job Market Dashboard")
        st.markdown("Sign in to continue")
        st.markdown("---")

        if "show_signup" not in st.session_state:
            st.session_state["show_signup"] = False

        if st.session_state["show_signup"]:
            # SIGNUP FORM
            st.subheader("Create your account")
            name = st.text_input("Full Name", key="signup_name")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_pass")

            if st.button("Sign Up", use_container_width=True):
                if name and email and password:
                    if len(password) < 6:
                        st.error("Password must be at least 6 characters.")
                    elif signup_user(name, email, password):
                        st.success("Account created successfully!")
                        st.session_state["show_signup"] = False
                        st.rerun()
                    else:
                        st.error("Email already exists!")
                else:
                    st.warning("Please fill in all fields.")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("Already have an account?")
            if st.button("Sign In instead", use_container_width=True):
                st.session_state["show_signup"] = False
                st.rerun()

        else:
            # LOGIN FORM
            st.subheader("Welcome back")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pass")

            if st.button("Sign In", use_container_width=True):
                if email and password:
                    name = login_user(email, password)
                    if name:
                        st.session_state["logged_in"] = True
                        st.session_state["user_name"] = name
                        st.rerun()
                    else:
                        st.error("Invalid email or password!")
                else:
                    st.warning("Please fill in all fields.")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("Don't have an account?")
            if st.button("Create account", use_container_width=True):
                st.session_state["show_signup"] = True
                st.rerun()