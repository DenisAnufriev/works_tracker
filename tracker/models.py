from django.db import models

NULLABLE = {"null": True, "blank": True}


class Employee(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="ФИО", **NULLABLE)
    position = models.CharField(max_length=100, verbose_name="Должность")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=15, blank=True, verbose_name="Телефон")
    hire_date = models.DateField(verbose_name="Дата найма", auto_now_add=True)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.full_name} ({self.position}) {self.email}"


class Task(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидается"),
        ("in_progress", "В работе"),
        ("completed", "Завершено"),
        ("cancelled", "Отменено"),
    ]

    title = models.CharField(max_length=255, verbose_name="Название задачи")
    description = models.TextField(blank=True, verbose_name="Описание")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Статус"
    )
    assigned_to = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        **NULLABLE,
        related_name="tasks",
        verbose_name="Ответственный сотрудник",
    )
    due_date = models.DateField(verbose_name="Срок выполнения", **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    parent_task = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        **NULLABLE,
        related_name="subtasks",
        verbose_name="Родительская задача",
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.title
