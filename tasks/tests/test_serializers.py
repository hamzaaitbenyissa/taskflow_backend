"""Unit tests for the serializers module."""

import pytest
from tasks import models as task_models
from tasks import serializers as task_serializers


@pytest.mark.django_db
def testTaskSerializerSerialization_whenValidDataProvided_serializesCorrectly() -> None:
    task = task_models.Task.objects.create(
        title="Test Task", description="This is a test task.", completed=False
    )
    serializer = task_serializers.TaskSerializer(task)
    serialized_data = serializer.data

    assert serialized_data["title"] == "Test Task"
    assert serialized_data["description"] == "This is a test task."
    assert serialized_data["completed"] is False
    assert "id" in serialized_data
    assert "created_at" in serialized_data
    assert "updated_at" in serialized_data


@pytest.mark.django_db
def testTaskSerializerDeserialization_whenValidDataProvided_createsTask() -> None:
    data = {
        "title": "New Task",
        "description": "This is a new task.",
        "completed": True,
    }
    serializer = task_serializers.TaskSerializer(data=data)
    is_valid = serializer.is_valid()
    task = serializer.save()

    assert is_valid is True
    assert task is not None
    assert task.title == "New Task"
    assert task.description == "This is a new task."
    assert task.completed is True


@pytest.mark.django_db
def testTaskSerializerValidation_whenInvalidDataProvided_returnsErrors() -> None:
    data = {
        "title": "",
        "description": "This is a task with no title.",
        "completed": "not_a_boolean",
    }
    serializer = task_serializers.TaskSerializer(data=data)
    is_valid = serializer.is_valid()

    assert is_valid is False
    assert "title" in serializer.errors
    assert "completed" in serializer.errors
