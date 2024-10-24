#!/usr/bin/env python3
"""
Redis module
"""

import redis
import uuid
from typing import Union

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
