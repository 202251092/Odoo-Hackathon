import streamlit as st
import json
import os
from backend.utils import is_user_banned

PROFILE_DB_PATH = "backend/profiles.json"
REQUEST_DB_PATH = "backend/requests.json"

# Load all profiles
def load_profiles():
    if not os.path.exists(PROFILE_DB_PATH):
        return []
    with open(PROFILE_DB_PATH, "r") as f:
        return json.load(f)

# Save request
def save_request(request):
    if not os.path.exists(REQUEST_DB_PATH):
        with open(REQUEST_DB_PATH, "w") as f:
            json.dump([], f)
    with open(REQUEST_DB_PATH, "r") as f:
        all_requests = json.load(f)
    all_requests.append(request)
    with open(REQUEST_DB_PATH, "w") as f:
        json.dump(all_requests, f, indent=4)

# Load all requests (used for duplicate check)
def load_requests():
    if not os.path.exists(REQUEST_DB_PATH):
        return []
    with open(REQUEST_DB_PATH, "r") as f:
        return json.load(f)

# Main function
def load():
    st.title("🔄 Send a Skill Swap Request")

    current_email = st.session_state.get("user_email", "")

    #  First, check if user is logged in
    if not current_email:
        st.warning("You must be logged in to send requests.")
        return

    #  Then check if user is banned
    if is_user_banned(current_email):
        st.error("🚫 Your account has been banned by the admin. Access denied.")
        st.stop()

    profiles = load_profiles()
    user_profile = next((p for p in profiles if p.get("email") == current_email), None)
    other_profiles = [
        p for p in profiles
        if p.get("email") != current_email and p.get("is_public") and not is_user_banned(p.get("email", ""))
    ]


    if not user_profile:
        st.info("Please complete your profile before sending requests.")
        return

    if not other_profiles:
        st.info("No public profiles available to send requests.")
        return

    recipient_names = [p["name"] for p in other_profiles]
    default_index = 0

    if "swap_to_email" in st.session_state:
        pre_email = st.session_state.swap_to_email
        for i, p in enumerate(other_profiles):
            if p["email"] == pre_email:
                default_index = i
                break
        del st.session_state.swap_to_email  # Clear after use

    recipient = st.selectbox("Choose a user to send a request to:", recipient_names, index=default_index)
    recipient_profile = next(p for p in other_profiles if p["name"] == recipient)

    # Validate skills are available
    if not user_profile.get("skills_offered"):
        st.warning("You must list some skills you're offering in your profile before sending requests.")
        return

    if not recipient_profile.get("skills_offered"):
        st.warning(f"{recipient} has no listed skills to request from.")
        return

    offered = st.selectbox("Select one of your skills to offer:", user_profile.get("skills_offered", []))
    wanted = st.selectbox("Select one of their skills you want:", recipient_profile.get("skills_offered", []))
    note = st.text_area("Optional note or preferred time")

    if st.button("Send Request"):
        all_requests = load_requests()
        
        # Prevent duplicate requests
        duplicate = any(
            r["from"] == current_email and
            r["to"] == recipient_profile["email"] and
            r["offered"] == offered and
            r["wanted"] == wanted
            for r in all_requests
        )
        if duplicate:
            st.warning("You have already sent a similar request.")
            return

        req = {
            "from": current_email,
            "to": recipient_profile["email"],
            "offered": offered,
            "wanted": wanted,
            "note": note,
            "status": "pending"
        }
        save_request(req)
        st.success("Swap request sent!")
