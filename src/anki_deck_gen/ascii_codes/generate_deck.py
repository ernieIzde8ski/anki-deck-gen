from genanki import Deck, Note
from loguru import logger

from ankidg_core import target as get_target_path
from genanki_ext import CLOZE_WITH_ID, cloze, html_escape, xml_wrap

from .ascii_data import AsciiData

__all__ = ["generate_deck"]


def gen_ascii_note(data: AsciiData, i: int) -> Note:
    repr_int: str
    "Representation of `i` as a number, eg `48`."
    repr_hex: str
    "Representation of `i` as a hexadecimal number, eg `'0x40`"
    repr_code: str
    "Representation of `i` as a (short) name, eg `'0'`"
    repr_name: str
    "Representation of `i` as a longer name, eg `'DIGIT ZERO'`"

    repr_int = cloze(str(i), 1)
    # ↓↓ f-string magic: pad at least 2 digits
    repr_hex = cloze(html_escape(f"{i:#04x}"), 2)

    (repr_code, repr_name) = data[i]
    repr_code = html_escape(repr_code)
    repr_code = cloze(repr_code, 3)
    repr_code = xml_wrap(repr_code, "code")
    repr_name = html_escape(repr_name)
    repr_name = cloze(repr_name, 3)

    display = "<br><br>".join(
        (
            f"int: {repr_int}",
            f"hex: {repr_hex}",
            f"repr: {repr_code}",
            f"name: {repr_name}",
        )
    )

    return Note(CLOZE_WITH_ID, fields=[f"ASCII_DECK_{i}", display, str()])


def generate_deck(upper_bound: int) -> None:
    ascii_map = AsciiData.load_from()

    deck = Deck(ascii_map.deck_id, "ASCII Codes", "ASCII codes, from 0 to 127.")
    deck.add_model(CLOZE_WITH_ID)

    for i in range(upper_bound):
        note = gen_ascii_note(ascii_map, i)
        deck.add_note(note)

    target_path = get_target_path("ascii.apkg")
    deck.write_to_file(target_path)
    logger.info("Successfully wrote to file!\nTarget: {}", target_path)
