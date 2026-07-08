"""Main entry point for the Resource Planning & Cost Management app.

Handles database setup, login/session state, and role-based navigation.
Run with:
    streamlit run app.py
"""

import streamlit as st

from database.connection import create_db_and_tables
from models.user import UserRole

st.set_page_config(page_title="Kautex Hackaton Dashboard", page_icon=":material/space_dashboard:", layout="wide")

# Make sure the database and tables exist before the app is used.
create_db_and_tables()

# --- Session state defaults ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "auth_view" not in st.session_state:
    st.session_state.auth_view = "login"

# --- Logged-out: show only login or register ---
if not st.session_state.logged_in:
    if st.session_state.auth_view == "register":
        auth_pages = [st.Page("app_pages/register.py", title="Sign up", icon=":material/person_add:")]
    else:
        auth_pages = [st.Page("app_pages/login.py", title="Log in", icon=":material/lock:")]

    nav = st.navigation(auth_pages, position="hidden")
    nav.run()
    st.stop()

# --- Logged-in: role-based navigation ---
role = st.session_state.user.role

shared_pages = [
    st.Page("app_pages/dashboard.py", title="General dashboard", icon=":material/space_dashboard:"),
    st.Page("app_pages/topics.py", title="Topics", icon=":material/folder:"),
    st.Page("app_pages/allocation_matrix.py", title="Allocation matrix", icon=":material/grid_on:"),
    st.Page("app_pages/reports.py", title="Reports", icon=":material/bar_chart:"),
]
admin_only_pages = [
    st.Page("app_pages/employees.py", title="Employees", icon=":material/group:"),
]

# TODO: once the admin/employee dashboard prototypes arrive, split shared_pages
# further instead of giving both roles the same four pages.
pages = {"": shared_pages, "Admin": admin_only_pages} if role == UserRole.ADMIN else {"": shared_pages}

with st.sidebar:
    st.write(f"**{st.session_state.user.username}**")
    st.caption(role.value.capitalize())
    if st.button("Log out", icon=":material/logout:", width="stretch"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.auth_view = "login"
        st.rerun()

nav = st.navigation(pages)
nav.run()
