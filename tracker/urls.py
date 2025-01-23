from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tracker.apps import TrackerConfig
from tracker.views import EmployeeViewSet, TaskViewSet, BusyEmployeesView, ImportantTasksView

app_name = TrackerConfig.name


router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('busy_employees/', BusyEmployeesView.as_view(), name='busy_employees'),
    path('important_tasks/', ImportantTasksView.as_view(), name='important_tasks'),

] + router.urls