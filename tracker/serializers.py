from rest_framework import serializers

from tracker.models import Employee, Task


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'full_name', 'position', 'email', 'phone', 'hire_date']


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = EmployeeSerializer()  # Вложенный сериализатор для сотрудника

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'assigned_to', 'due_date', 'parent_task']
