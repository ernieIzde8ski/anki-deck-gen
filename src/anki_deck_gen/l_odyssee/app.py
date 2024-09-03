import logging
from pathlib import Path

from genanki.note import Note
from genanki.package import Package

from anki_deck_gen.genanki import seeded_id
from anki_deck_gen.genanki.models import REVERSED_WITH_MEDIA_IN_FRONT

from ..genanki import AutoDeck
from ..media import media
from .cached_note import CachedNote
from .lockfile import Lockfile

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
                print(f'Translate phrase: "{file_name}"')
                note = CachedNote(front=None, back=required_input("> "))
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
        new_lockfile = prompt_update_lockfile(lockfile, AUDIO_DIRECTORY)
        """Lockfile only with the mp3s that definitely exist."""
    except EOFError:
        logging.debug("Saving lockfile")
        lockfile.save_to_file()
        raise

    # TODO: hold some kind of flag and *don't* save when there are no changes
    logging.debug("Saving lockfile")
    lockfile.save_to_file()
    # returning only the lockfile filtered by existing media
    return new_lockfile


def generate_decks(
    name: str, seed: str, lockfile: Lockfile, relative_directory: Path
) -> tuple[list[AutoDeck], list[Path]]:
    decks: list[AutoDeck] = []
    media_files: list[Path] = []

    for key, val in (lockfile.children or {}).items():
        sub_name = f"{name}::{key}"
        sub_seed = f"{seed}::{key.replace(":", ".")}"

        sub_decks, sub_media_files = generate_decks(
            sub_name, sub_seed, val, relative_directory / key
        )

        decks.extend(sub_decks)
        media_files.extend(sub_media_files)

    if lockfile.notes:
        deck = AutoDeck(name, seed=seed)
        for key, val in lockfile.notes.items():
            if val is None:
                continue
            filename = f"{key}.mp3"
            media_files.append(relative_directory / filename)
            note = Note(
                model=REVERSED_WITH_MEDIA_IN_FRONT,
                fields=[val.front or key, val.back, f"[sound:{filename}]"],
                guid=seeded_id(filename),
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
        seed="L'Odyssée by ernieIzde8ski",
        lockfile=lockfile,
        relative_directory=AUDIO_DIRECTORY,
    )
    package = Package(decks, media_files=media_files)

    target = media("l_odyssee.apkg")
    logging.debug(f"Writing package to file: {target}")
    package.write_to_file(target)
