from __future__ import annotations

from typing import Annotated

import typer

from .logger import Level, configure_logger, parse_level
from .versions import (
    AppVersion,
    AsciiVersion,
    CoreVersion,
    OdysseeVersion,
    VersionAnnotation,
)

__all__ = ["app"]

app = typer.Typer()


@app.callback()
def app_callback(
    level: Annotated[
        Level,
        typer.Option(
            envvar="ADG_LOG_LEVEL",
            parser=parse_level,
            help="Minimum log level, as understood by loguru.",
        ),
    ] = "INFO",
    _version: Annotated[
        bool | None, VersionAnnotation(CoreVersion, AppVersion, OdysseeVersion)
    ] = None,
):
    configure_logger(level)


@app.command(help="Generates the L'Odyssée deck.")
def odyssee(
    copy: Annotated[
        bool,
        typer.Option(help="Copy front-side text to clipboard when updating entries."),
    ] = False,
    _version: Annotated[
        bool | None, VersionAnnotation(CoreVersion, AppVersion, OdysseeVersion)
    ] = None,
):
    from ..l_odyssee.generate_package import generate_package

    generate_package(copy_input_text_to_clipboard=copy)


def parse_upper_bound(value: str | int):
    if isinstance(value, int):
        return value
    lowered = value.strip().lower()
    if lowered == "basic":
        return 128
    elif lowered == "extended":
        return 256
    try:
        return int(value)
    except ValueError:
        raise typer.BadParameter("Value must be an int, 'basic', or 'extended'.")


@app.command(help="Generates the ASCII Codes deck.")
def ascii(
    upper_bound: Annotated[int, typer.Option(parser=parse_upper_bound)] = 128,
    _version: Annotated[
        bool | None, VersionAnnotation(CoreVersion, AppVersion, AsciiVersion)
    ] = None,
):
    from ..ascii_codes.generate_deck import generate_deck

    generate_deck(upper_bound=upper_bound)


@app.command(help="Generates random IDs between 2^30 and 2^31.")
def gen_id(
    count: Annotated[int, typer.Argument(help="Number of IDs to generate.")] = 1,
    _version: Annotated[bool | None, VersionAnnotation(CoreVersion, AppVersion)] = None,
):
    from genanki_ext import random_id

    for _ in range(count):
        print(random_id())
