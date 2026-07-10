"""Reports page: data export/import and an executive cost report generator."""

from __future__ import annotations
import altair as alt
import pandas as pd
import streamlit as st

from app_theme import inject_app_theme, render_kautex_header
from models.user import UserRole
from services.cost_service import get_all_topic_cost_breakdowns, get_global_cost_totals, get_high_cost_topics
from services.export_service import (
    export_allocation_matrix_excel,
    export_allocations_csv,
    export_cost_report_excel,
    export_employees_csv,
    export_topics_csv,
)
from services.import_service import import_allocations_from_csv, import_employees_from_csv, import_topics_from_csv
from services.topic_service import get_all_topics

# Fetch raw dataset references for interactive on-screen report previews
from services.employee_service import get_all_employees
from services.allocation_service import get_all_allocations

inject_app_theme()
render_kautex_header(
    "Reports & data management",
    "Export data for offline analysis, bulk-import records, and review the executive cost report.",
    "Reporting",
)

is_admin = st.session_state.user.role == UserRole.ADMIN


# Each tab is its own fragment: interacting with a widget in one tab (e.g. the
# import-type dropdown) only reruns that fragment, not the whole page — without
# this, every interaction anywhere on the page re-triggers the Report Generator's
# Supabase queries too, which is both slow and causes tab content to flash/overlap
# while the full-page rerun repaints.
@st.fragment
def render_export_tab() -> None:
    # --- NEW: LIVE DATA PREVIEW GENERATOR ---
    st.subheader("Interactive Export File Previews")
    preview_type = st.radio(
        "Select Dataset to Preview Before Generation:",
        options=["Employees Roster", "Topics Pipeline", "Allocations Map"],
        horizontal=True,
    )

    with st.expander(f"📋 Live Data Engine View: {preview_type}", expanded=True):
        if preview_type == "Employees Roster":
            emp_data = get_all_employees()
            if emp_data:
                df_p = pd.DataFrame([e.model_dump() for e in emp_data])
                st.dataframe(df_p.head(5), use_container_width=True, hide_index=True)
                st.caption(f"Showing top 5 rows of {len(df_p)} active records.")
            else:
                st.info("No employee records found to preview.")

        elif preview_type == "Topics Pipeline":
            top_data = get_all_topics()
            if top_data:
                df_p = pd.DataFrame([t.model_dump() for t in top_data])
                st.dataframe(df_p.head(5), use_container_width=True, hide_index=True)
                st.caption(f"Showing top 5 rows of {len(df_p)} active pipeline rows.")
            else:
                st.info("No topic records found to preview.")

        else:
            alloc_data = get_all_allocations()
            if alloc_data:
                df_p = pd.DataFrame([a.model_dump() for a in alloc_data])
                st.dataframe(df_p.head(5), use_container_width=True, hide_index=True)
                st.caption(f"Showing top 5 rows of {len(df_p)} calculated allocations.")
            else:
                st.info("No allocation records found to preview.")

    st.divider()
    st.subheader("CSV exports")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Generate Employees.csv", width="stretch"):
            st.download_button(
                "Download Employees.csv",
                data=export_employees_csv(),
                file_name="employees.csv",
                mime="text/csv",
                width="stretch",
            )
    with col2:
        if st.button("Generate Topics.csv", width="stretch"):
            st.download_button(
                "Download Topics.csv",
                data=export_topics_csv(),
                file_name="topics.csv",
                mime="text/csv",
                width="stretch",
            )
    with col3:
        if st.button("Generate Allocations.csv", width="stretch"):
            st.download_button(
                "Download Allocations.csv",
                data=export_allocations_csv(),
                file_name="allocations.csv",
                mime="text/csv",
                width="stretch",
            )

    st.divider()
    st.subheader("Excel exports")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate Cost Report (Excel)", width="stretch"):
            st.download_button(
                "Download Cost_Report.xlsx",
                data=export_cost_report_excel(),
                file_name="cost_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                width="stretch",
            )
    with col2:
        if st.button("Generate Allocation Matrix (Excel)", width="stretch"):
            st.download_button(
                "Download Allocation_Matrix.xlsx",
                data=export_allocation_matrix_excel(),
                file_name="allocation_matrix.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                width="stretch",
            )


@st.fragment
def render_import_tab() -> None:
    if not is_admin:
        st.warning("Only admins can import data. Your role: " + st.session_state.user.role.value.capitalize())
        return

    import_type = st.selectbox("What would you like to import?", ["Employees", "Topics", "Allocations"])

    if import_type == "Employees":
        st.caption("Expected CSV columns: name, available_hours_per_year (optional), hourly_rate, status (optional)")
        uploaded_file = st.file_uploader("Upload CSV file", type="csv", key="report_emp_upload")
        if uploaded_file and st.button("Import Employees", type="primary"):
            result = import_employees_from_csv(uploaded_file.getvalue())
            if not result["success"]:
                st.error(f"Import failed: {result['error']}")
            else:
                st.success(f"Successfully imported {result['imported']} of {result['total']} employee(s).")
                if result["errors"]:
                    st.warning("\n".join(result["errors"][:5]))
                st.rerun(scope="fragment")

    elif import_type == "Topics":
        st.caption("Expected CSV columns: name, category (optional), area (optional), status (optional), business_justification (optional)")
        uploaded_file = st.file_uploader("Upload CSV file", type="csv", key="report_topic_upload")
        if uploaded_file and st.button("Import Topics", type="primary"):
            result = import_topics_from_csv(uploaded_file.getvalue())
            if not result["success"]:
                st.error(f"Import failed: {result['error']}")
            else:
                st.success(f"Successfully imported {result['imported']} of {result['total']} topic(s).")
                if result["errors"]:
                    st.warning("\n".join(result["errors"][:5]))
                st.rerun(scope="fragment")

    else:  # Allocations
        st.caption("Expected CSV columns: employee name, topic name, allocation % (0-100), comment (optional)")
        st.info("Employees and Topics must already exist — rows are matched by exact name.")
        uploaded_file = st.file_uploader("Upload CSV file", type="csv", key="report_alloc_upload")
        if uploaded_file and st.button("Import Allocations", type="primary"):
            result = import_allocations_from_csv(uploaded_file.getvalue())
            if not result["success"]:
                st.error(f"Import failed: {result['error']}")
            else:
                st.success(f"Successfully imported {result['imported']} of {result['total']} allocation(s).")
                if result["errors"]:
                    st.warning("\n".join(result["errors"][:5]))
                st.rerun(scope="fragment")


@st.fragment
def render_report_tab() -> None:
    topics = get_all_topics()
    breakdowns = get_all_topic_cost_breakdowns()
    metrics = get_global_cost_totals(breakdowns)

    st.subheader("Global metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total cost", f"${metrics['total_cost']:,.2f}")
    col2.metric("Total headcount", metrics["total_headcount"])
    col3.metric("Avg cost / employee", f"${metrics['average_cost_per_employee']:,.2f}")

    st.divider()
    st.subheader("Cost distribution by topic")

    topic_costs = []
    for topic in topics:
        cost = breakdowns.get(topic.id, {"internal_personnel": 0, "external_tooling": 0, "testing": 0, "recovery": 0, "total": 0})
        topic_costs.append(
            {
                "topic": topic.name,
                "Internal": cost["internal_personnel"],
                "External": cost["external_tooling"] + cost["testing"],
                "Recovery": cost["recovery"],
                "total": cost["total"],
            }
        )

    if topic_costs:
        df_costs = pd.DataFrame(topic_costs)
        df_long = df_costs.melt(id_vars=["topic", "total"], value_vars=["Internal", "External", "Recovery"], var_name="Cost type", value_name="amount")

        chart = (
            alt.Chart(df_long)
            .mark_bar()
            .encode(
                x=alt.X("topic:N", title=None, sort="-y", axis=alt.Axis(labelAngle=-28)),
                y=alt.Y("amount:Q", title="Cost ($)"),
                color=alt.Color("Cost type:N", title="Cost type"),
                tooltip=["topic", "Cost type", alt.Tooltip("amount:Q", format="$,.0f")],
            )
            .properties(height=380)
        )
        st.altair_chart(chart, use_container_width=True)

        st.divider()
        st.subheader("Cost breakdown table")
        df_display = df_costs.rename(columns={"topic": "Topic", "total": "Total"}).copy()

        # --- NEW: EXECUTIVE COST MATRIX HEATMAP STYLING ---
        # Sort values by total cost center impact for quick analysis
        df_display = df_display.sort_values("Total", ascending=False)

        # Highlight cost intensity relative to the largest total in view. Uses
        # Styler.map (no matplotlib dependency) instead of background_gradient,
        # which requires matplotlib and isn't in requirements.txt.
        max_total = df_display["Total"].max() or 1.0

        def style_cost_intensity(val):
            try:
                intensity = float(val) / max_total
            except (TypeError, ValueError):
                return ""
            if intensity >= 0.66:
                return "background-color: #2b6cb0; color: white; font-weight: bold;"
            if intensity >= 0.33:
                return "background-color: #bee3f8; color: #1a365d;"
            return "background-color: #ebf8ff; color: #2c5282;"

        styled_cost_df = df_display.style.map(
            style_cost_intensity, subset=["Internal", "External", "Total"]
        ).format({
            "Internal": "${:,.2f}",
            "External": "${:,.2f}",
            "Recovery": "${:,.2f}",
            "Total": "${:,.2f}"
        })

        st.dataframe(styled_cost_df, use_container_width=True, hide_index=True)
    else:
        st.info("No topics created yet.")

    st.divider()
    st.subheader("High-cost projects")
    st.caption("Topics where external tooling, testing and recovery costs exceed 30% of the topic's total cost.")

    high_cost = get_high_cost_topics(threshold_percentage=0.3, breakdowns=breakdowns)
    if high_cost:
        for i, info in enumerate(high_cost):
            with st.expander(f"{info['name']} — {info['external_ratio'] * 100:.1f}% external", expanded=(i == 0)):
                st.write(f"**Category:** {info['category']}")
                if info["business_justification"]:
                    st.write(f"**Business justification:** {info['business_justification']}")
                col1, col2, col3 = st.columns(3)
                col1.metric("Total cost", f"${info['total_cost']:,.2f}")
                col2.metric("External cost", f"${info['external_cost']:,.2f}")
                col3.metric("External %", f"{info['external_ratio'] * 100:.1f}%")
    else:
        st.info("All projects have reasonable external cost ratios.")


tab_export, tab_import, tab_report = st.tabs(["Export Data", "Import Data", "Report Generator"])

with tab_export:
    render_export_tab()

with tab_import:
    render_import_tab()

with tab_report:
    render_report_tab()