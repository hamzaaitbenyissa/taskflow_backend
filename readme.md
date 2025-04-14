# Task Flow Backend Design

## Django Project Structure
```
task_manager/
├── manage.py
├── task_manager/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── tasks/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── requirements.txt
```

## Data Model
```python
# tasks/models.py
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
```

## API Design

### HTTP Method Usage

#### GET /tasks/
**Purpose**: Retrieve all tasks
**Implementation**:
- Returns complete list of tasks
- Example Response:
```json
[
    {
        "id": 1,
        "title": "Task 1",
        "description": "First task",
        "completed": false,
        "created_at": "2025-04-14T10:00:00Z",
        "updated_at": "2025-04-14T10:00:00Z"
    }
]
```

#### POST /tasks/
**Purpose**: Create a new task
**Implementation**:
- Validates required fields (title, description)
- Sets default `completed` status to false
- Example Request:
```json
{
    "title": "New Task",
    "description": "Task description"
}
```
- Example Response:
```json
{
    "id": 2,
    "title": "New Task",
    "description": "Task description",
    "completed": false,
    "created_at": "2025-04-14T10:05:00Z",
    "updated_at": "2025-04-14T10:05:00Z"
}
```

#### GET /tasks/<id>/
**Purpose**: Retrieve a single task
**Implementation**:
- Returns complete task details
- Returns 404 if task not found
- Example Response:
```json
{
    "id": 1,
    "title": "Task 1",
    "description": "First task",
    "completed": false,
    "created_at": "2025-04-14T10:00:00Z",
    "updated_at": "2025-04-14T10:00:00Z"
}
```

#### PUT /tasks/<id>/
**Purpose**: Update an existing task
**Implementation**:
- Validates input data
- Updates all provided fields
- Returns updated task
- Example Request:
```json
{
    "title": "Updated Task",
    "description": "Updated description",
    "completed": true
}
```
- Example Response:
```json
{
    "id": 1,
    "title": "Updated Task",
    "description": "Updated description",
    "completed": true,
    "created_at": "2025-04-14T10:00:00Z",
    "updated_at": "2025-04-14T10:10:00Z"
}
```

#### DELETE /tasks/<id>/
**Purpose**: Delete a task
**Implementation**:
- Deletes task if exists
- Returns 204 No Content on success
- Returns 404 if task not found

### Serializer
```python
# tasks/serializers.py
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
```

### ViewSet
```python
# tasks/views.py
from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
```

### URL Configuration
```python
# tasks/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
```

### Versioning Strategy
1. **URL Versioning**: Version included in the URL path (e.g., /api/v1/tasks/)
2. **Default Version**: v1 as the initial version
3. **Future Versions**:
   - New versions will be added as v2, v3, etc.

### Example Versioned Endpoints
| Version | Endpoint                     |
|---------|------------------------------|
| v1      | /api/v1/tasks/               |
| v1      | /api/v1/tasks/{id}/          |
| v2      | /api/v2/tasks/               | (future)
| v2      | /api/v2/tasks/{id}/          | (future)

## Error Handling

### Standard Error Responses
All error responses follow this format:
```json
{
    "error": {
        "code": "error_code",
        "message": "Human-readable error message",
        "details": {
            // Optional field for additional error details
        }
    }
}
```

### Example Error Responses
```json
// 400 Bad Request (Validation Error)
{
    "error": {
        "code": "validation_error",
        "message": "Invalid input data",
        "details": {
            "title": ["This field is required."],
            "description": ["This field is required."]
        }
    }
}

// 404 Not Found
{
    "error": {
        "code": "not_found",
        "message": "The requested task was not found"
    }
}

// 500 Internal Server Error
{
    "error": {
        "code": "server_error",
        "message": "An unexpected error occurred. Please try again later."
    }
}
```

### Implementation
To implement this standardized error handling, we'll create a custom exception handler:

```python
# task_manager/exceptions.py
from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        error_data = {
            'error': {
                'code': exc.get_codes() if hasattr(exc, 'get_codes') else 'error',
                'message': str(exc),
                'details': response.data if isinstance(response.data, dict) else None
            }
        }
        response.data = error_data
    
    return response
```

Then register it in settings.py:
```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'task_manager.exceptions.custom_exception_handler'
}
```
