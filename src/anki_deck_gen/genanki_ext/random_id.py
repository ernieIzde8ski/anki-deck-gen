import random

__all__ = ["random_id"]

DECK_ID_LOWER_BOUND = 1 << 30
DECK_ID_UPPER_BOUND = 1 << 31


def random_id() -> int:
    return random.randrange(DECK_ID_LOWER_BOUND, DECK_ID_UPPER_BOUND)
