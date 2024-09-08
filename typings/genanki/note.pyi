"""
This type stub file was generated by pyright.
"""

from collections.abc import Iterable, Iterator
from re import Pattern
from sqlite3 import Cursor
from typing import Any, LiteralString, SupportsIndex, override

from cached_property import cached_property
from genanki import Card
from genanki.model import Model

class _TagList(list[str]):
    def __init__(self, tags: Iterable[str] = ...) -> None: ...
    @override
    def __repr__(self) -> str: ...
    @override
    def __setitem__(self, key, val) -> None: ...
    @override
    def append(self, tag: str) -> None: ...
    @override
    def extend(self, tags: Iterable[str]) -> None: ...
    @override
    def insert(self, i: SupportsIndex, tag: str) -> None: ...

class Note:
    _INVALID_HTML_TAG_RE: Pattern[str] = ...
    def __init__(
        self,
        model: Model = ...,
        fields: list[str] | None = ...,
        sort_field=...,
        tags: list[str] = ...,
        guid: int | str = ...,
        due: int = ...,
    ) -> None: ...
    @property
    def sort_field(self): ...
    @sort_field.setter
    def sort_field(self, val) -> None: ...
    @property
    def tags(self) -> _TagList: ...
    @tags.setter
    def tags(self, val: Iterable[str]) -> None: ...
    @cached_property
    def cards(self) -> list[Any] | list[Card]: ...
    @property
    def guid(self) -> LiteralString: ...
    @guid.setter
    def guid(self, val: LiteralString) -> None: ...
    def write_to_db(
        self, cursor: Cursor, timestamp: float, deck_id: int, id_gen: Iterator[int]
    ) -> None: ...
    @override
    def __repr__(self) -> str: ...
