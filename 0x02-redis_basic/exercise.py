#!/usr/bin/env python3
"""
Redis module with call history and replay functionality
"""

import redis
import uuid
from typing import Union, Callable, Optional
import functools


def count_calls(method: Callable) -> Callable:
    """Decorator that counts the number of calls to a method"""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # Generate the Redis key using the method's qualified name
        key = method.__qualname__
        # Increment the count in Redis
        self._redis.incr(key)
        # Call the original method and return its result
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for a method"""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # Generate Redis keys for inputs and output
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        # Store the input arguments (as a string) in the input list
        self._redis.rpush(input_key, str(args))
        # Call the original method and get the result
        result = method(self, *args, **kwargs)
        # Store the result in the output list
        self._redis.rpush(output_key, str(result))
        # Return the result of the original method
        return result
    return wrapper


def replay(method: Callable) -> None:
    """Display the history of calls for a particular method"""
    redis_instance = method.__self__._redis  # Access
    method_name = method.__qualname__  # Get the qualified name of the method

    # Get the input and output keys
    input_key = f"{method_name}:inputs"
    output_key = f"{method_name}:outputs"

    # Get the lists of inputs and outputs from Redis
    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)

    # Get the call count
    call_count = redis_instance.get(method_name)
    if call_count:
        call_count = int(call_count)
    else:
        call_count = 0

    # Display the history of calls
    print(f"{method_name} was called {call_count} times:")
    for i, (input_data, output_data) in enumerate(zip(inputs, outputs), 1):
        print(f"{method_name}(*{input_data.decode('utf-8')}) -> {output_data.decode('utf-8')}")


class Cache:
    def __init__(self) -> None:
        # Create Redis client and flush the database
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history  # Decorate the store method with call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        # Generate a random key using uuid
        random_key = str(uuid.uuid4())
        # Store the data in Redis using the random key
        self._redis.set(random_key, data)
        # Return the key
        return random_key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, None]:
        # Get the data from Redis using the key
        data = self._redis.get(key)
        # If the key doesn't exist, Redis.get() returns None
        if data is None:
            return None
        # Apply the conversion function if provided
        if fn:
            return fn(data)
        # Otherwise, return the data as-is (which is bytes)
        return data

    def get_str(self, key: str) -> Optional[str]:
        # Use get() with a lambda to decode the byte string to UTF-8
        return self.get(key, lambda d: d.decode('utf-8') if d else None)

    def get_int(self, key: str) -> Optional[int]:
        # Use get() with a lambda to convert bytes to an integer
        try:
            return self.get(key, lambda d: int(d) if d else None)
        except (ValueError, TypeError):
            return None


# Example Usage:
if __name__ == "__main__":
    cache = Cache()

    # Call the store method a few times
    key1 = cache.store("test data")
    key2 = cache.store(42)
    key3 = cache.store(b"bytes data")

    # Replay the history of the store method
    replay(cache.store)
