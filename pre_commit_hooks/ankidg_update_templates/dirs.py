from pathlib import Path

__all__ = ["ROOT", "TEMPLATEDIR"]

ROOT = Path(__file__).parent.parent.parent.resolve()
TEMPLATEDIR = ROOT / "templates"
