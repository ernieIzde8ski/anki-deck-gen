"""A generator for my Anki decks."""

__author__ = "Ernest Izdebski"
__copyright__ = "Copyright 2024-present, Ernest Izdebski"
__credits__ = ["Ernest Izdebski"]
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Ernest Izdebski"

### START GEN-INIT TEMPLATE ###

__all__ = [
    "app",
    "ROOT",
    "MEDIA",
    "media",
    "TARGET",
    "target",
    "REVERSED_WITH_MEDIA_IN_FRONT",
    "CLOZE_WITH_ID",
    "random_id",
    "html_escape",
    "cloze",
    "xml_wrap",
    "AsciiData",
    "generate_deck",
    "app",
    "CachedNote",
    "Lockfile",
    "LOCKFILE_PATH",
]

from .app import app
from .dirs import ROOT, MEDIA, media, TARGET, target
from .genanki_ext import (
    REVERSED_WITH_MEDIA_IN_FRONT,
    CLOZE_WITH_ID,
    random_id,
    html_escape,
    cloze,
    xml_wrap,
)
from .ascii_codes import AsciiData, generate_deck
from .l_odyssee import app, CachedNote, Lockfile, LOCKFILE_PATH

### END GEN-INIT TEMPLATE ###
