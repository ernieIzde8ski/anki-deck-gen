import genanki
from typing_extensions import LiteralString, override

from ankidg_core import StrMixin

__all__ = ["Package", "Deck", "Note", "Model"]


class Package(genanki.Package, StrMixin): ...


class Deck(genanki.Deck, StrMixin): ...


class Note(genanki.Note, StrMixin):
    __guid: LiteralString | None = None

    @property
    @override
    def guid(self) -> LiteralString:
        """
        Mimics the behavior described by Anki.

        What SHOULD happen:
          - genanki should NOT set note guid.
          - Anki itself should identify the note,
            based off the first field and the current model.
        What ACTUALLY happens:
          - genanki sets a guid for your note using a hash based off *all* fields.
          - The model in question is not accounted for.
        What this does:
          - creates a note GUID from the first field alone.

        More information:
            <https://docs.ankiweb.net/importing/text-files.html?highlight=guid#guid-column>
        """
        if self.__guid:
            return self.__guid
        if self.fields:
            return genanki.guid_for(self.fields[1])
        return ""

    @guid.setter
    def guid(self, val: LiteralString) -> None:
        self.__guid = val


class Model(genanki.Model, StrMixin): ...
