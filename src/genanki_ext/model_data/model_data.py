from pathlib import Path

from ..str_classes import Model
from .metadata import Metadata

__all__ = ["read_model"]


ModelDataDir = Path(__file__).parent


def read_model(name: str) -> Model:
    src = ModelDataDir / name
    metadata_file = src / "metadata.json"

    if not metadata_file.exists():
        raise RuntimeError(
            f"Missing metadata file for anki model with name: {name}"
            f"\n\tExpected file at: {metadata_file}"
        )

    data = metadata_file.read_bytes()
    return Metadata.model_validate_json(data).resolve(src)
