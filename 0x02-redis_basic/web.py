#!/usr/bin/env python3
"""
Caching request module
"""

import redis
import requests
from functools import wraps
from typing import Callable

# Global Redis client
client = redis.Redis()

def track_get_page(fn: Callable) -> Callable:
    """Decorator for get_page with caching and count tracking"""

    @wraps(fn)
    def wrapper(url: str) -> str:
        """Wrapper function"""
        client.incr(f"count:{url}")
        cached_page = client.get(f"cache:{url}")
        if cached_page:
            return cached_page.decode("utf-8")

        response = fn(url)
        client.set(f"cache:{url}", response, ex=10)
        return response

    return wrapper

@track_get_page
def get_page(url: str) -> str:
    """Fetch page content from the URL"""
    response = requests.get(url)
    return response.text
