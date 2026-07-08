"""Employees page: manage employee records. Admins only."""

import pandas as pd
import streamlit as st

from models.employee import Employee
from models.user import UserRole
from services.employee_service import (
    create_employee,
    delete_employee,
    get_all_employees,
)

if st.session_state.user.role != UserRole.ADMIN:
    st.error("You don't have access to this page.")
    st.stop()

st.title("Employees")
st.caption("View and manage employees, their teams, departments, and locations.")

employees = get_all_employees()

total_employees = len(employees)
active_employees = len([e for e in employees if e.status == "Active"])

rates = [e.hourly_rate for e in employees if e.hourly_rate]
hours = [e.available_hours_per_year for e in employees if e.available_hours_per_year]

avg_rate = round(sum(rates) / len(rates), 2) if rates else 0
avg_hours = round(sum(hours) / len(hours), 2) if hours else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Employees", total_employees)
col2.metric("Active Employees", active_employees)
col3.metric("Avg Hourly Rate", avg_rate)
col4.metric("Avg Hours / Year", avg_hours)

st.divider()

with st.expander("➕ Add Employee", expanded=False):
    with st.form("add_employee_form"):
        c1, c2 = st.columns(2)

        with c1:
            name = st.text_input("Name")
            team_id = st.number_input("Team ID", min_value=0, step=1)
            department_id = st.number_input("Department ID", min_value=0, step=1)
            location_id = st.number_input("Location ID", min_value=0, step=1)

        with c2:
            available_hours = st.number_input(
                "Available hours per year",
                min_value=0.0,
                value=1600.0,
                step=100.0,
            )
            hourly_rate = st.number_input(
                "Hourly rate",
                min_value=0.0,
                value=1.0,
                step=1.0,
            )
            status = st.selectbox("Status", ["Active", "Inactive"])
            manager = st.text_input("Manager")

        notes = st.text_area("Notes")

        submitted = st.form_submit_button("Save Employee")

        if submitted:
            if not name.strip():
                st.error("Employee name is required.")
            else:
                employee = Employee(
                    name=name,
                    team_id=team_id if team_id != 0 else None,
                    department_id=department_id if department_id != 0 else None,
                    location_id=location_id if location_id != 0 else None,
                    available_hours_per_year=available_hours,
                    hourly_rate=hourly_rate,
                    status=status,
                    manager=manager,
                    notes=notes,
                )

                create_employee(employee)
                st.success("Employee added successfully.")
                st.rerun()

st.subheader("Employee List")

search = st.text_input("🔍 Search employee", placeholder="Type a name...")

if search:
    employees = [
        e for e in employees
        if search.lower() in e.name.lower()
    ]

if not employees:
    st.info("No employees found.")
else:
    df = pd.DataFrame(
        [
            {
                "ID": e.id,
                "Name": e.name,
                "Team ID": e.team_id,
                "Department ID": e.department_id,
                "Location ID": e.location_id,
                "Hours / Year": e.available_hours_per_year,
                "Hourly Rate": e.hourly_rate,
                "Status": e.status,
                "Manager": e.manager,
                "Notes": e.notes,
            }
            for e in employees
        ]
    )

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Delete Employee")

    employee_options = {
        f"{e.name} - ID {e.id}": e.id
        for e in employees
    }

    selected_employee = st.selectbox(
        "Select employee",
        list(employee_options.keys()),
    )

    if st.button("🗑 Delete Employee"):
        delete_employee(employee_options[selected_employee])
        st.success("Employee deleted successfully.")
        st.rerun()