import enum

__all__ = ["ResultStatus"]


class ResultStatus(enum.Enum):
    SUCCESS = enum.auto()
    """Module was operated on without errors."""
    FAILURE = enum.auto()
    """Some exception occurred."""
    IGNORED = enum.auto()
    """Module contained an explicit ignore directive."""
    SKIPPED = enum.auto()
    """Module had no pertinent information, or module depended on failed module."""
