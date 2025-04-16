"""This module registers the Task model with the Django admin interface."""

from django.contrib import admin
from tasks import models as tasks_models


@admin.register(tasks_models.Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin interface for the Task model."""

    list_display = ("title", "completed", "created_at")
    list_filter = ("completed",)
    search_fields = ("title", "description")
