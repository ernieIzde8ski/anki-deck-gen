### GEN-INIT: IGNORE ###

import logging
from pathlib import Path
from typing import cast

from typing_extensions import Iterable

from ankidg_core import BaseModel

from ..random_id import random_id
from ..str_classes import Model
from .template import Template


class Metadata(BaseModel):
    name: str
    id: int | None = None
    fields: list[dict[str, str]]
    templates: list[Template] | None = None
    css: str | None = None

    def resolve_model_id(self, dir: Path):
        if self.id is not None:
            return self.id

        logging.warning("Missing model ID!")
        self.id = random_id()

        path = dir / "metadata.json"
        with open(path, "w+") as file:
            data = self.model_dump_json(indent=2, exclude_defaults=True)
            n = file.write(data)
            print("Wrote", n, "chars to", path)

        return self.id

    def resolve_templates(self, dir: Path) -> Iterable[Template]:
        yield from self.templates or ()

        for dir in dir.glob("Card */"):
            qfmt_path = dir / "qfmt.html"
            afmt_path = dir / "afmt.html"

            if not qfmt_path.exists():
                logging.warning("missing path: %s", qfmt_path)
            elif not afmt_path.exists():
                logging.warning("missing path: %s", afmt_path)
            else:
                next = Template(
                    name=dir.name, qfmt=qfmt_path.read_text(), afmt=afmt_path.read_text()
                )
                if not next["qfmt"]:
                    logging.warning("empty data read from %s", qfmt_path)
                if not next["afmt"]:
                    logging.warning("empty data read from %s", afmt_path)
                yield next

    def resolve_css(self, dir: Path, /) -> str:
        if self.css is not None:
            return self.css

        path = dir / "style.css"
        if path.exists():
            return path.read_text()
        return ""

    def resolve(self, dir: Path) -> Model:
        model_id = self.resolve_model_id(dir)
        name = self.name
        fields = self.fields
        templates = list(self.resolve_templates(dir))
        templates = cast(list[dict[str, str]], templates)
        css = self.resolve_css(dir)
        return Model(model_id, name, fields, templates, css)
