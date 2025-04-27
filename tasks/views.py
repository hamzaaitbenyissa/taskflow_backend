"""This module contains the view sets for the Task API."""

from django import http as django_http
from rest_framework import viewsets

from tasks import exceptions as tasks_exceptions
from tasks import models as tasks_models
from tasks import serializers as tasks_serializers
from rest_framework import pagination as rest_pagination
from rest_framework import response as rest_response


from rest_framework import filters as rest_filters

from django_filters import rest_framework


class CustomPageNumberPagination(rest_pagination.PageNumberPagination):
    """Custom pagination class for the Task API."""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return rest_response.Response(
            {
                "currentPage": self.page.number,
                "totalPages": self.page.paginator.num_pages,
                "pageSize": self.get_page_size(self.request),
                "tasks": data,
            }
        )


class TaskViewSet(viewsets.ModelViewSet):
    """This class provides the viewset for the Task model.
    For more information, see:
    https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
    """

    queryset = tasks_models.Task.objects.all()
    serializer_class = tasks_serializers.TaskSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [rest_filters.SearchFilter, rest_framework.DjangoFilterBackend]
    search_fields = ["title"]
    filterset_fields = ["completed"]

    def get_object(self) -> tasks_models.Task:
        """Override the get_object method to raise a custom exception when the task is not found."""
        try:
            return super().get_object()
        except django_http.Http404:
            raise tasks_exceptions.TaskNotFoundException(task_id=self.kwargs["pk"])
