"""Login page.

Layout mirrors the prototype: a branding panel next to the credentials
form. Colors/logo are left as native theme defaults for now and will be
styled once the real branding assets are provided.
"""

import streamlit as st

from services.auth_service import authenticate_user

with st.container(horizontal_alignment="center"):
    with st.container(width=700, border=True, horizontal=True, gap="large"):
        with st.container(width="stretch"):
            st.subheader("Kautex Hackaton Dashboard")
            st.caption("Resource planning & cost management")
            # TODO: replace with the real logo once provided

        with st.container(width="stretch"):
            st.subheader("Log in")

            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                # Not wired up yet: session state resets on browser refresh
                # regardless, until persistent (cookie-based) login is added.
                remember_me = st.checkbox("Remember me")
                submitted = st.form_submit_button("Log in", width="stretch")

            st.button("Forgot password?", type="tertiary", disabled=True)
            # TODO: real "forgot password" flow

            if submitted:
                user = authenticate_user(username, password)
                if user is None:
                    st.error("Invalid username or password.")
                else:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.rerun()

            st.divider()
            st.caption("Don't have an account?")
            if st.button("Sign up", width="stretch"):
                st.session_state.auth_view = "register"
                st.rerun()
