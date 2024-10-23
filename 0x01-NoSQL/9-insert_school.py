#!/usr/bin/env python3
"""
Insert a new document in Python
"""


def insert_school(mongo_collection: Collection, **kwargs) -> str:
    """
    Inserts a new document into the MongoDB collection based on kwargs.
    
    :param mongo_collection: The pymongo collection object
    :param kwargs: The key-value pairs for the new document
    :return: The _id of the inserted document
    """
    result = mongo_collection.insert_one(kwargs)
    return str(result.inserted_id)
