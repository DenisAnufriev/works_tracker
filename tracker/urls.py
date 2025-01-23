from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tracker.apps import TrackerConfig
from tracker.views import EmployeeViewSet, TaskViewSet

app_name = TrackerConfig.name


router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]