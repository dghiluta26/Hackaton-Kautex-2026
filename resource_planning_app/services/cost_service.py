"""Service layer for CostItem CRUD operations and cost aggregation.

Used by the Topics page (per-topic cost items) and the Reports page
(executive report generator).
"""
from __future__ import annotations
from sqlmodel import select

from database.connection import get_session
from models.allocation import Allocation
from models.cost_item import CostItem
from models.employee import Employee
from models.topic import Topic
from utils.calculations import calculate_employee_topic_cost


def create_cost_item(cost_item: CostItem) -> CostItem:
    with get_session() as session:
        session.add(cost_item)
        session.commit()
        session.refresh(cost_item)
        return cost_item


def get_all_cost_items() -> list[CostItem]:
    with get_session() as session:
        return session.exec(select(CostItem)).all()


def get_cost_items_by_topic(topic_id: int) -> list[CostItem]:
    with get_session() as session:
        statement = select(CostItem).where(CostItem.topic_id == topic_id)
        return session.exec(statement).all()


def update_cost_item(cost_item_id: int, updated_data: dict) -> CostItem | None:
    with get_session() as session:
        cost_item = session.get(CostItem, cost_item_id)
        if cost_item is None:
            return None
        for key, value in updated_data.items():
            setattr(cost_item, key, value)
        session.add(cost_item)
        session.commit()
        session.refresh(cost_item)
        return cost_item


def delete_cost_item(cost_item_id: int) -> None:
    with get_session() as session:
        cost_item = session.get(CostItem, cost_item_id)
        if cost_item is not None:
            session.delete(cost_item)
            session.commit()


def _empty_breakdown() -> dict:
    return {"internal_personnel": 0.0, "external_tooling": 0.0, "testing": 0.0, "recovery": 0.0, "total": 0.0}


def get_all_topic_cost_breakdowns() -> dict[int, dict]:
    """Cost breakdown for every topic, computed with a single round trip per table.

    Building this per-topic (one query per topic) turns into N+1 network calls
    against Supabase, which is slow. This fetches allocations+employees and cost
    items once, then aggregates in Python.
    """
    with get_session() as session:
        topics = session.exec(select(Topic)).all()
        alloc_rows = session.exec(
            select(Allocation, Employee).where(Allocation.employee_id == Employee.id)
        ).all()
        cost_items = session.exec(select(CostItem)).all()

    breakdowns = {topic.id: _empty_breakdown() for topic in topics}

    for alloc, emp in alloc_rows:
        breakdown = breakdowns.get(alloc.topic_id)
        if breakdown is None:
            continue
        breakdown["internal_personnel"] += calculate_employee_topic_cost(
            emp.available_hours_per_year, emp.hourly_rate, alloc.allocation_percentage
        )

    for item in cost_items:
        breakdown = breakdowns.get(item.topic_id)
        if breakdown is None:
            continue
        if item.cost_type == "External Tooling":
            breakdown["external_tooling"] += item.amount
        elif item.cost_type == "Testing":
            breakdown["testing"] += item.amount
        elif item.cost_type == "Recovery":
            breakdown["recovery"] += item.amount

    for breakdown in breakdowns.values():
        breakdown["total"] = (
            breakdown["internal_personnel"] + breakdown["external_tooling"] + breakdown["testing"] + breakdown["recovery"]
        )

    return breakdowns


def get_topic_cost_breakdown(topic_id: int) -> dict:
    """Full cost breakdown for a single topic: internal personnel time plus external cost items.

    total = internal_personnel + external_tooling + testing + recovery
    (recovery is typically entered as a negative amount, offsetting the total)
    """
    with get_session() as session:
        alloc_statement = select(Allocation, Employee).where(
            (Allocation.topic_id == topic_id) & (Allocation.employee_id == Employee.id)
        )
        internal_personnel = sum(
            calculate_employee_topic_cost(emp.available_hours_per_year, emp.hourly_rate, alloc.allocation_percentage)
            for alloc, emp in session.exec(alloc_statement).all()
        )

        cost_items = session.exec(select(CostItem).where(CostItem.topic_id == topic_id)).all()
        external_tooling = sum(c.amount for c in cost_items if c.cost_type == "External Tooling")
        testing = sum(c.amount for c in cost_items if c.cost_type == "Testing")
        recovery = sum(c.amount for c in cost_items if c.cost_type == "Recovery")

    return {
        "internal_personnel": internal_personnel,
        "external_tooling": external_tooling,
        "testing": testing,
        "recovery": recovery,
        "total": internal_personnel + external_tooling + testing + recovery,
    }


def get_global_cost_totals(breakdowns: dict[int, dict] | None = None) -> dict:
    """Global cost and headcount metrics across every topic."""
    if breakdowns is None:
        breakdowns = get_all_topic_cost_breakdowns()

    with get_session() as session:
        employee_ids = session.exec(select(Allocation.employee_id).distinct()).all()

    total_cost = sum(b["total"] for b in breakdowns.values())
    total_headcount = len(set(employee_ids))

    return {
        "total_cost": total_cost,
        "total_headcount": total_headcount,
        "average_cost_per_employee": total_cost / total_headcount if total_headcount > 0 else 0,
    }


def get_high_cost_topics(threshold_percentage: float = 0.3, breakdowns: dict[int, dict] | None = None) -> list[dict]:
    """Topics whose external costs (tooling + testing + recovery) exceed the given
    share of their total cost, sorted by that share descending.
    """
    if breakdowns is None:
        breakdowns = get_all_topic_cost_breakdowns()

    with get_session() as session:
        topics = session.exec(select(Topic)).all()

    high_cost_topics = []
    for topic in topics:
        breakdown = breakdowns.get(topic.id, _empty_breakdown())
        external_total = breakdown["external_tooling"] + breakdown["testing"] + breakdown["recovery"]
        external_ratio = external_total / breakdown["total"] if breakdown["total"] > 0 else 0

        if external_ratio > threshold_percentage:
            high_cost_topics.append(
                {
                    "name": topic.name,
                    "category": topic.category,
                    "business_justification": topic.business_justification,
                    "total_cost": breakdown["total"],
                    "external_cost": external_total,
                    "external_ratio": external_ratio,
                    "cost_breakdown": breakdown,
                }
            )

    return sorted(high_cost_topics, key=lambda x: x["external_ratio"], reverse=True)
