import pytest
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from tracker.models import Employee, Task
from tracker.serializers import TaskSerializer, EmployeeSerializer


@pytest.mark.django_db
def test_employee_creation():
    employee = Employee.objects.create(
        full_name="Иван Иванов", position="Менеджер", email="ivan@example.com"
    )
    assert employee.full_name == "Иван Иванов"
    assert employee.position == "Менеджер"
    assert employee.email == "ivan@example.com"


@pytest.mark.django_db
def test_task_creation():
    employee = Employee.objects.create(
        full_name="Иван Иванов", position="Менеджер", email="ivan@example.com"
    )
    task = Task.objects.create(
        title="Задача 1",
        status="pending",
        assigned_to=employee,
        due_date=timezone.now(),
    )
    assert task.title == "Задача 1"
    assert task.status == "pending"
    assert task.assigned_to == employee


@pytest.mark.django_db
def test_employee_serializer():
    employee = Employee.objects.create(
        full_name="Иван Иванов", position="Менеджер", email="ivan@example.com"
    )
    serializer = EmployeeSerializer(employee)
    assert serializer.data["full_name"] == "Иван Иванов"
    assert serializer.data["email"] == "ivan@example.com"


@pytest.mark.django_db
def test_task_serializer():
    employee = Employee.objects.create(
        full_name="Иван Иванов", position="Менеджер", email="ivan@example.com"
    )
    task = Task.objects.create(
        title="Задача 1", status="pending", assigned_to=employee, due_date="2025-01-01"
    )
    serializer = TaskSerializer(task)
    assert serializer.data["title"] == "Задача 1"
    assert serializer.data["assigned_to"]["id"] == employee.id
    assert serializer.data["assigned_to"]["email"] == "ivan@example.com"
    assert serializer.data["assigned_to"]["position"] == "Менеджер"


@pytest.mark.django_db
def test_create_employee():
    client = APIClient()
    data = {
        "full_name": "Иван Иванов",
        "position": "Менеджер",
        "email": "ivan@example.com",
    }
    response = client.post("/employees/", data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["full_name"] == "Иван Иванов"


@pytest.mark.django_db
def test_create_task():
    client = APIClient()
    employee = Employee.objects.create(
        full_name="Иван Иванов", position="Менеджер", email="ivan@example.com"
    )
    data = {
        "title": "Задача 1",
        "status": "pending",
        "assigned_to_id": employee.id,
        "due_date": "2025-10-11",
    }
    response = client.post("/tasks/", data, format="json")
    print(response.data)  # Отладочный вывод
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == "Задача 1"
    assert response.data["status"] == "pending"
