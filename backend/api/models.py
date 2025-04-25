# backend/api/models.py

from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=128)  # Store Firebase user ID

    def __str__(self):
        return self.name


class Column(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, related_name='columns', on_delete=models.CASCADE)
    order = models.IntegerField(default=0)  # To maintain column order

    def __str__(self):
        return f"{self.project.name} - {self.name}"