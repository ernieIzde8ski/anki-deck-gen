__all__ = ["OptionalKey", "RequiredKey", "StrMixin", "indent"]

from collections.abc import Iterable, Sequence
from typing import NewType, cast

from typing_extensions import override

from .reiterator import Reiterator

OptionalKey = NewType("OptionalKey", str)


class RequiredKey(str): ...


class StrMixin:
    _repr_keys: Sequence[OptionalKey | RequiredKey] | None = None

    def __str_items__(self) -> Iterable[tuple[str, object]]:
        if self._repr_keys:
            for key in self._repr_keys:
                value = getattr(self, key, None)
                if value is None and not isinstance(key, RequiredKey):
                    continue
                yield (cast(str, key), value)
        else:
            for key, value in self.__dict__.items():  # pyright: ignore[reportAny]
                if key.startswith("_") or value is None:
                    continue
                yield (key, value)

    @staticmethod
    def _str_other(key: str, obj: object) -> str:
        if isinstance(obj, (str, bytes)):
            return f"{key}={obj!r}"
        elif isinstance(obj, list):
            arr = cast(list[object], obj)
            if len(arr) > 2:
                types = {type(e).__name__ for e in arr}
                return f"{key}: list[{' | '.join(types)}]"
        elif isinstance(obj, set):
            arr = cast(set[object], obj)
            if len(arr) > 2:
                types = {type(e).__name__ for e in arr}
                return f"{key}: set[{' | '.join(types)}]"
        elif isinstance(obj, dict):
            map = cast(dict[object, object], obj)
            if len(map) > 0:
                return f"{key}: " "{...}"
        # fallback to the regular __str__
        return f"{key}={obj}"

    @override
    def __str__(self) -> str:
        res: str = type(self).__name__ + "("
        interior_variables_added = False

        for key, value in self.__str_items__():
            if interior_variables_added:
                res += ", "
            else:
                interior_variables_added = True

            res += self._str_other(key, value)

        return res + ")"

    @override
    def __repr__(self) -> str:
        """Like `__str__`, though decidedly more verbose"""
        res: str = type(self).__name__ + "("
        interior_variables_added = False
        completed = False

        items_generator = ((item[0], repr(item[1])) for item in self.__str_items__())
        items = Reiterator(items_generator)

        for key, value in items:
            if interior_variables_added:
                res += ", "
            else:
                interior_variables_added = True

            res += f"{key} = {value}"
            if len(res) > 90:
                break
        else:
            completed = True

        if completed is False:
            res = type(self).__name__ + "("
            for key, value in items:
                value = indent(value, indent_first_line=False)
                res += f"\n\t{key} = {value},"

        return res + ")"


def indent(
    __s: str, token: str = "\t", count: int | None = None, indent_first_line: bool = True
):
    if count is not None:
        token = token * count
    if indent_first_line:
        return token + token.join(__s.splitlines(keepends=True))
    else:
        return token.join(__s.splitlines(keepends=True))
