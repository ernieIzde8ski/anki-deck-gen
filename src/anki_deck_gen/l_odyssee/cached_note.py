from typing import Literal, TypeVar

from pydantic import BaseModel, ConfigDict, model_serializer, model_validator

__all__ = ["CachedNote"]


T = TypeVar("T")


class CachedNote(BaseModel):
    """A single cached note."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    front: str | None = None
    """The text on the front of the note. If is None, inferred from the audio file."""
    back: str
    """The text on the back of the note. Not optional."""

    @model_validator(mode="before")
    @classmethod
    def convert_from_string(cls, data: T) -> T | dict[str, str | None]:
        if isinstance(data, str):
            return {"front": None, "back": data}
        return data

    @model_serializer
    def ser_model(self) -> str | dict[Literal["front", "back"], str]:
        if self.front is None:
            return self.back
        else:
            return {"front": self.front, "back": self.back}
