import logging
import sys
from collections.abc import Iterable
from functools import partial
from pathlib import Path
from typing import Annotated

import typer

from .async_wrapper import async_wrapper
from .error import AstError, ResolutionError
from .init_generator import InitGenerator
from .result import ResultStatus

__all__ = ["app"]

eprint = partial(print, file=sys.stderr)


def is_a_normal_import(path: Path):
    return (
        path.is_file()
        and path.suffix == ".py"
        and "-" not in path.name
        and not path.name.startswith("_")
    )


app = typer.Typer()

OptionalListArg = Annotated[list[Path] | None, typer.Argument()]


@app.command()
@async_wrapper
async def main(
    updated_python_files: OptionalListArg = None, all: bool = False, debug: bool = False
):
    logging.basicConfig(level=logging.DEBUG if debug is True else logging.INFO)
    sources: Iterable[Path]

    if all:
        sources = Path().glob("src/**/*.py")
        sources = filter(is_a_normal_import, sources)
    elif updated_python_files:
        sources = updated_python_files
    else:
        logging.error("neither Python source files nor --all specified.")
        raise typer.Abort()

    sources = {source.parent for source in sources}

    errors: list[AstError | ResolutionError] = []

    async for path, result in InitGenerator(sources):
        name: str
        code: str

        name = str(path).ljust(72, ".")

        match result:
            case (ResultStatus.IGNORED, None):
                code = "Ignored"
            case (ResultStatus.SKIPPED, None):
                code = "Skipped"
            case (ResultStatus.SUCCESS, None):
                code = "Rebuilt"
            case (ResultStatus.FAILURE, error):
                errors.extend(error.excs)
                code = ".Failed"

        eprint(name + code)

    if not errors:
        return

    eprint("Additionally, the following errors were detected:")

    resolution_errors = 0

    for error in errors:
        if isinstance(error, ResolutionError):
            resolution_errors += 1
        else:
            eprint(error)

    if resolution_errors > 0:
        print()
        print("...and", resolution_errors, "resulting resolution errors.")

    raise typer.Abort()
