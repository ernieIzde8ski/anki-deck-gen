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
    "AsciiData",
    "generate_deck",
    "LOCKFILE_PATH",
    "CachedNote",
    "Lockfile",
    "generate_package",
    "required_input",
]

from .app import app
from .ascii_codes import AsciiData, generate_deck
from .l_odyssee import (
    LOCKFILE_PATH,
    CachedNote,
    Lockfile,
    generate_package,
    required_input,
)

### END GEN-INIT TEMPLATE ###
