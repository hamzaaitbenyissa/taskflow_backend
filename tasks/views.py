"""This module contains the view sets for the Task API."""
from django import http as django_http
from rest_framework import viewsets

from tasks import exceptions as tasks_exceptions
from tasks import models as tasks_models
from tasks import serializers as tasks_serializers


class TaskViewSet(viewsets.ModelViewSet):
    """This class provides the viewset for the Task model.
    For more information, see:
    https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
    """

    queryset = tasks_models.Task.objects.all()
    serializer_class = tasks_serializers.TaskSerializer

    def get_object(self) -> tasks_models.Task:
        """Override the get_object method to raise a custom exception when the task is not found."""
        try:
            return super().get_object()
        except django_http.Http404:
            raise tasks_exceptions.TaskNotFoundException(task_id=self.kwargs.get("pk"))
