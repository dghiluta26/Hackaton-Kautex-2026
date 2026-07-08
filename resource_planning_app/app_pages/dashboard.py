"""General Dashboard page: high-level overview of the resource plan."""

import streamlit as st

st.set_page_config(page_title="General Dashboard", layout="wide")

st.title("General Dashboard")
st.caption("High-level overview of employees, topics, cost, and utilization.")

# --- Key metrics placeholders ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Employees", "—")
    # TODO: replace with employee_service.get_all_employees() count

with col2:
    st.metric("Total Topics", "—")
    # TODO: replace with topic_service.get_all_topics() count

with col3:
    st.metric("Total Cost", "—")
    # TODO: replace with cost_service aggregation

with col4:
    st.metric("Overallocated Employees", "—")
    # TODO: replace with utils.calculations.is_overallocated logic per employee

st.divider()

# --- Charts placeholder ---
st.subheader("Charts")
st.info("Charts (e.g. cost by topic, utilization by team) will be added here using Plotly.")
