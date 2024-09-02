from genanki.model import Model

from .seeded_id import seeded_id

__all__ = ["AutoModel"]


class AutoModel(Model):
    """A deck with a seeded random ID."""

    def __init__(
        self,
        name: str,
        fields: list[dict[str, str]],
        templates: list[dict[str, str]],
        *,
        css: str = "",
        seed: str | None = None,
    ) -> None:
        """
        Creates an AutoDeck.

        If no `seed` is provided, the `name` is used as the seed.
        """
        if seed is None:
            seed = name
        super().__init__(seeded_id(seed), name, fields, templates, css=css)
