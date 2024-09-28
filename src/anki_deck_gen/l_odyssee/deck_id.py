from typing import NamedTuple

__all__ = ["DeckIds"]


class DeckIds(NamedTuple):
    normal: int
    """ID for deck with normal difficulty."""
    hard: int
    """ID for deck with increased difficulty."""
