from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from tracker.models import Employee, Task
from tracker.serializers import EmployeeSerializer, TaskSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class BusyEmployeesView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer

    def get(self, request):
        """
        Получаем сотрудников, отсортированных по количеству активных задач
        """
        employees = Employee.objects.annotate(
            active_tasks=Count("tasks", filter=Q(tasks__status="in_progress"))
        ).prefetch_related("tasks").order_by("-active_tasks")

        data = [
            {
                "employee": employee.full_name,
                "active_task_count": employee.active_tasks,
                "tasks": [task.title for task in employee.tasks.filter(status="in_progress")],
            }
            for employee in employees
        ]
        return Response(data)

    # def get(self, request):
    #     employees = Employee.objects.annotate(
    #         active_tasks=Count("tasks", filter=Q(tasks__status="in_progress"))
    #     ).order_by("-active_tasks")
    #
    #     serializer = EmployeeSerializer(employees, many=True)
    #     return Response(serializer.data)


class ImportantTasksView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get(self, request):
        """
        Получаем все задачи, которые не взяты в работу, но от которых зависят другие задачи
        """
        important_tasks = Task.objects.filter(
            status="pending", parent_task__isnull=False
        ).select_related("parent_task", "parent_task__assigned_to")

        employees = Employee.objects.annotate(
            active_tasks=Count("tasks", filter=Q(tasks__status="in_progress"))
        ).order_by("active_tasks")

        if not important_tasks.exists() or not employees.exists():
            return Response({"message": "Нет доступных задач или сотрудников"}, status=200)

        task_data = []
        min_active_tasks = employees.first().active_tasks

        for task in important_tasks:
            potential_employees = []

            for employee in employees:
                if (
                        task.parent_task
                        and task.parent_task.assigned_to == employee
                        and employee.active_tasks <= min_active_tasks + 2
                ) or employee.active_tasks == min_active_tasks:
                    potential_employees.append(employee)

            potential_employees_names = [employee.full_name for employee in potential_employees]

            task_data.append(
                {
                    "task": task.title,
                    "due_date": task.due_date,
                    "employees": potential_employees_names,
                }
            )

        return Response(task_data)
