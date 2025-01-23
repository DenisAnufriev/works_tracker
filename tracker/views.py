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

    def get(self, request):
        # Получаем сотрудников, отсортированных по количеству активных задач
        employees = Employee.objects.annotate(
            active_tasks=Count('tasks', filter=Q(tasks__status='in_progress'))).order_by('-active_tasks')

        data = []
        for employee in employees:
            tasks = employee.tasks.filter(status='in_progress')
            data.append({
                'employee': employee.full_name,
                'active_task_count': employee.active_tasks,
                'tasks': [task.title for task in tasks]
            })

        return Response(data)


class ImportantTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Получаем все задачи, которые не взяты в работу, но от которых зависят другие задачи
        """
        important_tasks = Task.objects.filter(status='pending', parent_task__isnull=False)

        """
        Поиск сотрудников, которые могут взять задачи
        - Сортировка по наименее загруженному сотруднику
        """
        employees = Employee.objects.annotate(active_tasks=Count('tasks', filter=Q(tasks__status='in_progress')))
        least_busy_employees = employees.order_by('active_tasks')  # наименее загруженные сотрудники

        """
        Для каждой важной задачи находим подходящего сотрудника
        """
        task_data = []
        for task in important_tasks:
            potential_employees = []
            for employee in least_busy_employees:
                if task.parent_task and employee in task.parent_task.subtasks.all() or employee.active_tasks < 3:
                    potential_employees.append(employee)

            potential_employees_names = [employee.full_name for employee in potential_employees]

            task_data.append({
                'task': task.title,
                'due_date': task.due_date,  # если есть поле с датой
                'employees': potential_employees_names
            })

        return Response(task_data)
