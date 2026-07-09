import pandas as pd
import io
from sqlmodel import Session
from services.employee_service import EmployeeService
from services.topic_service import TopicService
from services.allocation_service import AllocationService

class ImportService:
    """Service for importing data from Excel/CSV."""
    
    @staticmethod
    def import_employees_from_csv(session: Session, file_content: bytes) -> dict:
        """
        Import employees from CSV.
        
        Expected columns: Name, Location, Available Hours/Year (optional), Hourly Rate
        """
        try:
            df = pd.read_csv(io.BytesIO(file_content))
            
            # Validate columns
            required_cols = ['Name', 'Location', 'Hourly Rate']
            missing = [col for col in required_cols if col not in df.columns]
            if missing:
                return {"success": False, "error": f"Missing columns: {', '.join(missing)}"}
            
            imported = 0
            errors = []
            
            for idx, row in df.iterrows():
                try:
                    hours = int(row.get('Available Hours/Year', 1600))
                    rate = float(row['Hourly Rate'])
                    
                    EmployeeService.create_employee(
                        session,
                        name=row['Name'].strip(),
                        location=row['Location'].strip(),
                        available_hours_per_year=hours,
                        hourly_rate=rate
                    )
                    imported += 1
                except Exception as e:
                    errors.append(f"Row {idx+1}: {str(e)}")
            
            return {
                "success": True,
                "imported": imported,
                "errors": errors,
                "total": len(df)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def import_topics_from_csv(session: Session, file_content: bytes) -> dict:
        """
        Import topics from CSV.
        
        Expected columns: Name, Category, Business Justification
        """
        try:
            df = pd.read_csv(io.BytesIO(file_content))
            
            required_cols = ['Name', 'Category', 'Business Justification']
            missing = [col for col in required_cols if col not in df.columns]
            if missing:
                return {"success": False, "error": f"Missing columns: {', '.join(missing)}"}
            
            imported = 0
            errors = []
            
            for idx, row in df.iterrows():
                try:
                    TopicService.create_topic(
                        session,
                        name=row['Name'].strip(),
                        category=row['Category'].strip(),
                        business_justification=row['Business Justification'].strip()
                    )
                    imported += 1
                except Exception as e:
                    errors.append(f"Row {idx+1}: {str(e)}")
            
            return {
                "success": True,
                "imported": imported,
                "errors": errors,
                "total": len(df)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def import_allocations_from_csv(session: Session, file_content: bytes) -> dict:
        """
        Import allocations from CSV.
        
        Expected columns: Employee Name, Topic Name, Allocation %, Comment (optional)
        """
        try:
            df = pd.read_csv(io.BytesIO(file_content))
            
            required_cols = ['Employee Name', 'Topic Name', 'Allocation %']
            missing = [col for col in required_cols if col not in df.columns]
            if missing:
                return {"success": False, "error": f"Missing columns: {', '.join(missing)}"}
            
            imported = 0
            errors = []
            
            for idx, row in df.iterrows():
                try:
                    # Find employee
                    emp_name = row['Employee Name'].strip()
                    employees = EmployeeService.get_all_employees(session)
                    employee = next((e for e in employees if e.name == emp_name), None)
                    
                    if not employee:
                        errors.append(f"Row {idx+1}: Employee '{emp_name}' not found")
                        continue
                    
                    # Find topic
                    topic_name = row['Topic Name'].strip()
                    topics = TopicService.get_all_topics(session)
                    topic = next((t for t in topics if t.name == topic_name), None)
                    
                    if not topic:
                        errors.append(f"Row {idx+1}: Topic '{topic_name}' not found")
                        continue
                    
                    # Parse allocation
                    alloc_str = str(row['Allocation %']).rstrip('%')
                    allocation_pct = float(alloc_str) / 100.0
                    
                    if allocation_pct < 0 or allocation_pct > 1:
                        errors.append(f"Row {idx+1}: Allocation must be 0-100%")
                        continue
                    
                    comment = row.get('Comment', '')
                    
                    AllocationService.create_allocation(
                        session,
                        employee_id=employee.id,
                        topic_id=topic.id,
                        allocation_percentage=allocation_pct,
                        comment=comment
                    )
                    imported += 1
                except Exception as e:
                    errors.append(f"Row {idx+1}: {str(e)}")
            
            return {
                "success": True,
                "imported": imported,
                "errors": errors,
                "total": len(df)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
