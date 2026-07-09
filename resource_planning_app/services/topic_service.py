"""Service layer for Topic (project) CRUD operations.

This module will contain the functions used by the Topics page to talk
to the database. For now it only holds placeholders.
"""
from __future__ import annotations
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
    with get_session() as session:
        return session.get(Topic, topic_id)


def update_topic(topic_id: int, updated_data: dict) -> Topic | None:
    with get_session() as session:
        topic = session.get(Topic, topic_id)
        if topic is None:
            return None
        for key, value in updated_data.items():
            setattr(topic, key, value)
        session.add(topic)
        session.commit()
        session.refresh(topic)
        return topic


def delete_topic(topic_id: int) -> None:
    with get_session() as session:
        topic = session.get(Topic, topic_id)
        if topic is not None:
            session.delete(topic)
            session.commit()
