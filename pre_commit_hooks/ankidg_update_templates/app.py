import logging
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import TypedDict

import typer
from jinja2 import StrictUndefined, Template

from .dirs import ROOT, TEMPLATEDIR

app = typer.Typer()


def map_path_tmpl_to_target(paths: Iterable[Path]):
    for tmpl in paths:
        if not tmpl.exists():
            logging.error("path does not exist: %s", tmpl)
            continue
        if not tmpl.suffix == ".jinja":
            logging.error("path does not have a .jinja extension: %s", tmpl)
            continue
        try:
            relative = tmpl.resolve().relative_to(TEMPLATEDIR)
        except ValueError:
            logging.error("%s\n%s", tmpl.resolve, TEMPLATEDIR)
            logging.error("path is not in the template directory: %s", tmpl)
            continue
        target = (ROOT / relative).with_name(relative.name.removesuffix(".jinja"))
        yield (tmpl, target)


def read_requirements_file(path: Path) -> Iterator[str]:
    lines = path.read_text().splitlines()
    for line in lines:
        line = (line.split("#") or ("",))[0].strip()
        if not line:
            continue
        if line[0].isalnum() or line[0] == "_":
            yield line
        else:
            raise RuntimeError(f"Cannot parse requirements line: {line}")


class Data(TypedDict):
    full_requirements: list[str]


def collect_data():
    full_requirements: list[str] = []

    for fp in ("requirements.txt", "requirements-dev.txt"):
        requirements = read_requirements_file(ROOT / fp)
        full_requirements.extend(requirements)

    return Data(full_requirements=full_requirements)


@app.command()
def main(updated_templates: list[Path]) -> None:
    env = collect_data()

    for tmpl, target in map_path_tmpl_to_target(updated_templates):
        if not target.parent.exists():
            target.parent.mkdir()
        template = Template(
            tmpl.read_text(), undefined=StrictUndefined, keep_trailing_newline=True
        )
        logging.error("%s", env)
        render = template.render(env)

        if not target.exists():
            _ = target.write_text(render)
            logging.info(f"Created file: {target}")
        elif target.read_text() == template:
            logging.info(f"File had identical contents: {target}")
        else:
            _ = target.write_text(render)
            logging.info(f"Overwrote file: {target}")
