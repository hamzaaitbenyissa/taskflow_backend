"""Unit tests for the views module."""

import json

import pytest
from django.urls import reverse
from rest_framework import status

from tasks import models as task_models


@pytest.mark.django_db
def testTaskViewSetCreate_whenValidDataProvided_createsTask(client) -> None:
    data = {"title": "New Task", "description": "New Description", "completed": False}

    response = client.post(
        reverse("task-list"),
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert task_models.Task.objects.count() == 1
    task = task_models.Task.objects.first()
    assert isinstance(task, task_models.Task)
    assert task.title == "New Task"
    assert task.description == "New Description"
    assert task.completed is False


@pytest.mark.django_db
def testTaskViewSetUpdate_whenValidDataProvided_updatesTask(client) -> None:
    task = task_models.Task.objects.create(
        title="Task 1", description="Description 1", completed=False
    )
    data = {
        "title": "Updated Task",
        "description": "Updated Description",
        "completed": True,
    }

    response = client.put(
        reverse("task-detail", args=[task.id]),
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_200_OK
    task.refresh_from_db()
    assert task.title == "Updated Task"
    assert task.description == "Updated Description"
    assert task.completed is True


@pytest.mark.django_db
def testTaskViewSetDelete_whenTaskExists_deletesTask(client) -> None:
    task = task_models.Task.objects.create(
        title="Task 1", description="Description 1", completed=False
    )

    response = client.delete(
        reverse("task-detail", args=[task.id]),
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert task_models.Task.objects.count() == 0


@pytest.mark.django_db
def testTaskViewSetCreate_whenTitleIsMissing_returnsBadRequest(client) -> None:
    data = {"description": "New Description", "completed": False}

    response = client.post(
        reverse("task-list"),
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        "title": ["This field is required."],
    }
    assert task_models.Task.objects.count() == 0


@pytest.mark.django_db
def testTaskViewSetCreate_whenDescriptionIsMissing_returnsBadRequest(client) -> None:
    data = {"title": "New Task", "completed": False}

    response = client.post(
        reverse("task-list"),
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {
        "description": ["This field is required."],
    }
    assert task_models.Task.objects.count() == 0
