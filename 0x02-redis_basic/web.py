#!/usr/bin/env python3
"""
Web module to cache page content and track access count
"""

import redis
import requests
from typing import Callable
from functools import wraps


r = redis.Redis()

def cache_with_expiry(expiry: int) -> Callable:
    """Decorator to cache the result of a function in Redis with an expiry time"""
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(url: str, *args, **kwargs) -> str:
            # Create Redis key for caching the URL content
            cache_key = f"cached:{url}"

            # Try to retrieve the cached data
            cached_page = r.get(cache_key)
            if cached_page:
                # If cached content is available, return it
                return cached_page.decode('utf-8')

            # Otherwise, call the actual method to get the page
            result = method(url, *args, **kwargs)

            # Cache the result and set an expiration time
            r.setex(cache_key, expiry, result)
            
            return result
        return wrapper
    return decorator


@cache_with_expiry(10)  # Cache the page for 10 seconds
def get_page(url: str) -> str:
    """Fetch the HTML content of a URL and track access count"""
    # Increment the count for the number of times the URL was accessed
    count_key = f"count:{url}"
    r.incr(count_key)

    # Fetch the page content
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    # Example usage with a slow URL
    slow_url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
    
    # First call (fetches the page and caches it)
    print(get_page(slow_url))
    
    # Second call (returns cached result)
    print(get_page(slow_url))

    # To check how many times the URL was accessed
    print(f"URL {slow_url} accessed {r.get(f'count:{slow_url}').decode('utf-8')} times.")
