"""Reusable calculation helpers for cost and utilization.

These functions are pure (no database access) so they are easy to test
and reuse across services and pages.
"""


def calculate_employee_topic_cost(
    available_hours: float, hourly_rate: float, allocation_percentage: float
) -> float:
    """Cost of an employee's time spent on a topic.

    cost = available_hours * hourly_rate * (allocation_percentage / 100)
    """
    return available_hours * hourly_rate * (allocation_percentage / 100)


def calculate_total_utilization(allocation_percentages: list[float]) -> float:
    """Sum of allocation percentages for an employee across all topics."""
    return sum(allocation_percentages)


def is_overallocated(total_utilization: float) -> bool:
    """An employee is overallocated when their total utilization exceeds 100%."""
    return total_utilization > 100


def calculate_total_topic_cost(
    employee_internal_cost: float,
    additional_internal_cost: float,
    external_cost: float,
    recovery: float,
) -> float:
    """Total cost of a topic minus any recovery/offset amount.

    total_cost = employee_internal_cost + additional_internal_cost + external_cost - recovery
    """
    return employee_internal_cost + additional_internal_cost + external_cost - recovery
