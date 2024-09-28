import pydantic

__all__ = ["BaseConfig", "BaseModel"]

BaseConfig = pydantic.ConfigDict(extra="forbid")


class BaseModel(pydantic.BaseModel):
    """
    A subclass of `pydantic.BaseModel` with configuration applied.

    If configuration is specified in a child class, then that configuration
    overloads the configuration specified in this class.
    """

    model_config = BaseConfig
