import logging
from pathlib import Path

from genanki import Deck, Note, Package

from ..dirs import media
from ..genanki_ext import REVERSED_WITH_MEDIA_IN_FRONT
from .cached_note import CachedNote
from .lockfile import Lockfile

__all__ = ["app"]

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


def prompt_update_lockfile(old: Lockfile, relative_directory: Path) -> Lockfile:
    new = Lockfile()

    for file in relative_directory.iterdir():
        if file.is_dir():
            if file.name not in old.children:
                old.children[file.name] = Lockfile()

            sub_old = old.children[file.name]
            sub_dir = relative_directory / file
            sub_new = prompt_update_lockfile(sub_old, sub_dir)
            new.children[file.name] = sub_new
        elif file.suffix == ".mp3":
            file_name = file.name.removesuffix("".join(file.suffixes))
            if file_name in old.notes:
                new.notes[file_name] = old.notes[file_name]
            else:
                print(f"Front: {file_name}")
                back = required_input("Back:  ")
                if back == "NULL":
                    note = None
                    logging.debug("Skipping file.")
                else:
                    note = CachedNote(front=None, back=back)
                print()
                new.notes[file_name] = old.notes[file_name] = note

    return new


def prompt_for_updated_lockfile() -> Lockfile:
    """
    Gets a lockfile, prompts for new keys, saves to disk,
    and returns a lockfile with verified files.
    """

    logging.debug("Opening lockfile")
    lockfile = Lockfile.read_from_file()
    """Lockfile possibly containing deleted items."""

    try:
        print("Updating lockfile with new audio files.")
        print("Shortcuts:")
        print("\t<C-D>: save and quit")
        print("\t<C-C>: quit without saving")
        print("\tinput 'NULL': ignore current note")
        print("\tinput other: put text on back of note")
        print()
        new_lockfile = prompt_update_lockfile(lockfile, AUDIO_DIRECTORY)
        """Lockfile only with the mp3s that definitely exist."""
    except EOFError:
        print()
        logging.debug("Saving lockfile")
        lockfile.save_to_file()
        raise

    # TODO: hold some kind of flag and *don't* save when there are no changes
    logging.debug("Saving lockfile")
    lockfile.save_to_file()
    # returning only the lockfile filtered by existing media
    return new_lockfile


def generate_decks(
    name: str, lockfile: Lockfile, relative_directory: Path
) -> tuple[list[Deck], list[Path]]:
    decks: list[Deck] = []
    media_files: list[Path] = []

    for fp, sub_lockfile in (lockfile.children or {}).items():
        sub_decks, sub_media_files = generate_decks(
            f"{name}::{fp}", sub_lockfile, relative_directory / fp
        )

        decks.extend(sub_decks)
        media_files.extend(sub_media_files)

    if lockfile.notes:
        deck = Deck(lockfile.deck_id, name)
        deck.add_model(REVERSED_WITH_MEDIA_IN_FRONT)
        for fp, cached_note in lockfile.notes.items():
            if cached_note is None:
                continue
            filename = f"{fp}.mp3"
            media_files.append(relative_directory / filename)
            note = Note(
                model=REVERSED_WITH_MEDIA_IN_FRONT,
                fields=[cached_note.front or fp, cached_note.back, f"[sound:{filename}]"],
            )
            deck.add_note(note)
        decks.append(deck)

    return (decks, media_files)


def app():
    logging.basicConfig(level=logging.DEBUG)

    lockfile = prompt_for_updated_lockfile()

    logging.debug("Generating package")
    decks, media_files = generate_decks(
        name="L'Odyssée (TTS Quebecois)",
        lockfile=lockfile,
        relative_directory=AUDIO_DIRECTORY,
    )
    package = Package(decks, media_files=media_files)

    target = media("l_odyssee.apkg")
    logging.debug(f"Writing package to file: {target}")
    package.write_to_file(target)
