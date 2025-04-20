"""Unit tests for exceptions_handler.py."""


from rest_framework import exceptions as rest_framework_exceptions
from rest_framework import status

from task_manager import exceptions_handler
from tasks import exceptions as tasks_exceptions


def testHandleException_whenValidationError_thenReturns400():
    """Test that handle_exception returns 400 for ValidationError."""
    exception = exceptions_handler.BaseAPIException(
        code="validation_error",
        message="Given data is not valid.",
        http_status=status.HTTP_400_BAD_REQUEST,
        errors={"title": ["This field is required."]},
    )

    response = exceptions_handler.handle_exception(exception, None)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        "code": "validation_error",
        "message": "Given data is not valid.",
        "http_status": status.HTTP_400_BAD_REQUEST,
        "errors": {"title": ["This field is required."]},
    }


def testHandleException_whenBaseAPIException_returnsCustomResponse():
    """Test that handle_exception returns custom response for BaseAPIException."""
    exception = tasks_exceptions.TaskNotFoundException(task_id=1)

    response = exceptions_handler.handle_exception(exception, None)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data == {
        "code": "task_not_found",
        "message": "Task with id=1 not found.",
        "http_status": status.HTTP_404_NOT_FOUND,
        "errors": None,
    }


def testHandleException_whenNonBaseAPIException_returnsCorrectResponse():
    """Test that handle_exception returns correct response for non-custom BaseAPIException."""
    exception = rest_framework_exceptions.APIException(
        detail="Custom error message.",
        code="custom_error",
    )

    response = exceptions_handler.handle_exception(exception, None)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        "code": "error",
        "message": "Custom error message.",
        "http_status": status.HTTP_400_BAD_REQUEST,
        "errors": None,
    }
