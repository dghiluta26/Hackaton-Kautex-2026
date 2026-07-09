import streamlit as st
from utils.auth import authenticate_user
from database.init_db import initialize_database
import os

# Initialize database on app start
initialize_database()

st.set_page_config(
    page_title="Kautex - Resource Planning",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide sidebar on login page
st.markdown("""
<style>
    [data-testid="collapsedControl"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Beautiful login page design
st.markdown("""
<style>
    /* Reset */
    * { margin: 0; padding: 0; box-sizing: border-box; }

    /* Corporate, neutral background matching the BI theme */
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        background: linear-gradient(180deg, #f6f7f9 0%, #ffffff 100%);
        color: #1a1d24;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
    }

    .login-card {
        background: #ffffff; /* surface */
        border: 1px solid #e2e5ea; /* subtle border */
        border-radius: 12px;
        box-shadow: 0 8px 30px rgba(26,29,36,0.08);
        padding: 48px 36px;
        width: 100%;
        max-width: 520px;
        text-align: center;
    }

    .logo-section { margin-bottom: 28px; position: relative; }

    .logo-background {
        position: relative;
        display: inline-block;
        width: 100px;
        height: 100px;
        margin-bottom: 16px;
    }

    .logo-blur {
        position: absolute;
        width: 100px;
        height: 100px;
        background: #c9342b; /* primary */
        border-radius: 50%;
        filter: blur(22px);
        opacity: 0.12;
        top: 50%; left: 50%; transform: translate(-50%, -50%);
        z-index: 0;
    }

    .logo-img { position: relative; z-index: 1; width: 100%; height: 100%; }

    h1 { color: #1a1d24; font-size: 28px; margin-bottom: 6px; font-weight: 700; }

    .subtitle { color: #5b6470; font-size: 13px; margin-bottom: 22px; }

    .login-form { margin-top: 14px; text-align: left; }

    .form-group { margin-bottom: 14px; }

    label { display:block; color:#1a1d24; font-weight:600; margin-bottom:6px; font-size:13px; }

    input { width:100%; padding:10px 12px; border:1px solid #e2e5ea; border-radius:8px; font-size:14px; }

    input:focus { outline:none; border-color:#c9342b; box-shadow:0 0 0 4px rgba(201,52,43,0.06); }

    .login-btn {
        width:100%; padding:12px 14px; background:#c9342b; color:#ffffff; border:none; border-radius:8px; font-size:15px; font-weight:600; cursor:pointer; margin-top:8px;
    }

    .login-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(201,52,43,0.18); }

    .demo-section { margin-top:22px; padding-top:22px; border-top:1px solid #eaeef2; }

    .demo-title { color:#1a1d24; font-size:12px; font-weight:700; margin-bottom:10px; text-transform:uppercase; letter-spacing:0.08em; }

    .demo-btn { width:100%; padding:10px; background:#ffffff; color:#c9342b; border:1px solid #c9342b; border-radius:8px; font-size:14px; font-weight:600; margin-bottom:8px; }

    .demo-btn:hover { background:#fcf6f6; }

    .error-message { background-color:#fff4f4; color:#c53030; padding:12px 14px; border-radius:8px; margin-bottom:14px; font-size:14px; border-left:4px solid #c53030; }

    .footer { margin-top:18px; color:#7a8590; font-size:12px; text-align:center; }

    /* Streamlit container tweaks to center everything */
    .block-container { padding: 2rem 1rem; }
</style>
""", unsafe_allow_html=True)

# Check if already authenticated
if st.session_state.get("authenticated"):
    st.switch_page("pages/1_Dashboard.py")

# Login form
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("<div class='logo-section'>", unsafe_allow_html=True)
    
    # Try to load and display logo
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "kautex_logo.png")
    if os.path.exists(logo_path):
            st.image(logo_path, width=180, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<h1>KAUTEX</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Resource & Cost Planning Tool</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Login form
    st.markdown("<div class='login-form'>", unsafe_allow_html=True)
    
    username = st.text_input("Username", placeholder="admin or viewer")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    if st.button("Login", use_container_width=True, type="primary"):
        if not username or not password:
            st.error("Please enter both username and password!")
        else:
            user = authenticate_user(username, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.current_user = user
                st.session_state.role = user.get("role")
                st.success("Login successful! Redirecting...")
                st.switch_page("pages/1_Dashboard.py")
            else:
                st.error("Invalid username or password!")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Demo credentials section
    st.markdown("<div class='demo-section'>", unsafe_allow_html=True)
    st.markdown("<p class='demo-title'>Demo Credentials</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Admin", use_container_width=True):
            st.info("**Username:** admin\n**Password:** admin123")
    
    with col2:
        if st.button("Viewer", use_container_width=True):
            st.info("**Username:** viewer\n**Password:** viewer123")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='footer'>", unsafe_allow_html=True)
    st.markdown("Secure authentication • © 2026 Kautex GmbH", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
