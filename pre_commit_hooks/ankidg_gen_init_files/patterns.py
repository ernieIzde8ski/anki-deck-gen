import re

from typing_extensions import LiteralString

__all__ = ["patterns"]


def compile_comment_literal(title: LiteralString):
    return f"### GEN-INIT: {title} ###"


def compile_comment(title: LiteralString, /):
    pattern = r"^\s*###\s*GEN-INIT:\s*" + re.escape(title) + r"\s*### *$"
    return re.compile(pattern, re.IGNORECASE | re.MULTILINE)


class pattern_literals:
    DirectiveIgnore = compile_comment_literal("IGNORE")
    DirectiveTemplateStart = compile_comment_literal("TEMPLATE-START")
    DirectiveTemplateClose = compile_comment_literal("TEMPLATE-CLOSE")


# fixed an import resolution issue
# don't ask me why, I don't entirely know
class patterns:
    PythonImportModule = re.compile(r"^[A-Za-z][A-Za-z_]+$")
    PythonImportFile = re.compile(r"^[A-Za-z][A-Za-z_]+\.py$")

    DirectiveIgnore = compile_comment("IGNORE")
    DirectiveTemplateStart = compile_comment("TEMPLATE-START")
    DirectiveTemplateClose = compile_comment("TEMPLATE-CLOSE")
