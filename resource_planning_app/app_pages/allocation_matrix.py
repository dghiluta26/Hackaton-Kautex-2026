"""Allocation matrix page: assign employees to topics and check utilization."""

import streamlit as st

from app_theme import (
    TOPIC_COLUMNS,
    build_planning_model,
    inject_app_theme,
    load_sample_planning_data,
    money_column,
    percent_column,
    render_kautex_header,
    table_height,
    utilization_chart,
)


inject_app_theme()
render_kautex_header(
    "Allocation matrix",
    "Edit employee-to-topic percentages and immediately review utilization and cost impact.",
    "Responsive editable table",
)

employees, topics, allocations, costs = load_sample_planning_data()

st.markdown("### Allocation table")
st.html(
    '<div class="section-note">This frontend version uses sample data until allocation_service is implemented.</div>'
)

matrix_input = employees[["employee", "team", "department", "location", "hours_per_year", "hourly_rate"]].merge(
    allocations, on="employee", how="left"
)

edited_matrix = st.data_editor(
    matrix_input,
    key="allocation_matrix_editor",
    num_rows="fixed",
    hide_index=True,
    height=table_height(len(matrix_input), 360, 620),
    disabled=["employee", "team", "department", "location", "hours_per_year", "hourly_rate"],
    column_config={
        "employee": st.column_config.TextColumn("Employee", pinned=True),
        "team": "Team",
        "department": "Department",
        "location": "Location",
        "hours_per_year": st.column_config.NumberColumn("Hours / year", format="%d"),
        "hourly_rate": st.column_config.NumberColumn("Hourly rate", format="$ %.2f"),
        **{topic: percent_column(topic, editable=True) for topic in TOPIC_COLUMNS},
        "allocation_comment": st.column_config.TextColumn("Comment", width="large"),
    },
)

preview_allocations = edited_matrix[["employee", *TOPIC_COLUMNS, "allocation_comment"]].copy()
preview_model, preview_topics, _ = build_planning_model(employees, topics, preview_allocations, costs)

overallocated = int((preview_model["total_utilization"] > 100).sum())
with st.container(horizontal=True):
    st.metric("Employees in matrix", f"{len(preview_model)}", border=True)
    st.metric("Average utilization", f"{preview_model['total_utilization'].mean():.0f}%", border=True)
    st.metric("Overallocated employees", f"{overallocated}", delta="needs review" if overallocated else "clear", border=True)
    st.metric("Preview total topic cost", f"$ {preview_topics['total_topic_cost'].sum():,.0f}", border=True)

left, right = st.columns([1, 1], vertical_alignment="top")
with left:
    with st.container(border=True):
        st.markdown("**Utilization warnings**")
        warning_view = preview_model[
            ["employee", "team", "location", "total_utilization", "allocated_internal_cost", "risk"]
        ].sort_values("total_utilization", ascending=False)
        st.dataframe(
            warning_view,
            hide_index=True,
            height=table_height(len(warning_view), 300, 480),
            column_config={
                "employee": st.column_config.TextColumn("Employee", pinned=True),
                "total_utilization": st.column_config.ProgressColumn(
                    "Utilization", min_value=0, max_value=160, format="%.0f%%"
                ),
                "allocated_internal_cost": money_column("Internal cost"),
            },
        )

with right:
    with st.container(border=True):
        st.markdown("**Utilization chart**")
        st.altair_chart(utilization_chart(preview_model), height=360)

st.markdown("### Cost calculation by topic")
st.dataframe(
    preview_topics.sort_values("total_topic_cost", ascending=False),
    hide_index=True,
    height=table_height(len(preview_topics), 260, 460),
    column_config={
        "topic": st.column_config.TextColumn("Topic", pinned=True),
        "employees_involved": st.column_config.NumberColumn("Employees", format="%d"),
        "employee_internal_cost": money_column("Employee internal"),
        "additional_internal_cost": money_column("Additional internal"),
        "external_cost": money_column("External"),
        "recovery": money_column("Recovery"),
        "total_topic_cost": money_column("Total topic cost"),
    },
)

st.caption("The table is intentionally frontend-only here. Hook it to allocation_service once CRUD is implemented.")
