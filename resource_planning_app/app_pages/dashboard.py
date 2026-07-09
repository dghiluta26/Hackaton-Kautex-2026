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


def render_live_ticker(overallocated_count: int) -> None:
    """Renders the animated Live Pulse Activity Ticker based on active resource risks."""
    if overallocated_count > 0:
        border_color = "#D92D20"
        dot_color = "#D92D20"
        bg_badge = "#FEE2E2"
        text_badge = "#991B1B"
        badge_label = "Action Required"
        message = f"<strong>Live System Update:</strong> {overallocated_count} employees currently exceed 100% standard allocation. Revision needed."
    else:
        border_color = "#10B981"
        dot_color = "#10B981"
        bg_badge = "#ECFDF5"
        text_badge = "#047857"
        badge_label = "Optimal Status"
        message = "<strong>Live System Update:</strong> All employee workloads are balanced within normal parameters."

    st.markdown(
        f"""
        <style>
            .ticker-wrapper {{
                background: #FFFFFF;
                border: 1px solid #D9E2EC;
                border-left: 4px solid {border_color};
                border-radius: 8px;
                padding: 12px 16px;
                margin-top: -8px;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                box-shadow: 0 4px 12px rgba(23, 32, 51, 0.04);
            }}
            .ticker-left {{ display: flex; align-items: center; gap: 12px; }}
            .pulse-container {{ display: flex; align-items: center; justify-content: center; width: 16px; height: 16px; }}
            .pulse-dot {{
                width: 10px; height: 10px; background: {dot_color}; border-radius: 50%;
                animation: pulse-animation-custom 1.6s infinite;
            }}
            @keyframes pulse-animation-custom {{
                0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 {f"rgba(217, 45, 32, 0.5)" if overallocated_count > 0 else "rgba(16, 185, 129, 0.5)"}; }}
                70% {{ transform: scale(1); box-shadow: 0 0 0 8px rgba(217, 45, 32, 0); }}
                100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(217, 45, 32, 0); }}
            }}
            .ticker-text {{ font-size: 14px; color: #172033; font-weight: 500; }}
            .ticker-badge {{
                font-size: 11px; font-weight: 700; text-transform: uppercase; background: {bg_badge}; color: {text_badge};
                padding: 3px 8px; border-radius: 4px; letter-spacing: 0.05em; white-space: nowrap;
            }}
        </style>
        <div class="ticker-wrapper">
            <div class="ticker-left">
                <div class="pulse-container"><div class="pulse-dot"></div></div>
                <div class="ticker-text">{message}</div>
            </div>
            <div class="ticker-badge">{badge_label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_workflow_steps(current_step: int) -> None:
    """Renders an enterprise-grade step progress bar mapping the business workflow."""
    steps = [
        {"num": 1, "title": "Data Ingestion & Sync", "desc": "Database alignment"},
        {"num": 2, "title": "Capacity & Risk Audit", "desc": "Analyze workload & cost"},
        {"num": 3, "title": "Allocation Adjustments", "desc": "Resolve bottlenecks"},
        {"num": 4, "title": "Sign-off & Lock Budget", "desc": "Freeze planning quarter"}
    ]
    
    steps_html = ""
    for i, step in enumerate(steps):
        is_active = step["num"] == current_step
        is_completed = step["num"] < current_step

        node_bg = "#00A6DF" if is_active else ("#172033" if is_completed else "#FFFFFF")
        node_text_color = "#FFFFFF" if (is_active or is_completed) else "#94A3B8"
        node_border = "none" if (is_active or is_completed) else "2px solid #CBD5E1"
        title_weight = "700" if is_active else "500"
        title_color = "#172033" if is_active else ("#64748B" if is_completed else "#94A3B8")
  
        steps_html += f"""
        <div class="step-item">
            <div class="step-node" style="background: {node_bg}; color: {node_text_color}; border: {node_border};">
                { "✓" if is_completed else step["num"] }
            </div>
            <div class="step-content">
                <div class="step-title" style="font-weight: {title_weight}; color: {title_color};">{step["title"]}</div>
                <div class="step-desc">{step["desc"]}</div>
            </div>
        </div>
        """
        if i < len(steps) - 1:
            line_color = "#00A6DF" if step["num"] < current_step else "#E2E8F0"
            steps_html += f'<div class="step-line" style="background: {line_color};"></div>'

    st.markdown(
        f"""
        <style>
            .workflow-container {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                background: #FFFFFF;
                border: 1px solid #D9E2EC;
                border-radius: 8px;
                padding: 16px 24px;
                margin-bottom: 24px;
                box-shadow: 0 4px 12px rgba(23, 32, 51, 0.04);
            }}
            .step-item {{
                display: flex;
                align-items: center;
                gap: 12px;
                flex-shrink: 0;
            }}
            .step-node {{
                width: 28px;
                height: 28px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 13px;
                font-weight: 700;
                transition: all 0.3s ease;
            }}
            .step-content {{
                display: flex;
                flex-direction: column;
            }}
            .step-title {{
                font-size: 13px;
                line-height: 1.2;
            }}
            .step-desc {{
                font-size: 11px;
                color: #94A3B8;
            }}
            .step-line {{
                height: 2px;
                flex-grow: 1;
                margin: 0 16px;
                min-width: 20px;
                transition: background 0.3s ease;
            }}
            @media (max-width: 1024px) {{
                .workflow-container {{ flex-direction: column; align-items: flex-start; gap: 16px; }}
                .step-line {{ display: none; }}
            }}
        </style>
        
        <div class="workflow-container">
            {steps_html}
        </div>
        """,
        unsafe_allow_html=True
    )


inject_app_theme()
render_kautex_header(
    "Digital resource & cost dashboard",
    "Live overview of employee utilization and projected internal costs.",
    "Live Database Sync",
)

# --- 1. Fetch Real Data ---
db_employees = get_all_employees()
db_topics = get_all_topics()
db_allocations = get_all_allocations()

if not db_employees:
    st.info("Please add employees and topics to view dashboard analytics.")
    st.stop()

# --- 2. Calculate Live Analytics ---
employee_data = []
total_internal_cost = 0

for emp in db_employees:
    emp_allocs = [a for a in db_allocations if a.employee_id == emp.id]
    total_util = sum([a.allocation_percentage for a in emp_allocs])
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


# =========================================================================
# --- ACCESORII DE DESIGN REUNITE (TICKER + WORKFLOW STEPS) ---
# Se randează elegant unul sub celălalt, fix sub header-ul mare Kautex
# =========================================================================
render_live_ticker(overallocated_count=overallocated_count)

# Dashboard-ul reprezintă faza de analiză de risc și costuri, deci pasul curent este 2!
render_workflow_steps(current_step=2)


# --- 3. Top Metrics Row ---
with st.container(horizontal=True):
    st.metric("Total employees", f"{len(db_employees)}", border=True)
    st.metric("Total topics", f"{len(db_topics)}", border=True)
    st.metric("Average utilization", f"{avg_utilization:.0f}%", border=True)
    st.metric("Total internal cost", f"$ {total_internal_cost:,.0f}", border=True)
    st.metric("Overallocated employees", f"{overallocated_count}", delta="needs review" if overallocated_count else "clear", border=True)

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