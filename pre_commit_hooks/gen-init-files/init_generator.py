import asyncio
import re
from collections.abc import AsyncGenerator, Iterable
from pathlib import Path

from black import Mode, format_str
from black.mode import TargetVersion

from .ast_errors import AstError, AstErrors
from .ast_tools import AstSuccess, ExportDeclarations, extract_export_declarations

__all__ = ["InitGenerator"]

PythonImportModule = re.compile(r"^[A-Za-z][A-Za-z_]+$")
PythonImportFile = re.compile(r"^[A-Za-z][A-Za-z_]+\.py$")


class InitGenerator:
    """Generates `__init__.py` files for a set of directories."""

    __tasks: dict[Path, asyncio.Task[AstSuccess | AstErrors]]

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
                and re.match(PythonImportModule, path.name)
                and (path / "__init__.py").exists()
            ):
                yield (path / "__init__.py", path.name)
            elif path.is_file() and re.match(PythonImportFile, path.name) is not None:
                yield (path, path.name.removesuffix(path.suffix))

    @classmethod
    def __generate_template_text(cls, exports: dict[str, ExportDeclarations]) -> str:
        lines = ["### START GEN-INIT TEMPLATE ###\n", "__all__ = ["]

        for import_name, export_declarations in exports.items():
            lines[1] += '"' + '", "'.join(export_declarations) + '",'
            line = f"from .{import_name} import " + ", ".join(export_declarations)
            lines.append(line)
        lines[1] += "]\n"

        lines.append("### END GEN-INIT TEMPLATE ###")

        return format_str(
            "\n".join(lines),
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

    async def __generate_init_file(self, dir: Path) -> AstSuccess | AstErrors:
        exports: dict[str, ExportDeclarations] = {}
        errors = AstErrors()
        for path, import_name in self.__find_relative_imports(dir):
            task = self.__tasks.get(path.parent) if path.name == "__init__.py" else None
            if task and not task.done():
                print(f"{dir.name}: waiting on resolution of {import_name}")
                res = await task
                if isinstance(res, AstErrors):
                    return AstSuccess.IGNORED

            res = extract_export_declarations(path)
            if isinstance(res, AstError):
                errors.append(res)
            elif res is None:
                print("\tWARNING: missing `__all__` attribute in", path)
            else:
                exports[import_name] = res

            print(f"{dir.name}: scanned {import_name}")

        if errors:
            return errors

        init_path = dir / "__init__.py"
        template_text = self.__generate_template_text(exports)

        if not init_path.exists():
            _ = init_path.write_text(template_text)
            return AstSuccess.REBUILT
        else:
            old_file_text = init_path.read_text()
            old_file_lines = iter(old_file_text.splitlines())
            new_file_lines: list[str] = []

            for line in old_file_lines:
                if re.match(
                    r"###\s*START GEN-INIT TEMPLATE\s*###", line.strip(), re.IGNORECASE
                ):
                    break
                else:
                    new_file_lines.append(line)

            new_file_lines.append(template_text)

            for line in old_file_lines:
                if re.match(
                    r"###\s*END GEN-INIT TEMPLATE\s*###", line.strip(), re.IGNORECASE
                ):
                    break

            new_file_lines.extend(old_file_lines)
            new_file_text = "\n".join(new_file_lines)
            if old_file_text == new_file_text:
                return AstSuccess.IGNORED
            else:
                _ = init_path.write_text(new_file_text)
                return AstSuccess.REBUILT

    async def __aiter__(self) -> AsyncGenerator[tuple[Path, AstSuccess | AstErrors]]:
        for path, callback in self.__tasks.items():
            yield (path, await callback)
