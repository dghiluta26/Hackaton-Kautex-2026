"""Reports page: filter, view, and export allocation data."""

import streamlit as st
import pandas as pd

from app_theme import (
    inject_app_theme,
    render_kautex_header,
    money_column
)

from services.employee_service import get_all_employees
from services.topic_service import get_all_topics
from services.allocation_service import get_all_allocations

inject_app_theme()
render_kautex_header(
    "Resource Reports",
    "Filter and export allocation and cost data for your teams.",
    "Live Database Sync"
)

# --- 1. Fetch Real Data ---
db_employees = get_all_employees()
db_topics = get_all_topics()
db_allocations = get_all_allocations()

if not db_employees or not db_allocations:
    st.info("No allocation data available. Please assign employees to topics in the Matrix first.")
    st.stop()

# --- 2. Build the Flat Master Table ---
report_data = []
for alloc in db_allocations:
    # Only show active allocations greater than 0%
    if alloc.allocation_percentage > 0:
        emp = next((e for e in db_employees if e.id == alloc.employee_id), None)
        topic = next((t for t in db_topics if t.id == alloc.topic_id), None)

        if emp and topic:
            # Math: Calculate exact hours and costs based on the percentage
            allocated_hours = emp.available_hours_per_year * (alloc.allocation_percentage / 100)
            allocated_cost = allocated_hours * emp.hourly_rate

            report_data.append({
                "Employee": emp.name,
                "Team": emp.team_id or "Unassigned",
                "Location": emp.location_id or "Unassigned",
                "Project": topic.name,
                "Category": topic.category or "Unmapped",
                "Allocation (%)": alloc.allocation_percentage,
                "Allocated Hours": allocated_hours,
                "Internal Cost": allocated_cost
            })

df_report = pd.DataFrame(report_data)

if df_report.empty:
    st.warning("No active allocations found. Ensure you have saved allocations > 0% in the Matrix.")
    st.stop()

# --- 3. Interactive Filters ---
st.markdown("### Filter Data")
col1, col2, col3 = st.columns(3)

with col1:
    team_filter = st.multiselect("Filter by Team", options=df_report["Team"].unique())
with col2:
    project_filter = st.multiselect("Filter by Project", options=df_report["Project"].unique())
with col3:
    location_filter = st.multiselect("Filter by Location", options=df_report["Location"].unique())

# Apply filters if the user selected any
filtered_df = df_report.copy()
if team_filter:
    filtered_df = filtered_df[filtered_df["Team"].isin(team_filter)]
if project_filter:
    filtered_df = filtered_df[filtered_df["Project"].isin(project_filter)]
if location_filter:
    filtered_df = filtered_df[filtered_df["Location"].isin(location_filter)]

# --- 4. Display the Data Grid ---
st.divider()
st.markdown(f"### Report Results ({len(filtered_df)} records)")

st.dataframe(
    filtered_df,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Allocation (%)": st.column_config.NumberColumn("Allocation (%)", format="%d%%"),
        "Allocated Hours": st.column_config.NumberColumn("Allocated Hours", format="%.1f h"),
        "Internal Cost": money_column("Internal Cost")
    }
)

# --- 5. Export to CSV ---
st.divider()
csv_data = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Report as CSV",
    data=csv_data,
    file_name="kautex_resource_report.csv",
    mime="text/csv",
    type="primary"
)