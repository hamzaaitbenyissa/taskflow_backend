"""This module defines the Task model for the application."""

from django.db import models


class Task(models.Model):
    """
    Model representing a task in the application.
    Each task has a title, description, completion status, and timestamps for creation and last update.
    Attributes:
        title (str): The title of the task.
        description (str): A detailed description of the task.
        completed (bool): Indicates if the task is completed.
        created_at (datetime): Timestamp when the task was created.
        updated_at (datetime): Timestamp when the task was last updated.
    """

    title = models.CharField(max_length=255)
    description = models.TextField(
        verbose_name="Task Description",
        help_text="Provide a detailed description of the task.",
    )
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """
        String representation of the Task instance.
        """
        return self.title

    class Meta:
        """Metaclass for Task model."""

        ordering = ["-created_at"]
