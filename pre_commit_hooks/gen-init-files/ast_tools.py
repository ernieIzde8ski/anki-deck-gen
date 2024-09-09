import ast
import enum
from pathlib import Path

from .ast_errors import AstError

__all__ = ["AstSuccess", "extract_export_declarations"]


class AstSuccess(enum.Enum):
    REBUILT = enum.auto()
    IGNORED = enum.auto()
    SKIPPED = enum.auto()


class ExportDeclarations(list[str]): ...


def extract_literal_string_list(value: ast.expr) -> ExportDeclarations | None:
    """
    Validates that an expression is a list containing string literals.
    If not true, returns `None`.
    """
    if isinstance(value, ast.List):
        arr = ExportDeclarations()
        for item in value.elts:
            if isinstance(item, ast.Constant) and isinstance(
                item.value, str  # pyright: ignore[reportAny]
            ):
                arr.append(item.value)
            else:
                break
        else:
            return arr


def extract_export_declarations(path: Path):
    """Parses the AST at the given path and searches it for an `__all__` declaration."""
    result: ExportDeclarations | None = None

    text = path.read_text()
    module = ast.parse(text)

    # TODO: some kind of "# gen-init-ignore" comment
    assignments = (stmt for stmt in module.body if isinstance(stmt, ast.Assign))

    for assignment in assignments:
        target_names = (t.id for t in assignment.targets if isinstance(t, ast.Name))

        if "__all__" not in target_names:
            continue

        may8e_list = extract_literal_string_list(assignment.value)
        if may8e_list is None:

            return AstError(path, assignment, "Invalid assignment to __all__")
        else:
            result = may8e_list
        break

    return result
