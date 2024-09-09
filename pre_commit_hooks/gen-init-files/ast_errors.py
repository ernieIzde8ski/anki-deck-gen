import ast
from dataclasses import dataclass
from pathlib import Path

from typing_extensions import override

__all__ = ["AstErrors"]


@dataclass
class AstError(RuntimeError):
    path: Path
    stmt: ast.stmt
    reason: str

    @override
    def __str__(self) -> str:
        return f'File "{self.path}", line {self.stmt.lineno}: {self.reason}' + (
            "\t".join(ast.unparse(self.stmt).splitlines())
        )


class AstErrors(list[AstError]):
    pass
