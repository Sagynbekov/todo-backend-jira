# backend/api/models.py

from django.db import models

class FirebaseUser(models.Model):
    """
    Локальное представление пользователя из Firebase Auth.
    Храним его UID и email, чтобы иметь возможность 
    приглашать по почте и фильтровать существующих пользователей.
    """
    firebase_user_id = models.CharField(max_length=128, unique=True)
    email = models.EmailField(unique=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.email


class Project(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=128)  # Store Firebase user ID (владелец)
    # ------------------ добавлено:
    members = models.ManyToManyField(
        FirebaseUser,
        related_name="projects",  # проекты, в которых участвует пользователь
        blank=True,
    )

    def __str__(self):
        return self.name


class Column(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, related_name='columns', on_delete=models.CASCADE)
    order = models.IntegerField(default=0)  # To maintain column order

    def __str__(self):
        return f"{self.project.name} - {self.name}"


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    column = models.ForeignKey(Column, related_name='tasks', on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)  # Added completed field

    # И добавляем связь на FirebaseUser:
    creator = models.ForeignKey(
        FirebaseUser,
        related_name='tasks',
        on_delete=models.CASCADE,
        null=True,    # или blank=True, если нужна опциональность
    )
    
    # Добавляем поле для отслеживания, кто выполнил задачу
    completed_by = models.ForeignKey(
        FirebaseUser,
        related_name='completed_tasks',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title
