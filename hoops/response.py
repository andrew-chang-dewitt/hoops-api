"""Encapsulate API responses."""

from __future__ import annotations
from dataclasses import dataclass
from traceback import format_exception
from typing import (
    Any,
    Dict,
    Generic,
    Hashable,
    Literal,
    Optional,
    TypeVar,
    Union
)


@dataclass
class ErrObject:
    """Encapsulate error info as data."""

    message: str
    exception_type: str
    traceback: Optional[str]

    @staticmethod
    def from_exception(exception: Exception, debug: bool = False) -> ErrObject:
        """
        Create an ErrObject.

        Includes a traceback if debug == True.
        """
        exception_type = type(exception)

        message = str(exception)
        exception_type_name: str = exception_type.__name__
        traceback = \
            "".join(format_exception(
                exception_type,
                exception,
                exception.__traceback__)) if debug else None

        return ErrObject(message=message,
                         exception_type=exception_type_name,
                         traceback=traceback)


Data = TypeVar('Data', bound=Union[Dict[Hashable, Any], ErrObject])


@dataclass
class ResponseABC(Generic[Data]):
    """Object to encapsulate API responses."""

    success: bool


@dataclass
class OkResponse(ResponseABC[Data]):
    """Encapsulate a successful response."""

    body: Dict[Hashable, Any]

    def __init__(self, body: Dict[Hashable, Any]):
        super().__init__(success=True)
        self.body = body


@dataclass
class ErrResponse(ResponseABC[ErrObject]):
    """Encapsulate an error response."""

    success: Literal[False]
    exception: ErrObject

    def __init__(self, exception: ErrObject):
        super().__init__(success=False)
        self.exception = exception

    @staticmethod
    def from_exception(exception: Exception,
                       debug: bool = False) -> ErrResponse:
        """
        Create an ErrResponse.

        Includes a traceback if debug == True.
        """
        return ErrResponse(ErrObject.from_exception(exception, debug=debug))
