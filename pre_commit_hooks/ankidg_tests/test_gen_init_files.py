### GEN-INIT: IGNORE ###

from re import Pattern
from typing import TYPE_CHECKING, Any, TypeGuard

import pytest

if TYPE_CHECKING:
    from pre_commit_hooks.ankidg_gen_init_files.patterns import pattern_literals, patterns
else:
    from ankidg_gen_init_files.patterns import pattern_literals, patterns


def is_str_pattern(pattern: Pattern[Any]) -> TypeGuard[Pattern[str]]:
    return isinstance(getattr(pattern, "pattern", None), str)


@pytest.mark.parametrize(
    "literal_name", (key for key in pattern_literals.__dict__ if key[0] != "_")
)
def test_pattern_literals_str_and_match_pattern(literal_name: str) -> None:
    literal = getattr(pattern_literals, literal_name, None)
    pattern = getattr(patterns, literal_name, None)
    assert isinstance(literal, str)
    assert isinstance(pattern, Pattern)
    assert is_str_pattern(pattern)  # pyright: ignore[reportUnknownArgumentType]
    assert pattern.match(literal) is not None
