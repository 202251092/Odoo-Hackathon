# pages/Home.py
import streamlit as st
import json
import os
from backend.utils import is_user_banned 

PROFILE_DB_PATH = "backend/profiles.json"

# Load profile data (simulate database)
def load_profiles():
    if not os.path.exists(PROFILE_DB_PATH):
        return []
    with open(PROFILE_DB_PATH, "r") as f:
        return json.load(f)

# Load and show public profiles
def load():
    email = st.session_state.get("user_email", "")
    if is_user_banned(email):                 
        st.error("🚫 Your account has been banned by the admin. Access denied.")
        st.stop()

    st.title("🌍 Browse Skill Profiles")

    query = st.text_input("Search by skill or name (e.g., 'Python', 'Ananya')")
    profiles = load_profiles()

    # Filter only public profiles
    public_profiles = [
        p for p in profiles
        if p.get("is_public", False) and not is_user_banned(p.get("email", ""))
    ]

    # Filter by skill search query
    if query:
        query_lower = query.lower()
        public_profiles = [
            p for p in public_profiles
            if query_lower in p.get("name", "").lower()
            or query_lower in ' '.join(p.get("skills_offered", []) + p.get("skills_wanted", [])).lower()
        ]

    if not public_profiles:
        st.info("No profiles match your search.")       
        return

    # Pagination
    page_size = 5
    page_num = st.number_input("Page", min_value=1, max_value=(len(public_profiles)-1)//page_size + 1, step=1)
    start = (page_num - 1) * page_size
    end = start + page_size
    paginated_profiles = public_profiles[start:end]

    for profile in paginated_profiles:
        with st.container():
            col1, col2 = st.columns([1, 3])

            # Profile photo
            img_path = None
            for ext in ["jpg", "jpeg", "png"]:
                candidate = os.path.join("assets/profile_images", f"{profile['email']}.{ext}")
                if os.path.exists(candidate):
                    img_path = candidate
                    break
            if img_path:
                col1.image(img_path, width=100)
            else:
                col1.write("🧑 No Photo")

            # Profile details
            col2.subheader(profile.get("name", "No Name"))
            col2.write(f"📍 {profile.get('location', 'N/A')}")
            col2.write(f"🗓️ Availability: {profile.get('availability', 'Not specified')}")

            # Stylized Skills
            offered = profile.get("skills_offered", [])
            wanted = profile.get("skills_wanted", [])

            col2.markdown("🎁 **Offers:** " + " ".join([f"`{s}`" for s in offered]) or "-")
            col2.markdown("🎯 **Wants:** " + " ".join([f"`{s}`" for s in wanted]) or "-")


            if profile["email"] != email:
                if st.button(f"Send Swap Request to {profile['name']}", key=f"req_{profile['email']}"):
                    st.session_state.swap_to_email = profile["email"]
                    st.session_state.navigate_to = "Send Swap Request"
                    st.rerun()


            st.markdown("---")
