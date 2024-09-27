import sys
from functools import partial
from typing import Any, NamedTuple

import typer

from ankidg_core import __version__ as CoreBaseVersion

from ..ascii_codes import __version__ as AsciiBaseVersion
from ..l_odyssee import __version__ as OdysseeBaseVersion
from ..version import __version__ as AppBaseVersion

eprint = partial(print, file=sys.stderr)

__all__ = [
    "Version",
    "VersionAnnotation",
    "CoreVersion",
    "AppVersion",
    "AsciiVersion",
    "OdysseeVersion",
]


class Version(NamedTuple):
    name: str
    """The name of the generated package, or the name of the associated module."""
    semver: str
    """A version string like `1.0.0`."""
    is_deck: bool = True
    """If the `Version.name` corresponds to a deck name."""


def VersionAnnotation(*versions: Version) -> Any:  # pyright: ignore[reportAny]
    if not versions:
        eprint("error: no versions listed, something is catastrophically wrong")

    max_name_len = max(len(v[0]) + (6 if v.is_deck else 0) for v in versions)

    def inner(value: bool) -> None:
        if not value:
            return
        for name, version, is_deck in versions:
            if is_deck:
                print(f"deck: {name}".ljust(max_name_len), ":", f"v{version}")
            else:
                print(name.ljust(max_name_len), ":", "v" + version)
        raise typer.Exit()

    return typer.Option("--version", callback=inner)  # pyright: ignore[reportAny]


CoreVersion = Version("ankidg_core", CoreBaseVersion, False)
AppVersion = Version("anki-deck-gen", AppBaseVersion, False)
AsciiVersion = Version("ASCII Codes", AsciiBaseVersion)
OdysseeVersion = Version("L'Odyssée (TTS Quebecois)", OdysseeBaseVersion)
