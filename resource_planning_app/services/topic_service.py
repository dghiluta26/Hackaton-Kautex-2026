"""Service layer for Topic (project) CRUD operations.

This module will contain the functions used by the Topics page to talk
to the database. For now it only holds placeholders.
"""

from sqlmodel import select
from database.connection import get_session
from models.topic import Topic

def create_topic(topic: Topic) -> Topic:
    with get_session() as session:
        session.add(topic)
        session.commit()
        session.refresh(topic)
        return topic

def get_all_topics() -> list[Topic]:
    with get_session() as session:
        statement = select(Topic)
        return session.exec(statement).all()


def get_topic_by_id(topic_id: int) -> Topic | None:
    # TODO: return a single topic by id, or None if not found
    raise NotImplementedError


def update_topic(topic_id: int, updated_data: dict) -> Topic:
    """Updates an existing topic's fields in the database."""
    with get_session() as session:
        topic = session.get(Topic, topic_id)
        if not topic:
            raise ValueError(f"Topic with ID {topic_id} not found.")

        for key, value in updated_data.items():
            if hasattr(topic, key):
                setattr(topic, key, value)

        session.add(topic)
        session.commit()
        session.refresh(topic)
        return topic


def delete_topic(topic_id: int) -> None:
    """Deletes a topic from the database."""
    with get_session() as session:
        topic = session.get(Topic, topic_id)
        if topic:
            session.delete(topic)
            session.commit()
