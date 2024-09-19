### GEN-INIT: IGNORE ###

import sys

try:
    import pytest as _
except ModuleNotFoundError:
    print("Please install anki-deck-gen[devel] to use this script.", file=sys.stderr)
    exit(1)
