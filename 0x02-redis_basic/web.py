#!/usr/bin/env python3
'''A module web cache.'''

import redis
import requests
from functools import wraps
from typing import Callable

# Initialize the Redis client
redis_store = redis.Redis()
'''Redis inst.'''

def cache_requests(method: Callable) -> Callable:
    '''cache the output of fetched data.'''
    
    @wraps(method)
    def cache_wrapper(url: str) -> str:
        '''wrapper func for caching output.'''
        # Increment the access count for the URL
        redis_store.incr(f'count:{url}')
        
        # Check if the result is cached
        cached_result = redis_store.get(f'result:{url}')
        if cached_result:
            return cached_result.decode('utf-8')
        
        # Fetch the data since it's not cached
        result = method(url)
        
        # Reset the access count and cache the result with expiration
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        
        return result

    return cache_wrapper

@cache_requests
def get_page(url: str) -> str:
    '''returns content of a URL after caching request's response,
    and track req.
    '''
    return requests.get(url).text

# Example usage
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
    print(get_page(url))
