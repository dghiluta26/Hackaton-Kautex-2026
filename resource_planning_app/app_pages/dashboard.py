"""General dashboard: high-level overview of the resource plan."""

import streamlit as st
import pandas as pd

from app_theme import (
    inject_app_theme,
    render_kautex_header,
    money_column,
    table_height,
    utilization_chart,
)

from services.employee_service import get_all_employees
from services.topic_service import get_all_topics
from services.allocation_service import get_all_allocations
from services.cost_service import get_all_cost_items

inject_app_theme()
render_kautex_header(
    "Digital resource & cost dashboard",
    "Live overview of employee utilization and projected internal costs.",
    "Live Database Sync",
)

# --- 1. Fetch Real Data ---
# --- 1. Fetch Real Data ---
db_employees = get_all_employees()
db_topics = get_all_topics()
db_allocations = get_all_allocations()
db_costs = get_all_cost_items() # NEW: Fetch all external costs

if not db_employees:
    st.info("Please add employees and topics to view dashboard analytics.")
    st.stop()

# --- 2. Calculate Live Analytics ---
employee_data = []
total_internal_cost = 0

for emp in db_employees:
    # Find all allocations for this specific employee
    emp_allocs = [a for a in db_allocations if a.employee_id == emp.id]

    # Calculate total utilization percentage (e.g., 20% + 50% = 70%)
    total_util = sum([a.allocation_percentage for a in emp_allocs])

    # Calculate cost: (Hours * Rate) * (Utilization / 100)
    emp_cost = (emp.available_hours_per_year * emp.hourly_rate) * (total_util / 100)
    total_internal_cost += emp_cost

    employee_data.append({
        "employee": emp.name,
        "team": emp.team_id or "Unassigned",
        "department": emp.department_id or "Unassigned",
        "location": emp.location_id or "Unassigned",
        "hours_per_year": emp.available_hours_per_year,
        "hourly_rate": emp.hourly_rate,
        "total_utilization": total_util,
        "allocated_internal_cost": emp_cost,
        "risk": "Overallocated" if total_util > 100 else "OK"
    })

df_employees = pd.DataFrame(employee_data)
overallocated_count = len(df_employees[df_employees["total_utilization"] > 100])
avg_utilization = df_employees["total_utilization"].mean() if not df_employees.empty else 0

# --- 3. Top Metrics Row ---
# Calculate external costs from the CostItem table
total_external_cost = sum([c.amount for c in db_costs if c.amount is not None])
grand_total_cost = total_internal_cost + total_external_cost

with st.container(horizontal=True):
    st.metric("Total employees", f"{len(db_employees)}", border=True)
    st.metric("Total topics", f"{len(db_topics)}", border=True)
    st.metric("Average utilization", f"{avg_utilization:.0f}%", border=True)

    # Cost Breakdown
    st.metric("Internal Cost", f"${total_internal_cost:,.0f}", border=True)
    st.metric("External Cost", f"${total_external_cost:,.0f}", border=True)
    st.metric("Grand Total", f"${grand_total_cost:,.0f}", border=True)
# --- 4. Live Utilization Chart ---
st.markdown("### Utilization by Employee")
if not df_employees.empty:
    st.altair_chart(utilization_chart(df_employees), use_container_width=True)

# --- 5. Data Grid ---
st.markdown("### Detailed Employee Breakdown")
st.dataframe(
    df_employees.sort_values("total_utilization", ascending=False),
    hide_index=True,
    height=table_height(len(df_employees), 300, 540),
    column_config={
        "employee": st.column_config.TextColumn("Employee", pinned=True),
        "team": "Team",
        "department": "Department",
        "location": "Location",
        "hours_per_year": st.column_config.NumberColumn("Hours / year", format="%d"),
        "hourly_rate": st.column_config.NumberColumn("Hourly rate", format="$ %.2f"),
        "total_utilization": st.column_config.ProgressColumn(
            "Utilization", min_value=0, max_value=160, format="%.0f%%"
        ),
        "allocated_internal_cost": money_column("Employee internal cost"),
        "risk": "Status",
    },
)