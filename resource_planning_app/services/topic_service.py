from sqlmodel import Session, select
from models.topic import Topic
from typing import List, Optional

class TopicService:
    """Service for Topic (Project) CRUD operations."""
    
    @staticmethod
    def create_topic(session: Session, name: str, category: str, business_justification: str = "") -> Topic:
        """Create a new topic/project."""
        topic = Topic(
            name=name,
            category=category,
            business_justification=business_justification
        )
        session.add(topic)
        session.commit()
        session.refresh(topic)
        return topic
    
    @staticmethod
    def get_all_topics(session: Session) -> List[Topic]:
        """Get all topics."""
        stmt = select(Topic).order_by(Topic.category, Topic.name)
        return session.exec(stmt).all()
    
    @staticmethod
    def get_topic_by_id(session: Session, topic_id: int) -> Optional[Topic]:
        """Get topic by ID."""
        return session.get(Topic, topic_id)
    
    @staticmethod
    def get_topics_by_category(session: Session, category: str) -> List[Topic]:
        """Get all topics for a category."""
        stmt = select(Topic).where(Topic.category == category).order_by(Topic.name)
        return session.exec(stmt).all()
    
    @staticmethod
    def update_topic(session: Session, topic_id: int, **kwargs) -> Optional[Topic]:
        """Update topic by ID."""
        topic = session.get(Topic, topic_id)
        if topic:
            for key, value in kwargs.items():
                if hasattr(topic, key):
                    setattr(topic, key, value)
            session.add(topic)
            session.commit()
            session.refresh(topic)
        return topic
    
    @staticmethod
    def delete_topic(session: Session, topic_id: int) -> bool:
        """Delete topic by ID."""
        topic = session.get(Topic, topic_id)
        if topic:
            session.delete(topic)
            session.commit()
            return True
        return False
