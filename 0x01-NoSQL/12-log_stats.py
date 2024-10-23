#!/usr/bin/env python3
"""
Nginx logs statistics from MongoDB.
"""

from pymongo import MongoClient

def log_stats():
    """
    Provides statistics about Nginx logs stored in MongoDB.
    Displays:
    - Total number of logs
    - Count of logs for each HTTP method (GET, POST, PUT, PATCH, DELETE)
    - Count of GET requests to the "/status" path
    """
    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017/')
    db = client.logs
    collection = db.nginx

    # Get the total number of logs
    total_logs = collection.count_documents({})

    # Count documents with each HTTP method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: collection.count_documents({"method": method}) for method in methods}

    # Count the number of GET requests to the "/status" path
    get_status_count = collection.count_documents({"method": "GET", "path": "/status"})

    # Display results
    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")
    print(f"{get_status_count} status check")

if __name__ == "__main__":
    log_stats()
