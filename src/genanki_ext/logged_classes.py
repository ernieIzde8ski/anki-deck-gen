__all__ = ["LoggedDeck", "LoggedPackage"]

from typing import override

import genanki
from loguru import logger

from .str_classes import *


class LoggedDeck(Deck):
    @override
    def add_note(self, note: genanki.Note) -> None:
        assert isinstance(note.guid, str)
        assert isinstance(self.deck_id, int)
        logger.debug(
            "Deck(name={}, deck_id={}): registered note: {}",
            self.name and self.name.ljust(50),
            self.deck_id,
            (note.fields or ("",))[0],
        )
        return super().add_note(note)


class LoggedPackage(Package):
    def log_decks(self) -> None:
        logger.debug("{} deck(s) within package.", len(self.decks))
        for deck in self.decks:
            logger.debug("\tDeck(deck_id={}, len={})", deck.deck_id, len(deck.notes))
