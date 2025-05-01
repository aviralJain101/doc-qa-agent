import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"  # Change this if backend is hosted elsewhere

# Session state for managing login status
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None
# if 'user_id' not in st.session_state:
#     st.session_state.user_id = None

# Login page

def login_page():
    st.title("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        response = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
        if response.status_code == 200:
            token = response.json()["access_token"]
            st.session_state.auth_token = token
            # st.session_state.user_id = response.json()["user_id"]
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Login failed")

    st.markdown("Don't have an account? Go to Register tab")

# Register page

def register_page():
    st.title("Register")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")

    if st.button("Register"):
        response = requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password})
        if response.status_code == 200:
            st.success("Registration successful! Go to Login tab")
        else:
            st.error("Registration failed")

# Chat page

def chat_page():
    st.title("DocuChat")
    uploaded_file = st.file_uploader("Upload a file")
    if uploaded_file:
        files = {
            "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
        }
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        response = requests.post(f"{BASE_URL}/api/upload", files=files, headers=headers)
        if response.status_code == 200:
            st.success("File uploaded")
        else:
            st.error("Failed to upload file")

    query = st.text_input("Ask a question", key="chat_query")
    if st.button("Ask"):
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        response = requests.post(f"{BASE_URL}/api/query", json={"question": query}, headers=headers)
        if response.status_code == 200:
            st.write("Answer:", response.json()["answer"])
        else:
            st.error("Error fetching answer")

    if st.button("Logout"):
        st.session_state.auth_token = None
        # st.session_state.user_id = None
        st.rerun()

# Page routing

def main():
    if st.session_state.auth_token:
        chat_page()
    else:
        tab1, tab2 = st.tabs(["Login", "Register"])
        with tab1:
            login_page()
        with tab2:
            register_page()


if __name__ == "__main__":
    main()
