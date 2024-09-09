"""
This type stub file was generated by pyright.
"""

from sqlite3 import Cursor

class Card:
    def __init__(self, ord, suspend: bool = False) -> None: ...
    def write_to_db(
        self,
        cursor: Cursor,
        timestamp: float,
        deck_id: int,
        note_id: int,
        id_gen,
        due=...,
    ) -> None: ...
