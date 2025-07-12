# backend/utils.py
import json
import os

PROFILE_DB_PATH = "backend/profiles.json"

def is_user_banned(email):
    if not os.path.exists(PROFILE_DB_PATH):
        return False
    with open(PROFILE_DB_PATH, "r") as f:
        profiles = json.load(f)
    for profile in profiles:
        if profile.get("email") == email:
            return profile.get("banned", False)
    return False
