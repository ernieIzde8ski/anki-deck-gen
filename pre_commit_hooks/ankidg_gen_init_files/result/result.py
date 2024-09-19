from typing import Literal, TypeVar

from .result_status import ResultStatus

__all__ = ["Result", "ResultErr", "ResultOk", "ResultEmpty"]

Rs = TypeVar("Rs", bound=ResultStatus)
E = TypeVar("E", bound=Exception)
T = TypeVar("T")
ResultItem = tuple[Rs, T]

ResultOk = ResultItem[Literal[ResultStatus.SUCCESS], T]
ResultErr = ResultItem[Literal[ResultStatus.FAILURE], E]
ResultEmpty = ResultItem[Literal[ResultStatus.IGNORED, ResultStatus.SKIPPED], None]

Result = ResultOk[T] | ResultErr[E] | ResultEmpty
