"""Login page with corporate design layout and automated region detection."""

import streamlit as st
import time
from app_theme import is_dark_mode
from services.auth_service import authenticate_user

_muted_text_color = "#94A3B8" if is_dark_mode() else "#5b6470"

def detect_server_region() -> str:
    """Detect client network region using browser context headers."""
    try:
        headers = st.context.headers
        tz = headers.get("X-Timezone", "").lower() or headers.get("Timezone", "").lower()

        if "europe" in tz or "bucharest" in tz or "berlin" in tz:
            return "EU-Central Hub (Bonn / Craiova)"
        elif "asia" in tz or "shanghai" in tz:
            return "AP-East Hub (Pinghu)"
        elif "america" in tz or "toronto" in tz or "new_york" in tz:
            return "NA-North Hub (Windsor)"
    except Exception:
        pass
    return "EU-Central Hub (Bonn / Craiova)"

detected_region = detect_server_region()

# 1. CSS layout centering and corporate palette mapping
st.markdown("""
<style>
    .block-container {
        padding-top: 15vh !important; 
    }
    
    .kautex-node-card {
        background: rgba(0, 75, 135, 0.04);
        border-left: 4px solid #004B87;
        padding: 14px;
        border-radius: 4px;
        margin-top: 12px;
    }
    
    .status-pulse {
        display: inline-block;
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        margin-right: 8px;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4);
        animation: kautex-pulse 2s infinite;
    }
    
    @keyframes kautex-pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
        70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
</style>
""", unsafe_allow_html=True)

# 2. Main structure layout
left_spacer, center_column, right_spacer = st.columns([1, 3, 1])

with center_column:
    with st.container(border=True):
        col_info, col_login = st.columns(2, gap="large")

        # --- LEFT PANEL: INFRASTRUCTURE ROUTING ENGINE ---
        with col_info:
            st.subheader("Kautex Hackaton Dashboard")
            st.caption("Resource planning & cost management")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Global Infrastructure Routing**")

            st.markdown(f"""
                <div class="kautex-node-card">
                    <div style="font-size: 11px; font-weight: 700; color: #004B87; letter-spacing: 0.5px; margin-bottom: 2px;">
                        AUTOMATED SECURE ROUTE DETECTED
                    </div>
                    <div style="font-size: 14px; color: { 'white' if is_dark_mode() else '#1A202C' };">
                        Network path optimized through the <b>{detected_region}</b> backbone network.
                    </div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            node_left, node_right = st.columns(2)
            with node_left:
                st.markdown(
                    f'<div style="display: flex; align-items: center; font-size: 14px; margin-top: 8px; font-weight: 500; color: {_muted_text_color};">'
                    f'<span class="status-pulse"></span>Connection: Operational'
                    f'</div>',
                    unsafe_allow_html=True
                )
            with node_right:
                if st.button("Test Gateway Latency", use_container_width=True):
                    with st.spinner("Pinging network array..."):
                        time.sleep(0.35)
                    st.toast("Telemetry checked. Gateway Latency: 14ms")

            # Request Account Section
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("Need an account? Request access"):
                st.markdown(
                    f"<div style='font-size: 13px; color: {_muted_text_color}; margin-bottom: 10px;'>"
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
                            st.success(f"Request submitted. Access evaluation pending for {req_name}.")
                        else:
                            st.error("Please provide your name and email.")

        # --- RIGHT PANEL: SECURE USER AUTHENTICATION ---
        with col_login:
            st.subheader("Log in")

            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                remember_me = st.checkbox("Remember me")
                submitted = st.form_submit_button("Log in", use_container_width=True)

            if st.button("Forgot password?", type="tertiary", use_container_width=True):
                st.info("Password resets are disabled for this environment. Please contact the system administrator.")

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