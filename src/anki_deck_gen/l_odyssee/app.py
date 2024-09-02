import logging

from ..media import media
from .cached_note import CachedNote
from .lockfile import get_lockfile, set_lockfile


def required_input(prompt: str = "") -> str:
    res = ""
    while not res:
        res = input(prompt).strip()
    return res


def app():
    logging.basicConfig(level=logging.DEBUG)

    logging.debug("Opening lockfile")
    lockfile = get_lockfile()
    audio_files = media("l_odyssee", "audio")

    for audio_file in audio_files.iterdir():
        if audio_file.suffix != ".mp3":
            continue

        note: CachedNote

        filename = audio_file.name.removesuffix("".join(audio_file.suffixes))

        if filename in lockfile:
            note = lockfile[filename]
        else:
            print(f'Translate phrase: "{filename}"')
            note = CachedNote(front=None, back=required_input("> "))
            lockfile[filename] = note

    set_lockfile(lockfile)
