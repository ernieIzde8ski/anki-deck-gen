from typing import LiteralString, cast

from genanki_ext import XmlTag, cloze
from genanki_ext.str_classes import Note
from genanki_ext.text_utils import HtmlTag

from .ascii_data import AsciiData
from .ascii_model import CLOZE_WITH_ID

__all__ = []

_colors = {
    "0": "5F0000",
    "1": "AF5F00",
    "2": "5F5F00",
    "3": "005F00",
    "4": "000080",
    "5": "005F5F",
    "6": "5F0087",
    "7": "87005F",
    "8": "FF0000",
    "9": "D78700",
    "A": "808000",
    "B": "008000",
    "C": "0000FF",
    "D": "008080",
    "E": "800080",
    "F": "D7005F",
}

colors_array = tuple(_colors.values())
assert len(colors_array) == 16


def _generate_int_repr(num: int):
    color = colors_array[num // 16 % 16]
    tag = XmlTag(
        name="span",
        content=[str(num)],
        attrs={"style": f"color: #{color}", "class": "mono"},
    )
    return cloze(tag, 1)


def _generate_hex_repr(num: int) -> XmlTag:
    tags: list[str | XmlTag] = []

    for char in f"{num:02X}":
        color = _colors[char]
        tag = XmlTag(name="span", content=[char], attrs={"style": f"color: #{color}"})
        tags.append(tag)

    tag = XmlTag(name="span", content=tags, attrs={"class": "mono"})
    return cloze(tag, 2)


def _generate_literal_repr_row(i: int, data: AsciiData) -> XmlTag:
    """Generates a literal-name representation."""
    (repr_code, repr_name) = data[i]
    tag_code = XmlTag(name="code", content=[repr_code])
    tag_code = cloze(tag_code, level=3)
    tag_name = XmlTag(name="code", content=[repr_name])
    tag_name = cloze(tag_name, level=3)

    return XmlTag(name="span", content=[tag_code, XmlTag(name="br"), tag_name])


def generate_note(data: AsciiData, i: int) -> Note:
    repr_int = _generate_int_repr(i)
    repr_hex = _generate_hex_repr(i)
    repr_literal = _generate_literal_repr_row(i, data)

    table_rows: list[XmlTag | str] = []

    for name, tag in (("int", repr_int), ("hex", repr_hex), ("name", repr_literal)):
        table_header = XmlTag(name="th", content=name, attrs={"scope": "row"})
        table_data = XmlTag(name="td", content=tag)
        table_row = XmlTag(name="tr", content=[table_header, table_data])
        table_rows.append(table_row)

    table = HtmlTag(name="table", content=table_rows)
    table.set_class("centerTable")

    sort_field = f"ASCII_DECK_{i}"

    note = Note(CLOZE_WITH_ID, fields=[sort_field, str(table), str()])
    note.guid = cast(LiteralString, sort_field)
    return note
