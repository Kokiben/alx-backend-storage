#!/usr/bin/env python3
"""
Return all students sorted by average score.
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by their average score.

    :param mongo_collection: The pymongo collection object.
    :return: A list of students sorted by average score, each with a key.
    """
    # MongoDB aggregation pipeline
    pipeline = [
        {
            "$addFields": {  # Calculate average score for each student
                "averageScore": { "$avg": "$scores" }
            }
        },
        {
            "$sort": { "averageScore": -1 }
        }
    ]
    
    # Aggregate and return the result
    return list(mongo_collection.aggregate(pipeline))
