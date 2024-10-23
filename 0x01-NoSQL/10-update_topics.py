#!/usr/bin/env python3
"""
Update topics of a school document in MongoDB based on the school name.
"""


def update_topics(mongo_collection, name: str, topics: list) -> None:
    """
    Changes all topics of a school document based on the school name.

    :param mongo_collection: The pymongo collection object.
    :param name: The name of the school to update.
    :param topics: The list of topics to set for the school.
    :return: None
    """
    mongo_collection.update_many(
        { "name": name },
        { "$set": { "topics": topics } }
    )
