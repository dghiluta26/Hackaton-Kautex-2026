import streamlit as st
import pandas as pd
from sqlmodel import Session
from database.connection import engine
from services.employee_service import EmployeeService
from utils.auth import is_authenticated, is_admin, get_current_user

if not is_authenticated():
    st.switch_page("Login.py")

st.set_page_config(page_title="Employees", page_icon="👥", layout="wide")

st.title("👥 Employee Management")
st.markdown("---")

# Check if admin
is_admin_user = is_admin()

with Session(engine) as session:
    # Tab layout
    tab1, tab2 = st.tabs(["View Employees", "Add Employee"])
    
    with tab1:
        st.subheader("📋 Employee Directory")
        
        employees = EmployeeService.get_all_employees(session)
        
        if employees:
            # Display as table
            df_employees = pd.DataFrame([
                {
                    'ID': emp.id,
                    'Name': emp.name,
                    'Location': emp.location,
                    'Available Hours/Year': emp.available_hours_per_year,
                    'Hourly Rate': f"${emp.hourly_rate:.2f}"
                }
                for emp in employees
            ])
            
            st.dataframe(df_employees, use_container_width=True, hide_index=True)
            
            # Edit/Delete section (Admin only)
            if is_admin_user:
                st.markdown("---")
                st.subheader("✏️ Edit or Delete Employee")
                
                selected_employee = st.selectbox(
                    "Select employee to edit/delete:",
                    options=[emp.id for emp in employees],
                    format_func=lambda eid: next(emp.name for emp in employees if emp.id == eid)
                )
                
                if selected_employee:
                    emp = EmployeeService.get_employee_by_id(session, selected_employee)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_name = st.text_input("Name:", emp.name)
                        new_location = st.text_input("Location:", emp.location)
                    
                    with col2:
                        new_hours = st.number_input(
                            "Available Hours/Year:",
                            min_value=0,
                            value=emp.available_hours_per_year
                        )
                        new_rate = st.number_input(
                            "Hourly Rate:",
                            min_value=0.0,
                            value=emp.hourly_rate,
                            format="%.2f"
                        )
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("💾 Update Employee", key="update_emp"):
                            EmployeeService.update_employee(
                                session,
                                selected_employee,
                                name=new_name,
                                location=new_location,
                                available_hours_per_year=new_hours,
                                hourly_rate=new_rate
                            )
                            st.success("✅ Employee updated successfully!")
                            st.rerun()
                    
                    with col2:
                        if st.button("🗑️ Delete Employee", key="delete_emp"):
                            EmployeeService.delete_employee(session, selected_employee)
                            st.success("✅ Employee deleted successfully!")
                            st.rerun()
        else:
            st.info("No employees found. Create one using the 'Add Employee' tab.")
    
    with tab2:
        if is_admin_user:
            st.subheader("➕ Add New Employee")
            
            with st.form("add_employee_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Employee Name:", placeholder="e.g., John Smith")
                    location = st.text_input("Location:", placeholder="e.g., GV CAE Bonn")
                
                with col2:
                    available_hours = st.number_input(
                        "Available Hours/Year:",
                        min_value=0,
                        value=1600,
                        help="Default is 1600 hours"
                    )
                    hourly_rate = st.number_input(
                        "Hourly Rate ($):",
                        min_value=0.0,
                        value=50.0,
                        format="%.2f"
                    )
                
                submitted = st.form_submit_button("➕ Add Employee", type="primary")
                
                if submitted:
                    if not name or not location:
                        st.error("❌ Name and Location are required!")
                    else:
                        try:
                            EmployeeService.create_employee(
                                session,
                                name=name,
                                location=location,
                                available_hours_per_year=available_hours,
                                hourly_rate=hourly_rate
                            )
                            st.success("✅ Employee added successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("📌 Only admins can add employees. Current role: " + get_current_user()['role'])

st.markdown("---")
user = get_current_user()
st.markdown(f"**Role:** {user['role']} — {user['name']} ({'Full CRUD access' if is_admin_user else 'Read-only access'})")
