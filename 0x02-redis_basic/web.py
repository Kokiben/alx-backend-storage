#!/usr/bin/env python3
""" Web cache """

import redis
import requests
from typing import Optional

# Initialize Redis client
redis_client = redis.Redis()

def get_page(url: str) -> Optional[str]:
    """Fetches the page content from a URL and caches it with expiration."""
    
    # Check if the page content is cached
    cached_page = redis_client.get(f"page:{url}")
    
    if cached_page:
        # Page is cached, increment the count and return the cached page
        redis_client.incr(f"count:{url}")
        return cached_page.decode('utf-8')
    
    # If not cached, fetch the page content using requests
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful
        page_content = response.text
        
        # Cache the result with an expiration of 10 seconds
        redis_client.setex(f"page:{url}", 10, page_content)
        
        # Set the access count to 1
        redis_client.set(f"count:{url}", 1)
        
        return page_content
    
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

# Bonus: Decorator to implement caching and counting
def cache_page(func):
    def wrapper(url: str):
        return func(url)
    return wrapper

# Example usage:
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
    print(get_page(url))
