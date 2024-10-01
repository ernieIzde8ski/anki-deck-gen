from pathlib import Path

from loguru import logger

from ankidg_core import media, target
from genanki_ext import (
    REVERSED_WITH_FRONT_MEDIA_AND_TEXT_INPUT,
    REVERSED_WITH_MEDIA_IN_FRONT,
)
from genanki_ext import LoggedDeck as Deck
from genanki_ext import LoggedPackage as Package
from genanki_ext import Note

from .lockfile import Lockfile
from .update_lockfile import read_and_update_lockfile

__all__ = ["generate_package"]

AUDIO_DIRECTORY = media("l_odyssee", "audio")


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
        normal_deck = Deck(lockfile.deck_ids.normal, name + "::00 Normal")
        normal_deck.add_model(REVERSED_WITH_MEDIA_IN_FRONT)

        hard_deck = Deck(lockfile.deck_ids.hard, name + "::01 Challenge")
        hard_deck.add_model(REVERSED_WITH_FRONT_MEDIA_AND_TEXT_INPUT)

        for fp, cached_note in lockfile.notes.items():
            if cached_note is None:
                continue

            path = relative_directory / f"{fp}.mp3"
            if path.exists():
                media_files.append(path)
            else:
                logger.warning(f"Path does not exist:\n\t{path}")
                continue

            fields = [f"[sound:{path.name}]", cached_note.front or fp, cached_note.back]

            normal_note = Note(
                model=REVERSED_WITH_MEDIA_IN_FRONT, fields=fields, tags=["normal"]
            )
            normal_deck.add_note(normal_note)

            hard_note = Note(
                model=REVERSED_WITH_FRONT_MEDIA_AND_TEXT_INPUT,
                fields=fields,
                tags=["hard"],
            )
            hard_deck.add_note(hard_note)

        new_decks = (normal_deck, hard_deck)
        logger.info(
            "Adding decks:\n\t{}",
            "\n\t".join(f"{deck.deck_id}, {deck.name}" for deck in new_decks),
        )

        for deck in new_decks:
            decks.append(deck)

    return (decks, media_files)


def generate_package(copy_input_text_to_clipboard: bool) -> None:
    lockfile = read_and_update_lockfile(
        root_audio_directory=AUDIO_DIRECTORY,
        copy_input_text_to_clipboard=copy_input_text_to_clipboard,
    )

    logger.debug("Generating package")
    decks, media_files = generate_decks(
        name="L'Odyssée (TTS Quebecois)",
        lockfile=lockfile,
        relative_directory=AUDIO_DIRECTORY,
    )
    package = Package(decks, media_files=media_files)
    package.log_decks()
    target_file = target("l_odyssee.apkg")
    package.write_to_file(target_file)
    logger.debug(f"Wrote package to file: {target_file}")
