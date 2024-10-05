from collections.abc import Sequence
from html import escape as html_escape
from html import unescape as html_unescape
from typing import TypeGuard, overload, override

from pydantic import Field

from ankidg_core import BaseModel

__all__ = ["html_escape", "html_unescape", "cloze", "XmlTag"]


def is_str_sequence(obj: Sequence[object]) -> TypeGuard[Sequence[str]]:
    return all(isinstance(s, str) for s in obj)


class XmlTag(BaseModel):
    name: str
    attrs: dict[str, str] = Field(default_factory=dict)
    content: "list[XmlTag | str] | XmlTag | str | None" = None

    @property
    def validated_content(self) -> list["XmlTag | str"] | None:
        """Render content, if it exists, as a list."""
        if self.content is None:
            return None
        if isinstance(self.content, list):
            return self.content
        self.content = result = [self.content]
        return result

    def xml_render(self) -> str:
        """Render this tag and its children. String contents are html-escaped."""
        texts = [f"<{self.name}"]

        if self.attrs:
            rendered_attrs = " ".join(
                f'{key}="{field}"' for key, field in self.attrs.items()
            )
            texts.append(" ")
            texts.append(rendered_attrs)

        content = self.validated_content
        if content is not None:
            texts.append(">")
            for value in content:
                match value:
                    case XmlTag() as tag:
                        texts.append(tag.xml_render())
                    case str() as __s:
                        texts.append(html_escape(__s))
            texts.append(f"</{self.name}>")
        else:
            texts.append(" />")

        return "".join(texts)

    @override
    def __str__(self) -> str:
        return self.xml_render()

    def __bool__(self) -> bool:
        return True


class HtmlTag(XmlTag):
    """XmlTag with HTML-related helpers."""

    def set_class(self, name: str, /):
        """Add class to list of classes."""
        if not name:
            raise RuntimeError("name cannot be empty")
        name = html_escape(name)
        KEY = "class"
        if KEY not in self.attrs:
            self.attrs[KEY] = name
        else:
            self.attrs[KEY] += " "
            self.attrs[KEY] += name


@overload
def cloze(string: str, /, level: int, hint: str | None = None) -> str:
    """Wraps string in a cloze block."""


@overload
def cloze[T: XmlTag](tag: T, /, level: int, hint: str | None = None) -> T:
    """Wraps the tag's contents in a cloze block and returns the same tag."""


def cloze[T: XmlTag](__value: str | T, /, level: int, hint: str | None = None) -> T | str:
    start = "{{" f"c{level}::"

    if hint:
        end = f"::{hint}" "}}"
    else:
        end = "}}"

    if isinstance(__value, str):
        if not __value:
            raise RuntimeError("String passed into cloze function is empty.")
        return start + __value + end

    content = __value.validated_content

    if content is None:
        raise RuntimeError("XML tag passed into cloze function is empty.")

    content.insert(0, start)
    content.append(end)
    return __value
