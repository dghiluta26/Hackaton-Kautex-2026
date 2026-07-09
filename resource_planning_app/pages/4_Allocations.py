import streamlit as st
import pandas as pd
import numpy as np
from sqlmodel import Session
from database.connection import engine
from services.employee_service import EmployeeService
from services.topic_service import TopicService
from services.allocation_service import AllocationService
from utils.calculations import AllocationValidator

st.set_page_config(page_title="Allocations", page_icon="🎯", layout="wide")

st.title("🎯 Employee Allocation Matrix")
st.markdown("---")

# Check if admin
is_admin = st.session_state.get("role") == "Admin"

st.info("⚠️ **100% CAPACITY RULE ENFORCED:** Each employee must have exactly 100% allocation across all topics.")

with Session(engine) as session:
    employees = EmployeeService.get_all_employees(session)
    topics = TopicService.get_all_topics(session)
    
    if not employees or not topics:
        st.warning("⚠️ Please create employees and topics first.")
    else:
        # Tab layout
        tab1, tab2 = st.tabs(["Allocation Matrix", "Single Employee"])
        
        with tab1:
            st.subheader("📊 Allocation Matrix View")
            
            # Build allocation matrix
            allocation_matrix = AllocationService.get_allocation_matrix(session)
            
            # Create DataFrame for display
            matrix_data = []
            for employee in employees:
                row = {"Employee": employee.name, "Location": employee.location}
                total_allocation = 0
                for topic in topics:
                    allocation_pct = allocation_matrix.get(employee.id, {}).get(topic.id, 0)
                    row[topic.name] = f"{allocation_pct*100:.0f}%"
                    total_allocation += allocation_pct
                row["Total %"] = f"{total_allocation*100:.1f}%"
                
                # Status indicator
                if total_allocation == 1.0:
                    row["Status"] = "✅"
                elif total_allocation == 0:
                    row["Status"] = "⚠️ Unallocated"
                else:
                    row["Status"] = f"❌ {total_allocation*100:.1f}%"
                
                matrix_data.append(row)
            
            df_matrix = pd.DataFrame(matrix_data)
            st.dataframe(df_matrix, use_container_width=True, hide_index=True)
            
            # Summary statistics
            st.markdown("---")
            st.subheader("📈 Allocation Statistics")
            
            fully_allocated = sum(1 for row in matrix_data if row["Status"] == "✅")
            unallocated = sum(1 for row in matrix_data if "Unallocated" in row["Status"])
            over_allocated = sum(1 for row in matrix_data 
                               if row["Status"].startswith("❌"))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("✅ Fully Allocated", fully_allocated)
            with col2:
                st.metric("⚠️ Partially Allocated", unallocated)
            with col3:
                st.metric("❌ Over/Under Allocated", over_allocated)
        
        with tab2:
            st.subheader("👤 Single Employee Allocation")
            
            selected_employee_id = st.selectbox(
                "Select Employee:",
                options=[e.id for e in employees],
                format_func=lambda eid: next(e.name for e in employees if e.id == eid)
            )
            
            selected_employee = EmployeeService.get_employee_by_id(session, selected_employee_id)
            
            if selected_employee:
                # Display employee info
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Location:** {selected_employee.location}")
                with col2:
                    st.markdown(f"**Hourly Rate:** ${selected_employee.hourly_rate:.2f}")
                
                st.markdown(f"**Available Hours/Year:** {selected_employee.available_hours_per_year} hours")
                
                # Get current allocations
                current_allocations = AllocationService.get_allocations_by_employee(
                    session, selected_employee_id
                )
                
                # Current total
                current_total = AllocationService.get_employee_total_allocation(session, selected_employee_id)
                
                st.markdown("---")
                st.subheader("📋 Current Allocations")
                
                if current_allocations:
                    df_current = pd.DataFrame([
                        {
                            'Topic': next((t.name for t in topics if t.id == a.topic_id), "Unknown"),
                            'Allocation %': f"{a.allocation_percentage*100:.1f}%",
                            'Allocated Hours': f"{selected_employee.available_hours_per_year * a.allocation_percentage:.0f}",
                            'Cost': f"${selected_employee.available_hours_per_year * a.allocation_percentage * selected_employee.hourly_rate:,.2f}",
                            'Comment': a.comment
                        }
                        for a in current_allocations
                    ])
                    st.dataframe(df_current, use_container_width=True, hide_index=True)
                else:
                    st.info("No allocations yet for this employee.")
                
                # Capacity check
                st.markdown("---")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Current Total Allocation:**")
                    if current_total == 1.0:
                        st.success(f"✅ {current_total*100:.1f}% - Perfect!")
                    elif current_total == 0:
                        st.warning(f"⚠️ {current_total*100:.1f}% - Unallocated")
                    else:
                        st.error(f"❌ {current_total*100:.1f}% - Must be exactly 100%")
                
                with col2:
                    remaining = (1.0 - current_total) * 100
                    st.markdown("**Remaining Capacity:**")
                    st.info(f"{remaining:.1f}%")
                
                if is_admin:
                    st.markdown("---")
                    st.subheader("➕ Add or Update Allocation")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        selected_topic_id = st.selectbox(
                            "Select Topic:",
                            options=[t.id for t in topics],
                            format_func=lambda tid: next(t.name for t in topics if t.id == tid)
                        )
                    
                    with col2:
                        allocation_pct = st.number_input(
                            "Allocation %:",
                            min_value=0.0,
                            max_value=100.0,
                            value=0.0,
                            step=5.0,
                            help=f"Current total: {current_total*100:.1f}%, Remaining: {remaining:.1f}%"
                        )
                    
                    comment = st.text_input(
                        "Comment (why this allocation?):",
                        placeholder="e.g., Lead developer for this project"
                    )
                    
                    if st.button("💾 Save Allocation", type="primary"):
                        allocation_pct_float = allocation_pct / 100.0
                        
                        # Check if this would violate the 100% rule
                        test_total = current_total - next(
                            (a.allocation_percentage for a in current_allocations 
                             if a.topic_id == selected_topic_id),
                            0
                        ) + allocation_pct_float
                        
                        if abs(test_total - 1.0) > 0.001:  # Allow small floating point errors
                            remaining_after = (1.0 - test_total) * 100
                            st.error(
                                f"❌ **100% Rule Violation!**\n\n"
                                f"This allocation would result in: {test_total*100:.1f}%\n"
                                f"Remaining capacity: {remaining_after:.1f}%\n\n"
                                f"**You must allocate exactly 100% across all topics.**"
                            )
                        else:
                            try:
                                # Check if allocation already exists for this topic
                                existing = next(
                                    (a for a in current_allocations if a.topic_id == selected_topic_id),
                                    None
                                )
                                
                                if existing:
                                    AllocationService.update_allocation(
                                        session,
                                        existing.id,
                                        allocation_percentage=allocation_pct_float,
                                        comment=comment
                                    )
                                    st.success("✅ Allocation updated!")
                                else:
                                    AllocationService.create_allocation(
                                        session,
                                        employee_id=selected_employee_id,
                                        topic_id=selected_topic_id,
                                        allocation_percentage=allocation_pct_float,
                                        comment=comment
                                    )
                                    st.success("✅ Allocation created!")
                                
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                    
                    # Delete allocation
                    if current_allocations:
                        st.markdown("---")
                        st.subheader("🗑️ Remove Allocation")
                        
                        allocation_to_delete = st.selectbox(
                            "Select allocation to remove:",
                            options=[a.id for a in current_allocations],
                            format_func=lambda aid: next(
                                (f"{next((t.name for t in topics if t.id == a.topic_id), 'Unknown')} "
                                 f"({a.allocation_percentage*100:.1f}%)")
                                for a in current_allocations if a.id == aid
                            )
                        )
                        
                        if st.button("🗑️ Delete Allocation", type="secondary"):
                            AllocationService.delete_allocation(session, allocation_to_delete)
                            st.success("✅ Allocation deleted!")
                            st.rerun()
                else:
                    current_user = st.session_state.get("current_user", {})
                    role = current_user.get("role", "Unknown")
                    st.warning(f"📌 Only admins can create/edit allocations. Current role: {role}")

st.markdown("---")
current_user = st.session_state.get("current_user", {})
role = current_user.get("role", "Unknown")
st.markdown(f"**Role:** {role} — {'Full CRUD access' if is_admin else 'Read-only access'}")
