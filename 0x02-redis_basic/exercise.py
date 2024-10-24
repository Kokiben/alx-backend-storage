#!/usr/bin/env python3
"""
Redis module
"""

import redis
import uuid
from typing import Union, Callable, Optional

class Cache:
    def __init__(self) -> None:
        # Create Redis client and flush the database
        self._redis = redis.Redis()
        self._redis.flushdb()

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
