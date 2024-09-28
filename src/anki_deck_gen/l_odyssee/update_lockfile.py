import logging
from pathlib import Path

from .cached_note import CachedNote
from .lockfile import Lockfile
from .required_input import required_input

__all__ = ["prompt_for_updated_root_lockfile"]


def prompt_update_relative_lockfile(old: Lockfile, relative_directory: Path) -> Lockfile:
    """Updates a given lockfile, specified to be relative to a specific directory, from prompted input."""
    new = Lockfile()

    for file in relative_directory.iterdir():
        if file.is_dir():
            previously_present = file.name in old.children
            if not previously_present:
                old.children[file.name] = Lockfile()

            sub_old = old.children[file.name]
            sub_dir = relative_directory / file
            sub_new = prompt_update_relative_lockfile(sub_old, sub_dir)
            if sub_new.notes:
                sub_new.maybe_deck_ids = sub_old.deck_ids
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


def print_deck_ids(lockfile: Lockfile):
    if lockfile.maybe_deck_ids:
        logging.debug("\t%s", lockfile.maybe_deck_ids)
    for child in lockfile.children.values():
        print_deck_ids(child)


def prompt_for_updated_root_lockfile(root_audio_directory: Path) -> Lockfile:
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
            disk_lockfile, root_audio_directory
        )
        """Lockfile only with the mp3s that definitely exist."""
        logging.debug("deck ids of new_lockfile:")
        print_deck_ids(new_lockfile)
    except EOFError:
        print()
        logging.debug("Saving lockfile")
        disk_lockfile.save_to_file()
        raise

    # if the user was prompted,
    # then we can say something pro8a8ly changed
    if required_input.is_notified:
        logging.debug("Updating lockfile")
        disk_lockfile.save_to_file()
    else:
        logging.debug("No new entries for lockfile")
    # returning only the lockfile filtered by existing media
    return new_lockfile
