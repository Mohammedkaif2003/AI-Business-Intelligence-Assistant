import streamlit as st

USERS = {
    "admin": {"password": "admin123", "role": "Admin"},
    "sales": {"password": "sales123", "role": "Sales"},
    "hr": {"password": "hr123", "role": "HR"}
}

def login():

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.role = None

    if not st.session_state.authenticated:

        st.title("🔐 Login to AI BI System")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            if username in USERS and USERS[username]["password"] == password:
                st.session_state.authenticated = True
                st.session_state.role = USERS[username]["role"]
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

        st.stop()