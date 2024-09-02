from random import Random

__all__ = ["seeded_id"]

DECK_ID_LOWER_BOUND = 1 << 30
DECK_ID_UPPER_BOUND = 1 << 31


def seeded_id(seed: int | float | bytes | str | bytearray):
    random = Random()
    random.seed(seed, version=2)
    return random.randrange(DECK_ID_LOWER_BOUND, DECK_ID_UPPER_BOUND)
