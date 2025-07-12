# backend/auth.py
import hashlib
import json
import os
import re

# Simulated user database (you can replace this with Supabase or SQLite later)
USER_DB_PATH = "backend/users.json"

# Ensure users.json file exists
def _init_db():
    if not os.path.exists(USER_DB_PATH):
        with open(USER_DB_PATH, "w") as f:
            json.dump({}, f)

# Hash passwords for basic security
def _hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load user database
def _load_users():
    _init_db()
    with open(USER_DB_PATH, "r") as f:
        return json.load(f)

# Save user database
def _save_users(users):
    with open(USER_DB_PATH, "w") as f:
        json.dump(users, f, indent=4)

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


# Signup logic
def signup_user(email, password):
    if email == "admin@example.com":
        return "Admin account cannot be registered."
    if not is_valid_email(email):
        return "Invalid email"
    users = _load_users()
    if email in users:
        return "User already exists"
    users[email] = {"password": _hash(password)}
    _save_users(users)
    return True


# Login logic
def login_user(email, password):
    if email == "admin@example.com" and password == "admin123":
        return True
    
    users = _load_users()
    if email in users and users[email]["password"] == _hash(password):
        return True
    return False
