#!/usr/bin/env python3
"""
Retrieve all documents in Python
"""

def list_all(mongo_collection):
    """
    Retrieves all documents from a MongoDB collection.
    
    :param mongo_collection: The pymongo collection object
    :return: A list of documents, or an empty list if no documents are present
    """
    return list(mongo_collection.find())
