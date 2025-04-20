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
    assert json.loads(response.content) == {
        "code": "validation_error",
        "errors": {"title": ["This field is required."]},
        "http_status": 400,
        "message": "Given data is not valid.",
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
    assert json.loads(response.content) == {
        "code": "validation_error",
        "errors": {"description": ["This field is required."]},
        "http_status": 400,
        "message": "Given data is not valid.",
    }
    assert task_models.Task.objects.count() == 0


@pytest.mark.django_db
def testGetTaskById_whenTaskExists_returnsTask(mocker, client) -> None:
    mocker.patch(
        "django.utils.timezone.now", return_value="2025-04-20T10:19:36.142755Z"
    )
    task = task_models.Task.objects.create(
        title="Task 1", description="Description 1", completed=False
    )
    response = client.get(
        reverse("task-detail", args=[task.id]),
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content) == {
        "completed": False,
        "created_at": "2025-04-20T10:19:36.142755Z",
        "description": "Description 1",
        "id": 1,
        "title": "Task 1",
        "updated_at": "2025-04-20T10:19:36.142755Z",
    }


@pytest.mark.django_db
def testGetTaskById_whenTaskDoesNotExist_returnsTaskNotFound(client) -> None:
    response = client.get(
        reverse("task-detail", args=[999]),
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert json.loads(response.content) == {
        "code": "task_not_found",
        "http_status": 404,
        "message": "Task with id=999 not found.",
        "errors": None,
    }


@pytest.mark.django_db
def testUpdateTask_whenTaskDoesNotExist_returnsTaskNotFound(client) -> None:
    data = {
        "title": "Updated Task",
        "description": "Updated Description",
        "completed": True,
    }

    response = client.put(
        reverse("task-detail", args=[999]),
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert json.loads(response.content) == {
        "code": "task_not_found",
        "http_status": 404,
        "message": "Task with id=999 not found.",
        "errors": None,
    }


@pytest.mark.django_db
def testDeleteTask_whenTaskDoesNotExist_returnsTaskNotFound(client) -> None:
    response = client.delete(
        reverse("task-detail", args=[999]),
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert json.loads(response.content) == {
        "code": "task_not_found",
        "http_status": 404,
        "message": "Task with id=999 not found.",
        "errors": None,
    }
