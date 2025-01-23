from django.utils import timezone
from rest_framework import serializers

from tracker.models import Employee, Task


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "full_name", "position", "email", "phone", "hire_date"]
        # fields = '__all__'

    def validate_email(self, value):
        if Employee.objects.filter(email=value).exists():
            raise serializers.ValidationError("Этот email уже используется.")
        return value


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = EmployeeSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), source="assigned_to", write_only=True
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "assigned_to",
            "assigned_to_id",
            "due_date",
            "parent_task",
        ]
        # fields = '__all__'

    def validate_due_date(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError("Срок выполнения не может быть в прошлом.")
        return value