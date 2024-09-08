from html import escape as html_escape

__all__ = ["html_escape", "cloze", "xml_wrap"]


def cloze(__s: str, /, level: int, hint: str | None = None) -> str:
    if hint is not None:
        return "{{" f"c{level}::{__s}::{hint}" "}}"
    else:
        return "{{" f"c{level}::{__s}" "}}"


def xml_wrap(content: str, tag: str, tag_attrs: dict[str, str] | None = None) -> str:
    """
    Wraps some content in an XML tag.

    Aside from escaping the values of the `tag_attrs` dict, no special validation
    is done. Please ensure that the input to this function is reasonable.
    """
    tag_open: str
    tag_close: str

    if tag_attrs:
        tag_open = f"<{tag}"
        for key, value in tag_attrs.items():
            tag_open += f' {key}="{html_escape(value)}"'
        tag_open += ">"
    else:
        tag_open = f"<{tag}>"

    tag_close = f"</{tag}>"

    return tag_open + content + tag_close
