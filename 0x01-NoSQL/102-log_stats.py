#!/usr/bin/env python3
"""
Nginx logs statistics from MongoDB with top 10 most present IPs.
"""

from pymongo import MongoClient


def log_stats():
    """
    Provides statistics about Nginx logs stored in MongoDB, including:
    - Total number of logs
    - Count of logs for each HTTP method (GET, POST, PUT, PATCH, DELETE)
    - Count of GET requests to the "/status" path
    - Top 10 most present IPs
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

    # Get the top 10 most present IPs
    top_ips = collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},  # Sort by count in descending order
        {"$limit": 10}  # Limit to top 10 IPs
    ])

    # Display results
    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")
    print(f"{get_status_count} status check")

    # Print the top 10 IPs
    print("IPs:")
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")

if __name__ == "__main__":
    log_stats()
