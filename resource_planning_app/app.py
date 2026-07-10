"""Main entry point for the Resource Planning & Cost Management app.

Handles database setup, login/session state, and role-based navigation.
Run with:
    streamlit run app.py
"""
from __future__ import annotations
import streamlit as st

from app_theme import inject_app_theme, render_theme_toggle
from database.connection import create_db_and_tables
from models.user import UserRole

st.set_page_config(
    page_title="Kautex Engineering Planning",
    page_icon=":material/space_dashboard:",
    layout="wide",
    initial_sidebar_state="auto",
)
render_theme_toggle()
inject_app_theme()

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
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {
            position: relative;
            background: linear-gradient(180deg, #041426 0%, #0A2D56 100%);
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        section[data-testid="stSidebar"] * {
            color: rgba(255,255,255,0.88) !important;
        }

        section[data-testid="stSidebar"] > div:first-child {
            padding-bottom: 145px !important;
        }

        section[data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.14);
            margin: 10px 0 12px 0;
        }

        section[data-testid="stSidebar"] button {
            border-radius: 14px;
            transition: filter 0.2s ease;
        }

        .st-key-sidebar_bottom button:hover {
            background: rgba(255,255,255,0.24) !important;
        }

        .st-key-sidebar_bottom {
            position: absolute;
            left: 8px;
            right: 8px;
            bottom: 14px;
            width: auto;
            z-index: 9999;
            background: #08294f;
            padding: 10px 0 0 0;
            box-sizing: border-box;
        }

        .st-key-sidebar_bottom button {
            background: rgba(255,255,255,0.10) !important;
            border: 1px solid rgba(255,255,255,0.18) !important;
        }

        .st-key-sidebar_bottom button,
        .st-key-sidebar_bottom button span,
        .st-key-sidebar_bottom button p,
        .st-key-sidebar_bottom button svg {
            color: #ffffff !important;
            fill: #ffffff !important;
        }

        .sidebar-profile {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 6px 2px 10px 2px;
        }

        .sidebar-avatar {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background: #0057B8;
            color: white !important;
            font-weight: 800;
            font-size: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid rgba(255,255,255,0.28);
            flex-shrink: 0;
        }

        .sidebar-name {
            color: white !important;
            font-size: 15px;
            font-weight: 400;
            margin: 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    initial = st.session_state.user.username[0].upper()

    with st.container(key="sidebar_bottom"):
        st.divider()

        st.markdown(
            f"""
            <div class="sidebar-profile">
                <div class="sidebar-avatar">{initial}</div>
                <div>
                    <p class="sidebar-name">
                        {st.session_state.user.username}
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Log out",
            icon=":material/logout:",
            width="stretch",
        ):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.auth_view = "login"
            st.rerun()
nav = st.navigation(pages)
nav.run()