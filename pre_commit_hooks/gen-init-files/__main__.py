import sys
from collections.abc import Iterable
from functools import partial
from pathlib import Path
from typing import Annotated

import typer

from .ast_errors import AstErrors
from .ast_tools import AstSuccess
from .async_wrapper import async_wrapper
from .init_generator import InitGenerator

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
async def main(updated_python_files: OptionalListArg = None, all: bool = False):
    sources: Iterable[Path]

    if all:
        sources = Path().glob("src/**/*.py")
    elif updated_python_files:
        sources = updated_python_files
    else:
        eprint("error: neither Python source files nor --all specified.")
        raise typer.Abort()

    sources = {source.parent for source in sources}

    ast_errors = AstErrors()

    async for path, errors in InitGenerator(sources):
        name: str
        code: str

        name = str(path).ljust(73, ".")

        match errors:
            case AstSuccess.IGNORED:
                code = "Ignored"
            case AstSuccess.REBUILT:
                code = "Rebuilt"
            case AstSuccess.SKIPPED:
                code = "Skipped"
            case _:
                code = ".Failed"
                ast_errors.extend(errors)

        eprint(name + code)

    if not ast_errors:
        return

    print("Additionally, the following errors were detected:")
    for error in ast_errors:
        eprint(error)
    raise typer.Abort()


if __name__ == "__main__":
    app()
