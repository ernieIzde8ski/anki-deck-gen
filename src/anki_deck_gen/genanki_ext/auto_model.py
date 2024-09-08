from typing import Literal

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
        model_type: Literal[0, 1] = Model.FRONT_BACK,
        seed: str | None = None,
    ) -> None:
        """
        Creates an AutoDeck.

        If no `seed` is provided, the `name` is used as the seed.
        """
        if seed is None:
            seed = name
        super().__init__(
            model_id=seeded_id(seed),
            name=name,
            fields=fields,
            templates=templates,
            css=css,
            model_type=model_type,
        )
