import streamlit as st
import json
import os
from datetime import datetime, timedelta

# Default users file
USERS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "users.json")

def load_users():
    """Load user credentials from file."""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    else:
        # Default users
        default_users = {
            "admin": {
                "password": "admin123",
                "role": "Admin",
                "name": "Administrator"
            },
            "viewer": {
                "password": "viewer123",
                "role": "LST / Viewer",
                "name": "Executive Viewer"
            }
        }
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        with open(USERS_FILE, "w") as f:
            json.dump(default_users, f, indent=2)
        return default_users

def authenticate_user(username: str, password: str) -> dict:
    """
    Authenticate user credentials.
    
    Returns:
        dict with user info if valid, None if invalid
    """
    users = load_users()
    
    if username in users and users[username]["password"] == password:
        return {
            "username": username,
            "role": users[username]["role"],
            "name": users[username]["name"],
            "login_time": datetime.now()
        }
    return None

def is_authenticated():
    """Check if user is authenticated."""
    return "authenticated" in st.session_state and st.session_state.authenticated

def get_current_user():
    """Get current logged-in user."""
    if is_authenticated():
        return st.session_state.get("current_user")
    return None

def get_current_role():
    """Get current user's role."""
    user = get_current_user()
    if user:
        return user["role"]
    return None

def is_admin():
    """Check if current user is admin."""
    return get_current_role() == "Admin"

def logout():
    """Logout current user."""
    st.session_state.authenticated = False
    st.session_state.current_user = None
