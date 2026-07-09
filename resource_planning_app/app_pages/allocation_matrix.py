"""Allocation matrix page: assign employees to topics and check utilization."""

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
from services.allocation_service import get_all_allocations, upsert_allocation

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