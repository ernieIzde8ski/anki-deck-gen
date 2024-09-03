from pydantic import BaseModel, ConfigDict

__all__ = ["CachedNote"]


class CachedNote(BaseModel):
    """A single cached note."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    front: str | None = None
    """The text on the front of the note. If is None, inferred from the audio file."""
    back: str
    """The text on the back of the note. Not optional."""
