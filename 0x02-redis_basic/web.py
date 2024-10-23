#!/usr/bin/env python3
'''A module providing tools for caching HTTP requests and tracking access
'''
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
'''A Redis instance used for caching request data and tracking access counts.
'''


def data_cacher(method: Callable) -> Callable:
    '''A decorator that caches the result of an HTTP request and tracks
    the number of times the request has been made for a given URL.
    '''
    @wraps(method)
    def invoker(url: str) -> str:
        '''Wraps the original function to add caching and request tracking
        '''
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''Fetches the content of a webpage and caches the result.
    '''
    return requests.get(url).text
