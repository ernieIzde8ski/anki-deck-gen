import asyncio
import logging
import re
from collections.abc import AsyncGenerator, Iterable
from pathlib import Path
from typing import TypeVar

from black import Mode, format_str
from black.mode import TargetVersion

from .error import AstError, Errors, ResolutionError
from .export_declarations import extract_export_declarations
from .patterns import pattern_literals, patterns
from .result import Result, ResultStatus

T = TypeVar("T")

__all__ = ["InitResult", "InitGenerator"]

InitResult = Result[None, Errors[AstError | ResolutionError]]


class InitGenerator:
    """Generates `__init__.py` files for a set of directories."""

    __tasks: dict[Path, asyncio.Task[InitResult]]

    def __init__(self, dirs: Iterable[Path]) -> None:
        self.__tasks = tasks = {}
        for dir in dirs:
            task = asyncio.create_task(self.__generate_init_file(dir))
            tasks[dir] = task

    @staticmethod
    def __find_relative_imports(dir: Path) -> Iterable[tuple[Path, str]]:
        """Finds relative imports within a module."""
        for path in dir.iterdir():
            if (
                path.is_dir()
                and re.match(patterns.PythonImportModule, path.name)
                and (path / "__init__.py").exists()
            ):
                yield (path / "__init__.py", path.name)
            elif (
                path.is_file()
                and re.match(patterns.PythonImportFile, path.name) is not None
            ):
                yield (path, path.name.removesuffix(path.suffix))

    @staticmethod
    def __sort_key(s: str) -> tuple[bool, str]:
        return (not s.isupper(), s)

    @classmethod
    def __generate_template_text(cls, import_module_data: dict[str, list[str]]) -> str:
        """Generate the `__all__ = [...]`, `from .foo import bar` text."""
        export_names: list[str] = []
        import_froms: list[str] = []

        sort_key = cls.__sort_key
        import_module_names = sorted(import_module_data, key=sort_key)

        for mod_name in import_module_names:
            import_values = sorted(import_module_data[mod_name], key=sort_key)

            if not import_values:
                continue

            export_names.extend(import_module_data[mod_name])

            import_from = f"from .{mod_name} import " + ", ".join(import_values)
            import_froms.append(import_from)

        export_names.sort(key=sort_key)
        export_names_stmt = "__all__ = [" + ", ".join(repr(i) for i in export_names) + "]"

        res = (
            pattern_literals.DirectiveTemplateStart,
            "",
            export_names_stmt,
            "",
            *import_froms,
            "",
            pattern_literals.DirectiveTemplateClose,
        )

        return format_str(
            "\n".join(res),
            mode=Mode(
                line_length=90,
                target_versions={
                    TargetVersion.PY310,
                    TargetVersion.PY311,
                    TargetVersion.PY312,
                },
                magic_trailing_comma=False,
            ),
        )

    async def __generate_init_file(self, dir: Path) -> InitResult:
        imports: dict[str, list[str]] = {}
        errors: Errors[AstError | ResolutionError] = Errors()

        for path, import_module_name in self.__find_relative_imports(dir):
            # resolve dependencies on other things that should be updated
            if path.name == "__init__.py":
                task = self.__tasks.get(path.parent)
                if task and not task.done():
                    logging.debug(
                        f"{dir.name}: waiting on resolution of {import_module_name}"
                    )
                    task_code, _ = await task
                    if task_code == ResultStatus.FAILURE:
                        errors.append(ResolutionError())
                        continue

            res = extract_export_declarations(path)
            match res:
                case (ResultStatus.SUCCESS, import_values):
                    imports[import_module_name] = import_values
                case (ResultStatus.FAILURE, error):
                    errors.append(error)
                case (ResultStatus.IGNORED, _):
                    # module had an explicit ignore directive
                    pass
                case (ResultStatus.SKIPPED, _):
                    logging.warning(
                        f"missing `__all__` attribute or {pattern_literals.DirectiveIgnore} directive in {path}"
                    )
            logging.debug(f"{dir.name}: scanned {import_module_name}")

        if errors:
            return (ResultStatus.FAILURE, errors)

        init_path = dir / "__init__.py"
        template_text = self.__generate_template_text(imports)

        if not init_path.exists():
            _ = init_path.write_text(template_text)
            return (ResultStatus.SKIPPED, None)
        else:
            old_file_text = init_path.read_text()
            old_file_lines = iter(old_file_text.splitlines())
            new_file_lines: list[str] = []

            for line in old_file_lines:
                stripped = line.strip()
                if re.match(patterns.DirectiveTemplateStart, stripped):
                    break
                elif re.match(patterns.DirectiveIgnore, stripped):
                    return (ResultStatus.IGNORED, None)
                else:
                    new_file_lines.append(line)

            new_file_lines.append(template_text)

            for line in old_file_lines:
                if re.match(patterns.DirectiveTemplateClose, line.strip()):
                    break

            new_file_lines.extend(old_file_lines)
            new_file_text = "\n".join(new_file_lines)
            if old_file_text == new_file_text:
                return (ResultStatus.SKIPPED, None)
            else:
                _ = init_path.write_text(new_file_text)
                return (ResultStatus.SUCCESS, None)

    async def __aiter__(self) -> AsyncGenerator[tuple[Path, InitResult]]:
        for path, callback in self.__tasks.items():
            yield (path, await callback)
