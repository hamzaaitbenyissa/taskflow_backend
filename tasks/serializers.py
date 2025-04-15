"""This module contains the serializers for the Task model."""

from rest_framework import serializers
from tasks import models as tasks_models


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = tasks_models.Task
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
