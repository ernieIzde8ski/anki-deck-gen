import ast
from collections.abc import Iterable
from pathlib import Path
from typing import Generic, TypeVar

__all__ = ["AstError", "Errors"]

Exc = TypeVar("Exc", bound=Exception)


class AstError(SyntaxError):
    def __init__(self, reason: str, stmt: ast.stmt, path: Path | None) -> None:
        super().__init__()
        self.msg: str = reason
        self.lineno: int | None = stmt.lineno
        self.offset: int | None = stmt.col_offset
        self.text: str | None = ast.unparse(stmt)
        self.filename: str | None = str(path) if path else None


class ResolutionError(RuntimeError):
    """A child `__init__` file for a module failed."""


class Errors(Exception, Generic[Exc]):
    excs: list[Exc]

    def __init__(self, excs: Iterable[Exc] | None = None):
        if excs is None:
            self.excs = []
        else:
            self.excs = list(excs)
        super().__init__()

    @property
    def append(self):
        return self.excs.append

    def __bool__(self):
        return bool(self.excs)

    def __iter__(self):
        return iter(self.excs)
