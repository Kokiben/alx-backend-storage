#!/usr/bin/env python3
"""
Find schools by a specific topic in MongoDB.
"""


def schools_by_topic(mongo_collection, topic: str) -> list:
    """
    Returns the list of schools that have a specific topic.

    :param mongo_collection: The pymongo collection object.
    :param topic: The topic to search for.
    :return: A list of schools with the specified topic.
    """
    return list(mongo_collection.find({ "topics": topic }))
