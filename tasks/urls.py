"""This module defines the URL routing for the tasks application."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks import views as tasks_views

router = DefaultRouter()
router.register(r"tasks", tasks_views.TaskViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
