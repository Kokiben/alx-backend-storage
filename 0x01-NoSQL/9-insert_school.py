#!/usr/bin/env python3
"""
Add a new document to a collection using keyword arguments.
"""


def insert_school(mongo_collection, **kwargs):
    """
    Adds a n document to MongoDB collection based on provided keyword arg.

    :param mongo_collection: The pymongo collection object.
    :param kwargs: The key-value pairs representing the new document.
    :return: The _id of the newly inserted document.
    """
    n_dcmnt = mongo_collection.insert_one(kwargs)
    return n_dcmnt.inserted_id
