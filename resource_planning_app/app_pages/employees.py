"""Employees page: manage employee records. Admins only."""

from __future__ import annotations
import streamlit as st
import pandas as pd

from app_theme import inject_app_theme, render_kautex_header
from models.user import UserRole
from models.employee import Employee
from services.employee_service import create_employee, delete_employee, get_all_employees, update_employee
from services.allocation_service import get_all_allocations

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

all_employees = get_all_employees()

# Utilization per employee, computed the same way as the Dashboard's Live
# System Update ticker, so the "overallocated" flag stays in sync across pages.
db_allocations = get_all_allocations()
utilization_by_employee: dict[int, float] = {}
for alloc in db_allocations:
    utilization_by_employee[alloc.employee_id] = (
        utilization_by_employee.get(alloc.employee_id, 0.0) + (alloc.allocation_percentage or 0.0)
    )
overallocated_ids = {emp.id for emp in all_employees if utilization_by_employee.get(emp.id, 0.0) > 100}

# --- NEW: CORPORATE METRICS HIGHLIGHT ROW ---
# This mirrors the clean executive dashboard summary cards seen on your landing page.
if len(all_employees) > 0:
    total_staff = len(all_employees)
    active_staff = sum(1 for emp in all_employees if str(emp.status).strip().lower() == "active")

    # Calculate averages safely avoiding any division by zero
    avg_rate = sum(float(emp.hourly_rate or 0.0) for emp in all_employees) / total_staff
    total_capacity = sum(float(emp.available_hours_per_year or 0.0) for emp in all_employees)

    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.metric(label="Total Registries", value=f"{total_staff} Headcount")
    with m_col2:
        st.metric(label="Active Staff Status", value=f"{active_staff} Active", delta=f"{total_staff - active_staff} Non-Active", delta_color="off")
    with m_col3:
        st.metric(label="Average Standard Rate", value=f"€ {avg_rate:.2f} / hr")
    with m_col4:
        st.metric(label="Gross Planned Capacity", value=f"{total_capacity:,.0f} hrs/yr")

    st.divider()

# --- 1. Display the Current Database Table ---
st.subheader("Employee List")

if len(all_employees) > 0:
    # Convert the SQL database objects into a clean Pandas dataframe for Streamlit
    st.dataframe([emp.model_dump() for emp in all_employees], hide_index=True)
else:
    st.info("No employees found. Please add or upload a CSV below.")

st.divider()

# --- 2. Add New Employee Form ---
st.subheader("Add New Employee Manually")
with st.form("add_employee_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        new_name = st.text_input("Full Name:", placeholder="e.g. John Doe")
        new_status = st.selectbox("Status:", options=["Active", "Temporary", "Inactive", "Replacement"])
        new_manager = st.text_input("Manager Name (Optional):")
    with col2:
        new_hours = st.number_input("Available Hours/Year:", min_value=0.0, value=1768.0, step=1.0)
        new_rate = st.number_input("Hourly Rate (€/$):", min_value=0.0, value=50.0, step=0.50, format="%.2f")

    new_notes = st.text_area("Notes:")

    submit_button = st.form_submit_button("Add Employee", type="primary")

    if submit_button:
        if not new_name.strip():
            st.error("Employee name cannot be empty.")
        else:
            new_emp = Employee(
                name=new_name.strip(),
                status=new_status,
                manager=new_manager.strip() if new_manager.strip() else None,
                available_hours_per_year=new_hours,
                hourly_rate=new_rate,
                notes=new_notes.strip() if new_notes.strip() else None
            )
            create_employee(new_emp)
            st.success(f"Successfully added {new_name}!")
            st.rerun()

st.divider()

# --- 3. Edit or Delete an Employee ---
st.subheader("Edit or Delete Employee")

filter_overallocated = st.session_state.get("employees_filter_overallocated", False)
if filter_overallocated and overallocated_ids:
    editable_employees = [emp for emp in all_employees if emp.id in overallocated_ids]
    st.warning(f"⚠️ Showing only the {len(editable_employees)} employee(s) flagged as overallocated from the Dashboard alert.")
    if st.button("Show all employees", key="clear_overallocated_filter"):
        st.session_state["employees_filter_overallocated"] = False
        st.rerun()
else:
    if filter_overallocated:
        # Flag was set but nothing is overallocated anymore (e.g. allocations changed) — fall back to full list.
        st.session_state["employees_filter_overallocated"] = False
    editable_employees = all_employees

if not editable_employees:
    st.info("No employees yet.")
else:
    def _format_employee_option(eid: int) -> str:
        emp = next((e for e in editable_employees if e.id == eid), None)
        if emp is None:
            return "Unknown"
        util = utilization_by_employee.get(eid, 0.0)
        return f"{emp.name} — ⚠ {util:.0f}% allocated" if util > 100 else emp.name

    # Safely select the precise unique database ID mapping
    selected_id = st.selectbox(
        "Select employee to edit/delete:",
        options=[emp.id for emp in editable_employees],
        format_func=_format_employee_option,
    )
    employee = next(emp for emp in editable_employees if emp.id == selected_id)

    col1, col2 = st.columns(2)
    with col1:
        edit_name = st.text_input("Name:", employee.name, key=f"edit_emp_name_{selected_id}")
        edit_status = st.text_input("Status:", employee.status or "", key=f"edit_emp_status_{selected_id}")
        edit_manager = st.text_input("Manager:", employee.manager or "", key=f"edit_emp_manager_{selected_id}")
    with col2:
        edit_hours = st.number_input(
            "Available Hours/Year:", min_value=0.0, value=float(employee.available_hours_per_year or 0.0), key=f"edit_emp_hours_{selected_id}"
        )
        edit_rate = st.number_input(
            "Hourly Rate:", min_value=0.0, value=float(employee.hourly_rate or 0.0), format="%.2f", key=f"edit_emp_rate_{selected_id}"
        )
    edit_notes = st.text_area("Notes:", employee.notes or "", key=f"edit_emp_notes_{selected_id}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Update Employee", key=f"update_emp_{selected_id}"):
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
        if st.button("Delete Employee", key=f"delete_emp_{selected_id}"):
            delete_employee(selected_id)
            st.success("Employee deleted successfully!")
            st.rerun()

st.divider()

# --- 4. The CSV Uploader ---
st.subheader("Mass Import Employees (CSV)")
st.caption("Required columns: name, available_hours_per_year, hourly_rate, status")

uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file is not None:

    # --- SMART DELIMITER DETECTION ---
    sample = uploaded_file.read(1024).decode("utf-8")
    uploaded_file.seek(0)

    separator = ";" if ";" in sample.split("\n")[0] else ","
    df = pd.read_csv(uploaded_file, sep=separator)
    df.columns = [str(col).strip().lower() for col in df.columns]

    st.write(f"Preview (Detected separator: '{separator}'):")
    st.dataframe(df.head(), hide_index=True)

    if st.button("Import to Database", type="primary"):
        success_count = 0

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
        st.rerun()