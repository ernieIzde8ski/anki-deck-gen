"""
This type stub file was generated by pyright.
"""

# import threading
# import asyncio
# from functools import wraps
# from time import time

__author__: str = ...
__email__: str = ...
__version__: str = ...
__license__: str = ...

class cached_property:
    """
    A property that is only computed once per instance and then replaces itself
    with an ordinary attribute. Deleting the attribute resets the property.
    Source: https://github.com/bottlepy/bottle/commit/fa7733e075da0d790d809aa3d2f53071897e6f76
    """

    def __init__(self, func) -> None: ...
    def __get__(self, obj, cls) -> Self: ...

class threaded_cached_property:
    """
    A cached_property version for use in environments where multiple threads
    might concurrently try to access the property.
    """

    def __init__(self, func) -> None: ...
    def __get__(self, obj, cls) -> Self: ...

class cached_property_with_ttl:
    """
    A property that is only computed once per instance and then replaces itself
    with an ordinary attribute. Setting the ttl to a number expresses how long
    the property will last before being timed out.
    """

    def __init__(self, ttl=...) -> None: ...
    def __call__(self, func) -> Self: ...
    def __get__(self, obj, cls) -> Self: ...
    def __delete__(self, obj) -> None: ...
    def __set__(self, obj, value) -> None: ...

cached_property_ttl = cached_property_with_ttl
timed_cached_property = cached_property_with_ttl

class threaded_cached_property_with_ttl(cached_property_with_ttl):
    """
    A cached_property version for use in environments where multiple threads
    might concurrently try to access the property.
    """

    def __init__(self, ttl=...) -> None: ...
    def __get__(self, obj, cls) -> threaded_cached_property_with_ttl: ...

threaded_cached_property_ttl = threaded_cached_property_with_ttl
timed_threaded_cached_property = threaded_cached_property_with_ttl
