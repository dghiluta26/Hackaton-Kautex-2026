import streamlit as st
import pandas as pd
from sqlmodel import Session
from database.connection import engine
from services.export_service import ExportService
from services.import_service import ImportService
from utils.auth import is_admin

st.set_page_config(page_title="Reports", page_icon="📤", layout="wide")

st.title("📤 Reports & Data Management")
st.markdown("---")

# Check admin access
if not is_admin():
    st.warning("⚠️ Reports page requires Admin access. Your role: " + st.session_state.get("role", "Unknown"))
    st.stop()

# Tab layout
tab1, tab2, tab3 = st.tabs(["Export Data", "Import Data", "Report Generator"])

with tab1:
    st.subheader("📥 Export Data")
    st.markdown("Download your data in various formats for analysis and backup.")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 CSV Exports")
        
        with Session(engine) as session:
            if st.button("📥 Export Employees as CSV", use_container_width=True):
                data = ExportService.export_employees_csv(session)
                st.download_button(
                    label="⬇️ Download Employees.csv",
                    data=data,
                    file_name="employees.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            if st.button("📥 Export Topics as CSV", use_container_width=True):
                data = ExportService.export_topics_csv(session)
                st.download_button(
                    label="⬇️ Download Topics.csv",
                    data=data,
                    file_name="topics.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            if st.button("📥 Export Allocations as CSV", use_container_width=True):
                data = ExportService.export_allocations_csv(session)
                st.download_button(
                    label="⬇️ Download Allocations.csv",
                    data=data,
                    file_name="allocations.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    with col2:
        st.markdown("### 📊 Excel Exports")
        
        with Session(engine) as session:
            if st.button("📊 Generate Cost Report (Excel)", use_container_width=True):
                data = ExportService.export_cost_report_excel(session)
                st.download_button(
                    label="⬇️ Download Cost_Report.xlsx",
                    data=data,
                    file_name="cost_report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            if st.button("📊 Export Allocation Matrix (Excel)", use_container_width=True):
                data = ExportService.export_allocation_matrix_excel(session)
                st.download_button(
                    label="⬇️ Download Allocation_Matrix.xlsx",
                    data=data,
                    file_name="allocation_matrix.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
    
    st.markdown("---")
    st.info("💡 **Tips for Data Export:**\n"
            "- Use CSV for quick backups and data analysis\n"
            "- Use Excel for formatted reports with formulas\n"
            "- Allocation Matrix shows a heatmap view of all employee allocations")

with tab2:
    st.subheader("📤 Import Data")
    st.markdown("Bulk import employees, topics, and allocations from CSV files.")
    
    st.markdown("---")
    
    import_type = st.selectbox(
        "What would you like to import?",
        ["Employees", "Topics", "Allocations"]
    )
    
    st.markdown("---")
    
    if import_type == "Employees":
        st.markdown("### 📥 Import Employees")
        st.markdown("**Expected CSV columns:** Name, Location, Available Hours/Year (optional), Hourly Rate")
        
        uploaded_file = st.file_uploader("Upload CSV file", type="csv", key="emp_upload")
        
        if uploaded_file and st.button("⬆️ Import Employees", type="primary", use_container_width=True):
            with Session(engine) as session:
                result = ImportService.import_employees_from_csv(session, uploaded_file.getvalue())
                
                if result["success"]:
                    st.success(f"✅ Successfully imported {result['imported']} employee(s)!")
                    if result.get("errors"):
                        st.warning(f"⚠️ {len(result['errors'])} rows had errors:")
                        for error in result['errors'][:5]:
                            st.write(f"  • {error}")
                else:
                    st.error(f"❌ Import failed: {result['error']}")
    
    elif import_type == "Topics":
        st.markdown("### 📥 Import Topics")
        st.markdown("**Expected CSV columns:** Name, Category, Business Justification")
        
        uploaded_file = st.file_uploader("Upload CSV file", type="csv", key="topic_upload")
        
        if uploaded_file and st.button("⬆️ Import Topics", type="primary", use_container_width=True):
            with Session(engine) as session:
                result = ImportService.import_topics_from_csv(session, uploaded_file.getvalue())
                
                if result["success"]:
                    st.success(f"✅ Successfully imported {result['imported']} topic(s)!")
                    if result.get("errors"):
                        st.warning(f"⚠️ {len(result['errors'])} rows had errors:")
                        for error in result['errors'][:5]:
                            st.write(f"  • {error}")
                else:
                    st.error(f"❌ Import failed: {result['error']}")
    
    else:  # Allocations
        st.markdown("### 📥 Import Allocations")
        st.markdown("**Expected CSV columns:** Employee Name, Topic Name, Allocation %, Comment (optional)")
        st.warning("⚠️ Note: Employees and Topics must exist before importing allocations!")
        
        uploaded_file = st.file_uploader("Upload CSV file", type="csv", key="alloc_upload")
        
        if uploaded_file and st.button("⬆️ Import Allocations", type="primary", use_container_width=True):
            with Session(engine) as session:
                result = ImportService.import_allocations_from_csv(session, uploaded_file.getvalue())
                
                if result["success"]:
                    st.success(f"✅ Successfully imported {result['imported']} allocation(s)!")
                    if result.get("errors"):
                        st.warning(f"⚠️ {len(result['errors'])} rows had errors:")
                        for error in result['errors'][:5]:
                            st.write(f"  • {error}")
                else:
                    st.error(f"❌ Import failed: {result['error']}")
    
    st.markdown("---")
    st.info("💡 **Tips for Data Import:**\n"
            "- Make sure CSV file has correct column names\n"
            "- For Allocations: Employee and Topic names must match exactly\n"
            "- Allocation % must be between 0-100")

with tab3:
    st.subheader("📊 Report Generator")
    st.markdown("Generate comprehensive reports and visualizations.")
    
    with Session(engine) as session:
        from services.employee_service import EmployeeService
        from services.topic_service import TopicService
        from utils.calculations import CostCalculator, ReportGenerator
        import plotly.graph_objects as go
        
        employees = EmployeeService.get_all_employees(session)
        topics = TopicService.get_all_topics(session)
        metrics = CostCalculator.get_global_totals(session)
        
        st.markdown("---")
        st.markdown("### 📈 Global Metrics")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Cost", f"${metrics['total_cost']:,.2f}")
        with col2:
            st.metric("Total Headcount", metrics['total_headcount'])
        with col3:
            st.metric("Avg Cost/Employee", f"${metrics['average_cost_per_employee']:,.2f}")
        
        st.markdown("---")
        st.markdown("### 💰 Cost Distribution by Topic")
        
        topic_costs = []
        for topic in topics:
            cost = CostCalculator.get_topic_total_cost(session, topic.id)
            topic_costs.append({
                "Topic": topic.name,
                "Internal": cost['internal_personnel'],
                "External": cost['external_tooling'] + cost['testing'],
                "Recovery": abs(cost['recovery']),
                "Total": cost['total']
            })
        
        if topic_costs:
            df_costs = pd.DataFrame(topic_costs)
            
            fig = go.Figure(data=[
                go.Bar(name='Internal', x=df_costs['Topic'], y=df_costs['Internal']),
                go.Bar(name='External', x=df_costs['Topic'], y=df_costs['External']),
                go.Bar(name='Recovery', x=df_costs['Topic'], y=-df_costs['Recovery'])
            ])
            fig.update_layout(
                barmode='stack',
                title="Cost Distribution",
                xaxis_title="Topic",
                yaxis_title="Cost ($)",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            st.markdown("### 📋 Cost Breakdown Table")
            df_display = df_costs.copy()
            for col in ['Internal', 'External', 'Recovery', 'Total']:
                df_display[col] = df_display[col].apply(lambda x: f"${x:,.2f}")
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        else:
            st.info("No topics created yet.")
        
        st.markdown("---")
        st.markdown("### ⚠️ High-Cost Projects")
        
        high_cost = ReportGenerator.get_high_cost_topics(session, threshold_percentage=0.3)
        if high_cost:
            for i, topic_info in enumerate(high_cost):
                with st.expander(
                    f"📌 {topic_info['name']} - {topic_info['external_ratio']*100:.1f}% External",
                    expanded=(i==0)
                ):
                    st.write(f"**Category:** {topic_info['category']}")
                    st.write(f"**Business Justification:**\n{topic_info['business_justification']}")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Cost", f"${topic_info['total_cost']:,.2f}")
                    with col2:
                        st.metric("External Cost", f"${topic_info['external_cost']:,.2f}")
                    with col3:
                        st.metric("External %", f"{topic_info['external_ratio']*100:.1f}%")
        else:
            st.info("✅ All projects have reasonable external cost ratios")

st.markdown("---")
st.markdown("**Role:** Admin — Full access to reports and import/export features")
