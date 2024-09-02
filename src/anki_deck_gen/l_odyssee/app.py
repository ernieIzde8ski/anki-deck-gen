import logging
from pathlib import Path

from genanki.note import Note
from genanki.package import Package

from anki_deck_gen.genanki import seeded_id
from anki_deck_gen.genanki.models import REVERSED_WITH_MEDIA_IN_FRONT

from ..genanki import AutoDeck
from ..media import media
from .cached_note import CachedNote
from .lockfile import Lockfile, get_lockfile, set_lockfile

AUDIO_DIRECTORY = media("l_odyssee", "audio")


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


def prompt_for_updated_lockfile() -> Lockfile:
    """
    Gets a lockfile, prompts for new keys, saves to disk,
    and returns a lockfile with verified files.
    """

    logging.debug("Opening lockfile")
    lockfile = get_lockfile()
    """Lockfile possibly containing deleted items."""
    new_lockfile: Lockfile = {}
    """Lockfile only with the mp3s that definitely exist."""

    for audio_file in AUDIO_DIRECTORY.iterdir():
        if audio_file.suffix != ".mp3":
            continue

        note: CachedNote

        filename = audio_file.name.removesuffix("".join(audio_file.suffixes))

        if filename in lockfile:
            new_lockfile[filename] = lockfile[filename]
        else:
            try:
                print(f'Translate phrase: "{filename}"')
                note = CachedNote(front=None, back=required_input("> "))
                new_lockfile[filename] = lockfile[filename] = note
            except EOFError:
                logging.debug("Saving lockfile")
                set_lockfile(lockfile)
                raise

    # TODO: hold some kind of flag and *don't* save when there are no changes
    logging.debug("Saving lockfile")
    set_lockfile(lockfile)
    # returning only the lockfile filtered by existing media
    return new_lockfile


# TODO: extend this to support nested packages
def generate_package(lockfile: Lockfile, name: str, seed: str) -> Package:
    autodeck = AutoDeck(name, seed=seed)
    media_files: list[Path] = []

    for key, val in lockfile.items():
        filename = f"{key}.mp3"

        media_files.append(AUDIO_DIRECTORY / filename)

        note = Note(
            model=REVERSED_WITH_MEDIA_IN_FRONT,
            fields=[val.front or key, val.back, f"[sound:{filename}]"],
            guid=seeded_id(filename),
        )
        autodeck.add_note(note)

    return Package(autodeck, media_files=media_files)


def app():
    logging.basicConfig(level=logging.DEBUG)

    lockfile = prompt_for_updated_lockfile()
    logging.debug("Generating package")
    package = generate_package(
        lockfile, name="L'Odyssée", seed="L'Odyssée by ernieIzde8ski"
    )
    target = media("l_odyssee.apkg")
    logging.debug(f"Writing package to file: {target}")
    package.write_to_file(target)
