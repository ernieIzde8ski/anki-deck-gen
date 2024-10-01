from collections.abc import Iterator, MutableMapping
from typing import Self, TypeVar

from typing_extensions import Callable, override

_KT = TypeVar("_KT")
_VT = TypeVar("_VT")

MutMap = MutableMapping[_KT, _VT]
type Factory[ReturnType] = Callable[[], ReturnType]

__all__ = ["MutMapDefaultView"]


Uninstantiated = RuntimeError(
    "This field cannot be accessed outside of the class instance."
)


class MutMapDefaultView(MutMap[_KT, _VT]):
    """A view over a MutableMapping with defaultdict features."""

    # This will always be set, thanks to
    __source_map: MutMap[_KT, _VT]  # pyright: ignore[reportUninitializedInstanceVariable]

    @property
    def source_map(self) -> MutMap[_KT, _VT]:
        return self.__source_map

    @source_map.setter
    def source_map(self, __source_map: MutMap[_KT, _VT]) -> None:
        self.__source_map = __source_map
        self.__len__ = __source_map.__len__
        self.__setitem__ = __source_map.__setitem__
        self.__delitem__ = __source_map.__delitem__

    def __init__(
        self, source: MutMap[_KT, _VT], *, default_factory: Factory[_VT]
    ) -> None:
        self.source_map = source
        self.default_factory = default_factory

    @classmethod
    def from_default_value(cls, source: MutMap[_KT, _VT], *, default: _VT) -> Self:
        return cls(source, default_factory=lambda: default)

    @override
    def __getitem__(self, key: _KT, /) -> _VT:
        try:
            return self.source_map[key]
        except KeyError:
            self[key] = resp = self.default_factory()
            return resp

    @override
    def __iter__(self) -> Iterator[_KT]:
        return iter(self.source_map)

    @override
    def __len__(self) -> int:
        raise Uninstantiated

    @override
    def __setitem__(self, key: _KT, value: _VT, /) -> None:
        raise Uninstantiated

    @override
    def __delitem__(self, key: _KT, /) -> None:
        raise Uninstantiated
