from django.utils import timezone
from rest_framework import serializers

from tracker.models import Employee, Task


class EmployeeSerializer(serializers.ModelSerializer):
    active_task_count = serializers.IntegerField(read_only=True)
    tasks = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "full_name",
            "position",
            "email",
            "phone",
            "hire_date",
            "active_task_count",
            "tasks",
        ]
        # fields = '__all__'

    def validate_email(self, value):
        if Employee.objects.filter(email=value).exists():
            raise serializers.ValidationError("Этот email уже используется.")
        return value

    def get_active_task_count(self, obj):
        return obj.tasks.filter(status="in_progress").count()


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = EmployeeSerializer(read_only=True, required=False)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), source="assigned_to", write_only=True,
        required=False
    )
    parent_task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(), required=False
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
            raise serializers.ValidationError(
                "Срок выполнения не может быть в прошлом."
            )
        return value

    def validate_parent_task(self, data):
        if data.get("parent_task") == self.instance:
            raise serializers.ValidationError(
                "Задача не может быть родительской для самой себя."
            )
        return data
