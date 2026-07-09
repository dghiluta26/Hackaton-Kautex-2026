"""General dashboard: high-level overview of the resource plan."""

import base64
from pathlib import Path

import streamlit as st

from app_theme import (
    build_planning_model,
    inject_app_theme,
    load_sample_planning_data,
    money_column,
    table_height,
    topic_cost_chart,
    utilization_chart,
)


def get_image_base64(image_path: Path) -> str | None:
    """Convert image to base64 for HTML display. Returns None if file is missing."""
    if not image_path.exists():
        return None
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def render_hero_header(title: str, subtitle: str, badge_text: str):
    """Render the Kautex hero card with the banner image as background,
    the real Kautex logo, title, subtitle and a badge — all in one card."""
    assets_dir = Path(__file__).resolve().parent.parent / "assets"
    banner_path = assets_dir / "Kautex.png"
    logo_path = assets_dir / "KAUTEX_Logo.jpg"  # ajusteaza extensia daca e .jpg

    banner_base64 = get_image_base64(banner_path)
    logo_base64 = get_image_base64(logo_path)

    if banner_base64 is None:
        st.warning(f"Banner image not found at: {banner_path}")
        background_layer = "linear-gradient(90deg, #062040 0%, #0b3d78 100%)"
    else:
        background_layer = (
            "linear-gradient(90deg, rgba(2,10,25,0.88) 0%, rgba(3,30,64,0.72) 45%, "
            "rgba(3,30,64,0.35) 100%), "
            f'url("data:image/png;base64,{banner_base64}")'
        )

    if logo_base64 is None:
        st.warning(f"Logo image not found at: {logo_path}")
        logo_html = '<div class="kautex-hero-logo-fallback">K</div>'
    else:
        logo_html = f'<img class="kautex-hero-logo" src="data:image/png;base64,{logo_base64}" alt="Kautex logo" />'

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
    "Demo Kautex Hackathon  "
    "(General dashboard)",
)

employees, topics, allocations, costs = load_sample_planning_data()
model, topic_summary, team_summary = build_planning_model(employees, topics, allocations, costs)

total_cost = topic_summary["total_topic_cost"].sum()
overallocated = int((model["total_utilization"] > 100).sum())
average_utilization = model["total_utilization"].mean()

with st.container(horizontal=True):
    st.metric("Total employees", f"{len(model)}", border=True)
    st.metric("Total topics", f"{len(topic_summary)}", border=True)
    st.metric("Average utilization", f"{average_utilization:.0f}%", border=True)
    st.metric("Total planning cost", f"$ {total_cost:,.0f}", border=True)
    st.metric("Overallocated employees", f"{overallocated}", delta="needs review" if overallocated else "clear", border=True)

st.markdown("### Planning overview")
st.html(
    '<div class="section-note">Inspired by the planning spreadsheet, but shaped as an interactive browser workflow.</div>'
)

chart_left, chart_right = st.columns([1.1, 1], vertical_alignment="top")
with chart_left:
    with st.container(border=True):
        st.markdown("**Topic cost split**")
        st.altair_chart(topic_cost_chart(topic_summary), height=330)

with chart_right:
    with st.container(border=True):
        st.markdown("**Utilization by employee**")
        st.altair_chart(utilization_chart(model), height=330)

st.markdown("### Responsive employee planning table")
employee_view = model[
    [
        "employee",
        "team",
        "department",
        "location",
        "hours_per_year",
        "hourly_rate",
        "total_utilization",
        "allocated_internal_cost",
        "risk",
    ]
].sort_values("total_utilization", ascending=False)

st.dataframe(
    employee_view,
    hide_index=True,
    height=table_height(len(employee_view), 300, 540),
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

st.markdown("### Topic summary")
st.dataframe(
    topic_summary.sort_values("total_topic_cost", ascending=False),
    hide_index=True,
    height=table_height(len(topic_summary), 260, 430),
    column_config={
        "topic": st.column_config.TextColumn("Topic", pinned=True),
        "employees_involved": st.column_config.NumberColumn("Employees", format="%d"),
        "employee_internal_cost": money_column("Employee cost"),
        "additional_internal_cost": money_column("Additional internal cost"),
        "external_cost": money_column("External cost"),
        "recovery": money_column("Recovery"),
        "total_topic_cost": money_column("Total topic cost"),
        "category": "Category",
        "status": "Status",
    },
)