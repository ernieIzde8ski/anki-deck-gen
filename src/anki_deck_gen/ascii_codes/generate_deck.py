from loguru import logger

from ankidg_core import target as get_target_path
from genanki_ext import Deck

from .ascii_data import AsciiData
from .ascii_model import CLOZE_WITH_ID
from .generate_note import generate_note

__all__ = ["generate_deck"]


def generate_deck(upper_bound: int) -> None:
    ascii_map = AsciiData.load_from()

    deck = Deck(ascii_map.deck_id, "ASCII Codes", "ASCII codes, from 0 to 127.")
    deck.add_model(CLOZE_WITH_ID)

    for i in range(upper_bound):
        note = generate_note(ascii_map, i)
        deck.add_note(note)

    target_path = get_target_path("ascii.apkg")
    deck.write_to_file(target_path)
    logger.info("Successfully wrote to file!\nTarget: {}", target_path)
