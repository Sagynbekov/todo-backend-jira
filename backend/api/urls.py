# backend/api/urls.py

from django.urls import path
from .views import (
    ProjectListCreateView, ProjectDetailView,
    ColumnListCreateView, ColumnDetailView,
    TaskListCreateView, TaskDetailView, FirebaseUserListCreateView
)

urlpatterns = [
    path('projects/', ProjectListCreateView.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('columns/', ColumnListCreateView.as_view(), name='column-list'),
    path('columns/<int:pk>/', ColumnDetailView.as_view(), name='column-detail'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('firebase-users/', FirebaseUserListCreateView.as_view(), name='firebaseuser-list-create'),
]