import asyncio
from collections.abc import Coroutine
from functools import wraps
from typing import Any, Callable, ParamSpec, TypeVar

__all__ = ["async_wrapper"]

P = ParamSpec("P")
R = TypeVar("R")


def async_wrapper(f: Callable[P, Coroutine[Any, Any, R]]) -> Callable[P, R]:
    @wraps(f)
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        return asyncio.run(f(*args, **kwargs))

    return inner
