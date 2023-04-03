from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TaskView


router = DefaultRouter()
router.register(r'tasks', TaskView, basename='TaskModel')

urlpatterns = [
    path('', include(router.urls)),
]
