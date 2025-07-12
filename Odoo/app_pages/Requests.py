import streamlit as st
import json
import os
from PIL import Image
from backend.utils import is_user_banned

REQUEST_DB_PATH = "backend/requests.json"
PROFILE_DB_PATH = "backend/profiles.json"
IMAGE_DIR = "assets/profile_images"
os.makedirs(IMAGE_DIR, exist_ok=True)  

# Load requests
def load_requests():
    if not os.path.exists(REQUEST_DB_PATH):
        return []
    with open(REQUEST_DB_PATH, "r") as f:
        return json.load(f)

# Save all requests
def save_requests(requests):
    with open(REQUEST_DB_PATH, "w") as f:
        json.dump(requests, f, indent=4)

# Load profile name from email
def get_name(email):
    if not os.path.exists(PROFILE_DB_PATH):
        return email
    with open(PROFILE_DB_PATH, "r") as f:
        profiles = json.load(f)
    for p in profiles:
        if p.get("email") == email:
            return p.get("name", email)
    return email

# Robust image loader
def get_profile_image(email):
    if not email:
        return None
    for ext in ["jpg", "jpeg", "png"]:
        path = os.path.join(IMAGE_DIR, f"{email}.{ext}")
        if os.path.exists(path):
            return path
    return None

# Main function
def load():
    st.title("📬 My Swap Requests")
    
    email = st.session_state.get("user_email", "")
    if not email:
        st.warning("You must be logged in to view your requests.")
        return

    if is_user_banned(email):  
        st.error("🚫 Your account has been banned by the admin. Access denied.")
        st.stop()   

    all_requests = load_requests()
    sent = [r for r in all_requests if r["from"] == email]
    received = [r for r in all_requests if r["to"] == email]

    tab1, tab2 = st.tabs(["📤 Sent Requests", "📥 Received Requests"])

    status_display = {
        "pending": "🕓 Pending",
        "accepted": "✅ Accepted",
        "rejected": "❌ Rejected"
    }

    with tab1:
        if sent:
            for req in sent:
                st.markdown(f"**To:** {get_name(req['to'])}")
                img_path = get_profile_image(req['to'])
                if img_path:
                    st.image(img_path, width=100)
                st.write(f"You offer: {req['offered']} ↔ Want: {req['wanted']}")
                status = req['status']
                st.write(f"Status: `{status}` {status_display.get(status, '')}")
                if req.get("note"):
                    st.write(f"Note: {req['note']}")
                st.markdown("---")
        else:
            st.info("No sent requests yet.")

    with tab2:
        if received:
            for i, req in enumerate(received):
                st.markdown(f"**From:** {get_name(req['from'])}")
                img_path = get_profile_image(req['from'])
                if img_path:
                    st.image(img_path, width=100)
                st.write(f"They offer: {req['offered']} ↔ Want: {req['wanted']}")
                st.write(f"Note: {req.get('note', '-')}")
                status = req['status']
                st.write(f"Status: `{status}` {status_display.get(status, '')}")

                if status == "pending":
                    col1, col2 = st.columns(2)
                    
                    if col1.button("✅ Accept", key=f"accept_{i}"):
                        for r in all_requests:
                            if r["from"] == req["from"] and r["to"] == req["to"] and r["status"] == "pending":
                                r["status"] = "accepted"
                                break
                        save_requests(all_requests)
                        st.success("Request accepted")
                        st.rerun()

                    if col2.button("❌ Reject", key=f"reject_{i}"):
                        for r in all_requests:
                            if r["from"] == req["from"] and r["to"] == req["to"] and r["status"] == "pending":
                                r["status"] = "rejected"
                                break
                        save_requests(all_requests)
                        st.warning("Request rejected")
                        st.rerun()


                st.markdown("---")
        else:
            st.info("No incoming requests yet.")
