"""Allocation matrix page: assign employees to topics and check utilization."""
from __future__ import annotations
import streamlit as st
import pandas as pd

from app_theme import (
    inject_app_theme,
    render_kautex_header,
    percent_column,
    table_height,
    utilization_chart
)

from services.employee_service import get_all_employees
from services.topic_service import get_all_topics
from services.allocation_service import (
    delete_allocation,
    get_all_allocations,
    get_allocations_by_employee,
    get_employee_total_allocation,
    upsert_allocation,
)
from utils.calculations import calculate_employee_topic_cost

inject_app_theme()
render_kautex_header(
    "Allocation matrix",
    "Assign people to projects and instantly save the resource plan to the database.",
    "Live Database Sync"
)

# --- 1. Fetch Real Data ---
db_employees = get_all_employees()
db_topics = get_all_topics()
db_allocations = get_all_allocations()

if not db_employees or not db_topics:
    st.warning("⚠️ You need to import both Employees and Topics before using the Matrix.")
    st.stop()

tab_grid, tab_single = st.tabs(["Allocation Grid", "Single Employee"])

# --- Tab 1: Interactive Grid (unchanged) ---
with tab_grid:
    # --- 2. Build the Dynamic Matrix ---
    topic_names = [t.name for t in db_topics]
    matrix_rows = []

    for emp in db_employees:
        # Set up the base employee data
        row = {
            "employee_id": emp.id,
            "employee": emp.name,
            "team": emp.team_id or "Unassigned",
            "hours_per_year": emp.available_hours_per_year or 0.0,
            "hourly_rate": emp.hourly_rate or 0.0,
        }
        # Default all topics to 0%
        for topic in db_topics:
            row[topic.name] = 0.0
        matrix_rows.append(row)

    df_matrix = pd.DataFrame(matrix_rows)

    # Fill the matrix with existing allocations from the database
    for alloc in db_allocations:
        emp = next((e for e in db_employees if e.id == alloc.employee_id), None)
        topic = next((t for t in db_topics if t.id == alloc.topic_id), None)
        if emp and topic:
            df_matrix.loc[df_matrix["employee_id"] == emp.id, topic.name] = alloc.allocation_percentage

    # --- 3. Configure the Interactive UI Columns ---
    col_config = {
        "employee_id": None, # Hide the database ID from the user
        "employee": st.column_config.TextColumn("Employee", pinned=True),
        "team": "Team",
        "hours_per_year": st.column_config.NumberColumn("Hours / year", format="%d"),
        "hourly_rate": st.column_config.NumberColumn("Hourly rate", format="$ %.2f")
    }

    # Dynamically add all topics as editable percentage columns
    for t_name in topic_names:
        col_config[t_name] = percent_column(t_name, editable=True)

    # --- 4. Render the Data Editor & Save Button ---
    st.markdown("### Interactive Allocation Grid")

    with st.form("matrix_form"):
        edited_df = st.data_editor(
            df_matrix,
            key="live_allocation_editor",
            num_rows="fixed",
            hide_index=True,
            height=table_height(len(df_matrix), 360, 620),
            disabled=["employee", "team", "hours_per_year", "hourly_rate"],
            column_config=col_config,
        )

        submitted = st.form_submit_button("Save Matrix to Database", type="primary", use_container_width=True)

        if submitted:
            # When clicked, loop through the grid and save everything
            for index, row in edited_df.iterrows():
                emp_id = row["employee_id"]
                for topic in db_topics:
                    percentage = row[topic.name]
                    upsert_allocation(emp_id, topic.id, float(percentage))

            st.success("Allocations successfully saved!")
            st.rerun()

    # --- 5. Live Chart ---
    st.divider()
    st.markdown("### Live Utilization Preview")

    # Calculate live utilization by summing up the topic columns
    edited_df["total_utilization"] = edited_df[topic_names].sum(axis=1)

    # Render the chart from app_theme
    st.altair_chart(utilization_chart(edited_df), use_container_width=True)

# --- Tab 2: Single Employee ---
with tab_single:
    selected_employee_id = st.selectbox(
        "Select employee:",
        options=[e.id for e in db_employees],
        format_func=lambda eid: next(e.name for e in db_employees if e.id == eid),
        key="single_emp_select",
    )
    employee = next(e for e in db_employees if e.id == selected_employee_id)

    col1, col2 = st.columns(2)
    col1.markdown(f"**Available Hours/Year:** {employee.available_hours_per_year or 0:.0f}")
    col2.markdown(f"**Hourly Rate:** ${employee.hourly_rate or 0:.2f}")

    current_allocations = get_allocations_by_employee(selected_employee_id)
    current_total = get_employee_total_allocation(selected_employee_id)

    st.divider()
    st.subheader("Current allocations")

    if current_allocations:
        df_current = pd.DataFrame(
            [
                {
                    "Topic": next((t.name for t in db_topics if t.id == a.topic_id), "Unknown"),
                    "Allocation %": f"{a.allocation_percentage:.1f}%",
                    "Allocated Hours": f"{(employee.available_hours_per_year or 0) * (a.allocation_percentage / 100):.0f}",
                    "Cost": f"${calculate_employee_topic_cost(employee.available_hours_per_year or 0, employee.hourly_rate or 0, a.allocation_percentage):,.2f}",
                    "Comment": a.comment,
                }
                for a in current_allocations
            ]
        )
        st.dataframe(df_current, use_container_width=True, hide_index=True)
    else:
        st.info("No allocations yet for this employee.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Current total allocation:**")
        if current_total == 100:
            st.success(f"{current_total:.1f}% — perfect!")
        elif current_total == 0:
            st.warning(f"{current_total:.1f}% — unallocated")
        else:
            st.error(f"{current_total:.1f}% — target is 100%")
    with col2:
        remaining = 100 - current_total
        st.markdown("**Remaining capacity:**")
        st.info(f"{remaining:.1f}%")

    st.divider()
    st.subheader("Add or update allocation")

    col1, col2 = st.columns(2)
    with col1:
        selected_topic_id = st.selectbox(
            "Select topic:",
            options=[t.id for t in db_topics],
            format_func=lambda tid: next(t.name for t in db_topics if t.id == tid),
            key="single_topic_select",
        )
    with col2:
        allocation_pct = st.number_input(
            "Allocation %:",
            min_value=0.0,
            max_value=200.0,
            value=0.0,
            step=5.0,
            help=f"Current total: {current_total:.1f}%, remaining: {remaining:.1f}%",
            key="single_alloc_pct",
        )

    comment = st.text_input("Comment (why this allocation?):", placeholder="e.g., Lead developer for this project", key="single_alloc_comment")

    if st.button("Save Allocation", type="primary", key="single_save_alloc"):
        upsert_allocation(selected_employee_id, selected_topic_id, allocation_pct, comment)
        st.success("Allocation saved!")
        st.rerun()

    if current_allocations:
        st.divider()
        st.subheader("Remove allocation")

        allocation_to_delete = st.selectbox(
            "Select allocation to remove:",
            options=[a.id for a in current_allocations],
            format_func=lambda aid: next(
                f"{next((t.name for t in db_topics if t.id == a.topic_id), 'Unknown')} ({a.allocation_percentage:.1f}%)"
                for a in current_allocations if a.id == aid
            ),
            key="single_delete_select",
        )

        if st.button("Delete Allocation", key="single_delete_btn"):
            delete_allocation(allocation_to_delete)
            st.success("Allocation deleted!")
            st.rerun()
