import pandas as pd
import io
from sqlmodel import Session, select
from models.employee import Employee
from models.topic import Topic
from models.allocation import Allocation
from models.cost_item import CostItem
from utils.calculations import CostCalculator
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows

class ExportService:
    """Service for exporting data to various formats."""
    
    @staticmethod
    def export_employees_csv(session: Session) -> bytes:
        """Export employees to CSV."""
        stmt = select(Employee)
        employees = session.exec(stmt).all()
        
        df = pd.DataFrame([
            {
                'ID': e.id,
                'Name': e.name,
                'Location': e.location,
                'Available Hours/Year': e.available_hours_per_year,
                'Hourly Rate': e.hourly_rate
            }
            for e in employees
        ])
        
        return df.to_csv(index=False).encode()
    
    @staticmethod
    def export_topics_csv(session: Session) -> bytes:
        """Export topics to CSV."""
        stmt = select(Topic)
        topics = session.exec(stmt).all()
        
        df = pd.DataFrame([
            {
                'ID': t.id,
                'Name': t.name,
                'Category': t.category,
                'Business Justification': t.business_justification
            }
            for t in topics
        ])
        
        return df.to_csv(index=False).encode()
    
    @staticmethod
    def export_allocations_csv(session: Session) -> bytes:
        """Export allocations to CSV."""
        stmt = select(Allocation, Employee, Topic).where(
            (Allocation.employee_id == Employee.id) &
            (Allocation.topic_id == Topic.id)
        )
        results = session.exec(stmt).all()
        
        df = pd.DataFrame([
            {
                'Employee': f"{r[1].name} ({r[1].location})",
                'Topic': r[2].name,
                'Allocation %': f"{r[0].allocation_percentage*100:.1f}%",
                'Allocated Hours': f"{r[1].available_hours_per_year * r[0].allocation_percentage:.0f}",
                'Cost': f"${r[1].available_hours_per_year * r[0].allocation_percentage * r[1].hourly_rate:,.2f}",
                'Comment': r[0].comment
            }
            for r in results
        ])
        
        return df.to_csv(index=False).encode()
    
    @staticmethod
    def export_cost_report_excel(session: Session) -> bytes:
        """Export comprehensive cost report to Excel."""
        wb = Workbook()
        
        # Summary sheet
        ws_summary = wb.active
        ws_summary.title = "Summary"
        
        metrics = CostCalculator.get_global_totals(session)
        
        ws_summary['A1'] = "Kautex Resource & Cost Planning - Summary Report"
        ws_summary['A1'].font = Font(size=14, bold=True)
        
        ws_summary['A3'] = "Total Cost:"
        ws_summary['B3'] = metrics['total_cost']
        ws_summary['A4'] = "Total Headcount:"
        ws_summary['B4'] = metrics['total_headcount']
        ws_summary['A5'] = "Avg Cost/Employee:"
        ws_summary['B5'] = metrics['average_cost_per_employee']
        
        # Topics sheet
        ws_topics = wb.create_sheet("Topics")
        topics = session.exec(select(Topic)).all()
        
        headers = ['Topic', 'Category', 'Internal Cost', 'External Tooling', 'Testing', 'Recovery', 'Total Cost']
        ws_topics.append(headers)
        
        for topic in topics:
            cost = CostCalculator.get_topic_total_cost(session, topic.id)
            ws_topics.append([
                topic.name,
                topic.category,
                cost['internal_personnel'],
                cost['external_tooling'],
                cost['testing'],
                cost['recovery'],
                cost['total']
            ])
        
        # Allocations sheet
        ws_alloc = wb.create_sheet("Allocations")
        allocations = session.exec(select(Allocation, Employee, Topic).where(
            (Allocation.employee_id == Employee.id) &
            (Allocation.topic_id == Topic.id)
        )).all()
        
        headers = ['Employee', 'Location', 'Topic', 'Allocation %', 'Allocated Hours', 'Cost', 'Comment']
        ws_alloc.append(headers)
        
        for alloc, emp, topic in allocations:
            hours = emp.available_hours_per_year * alloc.allocation_percentage
            cost = hours * emp.hourly_rate
            ws_alloc.append([
                emp.name,
                emp.location,
                topic.name,
                f"{alloc.allocation_percentage*100:.1f}%",
                f"{hours:.0f}",
                f"${cost:,.2f}",
                alloc.comment
            ])
        
        # Format sheets
        for ws in [ws_summary, ws_topics, ws_alloc]:
            for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
                for cell in row:
                    cell.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
        
        output = io.BytesIO()
        wb.save(output)
        return output.getvalue()
    
    @staticmethod
    def export_allocation_matrix_excel(session: Session) -> bytes:
        """Export allocation matrix as Excel heatmap."""
        employees = session.exec(select(Employee)).all()
        topics = session.exec(select(Topic)).all()
        
        matrix_data = []
        for emp in employees:
            row = {"Employee": f"{emp.name}\n({emp.location})", "Hourly Rate": emp.hourly_rate}
            for topic in topics:
                allocation = session.exec(
                    select(Allocation).where(
                        (Allocation.employee_id == emp.id) &
                        (Allocation.topic_id == topic.id)
                    )
                ).first()
                row[topic.name] = allocation.allocation_percentage * 100 if allocation else 0
            
            total_alloc = sum(row.get(t.name, 0) for t in topics)
            row["Total %"] = total_alloc
            matrix_data.append(row)
        
        df = pd.DataFrame(matrix_data)
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Allocation Matrix"
        
        for r_idx, r in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
            for c_idx, value in enumerate(r, 1):
                cell = ws.cell(row=r_idx, column=c_idx, value=value)
                if r_idx == 1:
                    cell.font = Font(bold=True, color="FFFFFF")
                    cell.fill = PatternFill(start_color="1f77b4", end_color="1f77b4", fill_type="solid")
        
        output = io.BytesIO()
        wb.save(output)
        return output.getvalue()
