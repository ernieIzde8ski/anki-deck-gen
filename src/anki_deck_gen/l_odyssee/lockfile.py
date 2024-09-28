from __future__ import annotations

import logging

import pydantic
from typing_extensions import Self

from ankidg_core import BaseModel, media
from ankidg_core.strtools import StrMixin
from genanki_ext import random_id

from .cached_note import CachedNote
from .deck_id import DeckIds

__all__ = ["Lockfile", "LOCKFILE_PATH"]


LOCKFILE_PATH = media("l_odyssee", "lockfile.json")


class Lockfile(BaseModel, StrMixin):
    children: dict[str, Lockfile] = pydantic.Field(default_factory=dict)
    notes: dict[str, CachedNote | None] = pydantic.Field(default_factory=dict)
    maybe_deck_ids: DeckIds | None = pydantic.Field(default=None, alias="deck-id")

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
        self.maybe_deck_ids = other.maybe_deck_ids
        self.notes.update(other.notes)
        if other.children:
            if not self.children:
                self.children = {}
            self.children.update(other.children)

    @property
    def deck_ids(self) -> DeckIds:
        if self.maybe_deck_ids is None:
            logging.debug("maybe_deck_id is None!")
            self.maybe_deck_ids = DeckIds(random_id(), random_id())
        return self.maybe_deck_ids
