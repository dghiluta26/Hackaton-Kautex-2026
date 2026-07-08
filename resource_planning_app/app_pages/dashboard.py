"""General dashboard: high-level overview of the resource plan."""

import streamlit as st

from app_theme import (
    build_planning_model,
    inject_app_theme,
    load_sample_planning_data,
    money_column,
    render_kautex_header,
    table_height,
    topic_cost_chart,
    utilization_chart,
)


inject_app_theme()
render_kautex_header(
    "Digital resource, cost & portfolio dashboard",
    "Main working screen for allocation, utilization warnings and cost visibility.",
    "General dashboard",
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
        "additional_internal_cost": money_column("Additional internal"),
        "external_cost": money_column("External"),
        "recovery": money_column("Recovery"),
        "total_topic_cost": money_column("Total topic cost"),
    },
)

with st.container(border=True):
    st.markdown("**Team report preview**")
    st.dataframe(
        team_summary,
        hide_index=True,
        height=table_height(len(team_summary), 240, 420),
        column_config={
            "team": st.column_config.TextColumn("Team", pinned=True),
            "team_members": st.column_config.NumberColumn("Members", format="%d"),
            "average_utilization": st.column_config.ProgressColumn(
                "Average utilization", min_value=0, max_value=160, format="%.0f%%"
            ),
            "total_internal_cost": money_column("Internal cost"),
            "overallocated": st.column_config.NumberColumn("Above 100%", format="%d"),
        },
    )
