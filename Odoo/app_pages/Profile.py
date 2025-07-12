# pages/Profile.py
import streamlit as st
import json
import os
from PIL import Image
from backend.utils import is_user_banned


PROFILE_DB_PATH = "backend/profiles.json"
IMAGE_DIR = "assets/profile_images"

# Load existing profiles
def load_profiles():
    if not os.path.exists(PROFILE_DB_PATH):
        return []
    with open(PROFILE_DB_PATH, "r") as f:
        return json.load(f)

# Save updated profile list
def save_profiles(profiles):
    with open(PROFILE_DB_PATH, "w") as f:
        json.dump(profiles, f, indent=4)

# Save uploaded image
def save_profile_image(uploaded_file, email):
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image.thumbnail((500, 500))  # Optional resize for large images
        ext = uploaded_file.name.split(".")[-1]
        os.makedirs(IMAGE_DIR, exist_ok=True)  # Ensure directory exists
        path = os.path.join(IMAGE_DIR, f"{email}.{ext}")
        image.save(path)


# Main function
def load():
    st.title("👤 Edit My Profile")

    email = st.session_state.get("user_email", "")
    if not email:
        st.warning("You must be logged in to edit your profile.")
        return

    if is_user_banned(email):
        st.error("🚫 Your account has been banned by the admin. Access denied.")
        st.stop()

    profiles = load_profiles()
    profile = next((p for p in profiles if p["email"] == email), {
        "email": email,
        "name": "",
        "location": "",
        "skills_offered": [],
        "skills_wanted": [],
        "availability": "",
        "is_public": True
    })

    with st.form("profile_form"):
        name = st.text_input("Name", value=profile.get("name", ""))
        location = st.text_input("Location (optional)", value=profile.get("location", ""))
        skills_offered = st.text_input("Skills You Offer (comma-separated)", value=", ".join(profile.get("skills_offered", [])))
        skills_wanted = st.text_input("Skills You Want (comma-separated)", value=", ".join(profile.get("skills_wanted", [])))
        AVAIL_OPTIONS = ["Weekends", "Evenings", "Weekdays"]
        current_avail = profile.get("availability", "Weekends")
        if current_avail not in AVAIL_OPTIONS:
            current_avail = "Weekends"

        availability = st.selectbox("Availability", AVAIL_OPTIONS, index=AVAIL_OPTIONS.index(current_avail))

        is_public = st.checkbox("Make Profile Public", value=profile.get("is_public", True))

        uploaded_file = st.file_uploader("Upload Profile Image (jpg/png)", type=["jpg", "jpeg", "png"])
        img_path = None
        for ext in ["jpg", "jpeg", "png"]:
            candidate = os.path.join(IMAGE_DIR, f"{email}.{ext}")
            if os.path.exists(candidate):
                img_path = candidate
                break
        if img_path:
            st.image(img_path, caption="Current Profile Photo", width=150)

        submitted = st.form_submit_button("Save Profile")
        
        if submitted:
            profile.update({
                "name": name,
                "location": location,
                "skills_offered": [s.strip() for s in skills_offered.split(",") if s.strip()],
                "skills_wanted": [s.strip() for s in skills_wanted.split(",") if s.strip()],
                "availability": availability,
                "is_public": is_public
            })

            if uploaded_file:
                save_profile_image(uploaded_file, email)

            profiles = sorted([p for p in profiles if p["email"] != email] + [profile], key=lambda x: x["email"])
            save_profiles(profiles)
            st.success("Profile saved successfully!")
