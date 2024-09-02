import logging

from ..media import media
from .cached_note import CachedNote
from .lockfile import get_lockfile, set_lockfile


# don't want to use `stdin.read`, I like this implementation a bit more
def required_input(prompt: str = "") -> str:
    """Get input. Does not return an empty string."""
    res = ""
    while True:
        res += input(prompt).strip()
        if not res:
            continue

        rev = reversed(res)
        backslash_count = 0
        for c in rev:
            if c == "\\":
                backslash_count += 1
            else:
                break

        if backslash_count % 2 == 0:
            return res
        else:
            res = res[: len(res) - 1].rstrip() + "\n"


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
            try:
                print(f'Translate phrase: "{filename}"')
                note = CachedNote(front=None, back=required_input("> "))
                lockfile[filename] = note
            except EOFError:
                logging.debug("Saving lockfile")
                set_lockfile(lockfile)
                raise

    logging.debug("Saving lockfile")
    set_lockfile(lockfile)
