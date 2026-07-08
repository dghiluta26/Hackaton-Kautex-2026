"""Employees page: manage employee records. Admins only."""

import streamlit as st

from models.user import UserRole

if st.session_state.user.role != UserRole.ADMIN:
    st.error("You don't have access to this page.")
    st.stop()

st.title("Employees")
st.caption("View and manage employees, their teams, departments, and locations.")

# --- Employee list placeholder ---
st.subheader("Employee List")
st.info("A table listing all employees will be displayed here.")
# TODO: fetch employees with employee_service.get_all_employees() and show with st.dataframe

st.divider()

# --- Add/Edit employee form placeholder ---
st.subheader("Add / Edit Employee")
st.info("A form to create or update an employee will be displayed here.")
# TODO: build a form using st.form with fields matching the Employee model
# TODO: call employee_service.create_employee() / update_employee() on submit
