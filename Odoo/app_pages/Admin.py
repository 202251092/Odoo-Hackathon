# pages/Admin.py
import streamlit as st
import json
import os
from backend.utils import is_user_banned

PROFILE_DB_PATH = "backend/profiles.json"
REQUEST_DB_PATH = "backend/requests.json"

# Load profiles
def load_profiles():
    if not os.path.exists(PROFILE_DB_PATH):
        return []
    with open(PROFILE_DB_PATH, "r") as f:
        return json.load(f)

# Save profiles
def save_profiles(profiles):
    with open(PROFILE_DB_PATH, "w") as f:
        json.dump(profiles, f, indent=4)

# Load requests
def load_requests():
    if not os.path.exists(REQUEST_DB_PATH):
        return []
    with open(REQUEST_DB_PATH, "r") as f:
        return json.load(f)

# Main Admin View
def load():
    email = st.session_state.get("user_email", "")
    if is_user_banned(email):
        st.error("🚫 Your account has been banned by the admin. Access denied.")
        return

    st.title("🛠️ Admin Dashboard")

    if email != "admin@example.com":
        st.error("Access Denied. Only admin can view this page.")
        return

    st.subheader("👥 All User Profiles")
    search_query = st.text_input("Search by name or email")
    profiles = load_profiles()
    edited = False

    # Filter based on search query
    if search_query:
        profiles = [p for p in profiles if search_query.lower() in p["email"].lower() or search_query.lower() in p["name"].lower()]


    for i, p in enumerate(profiles):
        label = f"{p['name']} ({p['email']})"
        if p.get("banned"):
            label = f"🚫 {label}"
        with st.expander(label):
            st.write(f"Location: {p.get('location', '-')}")
            st.write(f"Skills Offered: {', '.join(p.get('skills_offered', []))}")
            st.write(f"Skills Wanted: {', '.join(p.get('skills_wanted', []))}")
            st.write(f"Availability: {p.get('availability', '-')}")
            st.write("Public Profile: " + ("✅" if p.get("is_public") else "❌"))
            banned = p.get("banned", False)
            st.markdown(f"**Status:** {'🚫 BANNED' if banned else '✅ Active'}")
            if st.button("❌ Ban User", key=f"ban_{i}"):
                profiles[i]["banned"] = True
                edited = True
                st.warning(f"User {p['email']} has been banned.")
            if st.button("✅ Unban User", key=f"unban_{i}"):
                profiles[i]["banned"] = False
                edited = True
                st.success(f"User {p['email']} has been unbanned.")

    if edited:
        save_profiles(profiles)

    st.subheader("🔁 All Swap Requests")
    requests = load_requests()
    for r in requests:
        st.markdown(f"- `{r['from']}` ➡️ `{r['to']}`: {r['offered']} ↔ {r['wanted']} — **{r['status']}**")

    st.subheader("📤 Download Reports")
    if st.button("Download All Profiles JSON"):
        st.download_button("Download", json.dumps(profiles, indent=2), file_name="profiles.json")

    if st.button("Download All Requests JSON"):
        st.download_button("Download", json.dumps(requests, indent=2), file_name="requests.json")
