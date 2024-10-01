from pathlib import Path

import pydantic
from typing_extensions import Self

from .base_model import BaseModel

__all__ = ["FileModel"]


class FileModel(BaseModel):
    """A BaseModel expected to be read to/from disk."""

    _path: Path = pydantic.PrivateAttr()

    @classmethod
    def read_from_file(cls, path: Path) -> Self:
        """Retrieves data from the JSON lockfile."""
        with open(path, "rb") as file:
            data = file.read()
        res = cls.model_validate_json(data)
        res._path = path
        return res

    def save_to_file(self) -> None:
        """Writes data to the JSON lockfile."""
        data = self.model_dump_json(indent=2, exclude_defaults=True, by_alias=True)
        with open(self._path, "w+") as file:
            _ = file.write(data)
            _ = file.write("\n")
