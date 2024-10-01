### GEN-INIT: IGNORE ###

from collections.abc import Iterator
from typing import Generic, TypeVar

__all__ = ["Reiterator"]

T = TypeVar("T")


class Reiterator(Generic[T]):
    __array__: list[T]
    __iterator__: Iterator[T]

    def __init__(self, iter: Iterator[T], /):
        self.__array__ = []
        self.__iterator__ = iter

    def __iter__(self) -> Iterator[T]:
        yield from self.__array__
        for elem in self.__iterator__:
            self.__array__.append(elem)
            yield elem
