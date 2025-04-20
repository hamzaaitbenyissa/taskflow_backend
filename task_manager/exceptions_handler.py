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
    metadata: dict | None = None

    def to_dict(self):
        return {
            "error_code": self.error_code,
            "message": self.message,
            "http_status_code": self.http_status_code,
            "metadata": self.metadata,
        }


class BaseAPIException(drf_exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "bad_request"

    def __init__(
        self,
        *,
        error_code: str,
        message: str,
        http_status_code: int = 400,
        metadata: dict | None = None,
    ):
        self.detail = APIErrorPayload(
            error_code=error_code,
            message=message,
            http_status_code=http_status_code,
            metadata=metadata,
        ).to_dict()


def handle_exception(exc: Any, context: Any) -> drf_response.Response | None:
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

    if isinstance(exc, BaseAPIException):
        return drf_response.Response(exc.detail, status=exc.detail["http_status_code"])

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
