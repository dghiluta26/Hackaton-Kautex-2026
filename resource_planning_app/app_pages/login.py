"""Login page with unified account request functionality."""

import streamlit as st
from services.auth_service import authenticate_user

# 1. Safely push the entire layout down into the vertical center
st.markdown("""
<style>
    .block-container {
        padding-top: 15vh !important; /* Adjust this value if you want it higher or lower */
    }
</style>
""", unsafe_allow_html=True)

# 2. Use native Streamlit columns to perfectly center the box horizontally
# The [1, 3, 1] ratio creates empty space on the left and right, squeezing the center.
left_spacer, center_column, right_spacer = st.columns([1, 3, 1])

with center_column:
    # 3. Create the main bounded card
    with st.container(border=True):

        # 4. Split the card internally into two halves (Left: Info, Right: Login)
        col_info, col_login = st.columns(2, gap="large")

        with col_info:
            st.subheader("Kautex Hackaton Dashboard")
            st.caption("Resource planning & cost management")

            # Request Account Section
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("Need an account? Request access"):
                st.markdown(
                    "<div style='font-size: 13px; color: #5b6470; margin-bottom: 10px;'>"
                    "Self-service registration is disabled. Submit a request to the Kautex Craiova administration team to provision your workspace."
                    "</div>",
                    unsafe_allow_html=True
                )
                with st.form("request_account_form"):
                    req_name = st.text_input("Full Name")
                    req_email = st.text_input("Corporate Email")
                    req_submit = st.form_submit_button("Submit Request", use_container_width=True)

                    if req_submit:
                        if req_name and req_email:
                            st.success(f"Request sent! An administrator will review access for {req_name} shortly.")
                        else:
                            st.error("Please provide your name and email.")

        with col_login:
            st.subheader("Log in")

            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                remember_me = st.checkbox("Remember me")
                # use_container_width stretches the button beautifully across the column
                submitted = st.form_submit_button("Log in", use_container_width=True)

            # Fixed "Forgot password?" button
            if st.button("Forgot password?", type="tertiary", use_container_width=True):
                st.info("Password resets are disabled for this prototype. Please contact the Kautex Admin team.")

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
            if st.button("Sign up", use_container_width=True):
                st.session_state.auth_view = "register"
                st.rerun()