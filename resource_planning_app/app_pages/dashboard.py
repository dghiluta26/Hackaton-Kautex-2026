"""General dashboard: high-level overview of the resource plan."""
from __future__ import annotations
import base64
from pathlib import Path
import streamlit as st
import pandas as pd

from app_theme import (
    inject_app_theme,
    money_column,
    table_height,
    utilization_chart,
)

from services.employee_service import get_all_employees
from services.topic_service import get_all_topics
from services.allocation_service import get_all_allocations

def get_image_base64(image_path: Path) -> str | None:
    """Convert image to base64 for HTML display."""
    if not image_path.exists():
        return None

    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def render_hero_header(title: str, subtitle: str, badge_text: str) -> None:
    """Render Kautex dashboard hero banner."""
    assets_dir = Path(__file__).resolve().parent.parent / "assets"
    banner_path = assets_dir / "Kautex.png"
    logo_path = assets_dir / "KAUTEX_Logo.jpg"

    banner_base64 = get_image_base64(banner_path)
    logo_base64 = get_image_base64(logo_path)

    background_layer = (
        "linear-gradient(90deg, #062040 0%, #0b3d78 100%)"
        if banner_base64 is None
        else (
            "linear-gradient(90deg, rgba(2,10,25,0.88) 0%, "
            "rgba(3,30,64,0.72) 45%, rgba(3,30,64,0.35) 100%), "
            f'url("data:image/png;base64,{banner_base64}")'
        )
    )

    logo_html = (
        '<div class="kautex-hero-logo-fallback">K</div>'
        if logo_base64 is None
        else (
            f'<img class="kautex-hero-logo" '
            f'src="data:image/jpeg;base64,{logo_base64}" '
            f'alt="Kautex logo" />'
        )
    )

    st.markdown(
        f"""
        <style>
        .kautex-hero-card {{
            border-radius: 18px;
            overflow: hidden;
            margin-bottom: 28px;
            padding: 48px 40px;
            min-height: 260px;
            position: relative;
            background-image: {background_layer};
            background-size: cover;
            background-position: 50% 70%;
            box-shadow: 0 18px 40px rgba(15, 23, 42, 0.25);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 24px;
        }}

        .kautex-hero-left {{
            display: flex;
            align-items: center;
            gap: 18px;
        }}

        .kautex-hero-logo {{
            height: 52px;
            width: auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 8px;
            padding: 6px 10px;
        }}

        .kautex-hero-logo-fallback {{
            width: 52px;
            height: 52px;
            min-width: 52px;
            border-radius: 10px;
            border: 2px solid #38bdf8;
            background: rgba(2, 20, 45, 0.55);
            color: #38bdf8;
            font-weight: 800;
            font-size: 26px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .kautex-hero-text .eyebrow {{
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            color: #7dd3fc;
            margin-bottom: 6px;
        }}

        .kautex-hero-text h1 {{
            font-size: 30px;
            line-height: 1.15;
            margin: 0 0 8px 0;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: -0.02em;
        }}

        .kautex-hero-text p {{
            font-size: 15px;
            margin: 0;
            color: rgba(255, 255, 255, 0.85);
        }}

        .kautex-hero-badge {{
            flex-shrink: 0;
            padding: 8px 16px;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.92);
            color: #0f172a;
            font-weight: 700;
            font-size: 13px;
            white-space: nowrap;
        }}
        </style>

        <div class="kautex-hero-card">
            <div class="kautex-hero-left">
                {logo_html}
                <div class="kautex-hero-text">
                    <div class="eyebrow">Kautex Engineering Planning</div>
                    <h1>{title}</h1>
                    <p>{subtitle}</p>
                </div>
            </div>
            <div class="kautex-hero-badge">{badge_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


inject_app_theme()
render_hero_header(
    "Digital resource, cost & portfolio dashboard",
    "Main working screen for allocation, utilization warnings and cost visibility.",
    "Demo Kautex Hackathon (General dashboard)",
)

from services.employee_service import get_all_employees
from services.topic_service import get_all_topics
from services.allocation_service import get_all_allocations


def render_live_ticker(overallocated_count: int) -> None:
    """Renders the animated Live Pulse Activity Ticker based on active resource risks."""
    if overallocated_count > 0:
        border_color = "#D92D20"  # Rosu alerta
        dot_color = "#D92D20"
        bg_badge = "#FEE2E2"
        text_badge = "#991B1B"
        badge_label = "Action Required"
        message = f"<strong>Live System Update:</strong> {overallocated_count} employees currently exceed 100% standard allocation. Revision needed."
        shadow_color = "rgba(217, 45, 32, 0.5)"
        shadow_fade = "rgba(217, 45, 32, 0)"
    else:
        border_color = "#10B981"  # Verde optim
        dot_color = "#10B981"
        bg_badge = "#ECFDF5"
        text_badge = "#047857"
        badge_label = "Optimal Status"
        message = "<strong>Live System Update:</strong> All employee workloads are balanced within normal parameters."
        shadow_color = "rgba(16, 185, 129, 0.5)"
        shadow_fade = "rgba(16, 185, 129, 0)"

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
                margin-bottom: 24px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                box-shadow: 0 4px 12px rgba(23, 32, 51, 0.04);
            }}
            .ticker-left {{
                display: flex;
                align-items: center;
                gap: 12px;
            }}
            .pulse-container {{
                display: flex;
                align-items: center;
                justify-content: center;
                width: 16px;
                height: 16px;
            }}
            .pulse-dot {{
                width: 10px;
                height: 10px;
                background: {dot_color};
                border-radius: 50%;
                animation: pulse-animation-custom 1.6s infinite;
            }}
            @keyframes pulse-animation-custom {{
                0% {{
                    transform: scale(0.95);
                    box-shadow: 0 0 0 0 {shadow_color};
                }}
                70% {{
                    transform: scale(1);
                    box-shadow: 0 0 0 8px {shadow_fade};
                }}
                100% {{
                    transform: scale(0.95);
                    box-shadow: 0 0 0 0 {shadow_fade};
                }}
            }}
            .ticker-text {{
                font-size: 14px;
                color: #172033;
                font-weight: 500;
            }}
            .ticker-badge {{
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
                background: {bg_badge};
                color: {text_badge};
                padding: 3px 8px;
                border-radius: 4px;
                letter-spacing: 0.05em;
                white-space: nowrap;
            }}
        </style>
        
        <div class="ticker-wrapper">
            <div class="ticker-left">
                <div class="pulse-container">
                    <div class="pulse-dot"></div>
                </div>
                <div class="ticker-text">{message}</div>
            </div>
            <div class="ticker-badge">
                {badge_label}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


db_employees = get_all_employees()
db_topics = get_all_topics()
db_allocations = get_all_allocations()

if not db_employees:
    st.info("Please add employees and topics to view dashboard analytics.")
    st.stop()

employee_data = []
total_internal_cost = 0

for emp in db_employees:
    # Find all allocations for this specific employee
    emp_allocs = [a for a in db_allocations if a.employee_id == emp.id]

    # Calculate total utilization percentage (e.g., 20% + 50% = 70%)
    total_util = sum([a.allocation_percentage for a in emp_allocs])

    # Securizare impotriva valorilor None/lipsa din baza de date pentru a preveni crash-ul calculelor
    hours = emp.available_hours_per_year if emp.available_hours_per_year is not None else 0
    rate = emp.hourly_rate if emp.hourly_rate is not None else 0

    # Calculate cost: (Hours * Rate) * (Utilization / 100)
    emp_cost = (hours * rate) * (total_util / 100)
    total_internal_cost += emp_cost

    employee_data.append({
        "employee": emp.name,
        "team": emp.team_id or "Unassigned",
        "department": emp.department_id or "Unassigned",
        "location": emp.location_id or "Unassigned",
        "hours_per_year": hours,
        "hourly_rate": rate,
        "total_utilization": total_util,
        "allocated_internal_cost": emp_cost,
        "risk": "Overallocated" if total_util > 100 else "OK"
    })

df_employees = pd.DataFrame(employee_data)
overallocated_count = len(df_employees[df_employees["total_utilization"] > 100])
avg_utilization = df_employees["total_utilization"].mean() if not df_employees.empty else 0

render_live_ticker(overallocated_count=overallocated_count)


with st.container(horizontal=True):
    st.metric("Total employees", f"{len(db_employees)}", border=True)
    st.metric("Total topics", f"{len(db_topics)}", border=True)
    st.metric("Average utilization", f"{avg_utilization:.0f}%", border=True)
    st.metric("Total internal cost", f"$ {total_internal_cost:,.0f}", border=True)
    st.metric("Overallocated employees", f"{overallocated_count}", delta="needs review" if overallocated_count else "clear", border=True)

st.markdown("### Utilization by Employee")
if not df_employees.empty:
    st.altair_chart(utilization_chart(df_employees), use_container_width=True)

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
inject_app_theme()
render_hero_header(
    "Digital resource, cost & portfolio dashboard",
    "Main working screen for allocation, utilization warnings and cost visibility.",
    "Demo Kautex Hackathon (General dashboard)",
)

from services.employee_service import get_all_employees
from services.topic_service import get_all_topics
from services.allocation_service import get_all_allocations


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
