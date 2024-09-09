from __future__ import annotations

import pydantic
from pydantic import BaseModel
from typing_extensions import Self

from ..dirs import media
from ..genanki_ext import random_id
from .cached_note import CachedNote

__all__ = ["Lockfile", "LOCKFILE_PATH"]


LOCKFILE_PATH = media("l_odyssee", "lockfile.json")


class Lockfile(BaseModel):
    children: dict[str, Lockfile] = pydantic.Field(default_factory=dict)
    notes: dict[str, CachedNote | None] = pydantic.Field(default_factory=dict)
    maybe_deck_id: int | None = pydantic.Field(default=None, alias="deck-id")

    @classmethod
    def read_from_file(cls) -> Self:
        """Retrieves data from the JSON lockfile."""
        with open(LOCKFILE_PATH, "rb") as file:
            data = file.read()
        return cls.model_validate_json(data)

    def save_to_file(self) -> None:
        """Writes data to the JSON lockfile."""
        data = self.model_dump_json(indent=2, exclude_defaults=True, by_alias=True)
        with open(LOCKFILE_PATH, "w+") as file:
            _ = file.write(data)
            _ = file.write("\n")

    def update(self, other: Lockfile) -> None:
        self.notes.update(other.notes)
        if other.children:
            if not self.children:
                self.children = {}
            self.children.update(other.children)

    @property
    def deck_id(self) -> int:
        if self.maybe_deck_id is None:
            self.maybe_deck_id = random_id()
        return self.maybe_deck_id
