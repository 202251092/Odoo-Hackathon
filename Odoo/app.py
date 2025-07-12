# app.py 
import streamlit as st
from backend import auth

st.set_page_config(page_title="Skill Swap Platform", layout="wide")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""

# --- LOGIN/SIGNUP PAGE --- #
def login_page():
    st.title("🔐 Welcome to Skill Swap Platform")

    choice = st.radio("Login or Signup?", ["Login", "Signup"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if choice == "Signup":
        if st.button("Create Account"):
            created = auth.signup_user(email, password)
            if created:
                st.success("Account created! You can now log in.")
            else:
                st.error("User already exists.")

    elif choice == "Login":
        if st.button("Log In"):
            success = auth.login_user(email, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials")

# --- MAIN APP NAVIGATION --- #
def main_app():
    st.sidebar.title("📂 Navigation")

    pages = ["Home", "My Profile", "Send Swap Request", "My Requests"]
    if st.session_state.user_email == "admin@example.com":
        pages.append("Admin")

    # Remember or redirect to a selected page
    if "navigate_to" in st.session_state:
        page = st.session_state.navigate_to
        st.session_state.current_page = page  # persist current page
        del st.session_state.navigate_to
    else:
        # Use current_page if already set, else default to "Home"
        default_page = st.session_state.get("current_page", "Home")
        page = st.sidebar.radio("Go to", pages, index=pages.index(default_page))
        st.session_state.current_page = page  # persist current page

    # --- Page routing --- #
    if page == "Home":
        from app_pages import Home
        Home.load()
    elif page == "My Profile":
        from app_pages import Profile
        Profile.load()
    elif page == "Send Swap Request":
        from app_pages import SwapRequest
        SwapRequest.load()
    elif page == "My Requests":
        from app_pages import Requests
        Requests.load()
    elif page == "Admin":
        from app_pages import Admin
        Admin.load()

    if st.sidebar.button("🚪 Log Out"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.rerun()


# --- RUN APP --- #
if st.session_state.logged_in:
    main_app()
else:
    login_page()
