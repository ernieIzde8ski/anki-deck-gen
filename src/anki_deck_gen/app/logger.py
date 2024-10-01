__all__ = ["logger", "configure_logger", "Level", "parse_level"]
from collections.abc import Iterable
from pathlib import Path
from sys import stderr
from typing import Literal, TextIO, cast

import loguru
import typer
from loguru import logger

Level = Literal["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def parse_level(__s: str) -> Level:
    __s = __s.upper()
    if __s in ["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        return cast(Level, __s)
    raise typer.BadParameter(f"Invalid level: {__s}")


configured: bool = False


class SplitLineFormatter:
    FORMAT_STRING = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> "
        "| <level>{level: <8}</level> "
        "| <cyan>{name}</cyan>:<cyan>{line: <3}</cyan>"
        "<level>{extra[message]}</level>\n{exception}"
    )

    FORMAT_STRING_SEP = "\n\t >>> "

    def __init__(self, name_length: int = 50, message_length: int = 30) -> None:
        self.acceptable_extra_length: int = name_length + message_length

    def __acceptable_extra_length(self, record: "loguru.Record") -> int:
        return (
            len(record["message"]) + len(str(record["name"]))
            < self.acceptable_extra_length
        )

    def __call__(self, record: "loguru.Record") -> str:
        lines = record["message"].splitlines()

        if len(lines) == 1 and self.__acceptable_extra_length(record):
            record["extra"]["message"] = "| " + record["message"]
        else:
            record["extra"]["message"] = (
                self.FORMAT_STRING_SEP + self.FORMAT_STRING_SEP.join(lines)
            )

        return self.FORMAT_STRING


def configure_logger(
    level: Level, sinks: Iterable[Path | str | TextIO] = (stderr,), force: bool = False
):
    global configured
    if configured and not force:
        logger.warning("Not reconfiguring logger without `force=True`.")
        return
    configured = True

    logger.remove()
    for sink in sinks:
        _ = logger.add(sink, level=level, format=SplitLineFormatter())
