from pydantic import TypeAdapter

from ..media import media
from .cached_note import CachedNote

__all__ = ["Lockfile", "LOCKFILE_PATH", "get_lockfile", "set_lockfile"]


type Lockfile = dict[str, CachedNote]

LockfileAdapter = TypeAdapter(dict[str, CachedNote])

LOCKFILE_PATH = media("l_odyssee", "lockfile.json")


def get_lockfile() -> Lockfile:
    """Retrieves data from the JSON lockfile."""
    with open(LOCKFILE_PATH, "rb") as file:
        data = file.read()
    return LockfileAdapter.validate_json(data)


def set_lockfile(lockfile: Lockfile, /) -> None:
    """Writes data to the JSON lockfile."""
    data = LockfileAdapter.dump_json(lockfile, indent=2)
    with open(LOCKFILE_PATH, "wb") as file:
        _ = file.write(data)
