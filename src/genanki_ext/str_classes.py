import genanki
from typing_extensions import LiteralString, override

from ankidg_core import StrMixin

__all__ = ["Package", "Deck", "Note", "Model"]


class Package(genanki.Package, StrMixin): ...


class Deck(genanki.Deck, StrMixin): ...


class Note(genanki.Note, StrMixin):
    @property
    @override
    def guid(self) -> LiteralString:  # pyright: ignore[reportIncompatibleMethodOverride]
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
          - disables the note GUID.

        More information:
            <https://docs.ankiweb.net/importing/text-files.html?highlight=guid#guid-column>
        """
        return ""


class Model(genanki.Model, StrMixin): ...
