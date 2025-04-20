from rest_framework import status

from task_manager import exceptions_handler


class TaskNotFoundException(exceptions_handler.BaseAPIError):
    def __init__(self, task_id: int):
        super().__init__(
            error_code="task_not_found",
            message=f"Task with id={task_id} not found.",
            http_status_code=status.HTTP_404_NOT_FOUND,
        )
