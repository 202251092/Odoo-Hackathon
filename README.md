
# 🔄 Skill Swap Platform

A web-based platform that allows users to **connect and exchange skills** with others in their community. Built using **Python and Streamlit**, it enables users to create public profiles, send swap requests, and manage their skill offerings – with a powerful admin dashboard to moderate and maintain the platform.

## 📺 Demo Video

🎥 [Click here to watch the demo video on Google Drive](https://drive.google.com/file/d/1lgWVaT9wfShc5wMsi6NfO9ydzFoQBdIA/view?usp=sharing)

---

## 🚀 Features

### 👤 User Features
- **Signup & Login** with email and password (stored with hashed security).
- **Create and update a public skill profile**, including name, location, skills offered/wanted, availability, and a profile image.
- **Browse other users' public profiles**.
- **Search** for people by skill or name.
- **Send skill swap requests** and track their status (pending, accepted, rejected).
- **View received requests** and **accept/reject** them.

### 🔐 Admin Features
- Special login with Admin.
- **View all users and their details**.
- **Ban/unban users**. Banned users:
  - Cannot log in or access the platform.
  - Do not appear in public profile listings.
  - Cannot receive swap requests.

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend/Logic**: Python
- **Storage**: JSON files (`users.json`, `profiles.json`, `requests.json`)
- **Image Uploads**: Stored in `assets/profile_images/`

---

## 📁 Directory Structure

```

.
├── app.py                    # Main entry point
├── backend/
│   ├── auth.py               # Signup/Login logic
│   ├── db.py                 # (optional DB init script)
│   └── utils.py              # Helper functions (e.g., ban check)
├── app\_pages/
│   ├── Home.py
│   ├── Profile.py
│   ├── SwapRequest.py
│   ├── Requests.py
│   └── Admin.py
├── assets/
│   └── profile\_images/       # Uploaded profile pictures
└── backend/
├── users.json            # Registered users
├── profiles.json         # Profile details
└── requests.json         # Swap request records

````

---

## ▶️ Getting Started

### ✅ 1. Clone the Repo
```bash
git clone https://github.com/yourusername/skill-swap-platform.git
cd skill-swap-platform
````

### ✅ 2. Install Dependencies

```bash
pip install streamlit pillow
```

### ✅ 3. Run the App

```bash
streamlit run app.py
```

---

## 🧪 Admin Login

* **Email:** `admin@example.com`
* **Password:** `admin123`

---

## 🧱 Future Improvements

* Replace JSON with a database (e.g., SQLite or Supabase).
* Add email notifications.
* Add chat or scheduling feature between matched users.
* UI enhancements for mobile users.

---

## 🙌 Contributors

* 👨‍💻 Nipur Patel (nipurpatel2004@gmail.com) – Backend, Frontend, UX
* 🤝 Contributions welcome!

---


