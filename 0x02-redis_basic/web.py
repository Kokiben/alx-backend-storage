#!/usr/bin/env python3
""" Expiring web cache module """

import redis
import requests
from typing import Callable
from functools import wraps

# Connect to Redis
redis_client = redis.Redis()

def wrap_requests(fn: Callable) -> Callable:
    """Decorator wrapper for caching responses and counting accesses."""

    @wraps(fn)
    def wrapper(url: str) -> str:
        """Wrapper that increments access count and manages caching."""
        
        # Increment the access count for the URL
        redis_client.incr(f"count:{url}")

        # Check if a cached response exists
        cached_response = redis_client.get(f"cached:{url}")
        
        # Return cached response if available
        if cached_response is not None:
            return cached_response.decode('utf-8')

        # Call the original function to fetch the response
        result = fn(url)
        
        # Cache the result with a 10-second expiration time
        redis_client.setex(f"cached:{url}", 10, result)
        
        return result

    return wrapper

@wrap_requests
def get_page(url: str) -> str:
    """Fetches HTML content from the specified URL."""
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.text
