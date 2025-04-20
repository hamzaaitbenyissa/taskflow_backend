"""Global exception handler for the API."""

import dataclasses
from typing import Any

from rest_framework import exceptions as drf_exceptions
from rest_framework import response as drf_response
from rest_framework import status
from rest_framework.views import exception_handler as drf_exception_handler


@dataclasses.dataclass
class APIErrorPayload:
    code: str
    message: str
    http_status: int
    errors: dict | None = None

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message,
            "http_status": self.http_status,
            "errors": self.errors,
        }


class BaseAPIException(drf_exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "bad_request"

    def __init__(
        self,
        *,
        code: str,
        message: str,
        http_status: int = 400,
        errors: dict | None = None,
    ):
        self.detail = APIErrorPayload(
            code=code, message=message, http_status=http_status, errors=errors
        ).to_dict()


def handle_exception(exc: Any, context: Any) -> drf_response.Response | None:
    if isinstance(exc, drf_exceptions.ValidationError):
        return drf_response.Response(
            data=APIErrorPayload(
                code="validation_error",
                message="Given data is not valid.",
                http_status=status.HTTP_400_BAD_REQUEST,
                errors=exc.detail,
            ).to_dict(),
            status=status.HTTP_400_BAD_REQUEST,
        )

    if isinstance(exc, BaseAPIException):
        return drf_response.Response(exc.detail, status=exc.detail["http_status"])

    # Fallback to DRF default handler
    response = drf_exception_handler(exc, context)

    # format non-custom errors
    if isinstance(exc, drf_exceptions.APIException):
        return drf_response.Response(
            APIErrorPayload(
                code=exc.default_code,
                message=str(exc.detail),
                http_status=status.HTTP_400_BAD_REQUEST,
            ).to_dict(),
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Handle other exceptions
    if response is not None and isinstance(response.data, dict):
        return drf_response.Response(
            data=APIErrorPayload(
                code="unhandled_error",
                message="Unknown error occurred.",
                http_status=response.status_code,
            ).to_dict(),
            status=response.status_code,
        )

    return response
