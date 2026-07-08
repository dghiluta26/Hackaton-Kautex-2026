"""Reports page: summaries and breakdowns of cost and allocation."""

import streamlit as st

st.title("Reports")
st.caption("Executive summary and detailed breakdowns by topic, team, and employee.")

# --- Executive summary placeholder ---
st.subheader("Executive Summary")
st.info("A high-level summary of cost and resource usage will be displayed here.")
# TODO: aggregate totals from cost_service and allocation_service

st.divider()

# --- Report by topic placeholder ---
st.subheader("Report by Topic")
st.info("A cost and allocation breakdown per topic will be displayed here.")
# TODO: group data by topic_id

st.divider()

# --- Report by team placeholder ---
st.subheader("Report by Team")
st.info("A cost and allocation breakdown per team will be displayed here.")
# TODO: group data by team_id

st.divider()

# --- Report by employee placeholder ---
st.subheader("Report by Employee")
st.info("A cost and allocation breakdown per employee will be displayed here.")
# TODO: group data by employee_id
