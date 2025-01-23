from django.contrib.auth.models import AbstractUser
from django.db import models

from tracker.models import NULLABLE


# class User(AbstractUser):
#     username = None
#     email = models.EmailField(
#         unique=True, verbose_name="Почта", help_text="Укажите почту"
#     )
#     phone = models.CharField(
#         max_length=35, **NULLABLE, verbose_name="Телефон", help_text="Укажите телефон"
#     )
#
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []
#
#     class Meta:
#         verbose_name = "Пользователь"
#         verbose_name_plural = "Пользователи"
#
#     def __str__(self):
#         return self.email
