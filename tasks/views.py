"""This module contains the viewsets for the Task API."""

from rest_framework import viewsets
from tasks import models as tasks_models
from tasks import serializers as tasks_serializers


class TaskViewSet(viewsets.ModelViewSet):
    queryset = tasks_models.Task.objects.all()
    serializer_class = tasks_serializers.TaskSerializer
