#!/usr/bin/env python3
""" Web cache module """

import redis
import requests
from typing import Callable
from functools import wraps

# Initialize Redis client
r = redis.Redis()

def cache_page_request(fn: Callable) -> Callable:
    """ Decorator wrapper to handle caching and counting """
    
    def cache_decorator(url: str) -> str:
        """ Wrapper for the decorated function """
        # Increment the access count for the URL
        r.incr(f"count:{url}")
        
        # Check if the response is cached
        cache = r.get(f"cached:{url}")
        if cache:
            return cache.decode('utf-8')
        
        # Call the actual function to get the page content
        page_content = fn(url)
        
        # Cache the result with an expiration time of 10 seconds
        r.setex(f"cached:{url}", 10, page_content)
        return page_content

    return cache_decorator

@cache_page_request
def get_page(url: str) -> str:
    """Fetches the HTML content of the specified URL."""
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.text

# Example usage
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
    print(get_page(url))
