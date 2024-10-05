import re
import unicodedata
from pathlib import Path

from pydantic import BaseModel, TypeAdapter
from typing_extensions import Self

from ankidg_core import media

__all__ = ["AsciiData"]


ASCII_DATA_JSON_PATH: Path = media() / "ascii-data.json"

Map = dict[int, tuple[str, str]]
MapAdapter = TypeAdapter(Map)

UPPERCASE_PATTERN = re.compile(r"^LATIN CAPITAL LETTER (\w)")
LOWERCASE_PATTERN = re.compile(r"^LATIN SMALL LETTER (\w)")


class AsciiData(BaseModel):
    deck_id: int
    map: Map

    def __getitem__(self, point: int) -> tuple[str, str]:
        """Returns a representation and name for the given character."""
        try:
            return self.map.__getitem__(point)
        except KeyError:
            # if not available in the dictionary, fallback to unicode data
            code = chr(point)
            name = unicodedata.name(code, None)
            if name is not None:
                name = UPPERCASE_PATTERN.sub(r"UPPERCASE \1", name)
                name = LOWERCASE_PATTERN.sub(r"LOWERCASE \1", name)
                return (repr(code), name)
            raise

    @classmethod
    def load_from(cls, fp: Path = ASCII_DATA_JSON_PATH) -> Self:
        with open(fp, "rb") as path:
            data = path.read()
        return cls.model_validate_json(data)
