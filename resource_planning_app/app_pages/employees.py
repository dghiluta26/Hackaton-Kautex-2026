"""Employees page: manage employee records. Admins only."""

import streamlit as st
import pandas as pd

from app_theme import inject_app_theme, render_kautex_header
from models.user import UserRole
from models.employee import Employee
from services.employee_service import create_employee, delete_employee, get_all_employees, update_employee

# Security check
if st.session_state.user.role != UserRole.ADMIN:
    st.error("You don't have access to this page.")
    st.stop()

inject_app_theme()
render_kautex_header(
    "Employees",
    "View and manage employees, their teams, departments, and locations.",
    "Admin",
)

# --- 1. Display the Current Database Table ---
st.subheader("Employee List")
all_employees = get_all_employees()

if len(all_employees) > 0:
    # Convert the SQL database objects into a clean Pandas dataframe for Streamlit
    st.dataframe([emp.model_dump() for emp in all_employees], hide_index=True)
else:
    st.info("No employees found. Please upload a CSV below.")

st.divider()

# --- 1b. Edit or Delete an Employee ---
st.subheader("Edit or Delete Employee")

if not all_employees:
    st.info("No employees yet.")
else:
    selected_id = st.selectbox(
        "Select employee:",
        options=[emp.id for emp in all_employees],
        format_func=lambda eid: next(emp.name for emp in all_employees if emp.id == eid),
    )
    employee = next(emp for emp in all_employees if emp.id == selected_id)

    col1, col2 = st.columns(2)
    with col1:
        edit_name = st.text_input("Name:", employee.name, key="edit_emp_name")
        edit_status = st.text_input("Status:", employee.status or "", key="edit_emp_status")
        edit_manager = st.text_input("Manager:", employee.manager or "", key="edit_emp_manager")
    with col2:
        edit_hours = st.number_input(
            "Available Hours/Year:", min_value=0.0, value=float(employee.available_hours_per_year or 0.0), key="edit_emp_hours"
        )
        edit_rate = st.number_input(
            "Hourly Rate:", min_value=0.0, value=float(employee.hourly_rate or 0.0), format="%.2f", key="edit_emp_rate"
        )
    edit_notes = st.text_area("Notes:", employee.notes or "", key="edit_emp_notes")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Update Employee", key="update_emp"):
            update_employee(
                selected_id,
                {
                    "name": edit_name,
                    "status": edit_status,
                    "manager": edit_manager,
                    "available_hours_per_year": edit_hours,
                    "hourly_rate": edit_rate,
                    "notes": edit_notes,
                },
            )
            st.success("Employee updated successfully!")
            st.rerun()
    with col2:
        if st.button("Delete Employee", key="delete_emp"):
            delete_employee(selected_id)
            st.success("Employee deleted successfully!")
            st.rerun()

st.divider()

# --- 2. The CSV Uploader ---
st.subheader("Mass Import Employees (CSV)")
st.caption("Required columns: name, available_hours_per_year, hourly_rate, status")

uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file is not None:

    # --- SMART DELIMITER DETECTION ---
    # Look at the first 1024 bytes to see how Excel formatted it
    sample = uploaded_file.read(1024).decode("utf-8")
    uploaded_file.seek(0) # Reset file pointer back to the beginning

    # If a semicolon is in the first row, use that. Otherwise, use a comma.
    separator = ";" if ";" in sample.split("\n")[0] else ","

    # Read the file with the correctly detected separator
    df = pd.read_csv(uploaded_file, sep=separator)

    # Clean up the column headers (forces lowercase, removes accidental spaces)
    df.columns = [str(col).strip().lower() for col in df.columns]

    # Show a preview to prove it worked
    st.write(f"Preview (Detected separator: '{separator}'):")
    st.dataframe(df.head(), hide_index=True)

    # The Action Button
    if st.button("Import to Database", type="primary"):
        success_count = 0

        # Loop through every row in the file
        for index, row in df.iterrows():
            new_emp = Employee(
                name=row.get("name"),
                available_hours_per_year=row.get("available_hours_per_year", 0.0),
                hourly_rate=row.get("hourly_rate", 0.0),
                status=row.get("status", "Active")
            )
            create_employee(new_emp)
            success_count += 1

        st.success(f"Successfully imported {success_count} employees!")

        # Instantly refresh the page to update the top table
        st.rerun()