import ast
import re
from pathlib import Path
from typing import overload

from .error import AstError
from .patterns import patterns
from .result import Result, ResultStatus

__all__ = ["extract_export_declarations", "ExportResult"]

ExportResult = Result[list[str], AstError]


@overload
def extract_export_declarations(path: Path, /) -> ExportResult:
    """Parses the AST at the given path and searches it for an `__all__` declaration."""


@overload
def extract_export_declarations(text: str, /) -> ExportResult:
    """Parses the given AST and searches it for an `__all__` declaration."""


def extract_export_declarations(arg0: Path | str, /) -> ExportResult:
    if isinstance(arg0, Path):
        path = arg0
        module_contents = arg0.read_text()
    else:
        path = None
        module_contents = arg0

    if re.search(patterns.DirectiveIgnore, module_contents):
        return (ResultStatus.IGNORED, None)

    module = ast.parse(module_contents)

    for stmt in module.body:
        if not isinstance(stmt, ast.Assign):
            continue

        for target in stmt.targets:
            if isinstance(target, ast.Name) and target.id == "__all__":
                break
        else:
            # the inner loop wasn't broken, so this is not an assignment to `__all__`
            # check the next assignment instead
            continue

        if not isinstance(stmt.value, ast.List):
            err = AstError("`__all__` should be a list of literal strings.", stmt, path)
            return (ResultStatus.FAILURE, err)

        result: list[str] = []
        for item in stmt.value.elts:
            if isinstance(item, ast.Constant) and isinstance(
                item.value, str  # pyright: ignore[reportAny]
            ):
                result.append(item.value)
            else:
                return (
                    ResultStatus.FAILURE,
                    AstError("Invalid assignment to __all__", stmt, path),
                )

        return (ResultStatus.SUCCESS, result)

    return (ResultStatus.SKIPPED, None)
