"""Import all models here so SQLModel's metadata knows about every table
before create_db_and_tables() runs, no matter which entry point is used.
"""

from models.allocation import Allocation  # noqa: F401
from models.cost_item import CostItem  # noqa: F401
from models.department import Department  # noqa: F401
from models.employee import Employee  # noqa: F401
from models.location import Location  # noqa: F401
from models.team import Team  # noqa: F401
from models.topic import Topic  # noqa: F401
from models.user import User  # noqa: F401
