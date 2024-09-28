import logging
from typing import Annotated, Literal, cast

import typer

from .versions import (
    AppVersion,
    AsciiVersion,
    CoreVersion,
    OdysseeVersion,
    VersionAnnotation,
)

__all__ = ["app"]

app = typer.Typer()

LogLevels = Literal[0, 10, 20, 30, 40, 50]


def parse_log_level(value: str | Literal[20]) -> LogLevels:
    if isinstance(value, int):
        return value

    value = value.strip().upper()
    match value:
        case "" | "NOTSET":
            return logging.NOTSET
        case "DEBUG":
            return logging.DEBUG
        case "INFO":
            return logging.INFO
        case "WARN" | "WARNING":
            return logging.WARN
        case "ERROR":
            return logging.ERROR
        case "FATAL" | "CRITICAL":
            return logging.FATAL
        case n:
            try:
                return cast(LogLevels, int(n))
            except ValueError:
                raise typer.BadParameter(
                    "log level must be a valid name or number for a level in `logging`"
                )


@app.callback()
def app_callback(
    log_level: Annotated[
        LogLevels,
        typer.Option(
            envvar="ADG_LOG_LEVEL",
            parser=parse_log_level,
            help="Set level for logging module. Accepts level names or integers.",
        ),
    ] = 20,
    _version: Annotated[
        bool | None, VersionAnnotation(CoreVersion, AppVersion, OdysseeVersion)
    ] = None,
):
    logging.basicConfig(level=log_level)


@app.command(help="Generates the L'Odyssée deck.")
def odyssee(
    _version: Annotated[
        bool | None, VersionAnnotation(CoreVersion, AppVersion, OdysseeVersion)
    ] = None
):
    from ..l_odyssee.generate_package import generate_package

    generate_package()


def parse_upper_bound(value: str):
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
