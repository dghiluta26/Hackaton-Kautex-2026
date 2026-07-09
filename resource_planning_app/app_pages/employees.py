"""Employees page: manage employee records. Admins only."""

import streamlit as st
import pandas as pd

from models.user import UserRole
from models.employee import Employee
from services.employee_service import create_employee, get_all_employees

# Security check
if st.session_state.user.role != UserRole.ADMIN:
    st.error("You don't have access to this page.")
    st.stop()

st.title("Employees")
st.caption("View and manage employees, their teams, departments, and locations.")

# --- 1. Display the Current Database Table ---
st.subheader("Employee List")
all_employees = get_all_employees()

if len(all_employees) > 0:
    # Convert the SQL database objects into a clean Pandas dataframe for Streamlit
    st.dataframe([emp.model_dump() for emp in all_employees], hide_index=True)
else:
    st.info("No employees found. Please upload a CSV below.")

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