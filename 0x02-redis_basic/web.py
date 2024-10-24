#!/usr/bin/env python3
""" Module that implements an expiring web cache system. """

import redis
import requests
from typing import Callable
from functools import wraps

redis_instance = redis.Redis()  # Create a Redis instance for caching

def data_out(fn: Callable) -> Callable:
    """ Decorator that caches web requests and tracks access counts. """

    @wraps(fn)
    def wra_fun(url):  # Function that wraps the original function
        """ Handles the caching logic for the decorated function. """
        redis_instance.incr(f"count:{url}")  # Increment the URL 
        cached_response = redis_instance.get(f"cached:{url}")
        if cached_response:
            return cached_response.decode('utf-8')  # Return cache
        cached_result = fn(url)  # Execute the original
        redis_instance.setex(f"cached:{url}", 10, cached_result)
        return cached_result  # Return the fresh response

    return wra_fun  # Return the wrapper function


@data_out  # Use the data_out decorator
def get_page(url: str) -> str:
    """ Fetch the content of a web page given its URL. """
    re_pons = requests.get(url)  # Make a GET request to the specified URL
    return re_pons.text  # Return the body of the response as text
