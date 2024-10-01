from pathlib import Path

import pyperclip
import typer
from loguru import logger

from .cached_note import CachedNote
from .lockfile import LOCKFILE_PATH, Lockfile, RootLockfile
from .required_input import required_input

__all__ = ["read_and_update_lockfile"]


def prompt_update_relative_lockfile(
    lockfile: Lockfile, relative_directory: Path, copy_input_text_to_clipboard: bool
) -> bool:
    """
    Updates a given (child?) lockfile, specified to be
    relative to a specific directory, using prompted input.
    """
    updated = False

    for file in relative_directory.iterdir():
        if file.is_dir():
            child = lockfile.children_view[file.name]
            subdir = relative_directory / file
            child_updated = prompt_update_relative_lockfile(
                child, subdir, copy_input_text_to_clipboard
            )
            updated = updated or child_updated
        elif file.suffix == ".mp3":
            card_name = file.name.removesuffix("".join(file.suffixes))

            if card_name in lockfile.notes:
                continue

            if copy_input_text_to_clipboard:
                pyperclip.copy(card_name)

            print(f"Front: {card_name}")
            back = required_input("Back:  ")

            if back == "NULL":
                note = None
                logger.debug("Skipping file: {}", file)
            else:
                note = CachedNote(front=None, back=back)

            lockfile.notes[card_name] = note
            updated = True

            print()

    return updated


def read_and_update_lockfile(
    root_audio_directory: Path, copy_input_text_to_clipboard: bool
):
    """
    Reads the lockfile from disk, updates said given
    lockfile with any new changes in the audio directory,
    and saves to disk if any changes occurred.
    """

    logger.debug("Reading lockfile.")
    lockfile = RootLockfile.read_from_file(LOCKFILE_PATH)

    updated = False

    try:
        logger.debug("Ensuring lockfile is up to date.")
        updated = prompt_update_relative_lockfile(
            lockfile, root_audio_directory, copy_input_text_to_clipboard
        )
    except EOFError:
        updated = True
        print()
        raise typer.Exit()
    finally:
        if updated:
            logger.info("Saving lockfile.")
            lockfile.save_to_file()
        else:
            logger.info("No changes to lockfile.")

    return lockfile
