"""This module contains the configuration for the Tasks application."""

from django import apps as django_apps


class TasksConfig(django_apps.AppConfig):
    """This class configures the Tasks application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "tasks"
