"""Topics page: manage topics/projects."""

import streamlit as st
import pandas as pd

from app_theme import inject_app_theme, render_kautex_header
from models.topic import Topic
from models.user import UserRole
from services.cost_service import (
    create_cost_item,
    delete_cost_item,
    get_cost_items_by_topic,
    get_topic_cost_breakdown,
)
from services.topic_service import create_topic, delete_topic, get_all_topics, update_topic

inject_app_theme()
render_kautex_header(
    "Topics",
    "View and manage topics/projects, their objectives, deliverables, and costs.",
    "Project management",
)

is_admin = st.session_state.user.role == UserRole.ADMIN

tab_list, tab_add, tab_costs = st.tabs(["Topic List", "Add / Edit Topic", "Manage Costs"])

# --- 1. Topic List ---
with tab_list:
    all_topics = get_all_topics()

    if len(all_topics) > 0:
        # --- NEW: PORTFOLIO EXECUTIVE METRICS ---
        total_topics = len(all_topics)
        active_topics = sum(1 for t in all_topics if str(t.status).strip().lower() == "active")
        at_risk_topics = sum(1 for t in all_topics if str(t.status).strip().lower() == "at risk")

        # Calculate cross-portfolio cumulative cost projections
        portfolio_total_cost = 0.0
        for t in all_topics:
            try:
                portfolio_total_cost += float(get_topic_cost_breakdown(t.id).get("total", 0.0))
            except Exception:
                pass

        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.metric(label="Total Portfolio Topics", value=f"{total_topics} Pipeline")
        with m_col2:
            st.metric(label="Active Pipelines", value=f"{active_topics} Projects")
        with m_col3:
            st.metric(
                label="At Risk Warning Flag",
                value=f"{at_risk_topics} Critical",
                delta="Needs Attention" if at_risk_topics > 0 else "Optimal",
                delta_color="inverse" if at_risk_topics > 0 else "normal"
            )
        with m_col4:
            st.metric(label="Total Portfolio Financial Valuation", value=f"$ {portfolio_total_cost:,.2f}")

        st.divider()

        # --- NATIVE STATUS HEATMAP STYLING ---
        topic_df = pd.DataFrame([topic.model_dump() for topic in all_topics])

        def style_topic_status(val):
            status_str = str(val).strip().lower()
            if status_str == "active":
                return "background-color: #e2f0d9; color: #385723; font-weight: bold;"      # Safe Corporate Green
            if status_str == "at risk":
                return "background-color: #fce4d6; color: #c65911; font-weight: bold;"     # Alert Orange/Red
            if status_str == "on hold":
                return "background-color: #fff2cc; color: #7f6000; font-weight: bold;"     # Muted Amber
            if status_str == "completed":
                return "background-color: #f2f2f2; color: #595959; font-style: italic;"     # Inactive Dark Grey
            return ""

        styled_topic_df = topic_df.style.map(style_topic_status, subset=["status"])
        st.dataframe(styled_topic_df, hide_index=True, use_container_width=True)
    else:
        st.info("No topics found. Add one in the 'Add / Edit Topic' tab.")

    st.divider()
    st.subheader("Mass Import Topics (CSV)")
    st.caption("Required columns: name, category, area, status")

    uploaded_file = st.file_uploader("Upload CSV", type="csv", key="topic_uploader")

    if uploaded_file is not None:
        sample = uploaded_file.read(1024).decode("utf-8-sig", errors="ignore")
        uploaded_file.seek(0)
        separator = ";" if ";" in sample.split("\n")[0] else ","

        df = pd.read_csv(uploaded_file, sep=separator, encoding="utf-8-sig")
        df.columns = [str(col).strip().lower() for col in df.columns]

        st.write(f"Preview (Detected separator: '{separator}'):")
        st.dataframe(df.head(), hide_index=True)

        if st.button("Import to Database", type="primary"):
            success_count = 0
            skipped_count = 0

            for index, row in df.iterrows():
                if pd.isna(row.get("name")) or str(row.get("name")).strip() == "":
                    skipped_count += 1
                    continue

                new_topic = Topic(
                    name=str(row["name"]).strip(),
                    category=str(row.get("category", "Unmapped")),
                    area=str(row.get("area", "")),
                    status=str(row.get("status", "Active"))
                )
                create_topic(new_topic)
                success_count += 1

            st.success(f"Successfully imported {success_count} topics! (Skipped {skipped_count} invalid rows)")
            st.rerun()

# --- 2. Add / Edit Topic ---
with tab_add:
    if not is_admin:
        st.warning("Only admins can add or edit topics. Your role: " + st.session_state.user.role.value.capitalize())
    else:
        st.subheader("Add new topic")
        with st.form("add_topic_form"):
            name = st.text_input("Topic name:", placeholder="e.g., Customer Request - Project X")
            category = st.selectbox(
                "Category:",
                ["Internal Efforts", "Customer Request", "CAE", "Testing", "Other"],
            )
            area = st.text_input("Area:", placeholder="e.g., AI initiatives")
            status = st.selectbox("Status:", ["Active", "At risk", "On hold", "Completed"])
            business_justification = st.text_area(
                "Business justification:",
                placeholder="Explain why this project is needed and its strategic value...",
                height=120,
            )

            submitted = st.form_submit_button("Add Topic", type="primary")
            if submitted:
                if not name:
                    st.error("Topic name is required.")
                else:
                    create_topic(
                        Topic(
                            name=name,
                            category=category,
                            area=area,
                            status=status,
                            business_justification=business_justification,
                        )
                    )
                    st.success("Topic added successfully!")
                    st.rerun()

        st.divider()
        st.subheader("Edit or delete an existing topic")

        all_topics = get_all_topics()
        if not all_topics:
            st.info("No topics yet.")
        else:
            selected_id = st.selectbox(
                "Select topic:",
                options=[t.id for t in all_topics],
                format_func=lambda tid: next(t.name for t in all_topics if t.id == tid),
                key="edit_topic_select",
            )
            topic = next(t for t in all_topics if t.id == selected_id)

            col1, col2 = st.columns(2)
            with col1:
                edit_name = st.text_input("Name:", topic.name, key="edit_topic_name")
                edit_category = st.text_input("Category:", topic.category or "", key="edit_topic_category")
            with col2:
                edit_area = st.text_input("Area:", topic.area or "", key="edit_topic_area")
                edit_status = st.text_input("Status:", topic.status or "", key="edit_topic_status")
            edit_justification = st.text_area(
                "Business justification:", topic.business_justification or "", key="edit_topic_justification"
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Update Topic", key="update_topic_btn"):
                    update_topic(
                        selected_id,
                        {
                            "name": edit_name,
                            "category": edit_category,
                            "area": edit_area,
                            "status": edit_status,
                            "business_justification": edit_justification,
                        },
                    )
                    st.success("Topic updated successfully!")
                    st.rerun()
            with col2:
                if st.button("Delete Topic", key="delete_topic_btn"):
                    delete_topic(selected_id)
                    st.success("Topic deleted successfully!")
                    st.rerun()

# --- 3. Manage Costs ---
with tab_costs:
    all_topics = get_all_topics()

    if not all_topics:
        st.info("No topics available. Add a topic first.")
    else:
        selected_id = st.selectbox(
            "Select topic:",
            options=[t.id for t in all_topics],
            format_func=lambda tid: next(t.name for t in all_topics if t.id == tid),
            key="costs_topic_select",
        )
        topic = next(t for t in all_topics if t.id == selected_id)

        breakdown = get_topic_cost_breakdown(selected_id)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Internal", f"${breakdown['internal_personnel']:,.2f}")
        col2.metric("External Tooling", f"${breakdown['external_tooling']:,.2f}")
        col3.metric("Testing", f"${breakdown['testing']:,.2f}")
        col4.metric("Recovery", f"${breakdown['recovery']:,.2f}")
        st.markdown(f"### Total: ${breakdown['total']:,.2f}")

        st.divider()

        if is_admin:
            st.subheader("Add cost item")
            with st.form("add_cost_item_form"):
                cost_type = st.selectbox("Cost type:", ["External Tooling", "Testing", "Recovery"])
                amount = st.number_input("Amount ($):", value=0.0, format="%.2f", help="Use negative values for Recovery")
                description = st.text_input("Description:", placeholder="e.g., Annual Jira license")

                submitted = st.form_submit_button("Add Cost Item", type="primary")
                if submitted:
                    from models.cost_item import CostItem

                    create_cost_item(CostItem(topic_id=selected_id, cost_type=cost_type, amount=amount, description=description))
                    st.success("Cost item added!")
                    st.rerun()

            st.divider()
            st.subheader("Cost items for this topic")
            cost_items = get_cost_items_by_topic(selected_id)
            if cost_items:
                for item in cost_items:
                    col1, col2, col3 = st.columns([2, 2, 1])
                    col1.write(f"**{item.cost_type}** — {item.description or ''}")
                    col2.write(f"${item.amount:,.2f}")
                    with col3:
                        if st.button("Delete", key=f"delete_cost_{item.id}"):
                            delete_cost_item(item.id)
                            st.success("Cost item deleted!")
                            st.rerun()
            else:
                st.info("No cost items added yet.")
        else:
            st.warning("Only admins can add or edit cost items. Your role: " + st.session_state.user.role.value.capitalize())