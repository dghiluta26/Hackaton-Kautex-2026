"""Import service: bulk-creates records from an uploaded CSV file.

Used by the Reports page's "Import Data" tab. Mirrors the column
conventions already used by the ad hoc CSV importers on the Employees and
Topics pages, plus a new Allocations importer.
"""

import io

import pandas as pd

from models.employee import Employee
from models.topic import Topic
from services.allocation_service import upsert_allocation
from services.employee_service import create_employee, get_all_employees
from services.topic_service import create_topic, get_all_topics


def import_employees_from_csv(file_content: bytes) -> dict:
    """Expected columns: name, available_hours_per_year (optional), hourly_rate, status (optional)."""
    try:
        df = pd.read_csv(io.BytesIO(file_content))
        df.columns = [str(col).strip().lower() for col in df.columns]

        if "name" not in df.columns:
            return {"success": False, "error": "Missing required column: name"}

        imported = 0
        errors = []
        for idx, row in df.iterrows():
            name = str(row.get("name", "")).strip()
            if not name or pd.isna(row.get("name")):
                errors.append(f"Row {idx + 1}: missing name, skipped")
                continue
            try:
                create_employee(
                    Employee(
                        name=name,
                        available_hours_per_year=float(row.get("available_hours_per_year", 1600) or 1600),
                        hourly_rate=float(row.get("hourly_rate", 0.0) or 0.0),
                        status=str(row.get("status", "Active")),
                    )
                )
                imported += 1
            except Exception as e:
                errors.append(f"Row {idx + 1}: {e}")

        return {"success": True, "imported": imported, "errors": errors, "total": len(df)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def import_topics_from_csv(file_content: bytes) -> dict:
    """Expected columns: name, category (optional), area (optional), status (optional),
    business_justification (optional)."""
    try:
        df = pd.read_csv(io.BytesIO(file_content))
        df.columns = [str(col).strip().lower() for col in df.columns]

        if "name" not in df.columns:
            return {"success": False, "error": "Missing required column: name"}

        imported = 0
        errors = []
        for idx, row in df.iterrows():
            name = str(row.get("name", "")).strip()
            if not name or pd.isna(row.get("name")):
                errors.append(f"Row {idx + 1}: missing name, skipped")
                continue
            try:
                create_topic(
                    Topic(
                        name=name,
                        category=str(row.get("category", "Unmapped")),
                        area=str(row.get("area", "")),
                        status=str(row.get("status", "Active")),
                        business_justification=str(row.get("business_justification", "")),
                    )
                )
                imported += 1
            except Exception as e:
                errors.append(f"Row {idx + 1}: {e}")

        return {"success": True, "imported": imported, "errors": errors, "total": len(df)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def import_allocations_from_csv(file_content: bytes) -> dict:
    """Expected columns: employee name, topic name, allocation % (0-100), comment (optional).

    Employees and Topics must already exist and are matched by exact name.
    """
    try:
        df = pd.read_csv(io.BytesIO(file_content))
        df.columns = [str(col).strip().lower() for col in df.columns]

        required = {"employee name", "topic name", "allocation %"}
        missing = required - set(df.columns)
        if missing:
            return {"success": False, "error": f"Missing columns: {', '.join(sorted(missing))}"}

        employees = get_all_employees()
        topics = get_all_topics()

        imported = 0
        errors = []
        for idx, row in df.iterrows():
            try:
                emp_name = str(row["employee name"]).strip()
                employee = next((e for e in employees if e.name == emp_name), None)
                if not employee:
                    errors.append(f"Row {idx + 1}: employee '{emp_name}' not found")
                    continue

                topic_name = str(row["topic name"]).strip()
                topic = next((t for t in topics if t.name == topic_name), None)
                if not topic:
                    errors.append(f"Row {idx + 1}: topic '{topic_name}' not found")
                    continue

                percentage = float(str(row["allocation %"]).rstrip("%"))
                if not (0 <= percentage <= 200):
                    errors.append(f"Row {idx + 1}: allocation % must be between 0-200")
                    continue

                comment = row.get("comment")
                comment = None if pd.isna(comment) else str(comment)

                upsert_allocation(employee.id, topic.id, percentage, comment)
                imported += 1
            except Exception as e:
                errors.append(f"Row {idx + 1}: {e}")

        return {"success": True, "imported": imported, "errors": errors, "total": len(df)}
    except Exception as e:
        return {"success": False, "error": str(e)}
