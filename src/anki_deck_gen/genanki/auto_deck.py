from random import Random

from genanki.deck import Deck

__all__ = ["AutoDeck"]

DECK_ID_LOWER_BOUND = 1 << 30
DECK_ID_UPPER_BOUND = 1 << 31


class AutoDeck(Deck):
    """A deck with a seeded random ID."""

    def __init__(
        self, name: str, description: str = "", *, seed: str | None = None
    ) -> None:
        """
        Creates an AutoDeck.

        If no `seed` is provided, the `name` is used as the seed.
        """
        if seed is None:
            seed = name
        random = Random()
        random.seed(seed, version=2)
        randint = random.randrange(DECK_ID_LOWER_BOUND, DECK_ID_UPPER_BOUND)
        super().__init__(randint, name, description)
