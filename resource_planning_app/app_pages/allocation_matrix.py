"""Allocation Matrix page: assign employees to topics and check utilization."""

import streamlit as st

st.title("Allocation Matrix")
st.caption("Allocate employees to topics and review utilization and cost.")

# --- Editable allocation table placeholder ---
st.subheader("Allocation Table")
st.info("An editable table (employees x topics) for allocation percentages will be displayed here.")
# TODO: build an editable table with st.data_editor
# TODO: read/write allocations with allocation_service

st.divider()

# --- Utilization warning placeholder ---
st.subheader("Utilization Warnings")
st.info("Warnings for overallocated employees will be displayed here.")
# TODO: use utils.calculations.calculate_total_utilization and is_overallocated

st.divider()

# --- Cost calculation placeholder ---
st.subheader("Cost Calculation")
st.info("Calculated costs based on allocations will be displayed here.")
# TODO: use utils.calculations.calculate_employee_topic_cost per allocation
