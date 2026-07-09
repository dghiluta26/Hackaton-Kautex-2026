import streamlit as st
import pandas as pd
from sqlmodel import Session
from database.connection import engine
from services.topic_service import TopicService
from services.cost_service import CostService
from utils.calculations import CostCalculator

st.set_page_config(page_title="Topics", page_icon="📌", layout="wide")

st.title("📌 Project & Topic Management")
st.markdown("---")

# Check if admin
is_admin = st.session_state.get("role") == "Admin"

with Session(engine) as session:
    # Tab layout
    tab1, tab2, tab3 = st.tabs(["View Topics", "Add Topic", "Manage Costs"])
    
    with tab1:
        st.subheader("📋 All Topics")
        
        topics = TopicService.get_all_topics(session)
        
        if topics:
            # Group by category
            categories = sorted(set(t.category for t in topics))
            
            for category in categories:
                st.markdown(f"### {category}")
                
                category_topics = [t for t in topics if t.category == category]
                
                for topic in category_topics:
                    with st.expander(f"📌 {topic.name}", expanded=False):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"**Business Justification:**\n\n{topic.business_justification}")
                        
                        with col2:
                            cost_breakdown = CostCalculator.get_topic_total_cost(session, topic.id)
                            st.metric("Total Cost", f"${cost_breakdown['total']:,.2f}")
                        
                        # Cost items
                        cost_items = CostService.get_cost_items_by_topic(session, topic.id)
                        if cost_items:
                            st.markdown("**Cost Items:**")
                            df_costs = pd.DataFrame([
                                {
                                    'Type': item.cost_type,
                                    'Amount': f"${item.amount:,.2f}",
                                    'Description': item.description
                                }
                                for item in cost_items
                            ])
                            st.dataframe(df_costs, use_container_width=True, hide_index=True)
                        
                        if is_admin:
                            # Edit/Delete buttons
                            col1, col2 = st.columns(2)
                            with col1:
                                # MODIFICARE: Am schimbat key în f"btn_edit_{topic.id}" ca să nu mai existe conflict
                                if st.button("✏️ Edit", key=f"btn_edit_{topic.id}"):
                                    st.session_state[f"edit_topic_{topic.id}"] = True
                                    st.rerun()  # Forțează o reîmprospătare ca să apară căsuța de editare instant
                            with col2:
                                if st.button("🗑️ Delete", key=f"delete_topic_{topic.id}"):
                                    TopicService.delete_topic(session, topic.id)
                                    st.success("✅ Topic deleted!")
                                    st.rerun()
        else:
            st.info("No topics found. Create one using the 'Add Topic' tab.")
    
    with tab2:
        if is_admin:
            st.subheader("➕ Add New Topic")
            
            with st.form("add_topic_form"):
                name = st.text_input(
                    "Topic Name:",
                    placeholder="e.g., Customer Request - Project X"
                )
                
                category = st.selectbox(
                    "Category:",
                    ["Internal Efforts", "Customer Request", "Allegro", "Pentatonic", "Other"]
                )
                
                business_justification = st.text_area(
                    "Business Justification:",
                    placeholder="Explain why this project is needed and its strategic value...",
                    height=150
                )
                
                submitted = st.form_submit_button("➕ Add Topic", type="primary")
                
                if submitted:
                    if not name or not business_justification:
                        st.error("❌ Name and Business Justification are required!")
                    else:
                        try:
                            TopicService.create_topic(
                                session,
                                name=name,
                                category=category,
                                business_justification=business_justification
                            )
                            st.success("✅ Topic added successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
        else:
            current_user = st.session_state.get("current_user", {})
            role = current_user.get("role", "Unknown")
            st.warning(f"📌 Only admins can add topics. Current role: {role}")
    
    with tab3:
        st.subheader("💰 Manage Cost Items")
        
        topics = TopicService.get_all_topics(session)
        
        if not topics:
            st.info("No topics available. Create a topic first.")
        else:
            selected_topic_id = st.selectbox(
                "Select Topic:",
                options=[t.id for t in topics],
                format_func=lambda tid: next(t.name for t in topics if t.id == tid)
            )
            
            selected_topic = TopicService.get_topic_by_id(session, selected_topic_id)
            
            if selected_topic:
                st.markdown(f"**Topic:** {selected_topic.name}")
                st.markdown(f"**Category:** {selected_topic.category}")
                
                # Display current costs
                cost_breakdown = CostCalculator.get_topic_total_cost(session, selected_topic_id)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Internal", f"${cost_breakdown['internal_personnel']:,.2f}")
                with col2:
                    st.metric("External Tooling", f"${cost_breakdown['external_tooling']:,.2f}")
                with col3:
                    st.metric("Testing", f"${cost_breakdown['testing']:,.2f}")
                with col4:
                    st.metric("Recovery", f"${cost_breakdown['recovery']:,.2f}")
                
                st.markdown(f"### Total: ${cost_breakdown['total']:,.2f}")
                
                st.markdown("---")
                
                if is_admin:
                    # Add cost item
                    st.subheader("➕ Add Cost Item")
                    
                    with st.form("add_cost_item_form"):
                        cost_type = st.selectbox(
                            "Cost Type:",
                            ["External Tooling", "Testing", "Recovery"]
                        )
                        
                        amount = st.number_input(
                            "Amount ($):",
                            value=0.0,
                            format="%.2f",
                            help="Use negative values for Recovery"
                        )
                        
                        description = st.text_input(
                            "Description:",
                            placeholder="e.g., Annual Jira license"
                        )
                        
                        submitted = st.form_submit_button("➕ Add Cost", type="primary")
                        
                        if submitted:
                            try:
                                CostService.create_cost_item(
                                    session,
                                    topic_id=selected_topic_id,
                                    cost_type=cost_type,
                                    amount=amount,
                                    description=description
                                )
                                st.success("✅ Cost item added!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                    
                    st.markdown("---")
                    
                    # Display and delete cost items
                    st.subheader("📋 Cost Items for this Topic")
                    cost_items = CostService.get_cost_items_by_topic(session, selected_topic_id)
                    
                    if cost_items:
                        for item in cost_items:
                            col1, col2, col3 = st.columns([2, 2, 1])
                            with col1:
                                st.write(f"**{item.cost_type}** - {item.description}")
                            with col2:
                                st.write(f"${item.amount:,.2f}")
                            with col3:
                                if st.button("🗑️", key=f"delete_cost_{item.id}"):
                                    CostService.delete_cost_item(session, item.id)
                                    st.success("✅ Cost item deleted!")
                                    st.rerun()
                    else:
                        st.info("No cost items added yet.")
                else:
                    current_user = st.session_state.get("current_user", {})
                    role = current_user.get("role", "Unknown")
                    st.warning(f"📌 Only admins can add/edit costs. Current role: {role}")

st.markdown("---")
current_user = st.session_state.get("current_user", {})
role = current_user.get("role", "Unknown")
st.markdown(f"**Role:** {role} — {'Full CRUD access' if is_admin else 'Read-only access'}")
