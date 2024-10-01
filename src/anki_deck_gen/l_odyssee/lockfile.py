from __future__ import annotations

from functools import cached_property

from loguru import logger
from pydantic import Field

from ankidg_core import BaseModel, FileModel, MutMapDefaultView, media
from ankidg_core.strtools import StrMixin
from genanki_ext import random_id

from .cached_note import CachedNote
from .deck_id import DeckIds

__all__ = ["LOCKFILE_PATH", "Lockfile", "RootLockfile"]


LOCKFILE_PATH = media("l_odyssee", "lockfile.json")


class Lockfile(BaseModel, StrMixin):
    """A lockfile. Contains either notes or children.

    The Mapping subclass aids with implementing"""

    children: dict[str, Lockfile] = Field(default_factory=dict, frozen=True)
    """Child Lockfile nodes."""

    notes: dict[str, CachedNote | None] = Field(default_factory=dict)
    """Notes for Anki decks."""

    maybe_deck_ids: DeckIds | None = Field(default=None, alias="deck-id")

    @property
    def deck_ids(self) -> DeckIds:
        if self.maybe_deck_ids is None:
            logger.debug("maybe_deck_id is None!")
            self.maybe_deck_ids = DeckIds(random_id(), random_id())
        return self.maybe_deck_ids

    @cached_property
    def children_view(self) -> MutMapDefaultView[str, Lockfile]:
        """Returns a defaultdict-like view of `.children`."""
        return MutMapDefaultView(self.children, default_factory=Lockfile)


class RootLockfile(Lockfile, FileModel): ...
