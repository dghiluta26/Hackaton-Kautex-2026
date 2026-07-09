from sqlmodel import Session
from database.connection import engine, create_db_and_tables
from models.employee import Employee
from models.topic import Topic
from models.allocation import Allocation
from models.cost_item import CostItem

def initialize_database():
    """Initialize database with seed data."""
    create_db_and_tables()
    
    # Seed data: Initial Topics/Categories
    with Session(engine) as session:
        # Check if data already exists
        existing_topics = session.query(Topic).count()
        if existing_topics == 0:
            # Create initial topics based on the CSV structure
            topics = [
                Topic(
                    name="Internal Efforts CI Non-bookable",
                    category="Internal Efforts",
                    business_justification="Core internal CI/CD infrastructure maintenance"
                ),
                Topic(
                    name="Internal Efforts CI Bookable 1",
                    category="Internal Efforts",
                    business_justification="Billable internal CI/CD development work"
                ),
                Topic(
                    name="Internal D Projects 1",
                    category="Internal Efforts",
                    business_justification="Internal development projects and research"
                ),
                Topic(
                    name="Customer Request",
                    category="Customer Request",
                    business_justification="Client-specific project deliverables"
                ),
                Topic(
                    name="Allegro D-Project 1",
                    category="Allegro",
                    business_justification="Allegro platform development initiative"
                ),
                Topic(
                    name="Pentatonic D-Project 1",
                    category="Pentatonic",
                    business_justification="Pentatonic framework development"
                ),
                Topic(
                    name="Agentic AI and LLM-Powered Enterprise Solutions",
                    category="Internal Efforts",
                    business_justification="AI/LLM integration and report generation with DEVOPS"
                ),
            ]
            session.add_all(topics)
            session.commit()
