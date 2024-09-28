import logging
from pathlib import Path

import pyperclip

from .cached_note import CachedNote
from .lockfile import Lockfile
from .required_input import required_input

__all__ = ["prompt_for_updated_root_lockfile"]


def prompt_update_relative_lockfile(
    old: Lockfile, relative_directory: Path, copy_input_text_to_clipboard: bool
):
    """Updates a given lockfile, specified to be relative to a specific directory, from prompted input."""

    for file in relative_directory.iterdir():
        if file.is_dir():
            previously_present = file.name in old.children
            if not previously_present:
                old.children[file.name] = Lockfile()

            sub_old = old.children[file.name]
            sub_dir = relative_directory / file
            sub_new = prompt_update_relative_lockfile(
                sub_old, sub_dir, copy_input_text_to_clipboard
            )
            if sub_new.notes:
                sub_new.maybe_deck_ids = sub_old.deck_ids
            new.children[file.name] = sub_new
        elif file.suffix == ".mp3":
            front_text = file.name.removesuffix("".join(file.suffixes))
            if front_text in old.notes:
                new.notes[front_text] = old.notes[front_text]
            else:
                if copy_input_text_to_clipboard:
                    pyperclip.copy(front_text)
                print(f"Front: {front_text}")
                back = required_input("Back:  ")
                if back == "NULL":
                    note = None
                    logging.debug("Skipping file.")
                else:
                    note = CachedNote(front=None, back=back)
                print()
                new.notes[front_text] = old.notes[front_text] = note

    return new


def print_deck_ids(lockfile: Lockfile):
    if lockfile.maybe_deck_ids:
        logging.debug("\t%s", lockfile.maybe_deck_ids)
    for child in lockfile.children.values():
        print_deck_ids(child)


def prompt_for_updated_root_lockfile(
    root_audio_directory: Path, copy_input_text_to_clipboard: bool
) -> Lockfile:
    """
    Gets a lockfile, prompts for new keys, saves to disk,
    and returns a lockfile with verified files.
    """

    logging.debug("Reading lockfile.")
    disk_lockfile = Lockfile.read_from_file()
    """Lockfile possibly containing deleted items."""

    logging.debug("deck ids of disk_lockfile:")
    print_deck_ids(disk_lockfile)

    try:
        logging.debug("Ensuring lockfile is up to date.")
        new_lockfile = prompt_update_relative_lockfile(
            disk_lockfile, root_audio_directory, copy_input_text_to_clipboard
        )
        """Lockfile only with the mp3s that definitely exist."""
        logging.debug("deck ids of new_lockfile:")
        print_deck_ids(new_lockfile)
    except EOFError:
        print()
        logging.info("Saving lockfile")
        disk_lockfile.save_to_file()
        raise

    # if the user was prompted,
    # then we can say something pro8a8ly changed
    if required_input.is_notified:
        logging.info("Updating lockfile")
        disk_lockfile.save_to_file()
    else:
        logging.debug("No new entries for lockfile")
    # returning only the lockfile filtered by existing media
    return new_lockfile
