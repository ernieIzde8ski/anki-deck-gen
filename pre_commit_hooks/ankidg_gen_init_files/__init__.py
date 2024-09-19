__version__ = "0.2.0"

import sys

try:
    import pytest as _
except ModuleNotFoundError:
    print("Please install anki-deck-gen[devel] to use this script.", file=sys.stderr)
    exit(1)

### GEN-INIT: TEMPLATE-START ###

__all__ = [
    "AstError",
    "Errors",
    "ExportResult",
    "InitGenerator",
    "InitResult",
    "Result",
    "ResultEmpty",
    "ResultErr",
    "ResultOk",
    "ResultStatus",
    "app",
    "async_wrapper",
    "extract_export_declarations",
    "patterns",
]

from .app import app
from .async_wrapper import async_wrapper
from .error import AstError, Errors
from .export_declarations import ExportResult, extract_export_declarations
from .init_generator import InitGenerator, InitResult
from .patterns import patterns
from .result import Result, ResultEmpty, ResultErr, ResultOk, ResultStatus

### GEN-INIT: TEMPLATE-CLOSE ###
