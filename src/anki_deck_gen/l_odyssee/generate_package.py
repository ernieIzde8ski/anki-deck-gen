import logging
from pathlib import Path

from ankidg_core import media, target
from genanki_ext import (
    REVERSED_WITH_FRONT_MEDIA_AND_TEXT_INPUT,
    REVERSED_WITH_MEDIA_IN_FRONT,
    Deck,
    Note,
    Package,
)

from .lockfile import Lockfile
from .update_lockfile import prompt_for_updated_root_lockfile

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
            filename = f"{fp}.mp3"
            fields = [f"[sound:{filename}]", cached_note.front or fp, cached_note.back]

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

        logging.info("Adding decks:")
        for deck in (normal_deck, hard_deck):
            decks.append(deck)
            logging.info("\t%d, %s", deck.deck_id, deck.name)

    return (decks, media_files)


def generate_package(copy_input_text_to_clipboard: bool) -> None:
    logging.basicConfig(level=logging.DEBUG)

    lockfile = prompt_for_updated_root_lockfile(
        root_audio_directory=AUDIO_DIRECTORY,
        copy_input_text_to_clipboard=copy_input_text_to_clipboard,
    )

    logging.debug("Generating package")
    decks, media_files = generate_decks(
        name="L'Odyssée (TTS Quebecois)",
        lockfile=lockfile,
        relative_directory=AUDIO_DIRECTORY,
    )
    package = Package(decks, media_files=media_files)
    target_file = target("l_odyssee.apkg")
    package.write_to_file(target_file)
    logging.debug(f"Wrote package to file: {target_file}")
