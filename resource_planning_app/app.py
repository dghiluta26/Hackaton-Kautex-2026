import streamlit as st
from sqlmodel import Session
from database.connection import engine
from database.init_db import initialize_database
from utils.auth import is_authenticated, get_current_user, logout, is_admin

# Initialize database
initialize_database()

# Check authentication
if not is_authenticated():
    st.switch_page("Login.py")

# Set up Streamlit page configuration
st.set_page_config(
    page_title="Kautex Resource & Cost Planning",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .stat-value {
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 5px;
    }
    
    .stat-label {
        font-size: 13px;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .warning-box {
        background-color: #fff5e6;
        border-left: 4px solid #ff9800;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .success-box {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .user-info {
        background: #f0f2f6;
        padding: 10px 15px;
        border-radius: 8px;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🔐 User Info")
    user = get_current_user()
    if user:
        st.markdown(f"""
        <div class='user-info'>
        <b>{user['name']}</b><br>
        <span style='color:#5b6470;'>@{user['username']}</span><br>
        <strong>Role:</strong> {user['role']}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.sidebar.title("📍 Navigation")
    st.sidebar.info(
        "Welcome to Kautex Resource Planning!\n\n"
        "📊 **Dashboard** - Overview and metrics\n"
        "👥 **Employees** - Manage headcount\n"
        "📌 **Topics** - Manage projects\n"
        "🎯 **Allocations** - Capacity matrix\n"
        "📤 **Reports** - Export & Import\n"
    )
    
    st.markdown("---")
    
    if st.button("🚪 Logout", use_container_width=True):
        logout()
        st.success("✅ Logged out successfully!")
        st.switch_page("Login.py")

# Main header
st.markdown("""
<div class='main-header'>
    <h1>📊 Kautex Resource & Cost Planning Tool</h1>
    <p>Executive Leadership Platform for Resource Optimization</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Main content
col1, col2, col3 = st.columns(3)

with Session(engine) as session:
    from services.employee_service import EmployeeService
    from services.topic_service import TopicService
    from utils.calculations import CostCalculator
    
    employees = EmployeeService.get_all_employees(session)
    topics = TopicService.get_all_topics(session)
    metrics = CostCalculator.get_global_totals(session)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='stat-label'>💰 Total Cost</div>
            <div class='stat-value'>${metrics['total_cost']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='stat-label'>👥 Total Headcount</div>
            <div class='stat-value'>{metrics['total_headcount']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='stat-label'>📊 Avg Cost/Employee</div>
            <div class='stat-value'>${metrics['average_cost_per_employee']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Quick stats
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Employees", len(employees))

with col2:
    st.metric("Total Topics", len(topics))

with col3:
    user_role = user['role'] if user else "Unknown"
    st.metric("Access Level", "🔓" if is_admin() else "🔒")

with col4:
    st.metric("Status", "✅ Online")

st.markdown("---")

st.markdown("""
## 🚀 Quick Navigation

Use the pages on the left sidebar to navigate:

**📊 Dashboard** - Executive overview with cost distribution and budget alerts
**👥 Employees** - Add, edit, or remove employees
**📌 Topics** - Create and manage projects
**🎯 Allocations** - Build allocation matrix with 100% validation
**📤 Reports** - Export reports and bulk import data

---

### 🎯 Key Features

✅ **100% Capacity Rule** - Enforces strict allocation rules  
✅ **Deep Cost Analysis** - Internal, external, testing, and recovery costs  
✅ **Executive Reports** - Budget justification and high-cost flags  
✅ **Role-Based Access** - LST viewers and Admins  
✅ **Data Export** - Excel, CSV formats with formatting  
✅ **Bulk Import** - Upload employee and allocation data  

---

### 📋 Getting Started

1. **Create Employees** → Go to Employees page
2. **Add Topics** → Go to Topics page and create projects
3. **Allocate** → Assign employees to topics (must sum to 100%)
4. **Review** → Check Dashboard for cost analysis
5. **Export** → Download reports in Reports page

---
""")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.85rem;'>"
    "Kautex Resource & Cost Planning Tool | v2.0 | 🔒 Secure"
    "</div>",
    unsafe_allow_html=True
)
