"""This module defines the URL routing for the tasks application."""

from django.urls import path, include
from rest_framework import routers as rest_routers
from tasks import views as tasks_views

router = rest_routers.DefaultRouter()
router.register(r"tasks", tasks_views.TaskViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
