"""Topics page: manage topics/projects."""

import streamlit as st
import pandas as pd

from models.topic import Topic
from services.topic_service import create_topic, get_all_topics

# --- NEW IMPORTS FOR COSTS ---
from models.cost_item import CostItem
from services.cost_service import create_cost_item, get_cost_items_by_topic

st.title("Topics")
st.caption("View and manage topics/projects, their objectives and deliverables.")

# --- 1. Display Current Topics ---
st.subheader("Topic List")
all_topics = get_all_topics()

if len(all_topics) > 0:
    st.dataframe([topic.model_dump() for topic in all_topics], hide_index=True)
else:
    st.info("No topics found. Please upload a CSV below.")

st.divider()

# --- 2. The CSV Uploader ---
st.subheader("Mass Import Topics (CSV)")
st.caption("Required columns: name, category, area, status")

uploaded_file = st.file_uploader("Upload CSV", type="csv", key="topic_uploader")

if uploaded_file is not None:
    # Smart delimiter detection (Comma vs Semicolon) and BOM handling
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
            # Skip blank rows
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

st.divider()

# --- 3. Manage Individual Topic & Costs (Tabs Approach) ---
if len(all_topics) > 0:
    st.subheader("Manage Topic Details & Costs")

    # Select a topic to manage
    selected_topic_name = st.selectbox("Select a Project to Manage:", [t.name for t in all_topics])
    selected_topic = next((t for t in all_topics if t.name == selected_topic_name), None)

    if selected_topic:
        # Create the tabs
        tab1, tab2 = st.tabs(["📊 Project Details", "💰 Topic Costs"])

        # --- TAB 1: Project Editing UI ---
        with tab1:
            st.markdown(f"### Edit: {selected_topic.name}")

            # Import the new functions you just created
            from services.topic_service import update_topic, delete_topic

            with st.form(key=f"edit_topic_{selected_topic.id}"):
                col1, col2 = st.columns(2)

                with col1:
                    edit_name = st.text_input("Project Name", value=selected_topic.name)
                    edit_category = st.text_input("Category", value=selected_topic.category or "")
                    edit_area = st.text_input("Area", value=selected_topic.area or "")

                    # Safely handle the status dropdown
                    status_options = ["Active", "On Hold", "Completed", "Cancelled"]
                    current_status_index = status_options.index(
                        selected_topic.status) if selected_topic.status in status_options else 0
                    edit_status = st.selectbox("Status", options=status_options, index=current_status_index)

                with col2:
                    edit_objective = st.text_area("Objective", value=selected_topic.objective or "")
                    edit_business = st.text_area("Business Justification",
                                                 value=selected_topic.business_justification or "")
                    edit_deliverables = st.text_area("Deliverables", value=selected_topic.deliverables or "")
                    edit_description = st.text_area("Description", value=selected_topic.description or "")
                    edit_notes = st.text_area("Notes", value=selected_topic.notes or "")

                submit_update = st.form_submit_button("Save Changes", type="primary")

                if submit_update:
                    updated_data = {
                        "name": edit_name,
                        "category": edit_category,
                        "area": edit_area,
                        "status": edit_status,
                        "objective": edit_objective,
                        "business_justification": edit_business,
                        "deliverables": edit_deliverables,
                        "description": edit_description,
                        "notes": edit_notes
                    }
                    update_topic(selected_topic.id, updated_data)
                    st.success("Project details updated successfully!")
                    st.rerun()

            # Delete Button (Outside the form to prevent accidental submission)
            st.divider()
            if st.button("🗑️ Delete Project", type="secondary"):
                delete_topic(selected_topic.id)
                st.success(f"Project '{selected_topic.name}' deleted.")
                st.rerun()
        # --- TAB 2: Cost Manager ---
        with tab2:
            st.markdown(f"### Budget & Costs for: {selected_topic.name}")

            # Fetch existing costs for this specific project
            current_costs = get_cost_items_by_topic(selected_topic.id)

            if current_costs:
                # Map to match your team's CostItem schema (cost_type, amount, description)
                cost_data = [
                    {"Type": c.cost_type, "Description": c.description, "Amount": c.amount}
                    for c in current_costs
                ]
                st.dataframe(
                    pd.DataFrame(cost_data),
                    use_container_width=True,
                    hide_index=True,
                    column_config={"Amount": st.column_config.NumberColumn("Amount", format="$%.2f")}
                )

                # Show total
                total_budget = sum(c.amount for c in current_costs if c.amount is not None)
                st.metric("Total Topic Budget", f"${total_budget:,.2f}")
            else:
                st.info("No external or hardware costs logged for this project yet.")

            st.divider()

            # Form to add a new hardware expense
            st.markdown("**Log New Expense**")
            with st.form(key=f"add_cost_{selected_topic.id}", clear_on_submit=True):
                col1, col2 = st.columns([2, 1])
                with col1:
                    new_cost_type = st.text_input("Cost Type (e.g., External, Internal, Hardware)")
                    new_description = st.text_input("Description (Optional)")
                with col2:
                    new_amount = st.number_input("Amount ($)", min_value=0.0, step=10.0)

                submit_cost = st.form_submit_button("Add Expense", type="primary")

                if submit_cost and new_cost_type:
                    # Create the model instance using your team's schema fields
                    new_expense = CostItem(
                        topic_id=selected_topic.id,
                        cost_type=new_cost_type,
                        description=new_description,
                        amount=new_amount
                    )
                    create_cost_item(new_expense)
                    st.success(f"Added {new_cost_type} cost to the budget!")
                    st.rerun()