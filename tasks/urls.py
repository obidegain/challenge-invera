from django.urls import path
from .views import TaskListCreateView, TaskDeleteView, TaskUpdateStatusView

urlpatterns = [
    path('create/', TaskListCreateView.as_view(), name='task-list-create'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
    path('update/<int:pk>/', TaskUpdateStatusView.as_view(), name='task-update'),
]