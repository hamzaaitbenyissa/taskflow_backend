"""Global exception handler for the API."""

import dataclasses
from typing import Any

from rest_framework import exceptions as drf_exceptions
from rest_framework import response as drf_response
from rest_framework import status
from rest_framework.views import exception_handler as drf_exception_handler


@dataclasses.dataclass
class APIErrorPayload:
    error_code: str
    message: str
    http_status_code: int
    metadata: dict | list | None = None

    def to_dict(self):
        """Convert the dataclass to a dictionary."""
        if isinstance(self.metadata, list):
            self.metadata = {"errors": self.metadata}
        return {
            "error_code": self.error_code,
            "message": self.message,
            "http_status_code": self.http_status_code,
            "metadata": self.metadata,
        }


class Error(Exception):
    """Base class for all exceptions in the API."""

    pass


class BaseAPIError(Error):
    http_status_code: int = status.HTTP_400_BAD_REQUEST
    default_detail = "An error occurred."
    error_code: str
    message: str
    metadata: dict | list | None = None

    def __init__(
        self,
        error_code="bad_request",
        message="Something went wrong.",
        http_status_code=status.HTTP_400_BAD_REQUEST,
        metadata=None,
    ):
        self.error_code = error_code
        self.message = message or self.default_detail
        self.http_status_code = http_status_code
        self.metadata = metadata or None

    @property
    def detail(self):
        """Return the error details."""
        return APIErrorPayload(
            error_code=self.error_code,
            message=self.message,
            http_status_code=self.http_status_code,
            metadata=self.metadata,
        ).to_dict()


def handle_exception(exc: Any, context: Any) -> drf_response.Response | None:
    if isinstance(exc, BaseAPIError):
        return drf_response.Response(data=exc.detail, status=exc.http_status_code)

    if isinstance(exc, drf_exceptions.ValidationError):
        return drf_response.Response(
            data=APIErrorPayload(
                error_code="validation_error",
                message="Given data is not valid.",
                http_status_code=status.HTTP_400_BAD_REQUEST,
                metadata=exc.detail,
            ).to_dict(),
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Fallback to DRF default handler
    response = drf_exception_handler(exc, context)

    # format non-custom errors
    if isinstance(exc, drf_exceptions.APIException):
        return drf_response.Response(
            APIErrorPayload(
                error_code=exc.default_code,
                message=str(exc.detail),
                http_status_code=status.HTTP_400_BAD_REQUEST,
            ).to_dict(),
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Handle other exceptions
    if response is not None and isinstance(response.data, dict):
        return drf_response.Response(
            data=APIErrorPayload(
                error_code="unhandled_error",
                message="Unknown error occurred.",
                http_status_code=response.status_code,
            ).to_dict(),
            status=response.status_code,
        )

    return response
