from rest_framework import status

from task_manager import exceptions_handler


class TaskNotFoundException(exceptions_handler.BaseAPIException):
    """Exception raised when a task is not found."""

    def __init__(self, task_id: int):
        super().__init__(
            code="task_not_found",
            message=f"Task with id={task_id} not found.",
            http_status=status.HTTP_404_NOT_FOUND,
        )
