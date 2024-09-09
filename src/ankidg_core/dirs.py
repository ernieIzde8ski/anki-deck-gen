from pathlib import Path

__all__ = ["ROOT", "MEDIA", "media", "TARGET", "target"]

ROOT = Path(__file__).parent.parent.parent.resolve()

MEDIA = ROOT / "media"
TARGET = ROOT / "target"

media = MEDIA.joinpath
target = TARGET.joinpath
