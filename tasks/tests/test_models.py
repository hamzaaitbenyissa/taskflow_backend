"""Unit tests for the models module."""

import pytest
from tasks import models as task_models


@pytest.mark.django_db
def testTaskCreation_whenValidDataProvided_createsTask() -> None:
    """Test creating a Task instance."""

    title: str = "Test Task"
    description: str = "This is a test task."
    completed: bool = False

    task = task_models.Task.objects.create(
        title=title, description=description, completed=completed
    )

    assert task.title == title
    assert task.description == description
    assert task.completed is completed
    assert task.created_at is not None
    assert task.updated_at is not None


@pytest.mark.django_db
def testTaskDefaultCompleted_whenNoValueProvided_defaultsToFalse() -> None:
    """Test that the default value of 'completed' is False."""

    title: str = "Default Completed Test"
    description: str = "Testing default completed value."

    task = task_models.Task.objects.create(title=title, description=description)

    assert task.completed is False


@pytest.mark.django_db
def testTaskStringRepresentation_whenCalled_returnsTitle() -> None:
    """Test the string representation of a Task instance."""

    title: str = "String Representation Test"
    description: str = "Testing string representation."

    task = task_models.Task.objects.create(title=title, description=description)

    assert str(task) == title


@pytest.mark.django_db
def testTaskOrdering_whenMultipleTasksCreated_ordersByCreatedAtDesc() -> None:
    """Test that tasks are ordered by '-created_at'."""

    task1 = task_models.Task.objects.create(title="Task 1", description="First task.")
    task2 = task_models.Task.objects.create(title="Task 2", description="Second task.")

    tasks = task_models.Task.objects.all()

    assert tasks[0] == task2
    assert tasks[1] == task1
