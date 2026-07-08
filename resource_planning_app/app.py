"""Main entry point for the Resource Planning & Cost Management app.

Run with:
    streamlit run app.py
"""

import streamlit as st

from database.connection import create_db_and_tables

st.set_page_config(page_title="Resource Planning App", page_icon="📊", layout="wide")

# Make sure the database and tables exist before the app is used.
create_db_and_tables()

st.title("Resource Planning & Cost Management")

st.markdown(
    """
    This application helps plan and manage resources across teams and topics/projects.
    It tracks employees, teams, departments, locations, topic allocations, and the
    resulting costs, so that planning and reporting can happen in one place.
    """
)

st.subheader("Navigation")
st.markdown(
    """
    Use the sidebar to navigate between pages:

    - **General Dashboard** — key metrics and charts overview
    - **Employees** — manage employee records
    - **Topics** — manage topics/projects
    - **Allocation Matrix** — allocate employees to topics and check utilization
    - **Reports** — executive summary and detailed cost/allocation reports
    """
)

st.divider()

# --- Basic dashboard placeholders ---
st.subheader("Quick Overview")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Employees", "—")
with col2:
    st.metric("Total Topics", "—")
with col3:
    st.metric("Total Cost", "—")
with col4:
    st.metric("Overallocated Employees", "—")

st.info("Detailed metrics and charts will be available on the General Dashboard page.")
