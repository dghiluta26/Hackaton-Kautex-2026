"""Registration page. Self-service sign-up always creates an employee account.

Admin accounts are only created via database/seed.py (for now).
"""

from __future__ import annotations
import streamlit as st

from models.user import UserRole
from services.auth_service import register_user

with st.container(horizontal_alignment="center"):
    with st.container(width=450, border=True):
        st.subheader("Create your account")
        st.caption("Kautex Hackaton Dashboard")

        with st.form("register_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm password", type="password")
            submitted = st.form_submit_button("Sign up", width="stretch")

        if submitted:
            if not username or not password:
                st.error("Username and password are required.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                try:
                    register_user(username, password, role=UserRole.EMPLOYEE)
                except ValueError as e:
                    st.error(str(e))
                else:
                    st.success("Account created. You can now log in.")

        st.divider()
        st.caption("Already have an account?")
        if st.button("Log in", width="stretch"):
            st.session_state.auth_view = "login"
            st.rerun()
