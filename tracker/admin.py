from django.contrib import admin

from tracker.models import Task, Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("full_name", "position", "email", "hire_date")
    search_fields = ("full_name", "email", "position")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "assigned_to",
        "due_date",
        "parent_task",
        "created_at",
    )
    list_filter = ("status", "due_date", "assigned_to")
    search_fields = ("title", "description")
