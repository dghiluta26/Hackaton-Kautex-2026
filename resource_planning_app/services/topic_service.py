"""Service layer for Topic (project) CRUD operations.

This module will contain the functions used by the Topics page to talk
to the database. For now it only holds placeholders.
"""

from database.connection import get_session
from models.topic import Topic


def create_topic(topic: Topic) -> Topic:
    # TODO: add the topic to the database and return the created record
    raise NotImplementedError


def get_all_topics() -> list[Topic]:
    # TODO: return all topics from the database
    raise NotImplementedError


def get_topic_by_id(topic_id: int) -> Topic | None:
    # TODO: return a single topic by id, or None if not found
    raise NotImplementedError


def update_topic(topic_id: int, updated_data: dict) -> Topic:
    # TODO: update an existing topic's fields
    raise NotImplementedError


def delete_topic(topic_id: int) -> None:
    # TODO: delete a topic from the database
    raise NotImplementedError
