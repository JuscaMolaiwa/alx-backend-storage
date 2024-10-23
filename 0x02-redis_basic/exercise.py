#!/usr/bin/env python3

"""
This module provides a `CacheManager` class to leverage Redis for caching.
It supports storing and retrieving various types of data using unique keys
generated for each entry.
"""

import redis
import uuid
from typing import Union


class CacheManager:
    """
    The `CacheManager` class handles a Redis connection and provides
    methods for caching data in Redis.
    """

    def __init__(self):
        """
        Creates an instance of `CacheManager`, establishes a connection to Redis,
        and clears the database to ensure a fresh state.
        """
        self.redis_instance = redis.Redis()
        self.redis_instance.flushdb()

    def save(self, data: Union[str, bytes, int, float]) -> str:
        """
        Saves the provided data to Redis and returns a unique key
        to retrieve it later.
        """
        key = str(uuid.uuid4())
        self.redis_instance.set(key, data)
        return key

    def retrieve(self, key: str, transformer=None):
        """
        Fetches the value associated with the given key from Redis.
        If a transformation function `transformer` is passed, it is
        applied to the data before returning.
        """
        data = self.redis_instance.get(key)
        if data is None:
            return None
        return transformer(data) if transformer else data

    def get_as_str(self, key: str) -> Union[str, None]:
        """
        Retrieves the value stored under the given key, decoding it as a UTF-8 string.
        """
        data = self.redis_instance.get(key)
        return data.decode('utf-8') if data else None

    def get_as_int(self, key: str) -> Union[int, None]:
        """
        Retrieves the value stored under the given key, converting it to an integer.
        """
        data = self.redis_instance.get(key)
        return int(data) if data else None
