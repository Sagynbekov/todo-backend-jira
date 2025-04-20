# backend/api/urls.py

from django.urls import path
from .views import projects

urlpatterns = [
    path('projects/', projects, name='projects'),
]
