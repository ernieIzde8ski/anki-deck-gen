from pathlib import Path

__all__ = ["ROOT", "MEDIA", "media"]

ROOT = Path(__file__).parent.parent.parent.resolve()
MEDIA = ROOT / "media"

media = MEDIA.joinpath
