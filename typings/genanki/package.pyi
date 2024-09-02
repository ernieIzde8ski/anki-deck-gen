"""
This type stub file was generated by pyright.
"""

from typing import Optional

class Package:
    def __init__(self, deck_or_decks=..., media_files=...) -> None: ...
    def write_to_file(self, file, timestamp: Optional[float] = ...):  # -> None:
        """
        :param file: File path to write to.
        :param timestamp: Timestamp (float seconds since Unix epoch) to assign to generated notes/cards. Can be used to
            make build hermetic. Defaults to time.time().
        """
        ...

    def write_to_db(self, cursor, timestamp: float, id_gen):  # -> None:
        ...

    def write_to_collection_from_addon(self):  # -> None:
        """
        Write to local collection. *Only usable when running inside an Anki addon!* Only tested on Anki 2.1.

        This writes to a temporary file and then calls the code that Anki uses to import packages.

        Note: the caller may want to use mw.checkpoint and mw.reset as follows:

          # creates a menu item called "Undo Add Notes From MyAddon" after this runs
          mw.checkpoint('Add Notes From MyAddon')
          # run import
          my_package.write_to_collection_from_addon()
          # refreshes main view so new deck is visible
          mw.reset()

        Tip: if your deck has the same name and ID as an existing deck, then the notes will get placed in that deck rather
        than a new deck being created.
        """
        ...
